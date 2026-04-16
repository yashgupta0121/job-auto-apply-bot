import requests
import csv
from datetime import datetime

KEYWORDS = [
    "Technical Business Analyst",
    "Business Systems Analyst",
    "API Business Analyst",
    "Business System Analyst",
]

def detect_ats(url):
    if not url:
        return "Unknown"

    if "greenhouse" in url:
        return "Greenhouse"
    elif "lever" in url:
        return "Lever"
    elif "workday" in url:
        return "Workday"
    elif "ashby" in url:
        return "Ashby"
    else:
        return "Direct/Other"


def search_jobs():
    url = "https://remoteok.com/api"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    jobs = response.json()
    matched = []

    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = job.get("position", "")
        link = job.get("url", "")
        company = job.get("company", "Unknown")

        if any(k.lower() in title.lower() for k in KEYWORDS):
            matched.append({
                "company": company,
                "role": title,
                "url": link,
                "ats": detect_ats(link),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

    return matched


def save_jobs(jobs):
    with open("jobs_output.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for job in jobs[:10]:
            writer.writerow([
                job["company"],
                job["role"],
                job["ats"],
                job["url"],
                job["date"]
            ])


def main():
    print("Searching jobs...")
    jobs = search_jobs()

    print(f"Found {len(jobs)} jobs")

    save_jobs(jobs)

    print("Saved successfully")


if __name__ == "__main__":
    main()
