-- Create reports table
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create report_elements table (subjects within reports)
CREATE TABLE IF NOT EXISTS report_elements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  element_type TEXT NOT NULL, -- 'regulation', 'risk', 'recommendation', 'benchmark', 'news'
  order_index INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create votes table
CREATE TABLE IF NOT EXISTS votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  element_id UUID NOT NULL REFERENCES report_elements(id) ON DELETE CASCADE,
  user_name TEXT NOT NULL,
  vote_type TEXT NOT NULL CHECK (vote_type IN ('upvote', 'downvote')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(element_id, user_name)
);

-- Create comments table
CREATE TABLE IF NOT EXISTS comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  element_id UUID NOT NULL REFERENCES report_elements(id) ON DELETE CASCADE,
  user_name TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chat_messages table for AI chat history
CREATE TABLE IF NOT EXISTS chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  element_id UUID NOT NULL REFERENCES report_elements(id) ON DELETE CASCADE,
  user_name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_report_elements_report_id ON report_elements(report_id);
CREATE INDEX IF NOT EXISTS idx_votes_element_id ON votes(element_id);
CREATE INDEX IF NOT EXISTS idx_comments_element_id ON comments(element_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_element_id ON chat_messages(element_id);

-- Enable RLS (Row Level Security) - but allow public access for demo
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_elements ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (demo mode - no auth required)
CREATE POLICY "Allow public read access to reports" ON reports FOR SELECT USING (true);
CREATE POLICY "Allow public read access to report_elements" ON report_elements FOR SELECT USING (true);
CREATE POLICY "Allow public read access to votes" ON votes FOR SELECT USING (true);
CREATE POLICY "Allow public insert to votes" ON votes FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public delete to votes" ON votes FOR DELETE USING (true);
CREATE POLICY "Allow public read access to comments" ON comments FOR SELECT USING (true);
CREATE POLICY "Allow public insert to comments" ON comments FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read access to chat_messages" ON chat_messages FOR SELECT USING (true);
CREATE POLICY "Allow public insert to chat_messages" ON chat_messages FOR INSERT WITH CHECK (true);
