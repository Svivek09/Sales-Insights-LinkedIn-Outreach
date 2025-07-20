# Quick Start Guide

Get Transcript Insight running in 5 minutes!

## Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Supabase account (free)
- OpenAI API key

## 1. One-Click Setup
```bash
./setup.sh
```

## 2. Configure API Keys

### Get Supabase Keys
1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Settings > API
4. Copy the "Project URL" and "anon public" key

### Get OpenAI Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account and add billing info
3. Go to API Keys and create a new key

### Update Environment
Edit `backend/.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
OPENAI_API_KEY=sk-your-openai-key
```

## 3. Set Up Database
1. In your Supabase dashboard, go to SQL Editor
2. Copy and paste the contents of `database/schema.sql`
3. Click "Run" to create the table

## 4. Start the Application

### Terminal 1 - Backend
```bash
cd backend
uvicorn main:app --reload
```

### Terminal 2 - Frontend
```bash
npm run dev
```

## 5. Test the Application
1. Open http://localhost:3000
2. Fill in the form with:
   - Company: "TechCorp"
   - Attendees: "Sarah, Mike, Lisa, David"
   - Date: Today's date
   - Transcript: Copy the content from `sample-transcript.txt`
3. Click "Analyze Transcript"
4. View the AI-generated insights!

## Troubleshooting

### Backend won't start
- Check that all environment variables are set in `backend/.env`
- Ensure Python dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Check that Node.js dependencies are installed: `npm install`
- Ensure you're using Node.js 18+

### Database errors
- Verify your Supabase URL and key are correct
- Check that the `transcripts` table was created successfully

### AI analysis not working
- Verify your OpenAI API key is valid and has credits
- Check the backend logs for error messages

## Next Steps
- Read the full [README.md](README.md) for detailed documentation
- Customize the AI analysis prompt in `backend/main.py`
- Add authentication and user management
- Deploy to production

Need help? Check the [README.md](README.md) for more detailed instructions. 