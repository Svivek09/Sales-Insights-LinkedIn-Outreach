import os
from celery import Celery
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "rediss://default:Ae6lAAIjcDE0YjJhOGM5MGMzNzg0OTQ4YTdmMTY0ZWY4N2RmMjIxOHAxMA@saving-starling-61093.upstash.io:6379")

# ✅ Configure Celery app
celery_app = Celery(
    "transcript_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# ✅ SSL settings for Upstash Redis (optional, safe to leave in)
if REDIS_URL.startswith("rediss://"):
    celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": "none"}
    celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "none"}

# --- Move analyze_transcript and analyze_linkedin_icebreaker here to avoid circular import ---
def analyze_transcript(transcript_text: str) -> str:
    """
    Analyze the transcript using Google Gemini Pro and return insights
    """
    try:
        import google.generativeai as genai
        import os
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"""
        Review this meeting transcript and provide a comprehensive analysis:\n\n{transcript_text}\n\nPlease provide insights in the following format:\n\n**What went well:**\n- [List specific positive aspects and why they were effective]\n\n**Areas for improvement:**\n- [List specific areas that could be enhanced]"""
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error analyzing transcript: {e}"

def analyze_linkedin_icebreaker(linkedin_bio: str, pitch_deck: str) -> str:
    """
    Analyze LinkedIn bio and pitch deck using Google Gemini Pro and return an icebreaker analysis
    """
    try:
        import google.generativeai as genai
        import os
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"""
        Review the following LinkedIn bio and pitch deck. Generate a detailed, structured analysis for sales outreach in the following format (using markdown, bold headings, and bullet points):

**Company Information:**
- Company LinkedIn: ...
- Website: ...

**Buying Signals from Pitch Deck:**
- **Signal:** ...
  - **Why it matters:** ...
  - **Source:** ...
  - **Discovery triggers:** ...

**Smart Questions to Ask:**
**At Company Level:**
- ...
**At Role Level:**
- ...

**Preferred Buying Style:**
- ...
- **How you inferred this:** ...

**Top 5 Things They'd Like from Your Deck:**
1. ...
2. ...
3. ...
4. ...
5. ...

**Potential Concerns/Clarifications Needed:**
- ...
- **Why it may not be clear/relevant:** ...
- **What to do instead:** ...

**Summary:**
...

**3 Reflection Questions to Prepare for the Meeting:**
1. ...
2. ...
3. ...

LinkedIn Bio:\n{linkedin_bio}\n\nPitch Deck:\n{pitch_deck}\n\nPlease use markdown, bold headings, and bullet points. Do NOT write an email or outreach message."""
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error analyzing LinkedIn icebreaker: {e}"

# ✅ Task to analyze transcript
@celery_app.task(bind=True, name="analyze_transcript_task")
def analyze_transcript_task(self, transcript_id, transcript_text):
    analysis = analyze_transcript(transcript_text)
    # Save analysis to Supabase
    try:
        from supabase import create_client
        import os
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            supabase.table("transcripts").update({"analysis": analysis}).eq("id", transcript_id).execute()
    except Exception as e:
        pass
    return analysis

# ✅ Task to analyze LinkedIn + pitch deck
@celery_app.task(bind=True, name="analyze_linkedin_icebreaker_task")
def analyze_linkedin_icebreaker_task(self, icebreaker_id, linkedin_bio, pitch_deck):
    analysis = analyze_linkedin_icebreaker(linkedin_bio, pitch_deck)
    # Save analysis to Supabase
    try:
        from supabase import create_client
        import os
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            supabase.table("linkedin_icebreakers").update({"icebreaker_analysis": analysis}).eq("id", icebreaker_id).execute()
    except Exception as e:
        pass
    return analysis
