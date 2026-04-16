import requests
import csv
from datetime import datetime

KEYWORDS = [
    "business analyst",
    "technical business analyst",
    "system analyst",
    "product analyst",
    "data analyst"
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
        print("API failed")
        return []

    jobs = response.json()
    matched = []

    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = job.get("position", "").lower()
        link = job.get("url", "")
        company = job.get("company", "Unknown")

        print("Checking:", title)  # debug line

        if any(k in title for k in KEYWORDS):
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

        for job in jobs:
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

    print(f"Found {len(jobs)} matching jobs")

    if jobs:
        save_jobs(jobs)
        print("Saved successfully")
    else:
        print("No matching jobs found")


if __name__ == "__main__":
    main()
