from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Transcript Insight API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://*.netlify.app",  # Netlify deployment
        "https://*.onrender.com", # Render deployment
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
        print(f"Warning: Could not initialize Supabase client: {e}")
        print("Database operations will be disabled. Please check your environment variables.")

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

def analyze_transcript(transcript_text: str) -> str:
    """
    Analyze the transcript using Google Gemini Pro and return insights
    """
    try:
        import google.generativeai as genai
        
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Review this meeting transcript and provide a comprehensive analysis:

        {transcript_text}

        Please provide insights in the following format:

        **What went well:**
        - [List specific positive aspects and why they were effective]

        **Areas for improvement:**
        - [List specific areas that could be enhanced]

        **Recommendations for next time:**
        - [List actionable suggestions for future meetings]

        **Key takeaways:**
        - [Summarize the most important points from the meeting]

        Focus on communication effectiveness, meeting structure, participant engagement, and actionable outcomes.
        Be specific, actionable, and encouraging in your feedback.
        """

        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise Exception("No response generated")
            
    except Exception as e:
        print(f"Error analyzing transcript: {e}")
        # Return a mock analysis for testing when API fails
        return f"""**What went well:**
- The meeting had clear participants and agenda
- Good structure with introduction and conclusion
- Participants were engaged in the discussion

**Areas for improvement:**
- Could benefit from more specific action items
- Consider adding time allocations for each topic
- Include follow-up meeting scheduling

**Recommendations for next time:**
- Create a detailed agenda with time slots
- Assign action items with deadlines
- Send meeting summary within 24 hours

**Key takeaways:**
- Meeting covered important quarterly planning topics
- Team collaboration was effective
- Clear next steps were identified

        *Note: This is a mock analysis. Please add your Gemini API key for real AI-powered insights.*"""

def analyze_linkedin_icebreaker(linkedin_bio: str, pitch_deck: str) -> str:
    """
    Analyze LinkedIn bio and pitch deck to generate icebreaker insights
    """
    try:
        import google.generativeai as genai
        
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Analyze this LinkedIn bio and pitch deck to create a comprehensive cold outreach strategy:

        **LinkedIn Bio:**
        {linkedin_bio}

        **Pitch Deck:**
        {pitch_deck}

        Please provide a detailed analysis in the following format:

        **Company Information:**
        - Company LinkedIn: [Extract or infer]
        - Website: [Extract or infer]

        **Buying Signals from Pitch Deck:**
        - [List specific buying signals]
        - Why they matter: [Explain significance]
        - Source of information: [Where this signal comes from]
        - Discovery triggers: [What questions this raises]

        **Smart Questions to Ask:**
        **At Company Level:**
        - [List strategic company-level questions]

        **At Role Level:**
        - [List role-specific questions]

        **Preferred Buying Style:**
        - [Analyze and infer their buying style]
        - How you inferred this: [Explain your reasoning]

        **Top 5 Things They'd Like from Your Deck:**
        - [List the most relevant aspects]
        - [Explain why each is valuable to them]

        **Potential Concerns/Clarifications Needed:**
        - [Identify unclear, irrelevant, or less valuable parts]
        - Why they may not be clear/relevant: [Explain]
        - What to do instead: [Suggest alternatives]

        **Summary:**
        [Brief summary of key insights]

        **3 Reflection Questions to Prepare for the Meeting:**
        1. [Strategic preparation question]
        2. [Tactical preparation question]
        3. [Relationship-building question]

        Focus on creating actionable insights that will help with cold outreach and meeting preparation.
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise Exception("No response generated")
            
    except Exception as e:
        print(f"Error analyzing LinkedIn icebreaker: {e}")
        # Return a mock analysis for testing when API fails
        return f"""**Company Information:**
- Company LinkedIn: [Extract from bio]
- Website: [Extract from bio]

**Buying Signals from Pitch Deck:**
- [Analyze pitch deck for buying signals]
- Why they matter: [Explain significance]
- Source of information: [Where this signal comes from]
- Discovery triggers: [What questions this raises]

**Smart Questions to Ask:**
**At Company Level:**
- What are your current priorities for this quarter?
- How do you measure success in your role?

**At Role Level:**
- What challenges are you currently facing?
- What solutions have you tried so far?

**Preferred Buying Style:**
- [Analyze bio for buying style indicators]
- How you inferred this: [Explain reasoning]

**Top 5 Things They'd Like from Your Deck:**
- [List relevant aspects from pitch deck]
- [Explain value to this specific person]

**Potential Concerns/Clarifications Needed:**
- [Identify unclear parts]
- Why they may not be clear: [Explain]
- What to do instead: [Suggest alternatives]

**Summary:**
Key insights for cold outreach strategy.

**3 Reflection Questions to Prepare for the Meeting:**
1. How can I best position our solution for their specific needs?
2. What objections might they have and how can I address them?
3. How can I build rapport and trust quickly?

*Note: This is a mock analysis. Please add your Gemini API key for real AI-powered insights.*"""

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

@app.post("/transcripts", response_model=TranscriptResponse)
async def create_transcript(transcript: TranscriptCreate):
    try:
        # Generate analysis using OpenAI
        analysis = analyze_transcript(transcript.transcript_text)
        
        # Create transcript record
        transcript_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        transcript_data = {
            "id": transcript_id,
            "company_name": transcript.company_name,
            "attendees": transcript.attendees,
            "date": transcript.date,
            "transcript_text": transcript.transcript_text,
            "analysis": analysis,
            "created_at": created_at
        }
        
        # Insert into Supabase if available
        if supabase:
            try:
                result = supabase.table("transcripts").insert(transcript_data).execute()
                if not result.data:
                    raise HTTPException(status_code=500, detail="Failed to save transcript")
            except Exception as e:
                print(f"Warning: Could not save to database: {e}")
                # Continue without database save for demo purposes
        else:
            print("Warning: Supabase not configured, transcript not saved to database")
        
        return TranscriptResponse(**transcript_data)
            
    except Exception as e:
        print(f"Error creating transcript: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
            print("Warning: Supabase not configured, returning empty list")
            return []
            
    except Exception as e:
        print(f"Error fetching transcripts: {e}")
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
        print(f"Error fetching transcript: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# LinkedIn Icebreaker endpoints
@app.post("/linkedin-icebreakers", response_model=LinkedInIcebreakerResponse)
async def create_linkedin_icebreaker(icebreaker: LinkedInIcebreakerCreate):
    try:
        # Generate analysis using Gemini
        analysis = analyze_linkedin_icebreaker(icebreaker.linkedin_bio, icebreaker.pitch_deck)
        
        # Create icebreaker record
        icebreaker_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        icebreaker_data = {
            "id": icebreaker_id,
            "linkedin_bio": icebreaker.linkedin_bio,
            "pitch_deck": icebreaker.pitch_deck,
            "icebreaker_analysis": analysis,
            "created_at": created_at
        }
        
        # Insert into Supabase if available
        if supabase:
            try:
                result = supabase.table("linkedin_icebreakers").insert(icebreaker_data).execute()
                if not result.data:
                    raise HTTPException(status_code=500, detail="Failed to save icebreaker")
            except Exception as e:
                print(f"Warning: Could not save to database: {e}")
                # Continue without database save for demo purposes
        else:
            print("Warning: Supabase not configured, icebreaker not saved to database")
        
        return LinkedInIcebreakerResponse(**icebreaker_data)
            
    except Exception as e:
        print(f"Error creating LinkedIn icebreaker: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
            print("Warning: Supabase not configured, returning empty list")
            return []
            
    except Exception as e:
        print(f"Error fetching LinkedIn icebreakers: {e}")
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
        print(f"Error fetching LinkedIn icebreaker: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 