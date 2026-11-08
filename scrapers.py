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
