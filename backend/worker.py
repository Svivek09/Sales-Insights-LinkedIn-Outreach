"""
Background worker for processing long-running AI analysis jobs using Arq.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any

from arq import create_pool
from arq.connections import RedisSettings
from dotenv import load_dotenv

# Import the analysis functions from main.py
from main import analyze_transcript, analyze_linkedin_icebreaker, supabase

load_dotenv()

# Redis configuration
REDIS_SETTINGS = RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://localhost:6379"))

async def update_job_status(job_id: str, status: str, result_data: Dict[Any, Any] = None, error_message: str = None):
    """Update job status in the database"""
    if not supabase:
        print("Warning: Supabase not configured, cannot update job status")
        return
    
    try:
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if result_data:
            update_data["result_data"] = result_data
        
        if error_message:
            update_data["error_message"] = error_message
        
        result = supabase.table("jobs").update(update_data).eq("job_id", job_id).execute()
        print(f"Updated job {job_id} with status {status}")
        
    except Exception as e:
        print(f"Error updating job status: {e}")

async def process_transcript_analysis(ctx, job_id: str, transcript_data: Dict[str, Any]):
    """
    Background task to process transcript analysis
    """
    print(f"Starting transcript analysis job {job_id}")
    
    try:
        # Update status to in_progress
        await update_job_status(job_id, "in_progress")
        
        # Extract transcript data
        company_name = transcript_data["company_name"]
        attendees = transcript_data["attendees"]
        date = transcript_data["date"]
        transcript_text = transcript_data["transcript_text"]
        
        # Perform AI analysis (this is the long-running task)
        analysis = analyze_transcript(transcript_text)
        
        # Create transcript record with analysis
        transcript_id = transcript_data.get("transcript_id")
        created_at = datetime.utcnow().isoformat()
        
        transcript_record = {
            "id": transcript_id,
            "company_name": company_name,
            "attendees": attendees,
            "date": date,
            "transcript_text": transcript_text,
            "analysis": analysis,
            "job_id": job_id,
            "created_at": created_at
        }
        
        # Save to database
        if supabase:
            try:
                result = supabase.table("transcripts").insert(transcript_record).execute()
                if not result.data:
                    raise Exception("Failed to save transcript to database")
            except Exception as e:
                raise Exception(f"Database error: {e}")
        
        # Update job status to completed with result
        result_data = {
            "transcript_id": transcript_id,
            "analysis": analysis,
            "company_name": company_name
        }
        
        await update_job_status(job_id, "completed", result_data)
        
        print(f"Completed transcript analysis job {job_id}")
        return result_data
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in transcript analysis job {job_id}: {error_msg}")
        await update_job_status(job_id, "failed", error_message=error_msg)
        raise

async def process_linkedin_icebreaker(ctx, job_id: str, icebreaker_data: Dict[str, Any]):
    """
    Background task to process LinkedIn icebreaker analysis
    """
    print(f"Starting LinkedIn icebreaker job {job_id}")
    
    try:
        # Update status to in_progress
        await update_job_status(job_id, "in_progress")
        
        # Extract icebreaker data
        linkedin_bio = icebreaker_data["linkedin_bio"]
        pitch_deck = icebreaker_data["pitch_deck"]
        
        # Perform AI analysis (this is the long-running task)
        analysis = analyze_linkedin_icebreaker(linkedin_bio, pitch_deck)
        
        # Create icebreaker record with analysis
        icebreaker_id = icebreaker_data.get("icebreaker_id")
        created_at = datetime.utcnow().isoformat()
        
        icebreaker_record = {
            "id": icebreaker_id,
            "linkedin_bio": linkedin_bio,
            "pitch_deck": pitch_deck,
            "icebreaker_analysis": analysis,
            "job_id": job_id,
            "created_at": created_at
        }
        
        # Save to database
        if supabase:
            try:
                result = supabase.table("linkedin_icebreakers").insert(icebreaker_record).execute()
                if not result.data:
                    raise Exception("Failed to save icebreaker to database")
            except Exception as e:
                raise Exception(f"Database error: {e}")
        
        # Update job status to completed with result
        result_data = {
            "icebreaker_id": icebreaker_id,
            "analysis": analysis
        }
        
        await update_job_status(job_id, "completed", result_data)
        
        print(f"Completed LinkedIn icebreaker job {job_id}")
        return result_data
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in LinkedIn icebreaker job {job_id}: {error_msg}")
        await update_job_status(job_id, "failed", error_message=error_msg)
        raise

# Worker configuration
class WorkerSettings:
    functions = [process_transcript_analysis, process_linkedin_icebreaker]
    redis_settings = REDIS_SETTINGS
    job_timeout = 300  # 5 minutes timeout for jobs
    keep_result = 3600  # Keep job results for 1 hour

if __name__ == "__main__":
    # Run the worker
    from arq.worker import run_worker
    import asyncio
    
    async def main():
        await run_worker(WorkerSettings)
    
    asyncio.run(main())