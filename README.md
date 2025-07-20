# Transcript Insight

A full-stack application that analyzes meeting transcripts using AI to provide actionable insights and recommendations.

## Features

### Transcript Analysis
- **Transcript Upload**: Paste meeting transcripts with metadata (company name, attendees, date)
- **AI Analysis**: Automatic analysis using Google Gemini Pro to identify:
  - What went well and why
  - Areas for improvement
  - Recommendations for next time
  - Key takeaways
- **Feed Display**: View all analyzed transcripts in a clean, organized feed

### LinkedIn Icebreaker
- **Bio Analysis**: Paste LinkedIn bios and pitch deck content
- **AI-Powered Insights**: Generate comprehensive cold outreach strategies including:
  - Company information extraction
  - Buying signals analysis
  - Smart questions for different levels
  - Preferred buying style analysis
  - Top 5 things they'd like from your deck
  - Potential concerns and clarifications
  - Reflection questions for meeting preparation

### Modern UI
- **Tabbed Interface**: Switch between features seamlessly
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Instant feedback and loading states
- **Error Handling**: Graceful fallbacks when services are unavailable

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI components
- **Lucide React** - Beautiful icons

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Supabase** - Database and backend services
- **Google Gemini Pro** - AI-powered analysis
- **Docker** - Containerization for deployment

### Database
- **Supabase** - PostgreSQL database with real-time capabilities

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Supabase account
- Google Gemini API key

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Settings > API to get your project URL and anon key
3. Run the database schema:

```sql
-- Copy and paste the contents of database/schema.sql into the Supabase SQL editor
```

### 3. Configure Environment Variables

#### Backend (.env file in backend directory)
```bash
cd backend
cp env.example .env
```

Edit `.env` with your actual values:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Start the Development Servers

#### Terminal 1 - Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. **Upload a Transcript**:
   - Fill in the company name, attendees, and date
   - Paste your meeting transcript in the text area
   - Click "Analyze Transcript"

2. **View Analysis**:
   - The AI will analyze your transcript and provide insights
   - Results are displayed in the feed below the upload form
   - Each analysis includes what went well, areas for improvement, and recommendations

3. **Browse Feed**:
   - View all previously analyzed transcripts
   - Sort by creation date (newest first)
   - See company, attendees, and date information

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check for deployment
- `POST /transcripts` - Create and analyze a new transcript
- `GET /transcripts` - Get all transcripts
- `GET /transcripts/{id}` - Get a specific transcript
- `POST /linkedin-icebreakers` - Create and analyze a new LinkedIn icebreaker
- `GET /linkedin-icebreakers` - Get all LinkedIn icebreakers
- `GET /linkedin-icebreakers/{id}` - Get a specific LinkedIn icebreaker

## Project Structure

```
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main page component
├── components/            # React components
│   └── ui/               # shadcn/ui components
├── lib/                  # Utility functions
├── backend/              # FastAPI backend
│   ├── main.py           # Main API application
│   ├── requirements.txt  # Python dependencies
│   └── env.example       # Environment variables template
├── database/             # Database schema
│   └── schema.sql        # Supabase table definitions
└── README.md             # This file
```

## Customization

### Modifying the AI Analysis

Edit the `analyze_transcript` function in `backend/main.py` to customize the analysis prompt or use different AI models.

### Styling

The application uses Tailwind CSS with shadcn/ui components. You can customize the design by:
- Modifying `app/globals.css` for global styles
- Updating component styles in the `components/ui/` directory
- Adding custom Tailwind classes to components

### Database Schema

To add new fields or modify the database structure:
1. Update `database/schema.sql`
2. Run the new SQL in your Supabase dashboard
3. Update the Pydantic models in `backend/main.py`
4. Update the frontend TypeScript interfaces

## Deployment

### Quick Deployment

Run the deployment script to prepare your application for deployment:

```bash
./deploy.sh
```

This script will:
- Install dependencies
- Test the build
- Set up Git repository
- Provide step-by-step deployment instructions

### Manual Deployment

#### 1. GitHub Repository
```bash
# Initialize Git repository
git init
git add .
git commit -m "Initial commit"

# Add your GitHub repository
git remote add origin https://github.com/yourusername/transcript-insight.git
git push -u origin main
```

#### 2. Backend Deployment (Render)
1. Go to [render.com](https://render.com) and create an account
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure settings:
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty)
5. Add environment variables:
   - `GOOGLE_API_KEY=your_gemini_api_key`
   - `SUPABASE_URL=your_supabase_url`
   - `SUPABASE_KEY=your_supabase_key`
6. Deploy and note the URL

#### 3. Frontend Deployment (Netlify)
1. Go to [netlify.com](https://netlify.com) and create an account
2. Create a new site from Git
3. Connect your GitHub repository
4. Configure build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com`
6. Deploy

### Environment Variables

#### Backend (Render)
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key

#### Frontend (Netlify)
- `NEXT_PUBLIC_API_URL`: Your deployed backend URL

### Database
- Supabase provides hosting for the PostgreSQL database
- No additional setup required

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes. 