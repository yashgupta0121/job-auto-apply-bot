import requests
import csv
from datetime import datetime

KEYWORDS = [
    "business analyst",
    "technical business analyst",
    "system analyst",
    "product analyst"
]

# -------- GREENHOUSE --------
def fetch_greenhouse():
    jobs = []
    boards_url = "https://boards-api.greenhouse.io/v1/boards"
    res = requests.get(boards_url)

    if res.status_code != 200:
        return jobs

    boards = res.json().get("boards", [])

    for board in boards[:40]:  # limit
        token = board.get("token")

        try:
            job_url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
            job_res = requests.get(job_url)

            if job_res.status_code != 200:
                continue

            for job in job_res.json().get("jobs", []):
                title = job.get("title", "").lower()

                if any(k in title for k in KEYWORDS):
                    jobs.append({
                        "company": token,
                        "role": job.get("title"),
                        "url": job.get("absolute_url"),
                        "source": "Greenhouse"
                    })

        except:
            continue

    return jobs


# -------- LEVER --------
def fetch_lever():
    jobs = []
    companies = [
        "netflix", "shopify", "airbnb", "stripe", "datadog"
    ]

    for company in companies:
        try:
            url = f"https://api.lever.co/v0/postings/{company}?mode=json"
            res = requests.get(url)

            if res.status_code != 200:
                continue

            for job in res.json():
                title = job.get("text", "").lower()

                if any(k in title for k in KEYWORDS):
                    jobs.append({
                        "company": company,
                        "role": job.get("text"),
                        "url": job.get("hostedUrl"),
                        "source": "Lever"
                    })

        except:
            continue

    return jobs


# -------- REMOTIVE --------
def fetch_remotive():
    jobs = []
    url = "https://remotive.com/api/remote-jobs"
    res = requests.get(url)

    if res.status_code != 200:
        return jobs

    for job in res.json().get("jobs", []):
        title = job.get("title", "").lower()

        if any(k in title for k in KEYWORDS):
            jobs.append({
                "company": job.get("company_name"),
                "role": job.get("title"),
                "url": job.get("url"),
                "source": "Remotive"
            })

    return jobs


# -------- SAVE --------
def save_jobs(all_jobs):
    with open("jobs_output.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Company", "Role", "Source", "Apply Link", "Date"])

        for job in all_jobs:
            writer.writerow([
                job["company"],
                job["role"],
                job["source"],
                job["url"],
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ])


# -------- MAIN --------
def main():
    print("Fetching jobs from multiple sources...")

    jobs = []
    jobs += fetch_greenhouse()
    jobs += fetch_lever()
    jobs += fetch_remotive()

    print(f"Total jobs found: {len(jobs)}")

    save_jobs(jobs)

    print("CSV file created successfully")


if __name__ == "__main__":
    main()
