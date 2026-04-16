import requests
import time

# Keywords based on your resume
KEYWORDS = [
    "Technical Business Analyst",
    "Business Systems Analyst",
    "API Business Analyst",
    "Integration Business Analyst"
]

REMOTE_FILTER = "remote"

def search_jobs():
    print("Searching jobs...")
    
    # Example API (RemoteOK)
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
        description = str(job)
        
        if any(k.lower() in title.lower() for k in KEYWORDS):
            matched_jobs.append({
                "company": job.get("company"),
                "role": title,
                "url": job.get("url")
            })
    
    return matched_jobs

def apply_jobs(jobs):
    print(f"Applying to {len(jobs)} jobs...")
    
    for job in jobs[:10]:  # limit batch
        print(f"Applied: {job['company']} - {job['role']}")
        time.sleep(2)

if __name__ == "__main__":
    jobs = search_jobs()
    apply_jobs(jobs)
