#!/usr/bin/env python3
"""
Generates assets/stats.svg and assets/languages.svg for the profile README.

Uses the GitHub GraphQL API with YOUR personal access token so that PRIVATE
contributions and PRIVATE repositories are included.

  export GH_TOKEN=ghp_xxx          # classic PAT with scopes: read:user, repo
  export GH_LOGIN=Jagadish-s-naik
  python scripts/update_profile_stats.py

  python scripts/update_profile_stats.py --demo   # render with placeholder data
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from html import escape

API = "https://api.github.com/graphql"
SANS = "'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

LANG_COLORS = {
    "Jupyter Notebook": "#F37626", "Python": "#3572A5", "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A", "HTML": "#E34C26", "CSS": "#8D5BD6", "Dart": "#00B4AB",
    "Java": "#B07219", "C++": "#F34B7D", "Shell": "#89E051", "Procfile": "#8a8a8a",
}


# --------------------------------------------------------------------------- API
def gql(query, variables, token):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


YEAR_Q = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}"""

USER_Q = """
query($login:String!, $after:String) {
  user(login:$login) {
    createdAt
    followers { totalCount }
    repositories(first:100, after:$after, ownerAffiliations:OWNER, isFork:false) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first:8, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}"""


def collect(login, token):
    after, repos, created, followers = None, [], None, 0
    while True:
        u = gql(USER_Q, {"login": login, "after": after}, token)["user"]
        created, followers = u["createdAt"], u["followers"]["totalCount"]
        repos += u["repositories"]["nodes"]
        total_repos = u["repositories"]["totalCount"]
        if not u["repositories"]["pageInfo"]["hasNextPage"]:
            break
        after = u["repositories"]["pageInfo"]["endCursor"]

    stars = sum(r["stargazerCount"] for r in repos)
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or LANG_COLORS.get(n, "#8a8a8a")])
            langs[n][0] += e["size"]

    first_year = int(created[:4])
    this_year = dt.date.today().year
    total = commits = prs = issues = private = 0
    days = {}
    for y in range(first_year, this_year + 1):
        c = gql(YEAR_Q, {"login": login, "from": f"{y}-01-01T00:00:00Z",
                         "to": f"{y}-12-31T23:59:59Z"}, token)["user"]["contributionsCollection"]
        total += c["contributionCalendar"]["totalContributions"]
        commits += c["totalCommitContributions"]
        prs += c["totalPullRequestContributions"]
        issues += c["totalIssueContributions"]
        private += c["restrictedContributionsCount"]
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    ordered = sorted(days.items())
    today = dt.date.today().isoformat()
    ordered = [(d, n) for d, n in ordered if d <= today]
    longest = cur = 0
    for _, n in ordered:
        cur = cur + 1 if n else 0
        longest = max(longest, cur)
    current = 0
    for d, n in reversed(ordered):
        if n:
            current += 1
        elif d != today:
            break
    last = [n for _, n in ordered[-182:]]
    weekly = [sum(last[i:i + 7]) for i in range(0, len(last), 7)]

    lang_list = sorted(((n, v[0], v[1]) for n, v in langs.items()), key=lambda x: -x[1])
    tot_bytes = sum(b for _, b, _ in lang_list) or 1
    return {
        "total": total, "private": private, "commits": commits, "prs": prs, "issues": issues,
        "repos": total_repos, "stars": stars, "followers": followers,
        "streak": current, "longest": longest, "weekly": weekly,
        "langs": [(n, round(100 * b / tot_bytes), c) for n, b, c in lang_list[:6]],
        "updated": today,
    }


# ------------------------------------------------------------------------ render
def fmt(v):
    return f"{v:,}" if isinstance(v, int) else str(v)


def stats_svg(d):
    W, H = 860, 330
    tiles1 = [("CONTRIBUTIONS", d["total"], "#5eead4"), ("REPOSITORIES", d["repos"], "#a78bfa"),
              ("STARS", d["stars"], "#fbbf24"), ("FOLLOWERS", d["followers"], "#60a5fa")]
    tiles2 = [("COMMITS", d["commits"], "#5eead4"), ("PULL REQUESTS", d["prs"], "#a78bfa"),
              ("ISSUES", d["issues"], "#fbbf24"), ("CURRENT STREAK", d["streak"], "#60a5fa")]
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats including private contributions">
<defs>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#2dd4bf"/>
<animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="12s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0d9488"/><stop offset="1" stop-color="#5eead4"/></linearGradient>
</defs>
<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="20" fill="#0b1214" stroke="url(#bd)" stroke-width="1.6"/>
<text x="34" y="44" font-family="{MONO}" font-size="13" fill="#2dd4bf" letter-spacing="3">&gt; stats.scan --include-private</text>
<circle cx="{W-40}" cy="39" r="4" fill="#5eead4"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="{W-52}" y="44" text-anchor="end" font-family="{MONO}" font-size="11" fill="#5b8f89">LIVE &#183; {escape(str(d["updated"]))}</text>''']
    for row, tiles in enumerate((tiles1, tiles2)):
        for i, (lab, val, col) in enumerate(tiles):
            x, y = 34 + i * 204, 66 + row * 92
            b = 0.15 * (row * 4 + i)
            out.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".5s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" begin="{b:.2f}s" dur=".5s" fill="freeze"/>
<rect x="{x}" y="{y}" width="190" height="78" rx="12" fill="#0f1b1d" stroke="{col}" stroke-opacity=".35"/>
<rect x="{x}" y="{y+14}" width="3" height="50" rx="1.5" fill="{col}"><animate attributeName="opacity" values="1;.35;1" dur="3s" begin="{b:.2f}s" repeatCount="indefinite"/></rect>
<text x="{x+20}" y="{y+43}" font-family="{SANS}" font-size="30" font-weight="800" fill="#f1f5f9">{escape(fmt(val))}</text>
<text x="{x+20}" y="{y+64}" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{col}">{lab}</text></g>''')
    # footer line with private count + pulse chart
    priv = d["private"]
    priv_txt = f"includes {fmt(priv)} private contributions" if isinstance(priv, int) else "private contributions are counted once the Action runs"
    out.append(f'<text x="34" y="262" font-family="{MONO}" font-size="12" fill="#7fb8b0">{escape(priv_txt)} &#183; longest streak {escape(fmt(d["longest"]))} days</text>')
    weekly = d.get("weekly") or []
    if weekly:
        mx = max(weekly) or 1
        bw = (W - 68) / len(weekly)
        for i, v in enumerate(weekly):
            h = max(3, 38 * v / mx)
            x = 34 + i * bw
            out.append(f'<rect x="{x:.1f}" y="{312-h:.1f}" width="{bw-3:.1f}" height="{h:.1f}" rx="2" fill="url(#bar)" opacity=".9">'
                       f'<animate attributeName="height" from="0" to="{h:.1f}" begin="{0.9+i*0.03:.2f}s" dur=".5s" fill="freeze"/>'
                       f'<animate attributeName="y" from="312" to="{312-h:.1f}" begin="{0.9+i*0.03:.2f}s" dur=".5s" fill="freeze"/></rect>')
    else:
        out.append(f'<text x="34" y="300" font-family="{MONO}" font-size="12" fill="#4b7a75">weekly pulse appears after the first run of the &quot;Profile stats&quot; workflow</text>')
    out.append("</svg>")
    return "\n".join(out)


def langs_svg(d):
    langs = d["langs"][:5]
    W, H = 860, 70 + 44 * len(langs)
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Language stack">
<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#2dd4bf"/>
<animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="12s" repeatCount="indefinite"/></linearGradient></defs>
<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="20" fill="#0b1214" stroke="url(#bd)" stroke-width="1.6"/>
<text x="34" y="42" font-family="{SANS}" font-size="22" font-weight="800" fill="#99f6e4">Language Stack</text>
<text x="{W-34}" y="42" text-anchor="end" font-family="{MONO}" font-size="13" fill="#2dd4bf">&gt; stack.scan<tspan fill="#5eead4"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/> _</tspan></text>''']
    bx, bw = 230, W - 230 - 90
    for i, (name, pct, col) in enumerate(langs):
        y = 66 + i * 44
        w = max(6, bw * pct / 100)
        b = 0.2 + i * 0.18
        out.append(f'''<circle cx="40" cy="{y+9}" r="6" fill="{col}"/>
<text x="56" y="{y+14}" font-family="{SANS}" font-size="15" font-weight="700" fill="#e2f5f2">{escape(name)}</text>
<text x="{bx-14}" y="{y+14}" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{col}">{pct}%</text>
<rect x="{bx}" y="{y+3}" width="{bw}" height="12" rx="6" fill="#1b2a2c"/>
<rect x="{bx}" y="{y+3}" width="0" height="12" rx="6" fill="{col}"><animate attributeName="width" from="0" to="{w:.1f}" begin="{b:.2f}s" dur="1.1s" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1" fill="freeze"/></rect>
<rect x="{bx}" y="{y+3}" width="26" height="12" rx="6" fill="#fff" opacity="0"><animate attributeName="opacity" values="0;.35;0" dur="2.6s" begin="{b+1.2:.2f}s" repeatCount="indefinite"/><animate attributeName="x" values="{bx};{bx+w-26:.1f}" dur="2.6s" begin="{b+1.2:.2f}s" repeatCount="indefinite"/></rect>''')
    out.append("</svg>")
    return "\n".join(out)


DEMO = {
    "total": 2775, "private": "—", "commits": "—", "prs": "—", "issues": "—",
    "repos": 45, "stars": 3, "followers": 1, "streak": "—", "longest": "—", "weekly": [],
    "langs": [("Jupyter Notebook", 66, "#F37626"), ("Python", 12, "#3572A5"),
              ("TypeScript", 11, "#3178C6"), ("HTML", 3, "#E34C26"), ("JavaScript", 3, "#F1E05A")],
    "updated": "pending first run",
}


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    if "--demo" in sys.argv:
        data = DEMO
    else:
        token, login = os.environ.get("GH_TOKEN"), os.environ.get("GH_LOGIN", "Jagadish-s-naik")
        if not token:
            sys.exit("Set GH_TOKEN (classic PAT with read:user + repo) or use --demo")
        data = collect(login, token)
    with open(os.path.join(out_dir, "stats.svg"), "w", encoding="utf-8") as f:
        f.write(stats_svg(data))
    with open(os.path.join(out_dir, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(langs_svg(data))
    print("written:", {k: v for k, v in data.items() if k != "weekly"})


if __name__ == "__main__":
    main()
