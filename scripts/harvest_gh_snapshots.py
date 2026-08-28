#!/usr/bin/env python3
"""harvest_gh_snapshots.py — Article XXIV (the Static Data Covenant, kody-w/RAR
CONSTITUTION.md): pages read committed static data, never the GitHub API.

classic.html and doorman/index.html used to make several unauthenticated
api.github.com calls per visitor: this seed's own repo metadata / recent
commits / agents/ directory listing, and the same three for the seed's
parent_repo (from rappid.json) to compute the lineage MMR gift. Each of
those calls is now served from a state/*.json file committed here, in the
IDENTICAL response shape the corresponding API endpoint returns — page
parsing code is unchanged, only the URL each fetch targets moved from
api.github.com to a committed snapshot.

Run this from CI (or by hand) with GITHUB_TOKEN set for a friendlier rate
limit; it works unauthenticated too (the same 60/hr-per-IP the pages used
to spend per visitor, but now spent once here instead of once per visitor).

Writes, all in state/:
  repo_snapshot.json            GET /repos/{owner}/{repo}
  commits_snapshot.json         GET /repos/{owner}/{repo}/commits?per_page=10
  agents_snapshot.json          GET /repos/{owner}/{repo}/contents/agents
  parent_repo_snapshot.json     GET /repos/{parent_owner}/{parent_repo}
  parent_commits_snapshot.json  GET /repos/{parent_owner}/{parent_repo}/commits?per_page=6
  parent_agents_snapshot.json   GET /repos/{parent_owner}/{parent_repo}/contents/agents

The parent_* files are skipped when rappid.json has no parent_repo, or when
parent_repo doesn't point at github.com.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"


def gh_get(path):
    """GET api.github.com/{path}. Returns the parsed JSON body even on a
    non-2xx (e.g. a 404 for a repo with no agents/ dir) — that error body is
    itself a valid, harmless static snapshot: the page's Array.isArray()
    guards already treat "not an array" as "nothing to show", same as a
    live 404 always did."""
    url = f"https://api.github.com/repos/{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def write(name, data):
    STATE.mkdir(parents=True, exist_ok=True)
    out = STATE / name
    out.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
    print(f"  {out.relative_to(ROOT)}")


def owner_repo_from_url(url):
    m = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url or "")
    return (m.group(1), m.group(2)) if m else (None, None)


def main():
    rappid = json.loads((ROOT / "rappid.json").read_text())
    owner, repo = owner_repo_from_url(rappid.get("github") or "")
    if not owner or not repo:
        print("✗ rappid.json has no parseable github URL", file=sys.stderr)
        return 2

    print(f"harvesting {owner}/{repo} ...")
    write("repo_snapshot.json", gh_get(f"{owner}/{repo}"))
    write("commits_snapshot.json", gh_get(f"{owner}/{repo}/commits?per_page=10"))
    write("agents_snapshot.json", gh_get(f"{owner}/{repo}/contents/agents"))

    parent_owner, parent_repo = owner_repo_from_url(rappid.get("parent_repo") or "")
    if parent_owner and parent_repo:
        print(f"harvesting parent {parent_owner}/{parent_repo} ...")
        write("parent_repo_snapshot.json", gh_get(f"{parent_owner}/{parent_repo}"))
        write("parent_commits_snapshot.json", gh_get(f"{parent_owner}/{parent_repo}/commits?per_page=6"))
        write("parent_agents_snapshot.json", gh_get(f"{parent_owner}/{parent_repo}/contents/agents"))
    else:
        print("  (no parent_repo — skipping parent_* snapshots)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
