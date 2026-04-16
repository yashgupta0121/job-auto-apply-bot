import requests
import csv
from datetime import datetime

KEYWORDS = [
    "analyst",
    "business",
    "product",
    "system"
]

def fetch_remotive():
    print("Fetching Remotive jobs...")
    jobs = []

    url = "https://remotive.com/api/remote-jobs"
    res = requests.get(url)

    if res.status_code != 200:
        print("Remotive API failed")
        return jobs

    for job in res.json().get("jobs", []):
        title = job.get("title", "").lower()

        print("Checking:", title)

        if any(k in title for k in KEYWORDS):
            jobs.append({
                "company": job.get("company_name"),
                "role": job.get("title"),
                "url": job.get("url"),
                "source": "Remotive"
            })

    return jobs


def save_jobs(jobs):
    with open("jobs_output.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Company", "Role", "Source", "Link", "Date"])

        for job in jobs:
            writer.writerow([
                job["company"],
                job["role"],
                job["source"],
                job["url"],
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ])


def main():
    jobs = fetch_remotive()

    print("Total jobs found:", len(jobs))

    save_jobs(jobs)

    print("CSV created successfully")


if __name__ == "__main__":
    main()
