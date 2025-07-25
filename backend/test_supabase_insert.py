import os
from supabase import create_client
from datetime import datetime
import uuid

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

transcript_id = str(uuid.uuid4())
company_name = "GoogleTest"
attendees = "Alice, Bob"
date = "2025-07-25"
transcript_text = "This is a test transcript for Google (direct insert)."
created_at = datetime.utcnow().isoformat()

try:
    response = supabase.table("transcripts").insert({
        "id": transcript_id,
        "company_name": company_name,
        "attendees": attendees,
        "date": date,
        "transcript_text": transcript_text,
        "analysis": "",
        "created_at": created_at,
        "job_id": "test-job-id"
    }).execute()
except Exception as e:
    pass 