#!/usr/bin/env python3
"""Read PR completion evidence once. Exit 0 is a stable snapshot, not readiness."""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse


def gh(host, *args):
    result = subprocess.run(
        ["gh", "api", "--hostname", host, *args],
        capture_output=True, text=True, check=False, timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    value = json.loads(result.stdout)
    if isinstance(value, dict) and value.get("errors"):
        raise RuntimeError(json.dumps(value["errors"]))
    return value


def rest_list(host, endpoint):
    pages = gh(host, "--paginate", "--slurp", endpoint + "?per_page=100")
    return [item for page in pages for item in page]


def connection(host, query, variables, path):
    nodes = []
    cursor = None
    while True:
        fields = ["-f", "query=" + query]
        for key, value in variables.items():
            fields.extend(["-F", f"{key}={value}"])
        if cursor:
            fields.extend(["-f", "cursor=" + cursor])
        page = gh(host, "graphql", *fields)["data"]
        for key in path:
            if page is None:
                # A commit without any check rollup has no check contexts.
                if key == "contexts":
                    return nodes
                raise RuntimeError("Missing GitHub evidence: " + ".".join(path))
            page = page[key]
        nodes.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return nodes
        next_cursor = page["pageInfo"]["endCursor"]
        if not next_cursor or next_cursor == cursor:
            raise RuntimeError("GitHub pagination did not advance")
        cursor = next_cursor


CHECKS = """
query($owner:String!, $repo:String!, $number:Int!, $head:GitObjectID!, $cursor:String) {
  repository(owner:$owner, name:$repo) {
    object(oid:$head) { ... on Commit {
      statusCheckRollup { contexts(first:100, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          __typename
          ... on CheckRun {
            id databaseId name status conclusion startedAt completedAt detailsUrl
            isRequired(pullRequestNumber:$number) title summary text
            checkSuite {
              app { slug } commit { oid }
              workflowRun { workflow { name } }
            }
          }
          ... on StatusContext {
            id context state createdAt targetUrl description creator { login }
            isRequired(pullRequestNumber:$number)
          }
        }
      } }
    } }
  }
}
"""

THREADS = """
query($owner:String!, $repo:String!, $number:Int!, $cursor:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) { reviewThreads(first:100, after:$cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id isResolved isOutdated path line
        comments(first:1) { nodes { databaseId url } }
      }
    } }
  }
}
"""


def pr_state(host, owner, repo, number):
    query = """
    query($owner:String!, $repo:String!, $number:Int!) {
      repository(owner:$owner, name:$repo) { pullRequest(number:$number) {
        url state isDraft headRefOid baseRefOid mergeable mergeStateStatus reviewDecision
      } }
    }
    """
    data = gh(host, "graphql", "-f", "query=" + query,
              "-f", "owner=" + owner, "-f", "repo=" + repo, "-F", f"number={number}")
    pr = data["data"]["repository"]["pullRequest"]
    if pr is None:
        raise RuntimeError("PR not found")
    return pr


def snapshot(url):
    parsed = urlparse(url)
    match = re.fullmatch(r"/([\w.-]+)/([\w.-]+)/pull/([1-9][0-9]*)/?", parsed.path)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.netloc != parsed.hostname
            or parsed.query or parsed.fragment or not match):
        raise ValueError("Expected https://HOST/OWNER/REPO/pull/NUMBER")
    owner, repo, number = match.groups()
    host = parsed.hostname
    before = pr_state(host, owner, repo, number)
    variables = {"owner": owner, "repo": repo, "number": number}
    checks = connection(host, CHECKS, {**variables, "head": before["headRefOid"]},
                        ["repository", "object", "statusCheckRollup", "contexts"])
    endpoint = f"repos/{owner}/{repo}"
    reviews = rest_list(host, f"{endpoint}/pulls/{number}/reviews")
    issue_comments = rest_list(host, f"{endpoint}/issues/{number}/comments")
    inline_comments = rest_list(host, f"{endpoint}/pulls/{number}/comments")
    threads = connection(host, THREADS, variables,
                         ["repository", "pullRequest", "reviewThreads"])
    after = pr_state(host, owner, repo, number)
    stable = all(before[key] == after[key] for key in ("headRefOid", "baseRefOid", "state"))
    return {
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "stable": stable,
        "prBefore": before,
        "prAfter": after,
        "checksHeadOid": before["headRefOid"],
        "checks": checks,
        "requiredChecks": [check for check in checks if check["isRequired"]],
        "reviews": reviews,
        "issueComments": issue_comments,
        "inlineComments": inline_comments,
        "reviewThreads": threads,
    }


def compact_check(check):
    if check.get("__typename") == "CheckRun":
        passing = check.get("status") == "COMPLETED" and check.get("conclusion") in ("SUCCESS", "NEUTRAL", "SKIPPED")
        out = {
            "__typename": "CheckRun",
            "name": check.get("name"),
            "status": check.get("status"),
            "conclusion": check.get("conclusion"),
            "isRequired": check.get("isRequired"),
            "startedAt": check.get("startedAt"),
            "completedAt": check.get("completedAt"),
            "detailsUrl": check.get("detailsUrl"),
            "app": ((check.get("checkSuite") or {}).get("app") or {}).get("slug"),
            "workflow": (((check.get("checkSuite") or {}).get("workflowRun") or {}).get("workflow") or {}).get("name"),
        }
        if not passing:
            out["title"] = check.get("title")
            out["summary"] = check.get("summary")
            out["text"] = check.get("text")
        return out
    return {
        "__typename": check.get("__typename"),
        "context": check.get("context"),
        "state": check.get("state"),
        "isRequired": check.get("isRequired"),
        "createdAt": check.get("createdAt"),
        "description": check.get("description"),
        "targetUrl": check.get("targetUrl"),
        "creator": (check.get("creator") or {}).get("login"),
    }


def compact_review(review):
    return {
        "id": review.get("id"),
        "user": (review.get("user") or {}).get("login"),
        "state": review.get("state"),
        "commit_id": review.get("commit_id"),
        "submitted_at": review.get("submitted_at"),
        "html_url": review.get("html_url"),
        "body": review.get("body"),
    }


def compact_comment(comment):
    out = {
        "id": comment.get("id"),
        "user": (comment.get("user") or {}).get("login"),
        "created_at": comment.get("created_at"),
        "updated_at": comment.get("updated_at"),
        "html_url": comment.get("html_url"),
        "body": comment.get("body"),
    }
    if "path" in comment:
        out["path"] = comment.get("path")
        out["line"] = comment.get("line")
        out["in_reply_to_id"] = comment.get("in_reply_to_id")
        out["commit_id"] = comment.get("commit_id")
    return out


def compact_snapshot(result):
    unresolved_threads = [t for t in result["reviewThreads"] if not t.get("isResolved")]
    resolved_root_ids = {
        node["databaseId"]
        for t in result["reviewThreads"]
        if t.get("isResolved")
        for node in ((t.get("comments") or {}).get("nodes") or [])
        if node.get("databaseId") is not None
    }
    unresolved_inline = [
        compact_comment(c)
        for c in result["inlineComments"]
        if c.get("id") not in resolved_root_ids and c.get("in_reply_to_id") not in resolved_root_ids
    ]
    checks = [compact_check(c) for c in result["checks"]]
    return {
        "observedAt": result["observedAt"],
        "stable": result["stable"],
        "prBefore": result["prBefore"],
        "prAfter": result["prAfter"],
        "checksHeadOid": result["checksHeadOid"],
        "checks": checks,
        "requiredChecks": [c for c in checks if c.get("isRequired")],
        "reviews": [compact_review(r) for r in result["reviews"]],
        "issueComments": [compact_comment(c) for c in result["issueComments"]],
        "inlineComments": unresolved_inline,
        "reviewThreads": unresolved_threads,
        "omitted": {
            "resolvedThreads": len(result["reviewThreads"]) - len(unresolved_threads),
            "resolvedInlineComments": len(result["inlineComments"]) - len(unresolved_inline),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Full GitHub PR URL")
    parser.add_argument("--compact", action="store_true",
                        help="Strip GitHub metadata noise, resolved threads and passing check logs")
    args = parser.parse_args()
    try:
        result = snapshot(args.url)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"error": str(error), "readiness": "unproven"}), file=sys.stderr)
        return 1
    output = compact_snapshot(result) if args.compact else result
    print(json.dumps(output, indent=2))
    return 0 if result["stable"] else 2


if __name__ == "__main__":
    sys.exit(main())
