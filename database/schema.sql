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