import requests
import time
import csv
from datetime import datetime

KEYWORDS = [
    "Technical Business Analyst",
    "Business Systems Analyst",
    "API Business Analyst",
    "Integration Business Analyst"
]

def search_jobs():
    url = "https://remoteok.com/api"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    jobs = response.json()
    matched_jobs = []

    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = job.get("position", "")
        
        if any(k.lower() in title.lower() for k in KEYWORDS):
            matched_jobs.append({
                "company": job.get("company"),
                "role": title,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

    return matched_jobs


def save_jobs(jobs):
    file = "applied_jobs.csv"

    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)
        
        for job in jobs[:10]:
            writer.writerow([
                job["company"],
                job["role"],
                "Remote",
                "Applied",
                job["date"]
            ])


def main():
    print("Searching jobs...")
    jobs = search_jobs()

    print(f"Found {len(jobs)} matching jobs")
    
    save_jobs(jobs)

    print("Jobs saved successfully")


if __name__ == "__main__":
    main()
