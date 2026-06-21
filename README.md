# job-search-bot

Automated weekly Product Designer job search across Europe. Runs every Monday at 10:00 AM and posts results as GitHub Issues.

## Countries covered
Germany · France · Netherlands · Austria · Switzerland

## Setup

### 1. Get Adzuna API credentials (free)
- Sign up at https://developer.adzuna.com
- Copy your `App ID` and `App Key`

### 2. Add GitHub Secrets
Go to **Settings → Secrets and variables → Actions** and add:
- `ADZUNA_APP_ID` — your Adzuna App ID
- `ADZUNA_APP_KEY` — your Adzuna App Key

### 3. Done
Every Monday at 10 AM a GitHub Issue appears with scored job listings.

## Scoring
Jobs are scored 1–10 based on:
- Title match (Product Designer > UX Designer)
- Junior signals (bonus) / Senior signals (penalty)
- Skills match: Figma, prototyping, user research, design systems
- Remote/hybrid availability
