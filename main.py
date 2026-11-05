from playwright.sync_api import sync_playwright

def get_google_jobs(page, location="Finland", job_title="Intern"):
    url = f"https://www.google.com/about/careers/applications/jobs/results?location={location}&q={job_title}"
    page.goto(url, wait_until="networkidle")
    
    jobs_ul = page.locator('h2:has-text("Jobs search results") ~ c-wiz ul').first
    jobs_ul.wait_for()

    job_items = jobs_ul.locator(":scope > li").all()    
    print(f"Found {len(job_items)} jobs on this page.")
    job_descriptions = []
    for item in job_items:
        job_descriptions.append(item.inner_text())

    return job_descriptions


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    google_jobs = get_google_jobs(page)

    print(page.title())
    print(page.url)

    browser.close()