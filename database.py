import os
import uuid
import psycopg2
from difflib import SequenceMatcher

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
    INSERT INTO seen_jobs (id, title, company, location, link)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    records = [
        (uuid.uuid4().hex, *(job.split("|") + ["-", "-", "-"])[:3], link)
        for job, link in jobs
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

    for job, link in found_jobs:
        seen = False
        for seen_job in seen_jobs:
            if similar(job, seen_job) > 0.9:
                seen = True

        if not seen:
            new_jobs.append((job, link))

    return new_jobs
