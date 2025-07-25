-- Create transcripts table
CREATE TABLE IF NOT EXISTS transcripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    attendees TEXT NOT NULL,
    date DATE NOT NULL,
    transcript_text TEXT NOT NULL,
    analysis TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_transcripts_created_at ON transcripts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transcripts_company_name ON transcripts(company_name);

-- Enable Row Level Security (RLS)
ALTER TABLE transcripts ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (you can customize this based on your needs)
CREATE POLICY "Allow all operations on transcripts" ON transcripts
    FOR ALL USING (true);

-- Create linkedin_icebreakers table
CREATE TABLE IF NOT EXISTS linkedin_icebreakers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    linkedin_bio TEXT NOT NULL,
    pitch_deck TEXT NOT NULL,
    icebreaker_analysis TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_linkedin_icebreakers_created_at ON linkedin_icebreakers(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE linkedin_icebreakers ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations
CREATE POLICY "Allow all operations on linkedin_icebreakers" ON linkedin_icebreakers
    FOR ALL USING (true);

-- Create jobs table for queue management
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id TEXT UNIQUE NOT NULL, -- Arq job ID
    job_type TEXT NOT NULL, -- 'transcript_analysis' or 'linkedin_icebreaker'
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed'
    input_data JSONB NOT NULL,
    result_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for job management
CREATE INDEX IF NOT EXISTS idx_jobs_job_id ON jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);

-- Enable Row Level Security
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations
CREATE POLICY "Allow all operations on jobs" ON jobs
    FOR ALL USING (true);

-- Add job_id column to existing tables to link to jobs
ALTER TABLE transcripts ADD COLUMN IF NOT EXISTS job_id TEXT;
ALTER TABLE linkedin_icebreakers ADD COLUMN IF NOT EXISTS job_id TEXT; 