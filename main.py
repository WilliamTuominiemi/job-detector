import os
import requests
import uuid
import psycopg2
from difflib import SequenceMatcher
from dotenv import load_dotenv
from google import genai
from playwright.sync_api import sync_playwright

def get_google_jobs(page, location="Finland", job_title="Intern"):
    url = f"https://www.google.com/about/careers/applications/jobs/results?location={location}&q={job_title}"
    page.goto(url, wait_until="networkidle")
    
    jobs_ul = page.locator('h2:has-text("Jobs search results") ~ c-wiz ul').first
    jobs_ul.wait_for()

    job_items = jobs_ul.locator(":scope > li").all()    
    print(f"Found {len(job_items)} Google jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_microsoft_jobs(page, location="Finland", job_title="Intern"):
    url = f"https://apply.careers.microsoft.com/careers?query={job_title}&start=0&location={location}&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0"
    page.goto(url, wait_until="networkidle")

    job_items = page.locator('div[aria-label="Job search results"] > div').all()
    print(f"Found {len(job_items)} Microsoft jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_amd_jobs(page, location="Espoo", job_title="Intern"):
    url = f"https://careers.amd.com/careers-home/jobs?stretchUnit=MILES&stretch=10&location={location}&keywords={job_title}&sortBy=relevance&page=1"
    page.goto(url, wait_until="networkidle")

    job_items = page.locator("mat-expansion-panel-header").all()
    print(f"Found {len(job_items)} AMD jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())
    
    return job_descriptions

def get_nvidia_jobs(page, location="Finland", job_title="Intern"):
    url = f"https://jobs.nvidia.com/careers?query={job_title}&start=0&location={location}&sort_by=relevance&filter_include_remote=1&filter_include_relocation=0"
    page.goto(url, wait_until="networkidle")

    job_items = page.locator('div[aria-label="Job search results"] > div').all()
    print(f"Found {len(job_items)} Nvidia jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_apple_jobs(page, location="finland-FINC", job_title="Intern"):
    url = f"https://jobs.apple.com/en-us/search?search={job_title}&sort=relevance&location={location}"
    page.goto(url, wait_until="networkidle")
    
    job_items = page.locator('ul[id="search-job-list"] > li').all()
    print(f"Found {len(job_items)} Apple jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_amazon_jobs(page, location="FIN", job_title="Intern"):
    url = f"https://www.amazon.jobs/en/search?base_query={job_title}&country={location}"
    page.goto(url, wait_until="networkidle")
    
    job_items = page.locator("div.job-tile-lists > div").all()
    print(f"Found {len(job_items)} Amazon jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_netflix_jobs(page, location="Finland", job_title="Intern"):
    url = f"https://explore.jobs.netflix.net/careers?query={job_title}&location={location}&domain=netflix.com&sort_by=relevance&triggerGoButton=false"
    page.goto(url, wait_until="networkidle")
    
    job_items = page.locator("div.position-sidebar-scroll-handler div[role='list'] > div").all()
    print(f"Found {len(job_items)} Netflix jobs.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions

def get_all_jobs(page):
    google_jobs = get_google_jobs(page)
    microsoft_jobs = get_microsoft_jobs(page)
    amd_jobs = get_amd_jobs(page)
    nvidia_jobs = get_nvidia_jobs(page)
    apple_jobs = get_apple_jobs(page)
    amazon_jobs = get_amazon_jobs(page)
    netflix_jobs = get_netflix_jobs(page)

    return google_jobs + microsoft_jobs + amd_jobs + nvidia_jobs + apple_jobs + amazon_jobs + netflix_jobs

def collect_to_list_with_ai(all_jobs_list):
    if len(all_jobs_list) > 0:    
        all_jobs = ''.join(all_jobs_list)

        client = genai.Client()
        prompt = f"""Create a bullet point list of these job openings. 
            It should be a single line per job.
            A line should contain job title, company and location (in that order). 
            These parameters should be separated with the character |.
            If you can't find a parameter, fill the spot with character -.
            It shouldn't have any markdown formatting. 
            Jobs: {all_jobs}"""
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )

        return interaction.output_text

def send_telegram_alert(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_seen_jobs() -> set:
    query = "SELECT title, company, location FROM seen_jobs;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {"|".join(row) for row in rows}

def save_new_jobs(jobs):
    if not jobs:
        return

    query = """
    INSERT INTO seen_jobs (id, title, company, location)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    records = [
        (uuid.uuid4().hex, *job.split("|")[:3])
        for job in jobs
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, records)
        conn.commit()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def filter_out_seen_jobs(found_jobs):
    new_jobs = []
    seen_jobs = get_seen_jobs()

    for job in found_jobs:
        seen = False
        for seen_job in seen_jobs:
            if similar(job, seen_job) > 0.9:
                seen = True

        if not seen:
            new_jobs.append(job)

    return new_jobs

with sync_playwright() as p:
    load_dotenv()

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    all_jobs_list = get_all_jobs(page)
    formatted_jobs_list = collect_to_list_with_ai(all_jobs_list).splitlines()
    print(formatted_jobs_list)
    filtered_jobs_list = filter_out_seen_jobs(formatted_jobs_list)
    print(filtered_jobs_list)

    if filtered_jobs_list:
        save_new_jobs(filtered_jobs_list)
        text = "*New jobs found:*\n\n" + "\n".join(f"• {job}" for job in formatted_jobs_list)
        send_telegram_alert(text)
    else: 
        print("No new jobs found")

    browser.close()