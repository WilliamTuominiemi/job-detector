from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from scrapers import get_all_jobs
from ai_parser import collect_to_list_with_ai
from notifier import send_telegram_alert
from database import save_new_jobs, filter_out_seen_jobs

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
        text = "*New jobs found:*\n\n" + "\n".join(f"• {job}" for job in filtered_jobs_list)
        send_telegram_alert(text)
    else: 
        print("No new jobs found")

    browser.close()