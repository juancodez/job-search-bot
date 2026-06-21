"""
Weekly Product Designer job search across Europe.
Uses Adzuna API (free tier). Results posted as GitHub Issues + saved to data/latest.json.
"""

import os
import json
import requests
from datetime import datetime

ADZUNA_APP_ID = os.environ["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = os.environ["ADZUNA_APP_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPOSITORY"]

COUNTRIES = {
    "de": "Germany",
    "fr": "France",
    "nl": "Netherlands",
    "at": "Austria",
    "ch": "Switzerland",
}

KEYWORDS = "product designer"
RESULTS_PER_COUNTRY = 10

JUNIOR_SIGNALS = ["junior", "entry", "graduate", "grad", "associate", "jr"]
SENIOR_SIGNALS = ["senior", "lead", "head", "principal", "director", "staff", "sr."]


def fetch_jobs(country_code: str) -> list[dict]:
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": KEYWORDS,
        "results_per_page": RESULTS_PER_COUNTRY,
        "max_days_old": 7,
        "content-type": "application/json",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])


def score_job(job: dict) -> int:
    title = job.get("title", "").lower()
    desc = job.get("description", "").lower()

    score = 5

    if "product designer" in title:
        score += 2
    elif "ux designer" in title or "ui/ux" in title:
        score += 1

    if any(s in title for s in JUNIOR_SIGNALS):
        score += 2
    if any(s in title for s in SENIOR_SIGNALS):
        score -= 4

    for skill in ["figma", "prototyping", "user research", "design system", "wireframe"]:
        if skill in desc:
            score += 0.5

    if "remote" in desc or "hybrid" in desc:
        score += 0.5

    return round(min(max(score, 1), 10))


def format_salary(job: dict) -> str:
    sal = job.get("salary_min")
    return f"~€{int(sal):,}/yr" if sal else "Not listed"


def normalize(job: dict, country_code: str) -> dict:
    desc = job.get("description", "").lower()
    return {
        "title": job.get("title", ""),
        "company": job.get("company", {}).get("display_name", ""),
        "location": job.get("location", {}).get("display_name", ""),
        "country": country_code,
        "salary": format_salary(job),
        "score": score_job(job),
        "url": job.get("redirect_url", ""),
        "posted": job.get("created", "")[:10],
        "remote": "remote" in desc or "hybrid" in desc,
    }


def save_json(jobs: list[dict]) -> None:
    os.makedirs("data", exist_ok=True)
    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total": len(jobs),
        "jobs": sorted(jobs, key=lambda j: j["score"], reverse=True),
    }
    with open("data/latest.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print("Saved data/latest.json")


def build_issue_body(jobs: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    top = [j for j in jobs if j["score"] >= 8]
    good = [j for j in jobs if 6 <= j["score"] < 8]
    rest = [j for j in jobs if j["score"] < 6]

    def section(title: str, items: list[dict]) -> str:
        if not items:
            return ""
        lines = [f"\n## {title}\n"]
        for j in items:
            flag = {"de": "🇩🇪", "fr": "🇫🇷", "nl": "🇳🇱", "at": "🇦🇹", "ch": "🇨🇭"}.get(j["country"], "🌍")
            lines.append(f"### [{j['title']}]({j['url']}) — {j['company']}")
            lines.append(f"- **Location:** {flag} {j['location']}")
            lines.append(f"- **Salary:** {j['salary']}")
            lines.append(f"- **Fit score:** {j['score']}/10")
            lines.append(f"- **Posted:** {j['posted']}")
            lines.append("")
        return "\n".join(lines)

    return (
        f"# 🔍 Product Designer Jobs Europe — {today}\n\n"
        f"**{len(jobs)} roles found** across {len(COUNTRIES)} countries\n"
        + section("🟢 Top Picks (8–10)", top)
        + section("🟡 Good Matches (6–7)", good)
        + section("⚪ Other Roles", rest[:5])
        + f"\n---\n*Auto-generated · {today}*"
    )


def post_github_issue(body: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    r = requests.post(url, headers=headers, json={
        "title": f"🔍 PD Jobs Europe — {today}",
        "body": body,
        "labels": ["job-search"],
    }, timeout=15)
    r.raise_for_status()
    print(f"Issue: {r.json()['html_url']}")


def main():
    all_jobs = []
    for code in COUNTRIES:
        print(f"Searching {COUNTRIES[code]}...")
        try:
            raw = fetch_jobs(code)
            all_jobs.extend(normalize(j, code) for j in raw)
        except Exception as e:
            print(f"  Failed {code}: {e}")

    if not all_jobs:
        print("No jobs found.")
        return

    all_jobs.sort(key=lambda j: j["score"], reverse=True)
    save_json(all_jobs)
    post_github_issue(build_issue_body(all_jobs))


if __name__ == "__main__":
    main()
