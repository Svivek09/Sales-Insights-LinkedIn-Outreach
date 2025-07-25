from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv
import redis
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from backend.celery_app import celery_app, analyze_transcript_task, analyze_linkedin_icebreaker_task
from celery.result import AsyncResult


load_dotenv()
CELERY_BROKER_URL = os.getenv("REDIS_URL")

app = FastAPI(title="Transcript Insight API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://sales-insights.netlify.app",  # Netlify production
        "https://sales-insights-linkedin-outreach.onrender.com", # Render production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        pass

# GEMINI API key will be used in the analyze_transcript function

class TranscriptCreate(BaseModel):
    company_name: str
    attendees: str
    date: str
    transcript_text: str

class TranscriptResponse(BaseModel):
    id: str
    company_name: str
    attendees: str
    date: str
    transcript_text: str
    analysis: str
    created_at: str

class LinkedInIcebreakerCreate(BaseModel):
    linkedin_bio: str
    pitch_deck: str

class LinkedInIcebreakerResponse(BaseModel):
    id: str
    linkedin_bio: str
    pitch_deck: str
    icebreaker_analysis: str
    created_at: str


@app.get("/")
async def root():
    return {"message": "Transcript Insight API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "api": "running",
            "database": "connected" if supabase else "disconnected"
        }
    }

@app.post("/transcripts", response_model=None)
async def create_transcript(transcript: TranscriptCreate):
    # Enqueue the analysis job
    transcript_id = str(uuid.uuid4())
    job = analyze_transcript_task.apply_async(args=[transcript_id, transcript.transcript_text])
    # Store metadata in Redis for later retrieval (optional, for demo)
    r = redis.Redis.from_url(CELERY_BROKER_URL)
    meta = {
        "id": transcript_id,
        "company_name": transcript.company_name,
        "attendees": transcript.attendees,
        "date": transcript.date,
        "transcript_text": transcript.transcript_text,
        "created_at": datetime.utcnow().isoformat(),
        "job_id": job.id
    }
    r.hset(f"transcript:{transcript_id}", mapping=meta)
    # Insert the new transcript into Supabase with empty analysis
    if supabase:
        try:
            supabase.table("transcripts").insert({
                "id": transcript_id,
                "company_name": transcript.company_name,
                "attendees": transcript.attendees,
                "date": transcript.date,
                "transcript_text": transcript.transcript_text,
                "analysis": "",
                "created_at": datetime.utcnow().isoformat(),
                "job_id": job.id
            }).execute()
        except Exception as e:
            pass
    return {"job_id": job.id, "transcript_id": transcript_id}

@app.get("/transcripts/job/{job_id}")
async def get_transcript_job_status(job_id: str):
    job = AsyncResult(job_id, app=celery_app)
    if job.state == "PENDING":
        return {"status": "pending"}
    elif job.state == "STARTED":
        return {"status": "started"}
    elif job.state == "SUCCESS":
        return {"status": "success", "result": job.result}
    elif job.state == "FAILURE":
        return {"status": "failure", "error": str(job.info)}
    else:
        return {"status": job.state}

@app.get("/transcripts", response_model=List[TranscriptResponse])
async def get_transcripts():
    try:
        if supabase:
            result = supabase.table("transcripts").select("*").order("created_at", desc=True).execute()
            
            if result.data:
                return [TranscriptResponse(**transcript) for transcript in result.data]
            else:
                return []
        else:
            pass
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/transcripts/{transcript_id}", response_model=TranscriptResponse)
async def get_transcript(transcript_id: str):
    try:
        if supabase:
            result = supabase.table("transcripts").select("*").eq("id", transcript_id).execute()
            
            if result.data:
                return TranscriptResponse(**result.data[0])
            else:
                raise HTTPException(status_code=404, detail="Transcript not found")
        else:
            raise HTTPException(status_code=503, detail="Database not configured")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# LinkedIn Icebreaker endpoints
@app.post("/linkedin-icebreakers", response_model=None)
async def create_linkedin_icebreaker(icebreaker: LinkedInIcebreakerCreate):
    # Enqueue the analysis job
    icebreaker_id = str(uuid.uuid4())
    job = analyze_linkedin_icebreaker_task.apply_async(args=[icebreaker_id, icebreaker.linkedin_bio, icebreaker.pitch_deck])
    # Store metadata in Redis for later retrieval (optional, for demo)
    r = redis.Redis.from_url(CELERY_BROKER_URL)
    meta = {
        "id": icebreaker_id,
        "linkedin_bio": icebreaker.linkedin_bio,
        "pitch_deck": icebreaker.pitch_deck,
        "created_at": datetime.utcnow().isoformat(),
        "job_id": job.id
    }
    r.hset(f"icebreaker:{icebreaker_id}", mapping=meta)
    # Insert the new icebreaker into Supabase with empty analysis
    if supabase:
        try:
            supabase.table("linkedin_icebreakers").insert({
                "id": icebreaker_id,
                "linkedin_bio": icebreaker.linkedin_bio,
                "pitch_deck": icebreaker.pitch_deck,
                "icebreaker_analysis": "",
                "created_at": datetime.utcnow().isoformat(),
                "job_id": job.id
            }).execute()
        except Exception as e:
            pass
    return {"job_id": job.id, "icebreaker_id": icebreaker_id}

@app.get("/linkedin-icebreakers/job/{job_id}")
async def get_linkedin_icebreaker_job_status(job_id: str):
    job = AsyncResult(job_id, app=celery_app)
    if job.state == "PENDING":
        return {"status": "pending"}
    elif job.state == "STARTED":
        return {"status": "started"}
    elif job.state == "SUCCESS":
        return {"status": "success", "result": job.result}
    elif job.state == "FAILURE":
        return {"status": "failure", "error": str(job.info)}
    else:
        return {"status": job.state}

@app.get("/linkedin-icebreakers", response_model=List[LinkedInIcebreakerResponse])
async def get_linkedin_icebreakers():
    try:
        if supabase:
            result = supabase.table("linkedin_icebreakers").select("*").order("created_at", desc=True).execute()
            
            if result.data:
                return [LinkedInIcebreakerResponse(**icebreaker) for icebreaker in result.data]
            else:
                return []
        else:
            pass
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/linkedin-icebreakers/{icebreaker_id}", response_model=LinkedInIcebreakerResponse)
async def get_linkedin_icebreaker(icebreaker_id: str):
    try:
        if supabase:
            result = supabase.table("linkedin_icebreakers").select("*").eq("id", icebreaker_id).execute()
            
            if result.data:
                return LinkedInIcebreakerResponse(**result.data[0])
            else:
                raise HTTPException(status_code=404, detail="LinkedIn icebreaker not found")
        else:
            raise HTTPException(status_code=503, detail="Database not configured")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 