-- Add sample votes from various employees
INSERT INTO votes (element_id, user_name, vote_type) 
SELECT id, 'Janusz Trucker', 'upvote' 
FROM report_elements 
WHERE element_type = 'recommendation' 
LIMIT 8;

INSERT INTO votes (element_id, user_name, vote_type) 
SELECT id, 'Anna Kowalska', 'upvote' 
FROM report_elements 
WHERE element_type = 'regulation' 
LIMIT 6;

INSERT INTO votes (element_id, user_name, vote_type) 
SELECT id, 'Piotr Nowak', 'downvote' 
FROM report_elements 
WHERE element_type = 'benchmark' 
LIMIT 3;

INSERT INTO votes (element_id, user_name, vote_type) 
SELECT id, 'Maria Wiśniewska', 'upvote' 
FROM report_elements 
WHERE element_type = 'risk' 
LIMIT 7;

-- Add sample comments
INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Janusz Trucker',
  'This is critical for our Q2 planning. We need to allocate budget immediately.'
FROM report_elements
WHERE title = 'Encryption Requirements for System Logs';

INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Anna Kowalska',
  'I agree with the recommendation. We should prioritize this over other IT projects.'
FROM report_elements
WHERE title = 'TMS (Transport Management System) Modernization';

INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Piotr Nowak',
  'The cost seems high. Can we explore open-source alternatives?'
FROM report_elements
WHERE title = 'Cybersecurity Infrastructure Investment Priority';

INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Maria Wiśniewska',
  'Our drivers have been complaining about this. Good to see data backing up their concerns.'
FROM report_elements
WHERE title = 'Working Time Directive Violations Risk';

INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Tomasz Zieliński',
  'We had a similar issue last year. The automated solution worked well for us.'
FROM report_elements
WHERE title = 'VAT Reverse Charge Mechanism Errors';

INSERT INTO comments (element_id, user_name, content)
SELECT 
  id,
  'Katarzyna Lewandowska',
  'This benchmark is eye-opening. We are falling behind competitors.'
FROM report_elements
WHERE title = 'Digital Maturity Benchmark - EU Logistics Sector';
