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


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    google_jobs = get_google_jobs(page)
    microsoft_jobs = get_microsoft_jobs(page)

    browser.close()