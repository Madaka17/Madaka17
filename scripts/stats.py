"""Draw the profile's stats and language cards as SVG from the GitHub GraphQL API.

    GH_TOKEN=... python scripts/stats.py            writes assets/stats.svg and assets/langs.svg

Only public data: the token in the Actions workflow (GITHUB_TOKEN) cannot see private repositories,
and the language card counts public repositories only. Standard library only.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = os.environ.get("PROFILE_USER", "Madaka17")
OUT = Path(__file__).resolve().parent.parent / "assets"

BG_TOP, BG_BOTTOM = "#1a1033", "#0d1117"
BORDER = "#3b2a6b"
TITLE = "#c4b5fd"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#a78bfa"
FONT = "'Segoe UI', 'Noto Sans', 'Noto Sans Thai', Ubuntu, sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar { totalContributions }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100, isFork: false) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch(token):
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def card(width, height, title, inner):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>
  </linearGradient>
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .title {{ font-size: 17px; font-weight: 600; fill: {TITLE}; }}
  .label {{ font-size: 13px; fill: {MUTED}; }}
  .value {{ font-size: 15px; font-weight: 600; fill: {TEXT}; }}
</style>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="url(#bg)" stroke="{BORDER}"/>
<text x="24" y="36" class="title">{escape(title)}</text>
{inner}
</svg>
"""


def stats_svg(user):
    c = user["contributionsCollection"]
    repos = user["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    rows = [
        ("Contributions (last year)", c["contributionCalendar"]["totalContributions"]),
        ("Commits", c["totalCommitContributions"]),
        ("Pull requests", c["totalPullRequestContributions"]),
        ("Public repositories", repos["totalCount"]),
        ("Stars", stars),
    ]
    inner = []
    for i, (label, value) in enumerate(rows):
        y = 70 + i * 26
        inner.append(
            '<g>'
            f'<circle cx="30" cy="{y - 5}" r="4" fill="{ACCENT}"/>'
            f'<text x="44" y="{y}" class="label">{escape(label)}</text>'
            f'<text x="326" y="{y}" class="value" text-anchor="end">{value:,}</text></g>')
    return card(350, 200, "GitHub activity", "\n".join(inner))


def langs_svg(user, top=5):
    sizes = {}
    colors = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            sizes[name] = sizes.get(name, 0) + e["size"]
            colors[name] = e["node"]["color"] or MUTED
    total = sum(sizes.values()) or 1
    ranked = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)[:top]
    bar, x = [], 24
    width = 302
    for name, size in ranked:
        w = width * size / total
        bar.append(f'<rect x="{x:.1f}" y="52" width="{max(w, 2):.1f}" height="8" fill="{colors[name]}"/>')
        x += w
    inner = ['<clipPath id="bar"><rect x="24" y="52" width="302" height="8" rx="4"/></clipPath>',
             f'<rect x="24" y="52" width="302" height="8" rx="4" fill="{BORDER}"/>',
             '<g clip-path="url(#bar)">' + "".join(bar) + "</g>"]
    for i, (name, size) in enumerate(ranked):
        y = 92 + i * 22
        inner.append(
            '<g>'
            f'<circle cx="30" cy="{y - 5}" r="5" fill="{colors[name]}"/>'
            f'<text x="44" y="{y}" class="label" style="fill:{TEXT}">{escape(name)}</text>'
            f'<text x="326" y="{y}" class="label" text-anchor="end">{100 * size / total:.1f}%</text></g>')
    return card(350, 200, "Languages (public repos)", "\n".join(inner))


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("Set GH_TOKEN or GITHUB_TOKEN")
    user = fetch(token)
    OUT.mkdir(exist_ok=True)
    (OUT / "stats.svg").write_text(stats_svg(user), encoding="utf-8")
    (OUT / "langs.svg").write_text(langs_svg(user), encoding="utf-8")
    print("wrote", OUT / "stats.svg", OUT / "langs.svg")


if __name__ == "__main__":
    main()
