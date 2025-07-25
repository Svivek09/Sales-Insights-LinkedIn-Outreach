'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, FileText, MessageSquare } from 'lucide-react';
import { 
  submitTranscript, 
  getTranscripts, 
  submitLinkedInIcebreaker, 
  getLinkedInIcebreakers 
} from '@/lib/api';

interface Transcript {
  id: string;
  company_name: string;
  attendees: string;
  date: string;
  transcript_text: string;
  analysis: string;
  created_at: string;
}

interface LinkedInIcebreaker {
  id: string;
  linkedin_bio: string;
  pitch_deck: string;
  icebreaker_analysis: string;
  created_at: string;
}

export default function Home() {
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [icebreakers, setIcebreakers] = useState<LinkedInIcebreaker[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('transcripts');
  
  // Transcript form state
  const [transcriptForm, setTranscriptForm] = useState({
    company_name: '',
    attendees: '',
    date: '',
    transcript_text: ''
  });
  
  // LinkedIn icebreaker form state
  const [icebreakerForm, setIcebreakerForm] = useState({
    linkedin_bio: '',
    pitch_deck: ''
  });

  useEffect(() => {
    fetchTranscripts();
    fetchIcebreakers();
  }, []);

  const fetchTranscripts = async () => {
    try {
      const data = await getTranscripts();
      setTranscripts(data);
    } catch (error) {
      console.error('Error fetching transcripts:', error);
    }
  };

  const fetchIcebreakers = async () => {
    try {
      const data = await getLinkedInIcebreakers();
      setIcebreakers(data);
    } catch (error) {
      console.error('Error fetching icebreakers:', error);
    }
  };

  const handleTranscriptSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await submitTranscript(transcriptForm);
          setTranscriptForm({
      company_name: '',
      attendees: '',
      date: '',
      transcript_text: ''
    });
      fetchTranscripts();
    } catch (error) {
      console.error('Error submitting transcript:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleIcebreakerSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await submitLinkedInIcebreaker(icebreakerForm);
      setIcebreakerForm({
        linkedin_bio: '',
        pitch_deck: ''
      });
      fetchIcebreakers();
    } catch (error) {
      console.error('Error submitting icebreaker:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Business Intelligence Suite
          </h1>
          <p className="text-lg text-gray-600">
            Analyze meeting transcripts and generate LinkedIn icebreakers with AI
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="transcripts" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Transcript Analysis
            </TabsTrigger>
            <TabsTrigger value="icebreakers" className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              LinkedIn Icebreaker
            </TabsTrigger>
          </TabsList>

          <TabsContent value="transcripts" className="space-y-6">
            {/* Transcript Form */}
            <Card>
              <CardHeader>
                <CardTitle>Upload Meeting Transcript</CardTitle>
                <CardDescription>
                  Paste your meeting transcript and get AI-powered insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleTranscriptSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="company_name">Company Name</Label>
                      <Input
                        id="company_name"
                        value={transcriptForm.company_name}
                        onChange={(e) => setTranscriptForm(prev => ({ ...prev, company_name: e.target.value }))}
                        placeholder="Enter company name"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="attendees">Attendees</Label>
                      <Input
                        id="attendees"
                        value={transcriptForm.attendees}
                        onChange={(e) => setTranscriptForm(prev => ({ ...prev, attendees: e.target.value }))}
                        placeholder="Enter attendees"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="date">Date</Label>
                      <Input
                        id="date"
                        type="date"
                        value={transcriptForm.date}
                        onChange={(e) => setTranscriptForm(prev => ({ ...prev, date: e.target.value }))}
                        required
                      />
                    </div>
                  </div>
                  <div>
                                            <Label htmlFor="transcript_text">Transcript Content</Label>
                        <Textarea
                          id="transcript_text"
                          value={transcriptForm.transcript_text}
                          onChange={(e) => setTranscriptForm(prev => ({ ...prev, transcript_text: e.target.value }))}
                      placeholder="Paste your meeting transcript here..."
                      rows={8}
                      required
                    />
                  </div>
                  <Button type="submit" disabled={loading} className="w-full">
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      'Analyze Transcript'
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Transcript Feed */}
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold">Analysis History</h2>
              {transcripts.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <p className="text-gray-500">No transcript analyses yet. Upload your first transcript to get started.</p>
                  </CardContent>
                </Card>
              ) : (
                transcripts.map((transcript) => (
                  <Card key={transcript.id}>
                    <CardHeader>
                      <CardTitle className="flex justify-between items-start">
                        <span>{transcript.company_name}</span>
                        <span className="text-sm font-normal text-gray-500">{transcript.date}</span>
                      </CardTitle>
                      <CardDescription>
                        Attendees: {transcript.attendees}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="prose max-w-none">
                        <div dangerouslySetInnerHTML={{ __html: transcript.analysis?.replace(/\n/g, '<br/>') || 'No analysis available' }} />
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>

          <TabsContent value="icebreakers" className="space-y-6">
            {/* LinkedIn Icebreaker Form */}
            <Card>
              <CardHeader>
                <CardTitle>Generate LinkedIn Icebreaker</CardTitle>
                <CardDescription>
                  Paste a LinkedIn bio and pitch deck to generate personalized outreach
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleIcebreakerSubmit} className="space-y-4">
                  <div>
                    <Label htmlFor="linkedin_bio">LinkedIn Bio</Label>
                    <Textarea
                      id="linkedin_bio"
                      value={icebreakerForm.linkedin_bio}
                      onChange={(e) => setIcebreakerForm(prev => ({ ...prev, linkedin_bio: e.target.value }))}
                      placeholder="Paste the LinkedIn bio here..."
                      rows={6}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="pitch_deck">Pitch Deck Content</Label>
                    <Textarea
                      id="pitch_deck"
                      value={icebreakerForm.pitch_deck}
                      onChange={(e) => setIcebreakerForm(prev => ({ ...prev, pitch_deck: e.target.value }))}
                      placeholder="Paste your pitch deck content here..."
                      rows={8}
                      required
                    />
                  </div>
                  <Button type="submit" disabled={loading} className="w-full">
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      'Generate Icebreaker'
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Icebreaker Feed */}
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold">Icebreaker History</h2>
              {icebreakers.length === 0 ? (
                <Card>
                  <CardContent className="text-center py-8">
                    <p className="text-gray-500">No icebreakers generated yet. Create your first one to get started.</p>
                  </CardContent>
                </Card>
              ) : (
                icebreakers.map((icebreaker) => (
                  <Card key={icebreaker.id}>
                    <CardHeader>
                      <CardTitle className="flex justify-between items-start">
                        <span>LinkedIn Icebreaker</span>
                        <span className="text-sm font-normal text-gray-500">
                          {new Date(icebreaker.created_at).toLocaleDateString()}
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="prose max-w-none">
                        <div dangerouslySetInnerHTML={{ __html: icebreaker.icebreaker_analysis?.replace(/\n/g, '<br/>') || 'No analysis available' }} />
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
} 