-- Insert 10 comprehensive logistics reports with detailed data

-- Report 1: NIS2 Directive Compliance
INSERT INTO reports (id, title, summary, created_at) VALUES 
('11111111-1111-1111-1111-111111111111', 
 'NIS2 Directive Compliance Requirements - Q2 2025',
 'Critical analysis of NIS2 cybersecurity requirements for logistics operators. Includes encryption mandates, incident reporting obligations, and supply chain security measures. Action required by Q2 2026.',
 NOW() - INTERVAL '2 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('11111111-1111-1111-1111-111111111111', 
 'Encryption Requirements for System Logs',
 'NIS2 Article 21 mandates encryption of all system logs containing sensitive operational data. Current assessment shows ERP backup systems lack SSL/TLS encryption. Risk Level: HIGH. Estimated implementation cost: 2,000-3,500 PLN. Timeline: 10-15 business days. Recommended solution: Implement automated certificate rotation using Let''s Encrypt with backup encryption via AES-256. Non-compliance penalties: up to 10M EUR or 2% of global turnover.',
 'regulation', 1),
('11111111-1111-1111-1111-111111111111',
 'Incident Reporting Timeline - 24 Hour Window',
 'NIS2 requires significant cybersecurity incidents to be reported within 24 hours of detection. Current incident response plan lacks automated detection mechanisms. Gap Analysis: No SIEM system in place, manual log review takes 48-72 hours. Recommendation: Deploy automated monitoring solution (Coroot/Keep) with real-time alerting. Budget: 5,000-8,000 PLN initial setup + 1,200 PLN/month operational costs.',
 'risk', 2),
('11111111-1111-1111-1111-111111111111',
 'Supply Chain Security Assessment',
 'NIS2 extends cybersecurity obligations to supply chain partners. Current vendor assessment shows 67% of logistics partners lack basic security certifications. Action Required: Implement vendor security questionnaire, require ISO 27001 or equivalent for critical partners. Timeline: Q3 2025. Legal basis: NIS2 Article 20(1). Industry benchmark: 78% of EU logistics firms already conducting vendor security audits.',
 'recommendation', 3),
('11111111-1111-1111-1111-111111111111',
 'EU Logistics Sector Compliance Benchmark',
 'Recent survey of 450 EU logistics operators shows: 72% have implemented log encryption, 65% have 24-hour incident response capability, 58% conduct regular penetration testing. Big Trucking Corp Ltd. currently meets 1 of 3 benchmarks. Competitive risk: Customers increasingly require NIS2 compliance proof for contract renewals.',
 'benchmark', 4);

-- Report 2: AI Act Implementation
INSERT INTO reports (id, title, summary, created_at) VALUES 
('22222222-2222-2222-2222-222222222222',
 'EU AI Act - Impact on Route Optimization Systems',
 'Assessment of AI Act obligations for logistics AI systems. Covers risk classification, transparency requirements, and documentation obligations for route optimization and predictive maintenance algorithms.',
 NOW() - INTERVAL '5 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('22222222-2222-2222-2222-222222222222',
 'Risk Classification of Route Optimization AI',
 'EU AI Act classifies route optimization systems as "limited risk" AI requiring transparency obligations. Current system lacks user notification of AI decision-making. Required actions: (1) Implement AI disclosure in driver interface, (2) Document training data sources, (3) Establish human oversight mechanism. Compliance deadline: August 2026. Legal basis: AI Act Article 52.',
 'regulation', 1),
('22222222-2222-2222-2222-222222222222',
 'Documentation Requirements for AI Systems',
 'AI Act mandates technical documentation including: training data characteristics, model architecture, validation results, and risk management procedures. Current gap: No centralized AI documentation system. Recommendation: Establish AI governance framework with quarterly audits. Estimated effort: 40-60 hours initial documentation + 8 hours/month maintenance.',
 'recommendation', 2),
('22222222-2222-2222-2222-222222222222',
 'Predictive Maintenance Algorithm Compliance',
 'Predictive maintenance AI for fleet management classified as "minimal risk" under AI Act. However, GDPR implications exist if driver behavior data is used. Current system processes driver performance metrics without explicit consent documentation. Risk: GDPR violation (Article 6). Recommendation: Update privacy policy and implement consent management system. Timeline: 30 days.',
 'risk', 3),
('22222222-2222-2222-2222-222222222222',
 'Industry AI Adoption Rates',
 'Market analysis shows 84% of major EU logistics operators use AI for route optimization, 62% for predictive maintenance, 45% for demand forecasting. Only 31% have completed AI Act compliance assessment. Early compliance provides competitive advantage in B2B contracts. Average compliance cost: 15,000-25,000 PLN for mid-size operators.',
 'benchmark', 4);

-- Report 3: CSRD Sustainability Reporting
INSERT INTO reports (id, title, summary, created_at) VALUES 
('33333333-3333-3333-3333-333333333333',
 'CSRD Environmental Reporting - Carbon Emissions Tracking',
 'Corporate Sustainability Reporting Directive (CSRD) obligations for logistics sector. Covers Scope 1, 2, and 3 emissions tracking, ESG disclosure requirements, and sustainability data management.',
 NOW() - INTERVAL '7 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('33333333-3333-3333-3333-333333333333',
 'Scope 3 Emissions Calculation Methodology',
 'CSRD requires comprehensive Scope 3 emissions reporting including supply chain transportation. Current gap: No automated fuel consumption tracking across subcontractor fleet. Recommendation: Implement IoT-based fuel monitoring system with API integration to accounting software. Estimated ROI: 18-24 months through fuel optimization. Compliance deadline: Fiscal year 2025 reporting (due 2026).',
 'regulation', 1),
('33333333-3333-3333-3333-333333333333',
 'ESG Data Management System Requirements',
 'CSRD mandates auditable ESG data with third-party verification. Current state: Manual Excel-based tracking, no audit trail. Risk: Reporting errors, audit failures, reputational damage. Solution: Deploy ESG data management platform (e.g., Renewator, Sphera). Budget: 12,000-18,000 PLN annually. Alternative: Custom solution using existing ERP integration (8,000 PLN development).',
 'recommendation', 2),
('33333333-3333-3333-3333-333333333333',
 'Double Materiality Assessment Gap',
 'CSRD requires double materiality assessment: environmental impact AND financial impact of sustainability issues. Current assessment incomplete - missing climate risk financial modeling. Required: Engage sustainability consultant for materiality workshop. Cost: 8,000-12,000 PLN. Timeline: 6-8 weeks. Legal basis: CSRD Article 19a, ESRS 1.',
 'risk', 3),
('33333333-3333-3333-3333-333333333333',
 'Logistics Sector Sustainability Performance',
 'Industry benchmark data: Average EU logistics operator carbon intensity: 62g CO2/ton-km. Big Trucking Corp Ltd. estimated at 71g CO2/ton-km (14% above average). Top quartile performers: 48g CO2/ton-km. Key success factors: Modern fleet (Euro 6 standards), route optimization AI, driver eco-training programs. Potential savings: 15-20% emissions reduction = 180,000 PLN annual fuel cost savings.',
 'benchmark', 4);

-- Report 4: Digital CMR Implementation
INSERT INTO reports (id, title, summary, created_at) VALUES 
('44444444-4444-4444-4444-444444444444',
 'Digital CMR (eCMR) - Legal Framework and Implementation',
 'Analysis of electronic consignment note requirements under UN eCMR protocol. Covers legal validity, system requirements, cross-border recognition, and integration with existing TMS.',
 NOW() - INTERVAL '10 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('44444444-4444-4444-4444-444444444444',
 'eCMR Legal Validity Across EU Borders',
 'UN eCMR protocol now ratified by 34 countries including all major EU markets. Digital CMR has same legal status as paper CMR. Current gap: TMS system lacks eCMR module. Recommendation: Upgrade to TMS version 8.2+ with native eCMR support OR integrate standalone eCMR platform (e.g., Transporeon, TimoCom). Cost comparison: TMS upgrade 6,500 PLN vs. standalone platform 3,200 PLN/year.',
 'regulation', 1),
('44444444-4444-4444-4444-444444444444',
 'Electronic Signature Requirements',
 'eCMR requires qualified electronic signatures (QES) or advanced electronic signatures (AES) depending on jurisdiction. Current driver mobile app lacks signature capability. Technical requirement: Implement signature pad with biometric authentication + timestamp + GPS coordinates. Development cost: 4,500 PLN. Alternative: Use third-party eCMR app (1,200 PLN/year for 50 drivers).',
 'recommendation', 2),
('44444444-4444-4444-4444-444444444444',
 'Paper CMR Backup Obligation',
 'Despite eCMR adoption, paper backup still required for non-eCMR countries (Russia, Belarus, Turkey). Risk: Drivers not carrying paper CMR for mixed routes. Recommendation: Update driver procedures, implement automated route analysis to flag non-eCMR destinations. Training required: 2-hour workshop for all drivers. Timeline: 30 days.',
 'risk', 3),
('44444444-4444-4444-4444-444444444444',
 'eCMR Adoption Rates in EU Logistics',
 'Market penetration: 68% of EU logistics companies use eCMR for at least 50% of shipments. Full digital adoption (90%+ eCMR): 42% of operators. Benefits reported: 35% faster document processing, 89% reduction in document errors, 12% improvement in invoice payment speed. Average payback period: 8 months. Big Trucking Corp Ltd. current eCMR usage: 0%.',
 'benchmark', 4);

-- Report 5: Cybersecurity Incident Response
INSERT INTO reports (id, title, summary, created_at) VALUES 
('55555555-5555-5555-5555-555555555555',
 'Cybersecurity Incident Response Plan - Gap Analysis',
 'Comprehensive review of current incident response capabilities against NIS2 and ISO 27035 standards. Identifies critical gaps in detection, containment, and recovery procedures.',
 NOW() - INTERVAL '14 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('55555555-5555-5555-5555-555555555555',
 'Automated Threat Detection Gaps',
 'Current security posture: Manual log review, no SIEM, no intrusion detection system (IDS). Mean time to detect (MTTD): 72+ hours. Industry standard: <4 hours. Critical risk: Ransomware attacks average 48-hour encryption cycle - current detection too slow to prevent major damage. Recommendation: Deploy Coroot or Wazuh SIEM with automated alerting. Cost: 6,000 PLN setup + 1,500 PLN/month.',
 'risk', 1),
('55555555-5555-5555-5555-555555555555',
 'Incident Response Team Structure',
 'NIS2 requires designated incident response team with defined roles. Current state: No formal team, IT manager handles all incidents part-time. Recommendation: Establish CSIRT (Computer Security Incident Response Team) with: (1) Incident Commander, (2) Technical Lead, (3) Communications Officer, (4) Legal Liaison. Training required: SANS SEC504 or equivalent. Budget: 15,000 PLN training + 8 hours/month retainer.',
 'recommendation', 2),
('55555555-5555-5555-5555-555555555555',
 'Backup and Recovery Testing Deficiency',
 'Last backup restoration test: 14 months ago. Current RTO (Recovery Time Objective): Unknown. RPO (Recovery Point Objective): 24 hours. Industry standard: RTO <4 hours, RPO <1 hour for critical systems. Risk: Backup corruption undetected, recovery procedures outdated. Mandatory action: Quarterly backup restoration drills. Next test: Within 30 days.',
 'risk', 3),
('55555555-5555-5555-5555-555555555555',
 'Cyber Insurance Coverage Analysis',
 'Current cyber insurance policy: 500,000 PLN coverage, excludes ransomware payments. Industry benchmark: 2,000,000 PLN coverage with ransomware rider. Average logistics sector cyber incident cost: 850,000 PLN (downtime + recovery + legal). Recommendation: Increase coverage to 2M PLN, add business interruption rider. Premium increase: ~4,500 PLN/year. ROI: Single incident prevention justifies 10+ years premiums.',
 'benchmark', 4);

-- Report 6: GDPR Compliance for Fleet Telematics
INSERT INTO reports (id, title, summary, created_at) VALUES 
('66666666-6666-6666-6666-666666666666',
 'GDPR Compliance - Fleet Telematics and Driver Monitoring',
 'Privacy impact assessment for GPS tracking, driver behavior monitoring, and tachograph data processing. Covers legal basis, data minimization, and employee privacy rights.',
 NOW() - INTERVAL '18 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('66666666-6666-6666-6666-666666666666',
 'Legal Basis for GPS Tracking',
 'GDPR Article 6(1)(f) allows GPS tracking based on legitimate interest (fleet management, safety). However, Article 88 requires balancing employer interests vs. employee privacy. Current gap: No documented legitimate interest assessment (LIA). Risk: GDPR violation, employee complaints to data protection authority. Required action: Complete LIA, update employee handbook, obtain works council approval. Timeline: 45 days. Legal support cost: 5,000 PLN.',
 'regulation', 1),
('66666666-6666-6666-6666-666666666666',
 'Data Retention Policy Violations',
 'Current practice: GPS data retained indefinitely. GDPR requires data minimization and defined retention periods. Recommendation: Implement automated data deletion: GPS tracks 90 days, driver performance data 12 months, accident-related data 7 years (legal requirement). Technical implementation: Database cleanup scripts + audit logging. Development cost: 3,500 PLN.',
 'risk', 2),
('66666666-6666-6666-6666-666666666666',
 'Driver Privacy Rights - GDPR Article 15',
 'Drivers have right to access all personal data. Current gap: No self-service portal for data access requests. Manual processing time: 8-12 hours per request. Recommendation: Develop driver portal showing: GPS history, performance metrics, tachograph data. Benefits: GDPR compliance + driver transparency + reduced admin workload. Development cost: 12,000 PLN. Alternative: Use existing telematics vendor portal (included in contract).',
 'recommendation', 3),
('66666666-6666-6666-6666-666666666666',
 'Telematics Privacy Compliance Benchmark',
 'Survey of 320 EU logistics operators: 76% have documented legal basis for GPS tracking, 58% have automated data retention policies, 41% provide driver self-service data access. GDPR fines in logistics sector 2023-2024: 12 cases, average fine 145,000 EUR. Common violations: Excessive data retention (42%), lack of transparency (31%), inadequate security (27%). Big Trucking Corp Ltd. compliance score: 4/10.',
 'benchmark', 4);

-- Report 7: Cross-Border VAT Compliance
INSERT INTO reports (id, title, summary, created_at) VALUES 
('77777777-7777-7777-7777-777777777777',
 'Cross-Border VAT and Customs Compliance - Post-Brexit Updates',
 'Analysis of VAT obligations for international transport services, customs documentation requirements, and AEO (Authorized Economic Operator) certification benefits.',
 NOW() - INTERVAL '21 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('77777777-7777-7777-7777-777777777777',
 'VAT Reverse Charge Mechanism Errors',
 'Audit of Q4 2024 invoices reveals 23 instances of incorrect VAT treatment on cross-border services. Risk: VAT penalties up to 30% of tax amount + interest. Root cause: Manual invoice processing, lack of automated VAT determination. Recommendation: Implement VAT compliance software (e.g., Avalara, Vertex) with TMS integration. Cost: 8,000 PLN setup + 2,400 PLN/year. Penalty avoidance: ~15,000 PLN/year.',
 'risk', 1),
('77777777-7777-7777-7777-777777777777',
 'AEO Certification Benefits Analysis',
 'Authorized Economic Operator status provides: Reduced customs inspections (80% fewer delays), priority treatment at borders, simplified customs procedures. Application requirements: 3 years clean compliance record, documented internal controls, financial solvency. Current readiness: 70%. Missing: Formal compliance manual, employee training records. Certification timeline: 6-9 months. Cost: 18,000 PLN (consultant + audit preparation). Annual savings: 45,000 PLN (reduced delays + admin efficiency).',
 'recommendation', 2),
('77777777-7777-7777-7777-777777777777',
 'UK Customs Documentation Post-Brexit',
 'UK routes require full customs declarations since Brexit. Current error rate: 8% of shipments delayed due to documentation issues. Common problems: Incorrect HS codes (42%), missing EORI numbers (28%), incomplete commercial invoices (30%). Recommendation: Mandatory customs training for dispatch team, implement pre-clearance document validation. Training cost: 4,500 PLN. Expected error reduction: 60%.',
 'risk', 3),
('77777777-7777-7777-7777-777777777777',
 'EU Logistics Customs Compliance Performance',
 'Industry data: Average customs clearance time EU-UK: 4.2 hours. Top performers: 1.8 hours (AEO certified with pre-clearance). Big Trucking Corp Ltd. average: 6.5 hours. Cost of delay: 85 PLN/hour (driver + vehicle). Annual delay cost: ~127,000 PLN. AEO certification + process optimization potential savings: 75,000 PLN/year. Payback period: 3 months.',
 'benchmark', 4);

-- Report 8: Driver Shortage and Retention
INSERT INTO reports (id, title, summary, created_at) VALUES 
('88888888-8888-8888-8888-888888888888',
 'Driver Shortage Crisis - Retention Strategies and Legal Compliance',
 'Analysis of driver shortage impact on operations, legal requirements for working time compliance, and evidence-based retention strategies from EU logistics sector.',
 NOW() - INTERVAL '25 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('88888888-8888-8888-8888-888888888888',
 'Working Time Directive Violations Risk',
 'Random audit of tachograph data reveals 12 instances of insufficient rest periods in Q4 2024. Violations: 9x daily rest <11 hours, 3x weekly rest <45 hours. Penalty risk: 2,000-5,000 PLN per violation = up to 60,000 PLN. Root cause: Manual route planning without working time validation. Recommendation: Implement automated route planning with working time compliance checks. Software cost: 7,500 PLN. Penalty avoidance: 60,000+ PLN/year.',
 'regulation', 1),
('88888888-8888-8888-8888-888888888888',
 'Driver Retention Program ROI Analysis',
 'Current driver turnover: 34% annually. Industry average: 28%. Replacement cost per driver: 12,000 PLN (recruitment + training + productivity loss). Annual turnover cost: 408,000 PLN (34 drivers). Proposed retention program: (1) Performance bonuses (120,000 PLN/year), (2) Modern truck upgrades (180,000 PLN one-time), (3) Flexible scheduling (software 8,000 PLN). Total investment: 308,000 PLN. Expected turnover reduction: 40% (to 20%). Annual savings: 168,000 PLN. ROI: 55% first year.',
 'recommendation', 2),
('88888888-8888-8888-8888-888888888888',
 'Driver Shortage Impact on Operations',
 'Current driver shortage: 8 positions unfilled (8% vacancy rate). Impact: 15% of shipments delayed, 12% increase in subcontractor costs, 23% overtime increase. Customer complaints up 34% YoY. Risk: Contract penalties (SLA violations), customer churn, employee burnout. Immediate action: Increase recruitment budget by 40%, partner with driving schools, implement referral bonus program (5,000 PLN per successful hire).',
 'risk', 3),
('88888888-8888-8888-8888-888888888888',
 'EU Driver Shortage Benchmark Data',
 'EU-wide driver shortage: 230,000 positions (2024). Poland: 28,000 shortage. Average driver age: 47 years. Retirement wave: 35% of drivers retire by 2030. Successful retention strategies: Modern fleet (78% effectiveness), performance bonuses (65%), flexible home time (71%), career development (52%). Top-performing companies: <15% turnover, 95% on-time delivery, 8% higher profit margins. Big Trucking Corp Ltd. current ranking: Bottom 40% for retention.',
 'benchmark', 4);

-- Report 9: Insurance and Liability Management
INSERT INTO reports (id, title, summary, created_at) VALUES 
('99999999-9999-9999-9999-999999999999',
 'Insurance Coverage Review - Liability Gaps and Cost Optimization',
 'Comprehensive review of cargo insurance, liability coverage, and cyber insurance. Identifies coverage gaps and cost optimization opportunities based on claims history and industry benchmarks.',
 NOW() - INTERVAL '28 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('99999999-9999-9999-9999-999999999999',
 'Cargo Insurance Coverage Gaps',
 'Current cargo insurance: 100,000 PLN per shipment. Analysis of 2024 shipments shows 18 loads exceeded coverage limit (max value: 245,000 PLN). Uncovered exposure: 2.6M PLN total. Risk: Customer contract violations (most require full value coverage), out-of-pocket loss in case of accident. Recommendation: Increase base coverage to 250,000 PLN, implement automated high-value shipment flagging. Premium increase: 8,500 PLN/year. Risk mitigation: 2.6M PLN.',
 'risk', 1),
('99999999-9999-9999-9999-999999999999',
 'CMR Liability Limitation Strategy',
 'CMR Convention limits carrier liability to 8.33 SDR per kg (~45 PLN/kg). Many contracts waive this limitation. Current practice: 67% of contracts have unlimited liability clauses. Risk: Catastrophic loss exposure. Recommendation: Renegotiate contracts to maintain CMR limitation, increase insurance for high-value customers only. Legal review cost: 6,000 PLN. Potential premium savings: 15,000 PLN/year.',
 'recommendation', 2),
('99999999-9999-9999-9999-999999999999',
 'Claims History Analysis and Prevention',
 '2024 claims: 23 cargo damage claims (total: 187,000 PLN), 8 liability claims (total: 94,000 PLN). Root cause analysis: 52% loading/unloading damage, 26% road accidents, 22% theft. Prevention opportunities: Driver training (loading procedures), GPS-based route monitoring (theft prevention), vehicle maintenance (accident reduction). Investment: 12,000 PLN training + 8,000 PLN monitoring. Expected claims reduction: 35% = 98,000 PLN/year savings.',
 'risk', 3),
('99999999-9999-9999-9999-999999999999',
 'Logistics Insurance Market Benchmark',
 'Industry average insurance cost: 2.8% of revenue. Big Trucking Corp Ltd.: 3.4% (21% above average). Top quartile performers: 2.1%. Key success factors: Strong safety culture (40% fewer accidents), modern fleet (30% lower premiums), claims management (25% better settlement rates). Optimization potential: 0.8% of revenue = 156,000 PLN/year. Recommended actions: Safety training program, telematics-based insurance discount, claims management process improvement.',
 'benchmark', 4);

-- Report 10: Digital Transformation Roadmap
INSERT INTO reports (id, title, summary, created_at) VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'Digital Transformation Strategy - Technology Investment Priorities',
 'Strategic roadmap for digital transformation aligned with regulatory compliance and operational efficiency goals. Prioritizes investments based on ROI, compliance urgency, and competitive positioning.',
 NOW() - INTERVAL '3 days');

INSERT INTO report_elements (report_id, title, content, element_type, order_index) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'TMS (Transport Management System) Modernization',
 'Current TMS: Version 6.2 (released 2019), lacks API integrations, no mobile app, manual data entry. Limitations: No real-time tracking, no eCMR support, no automated route optimization. Recommendation: Upgrade to cloud-based TMS (e.g., Transporeon, Trimble, Manhattan) with: API integrations, mobile driver app, AI route optimization, eCMR module. Cost: 45,000 PLN implementation + 18,000 PLN/year subscription. ROI: 24 months (efficiency gains + compliance + customer satisfaction).',
 'recommendation', 1),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'Cybersecurity Infrastructure Investment Priority',
 'NIS2 compliance deadline: Q2 2026 (15 months). Current cybersecurity maturity: Level 1/5 (ad-hoc). Required investments: (1) SIEM/monitoring: 6,000 PLN, (2) Backup encryption: 3,500 PLN, (3) Incident response plan: 8,000 PLN, (4) Employee training: 4,500 PLN, (5) Penetration testing: 7,000 PLN. Total: 29,000 PLN. Compliance risk: 10M EUR penalties. Priority: CRITICAL. Timeline: Complete by Q1 2026.',
 'regulation', 2),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'AI and Automation Opportunities',
 'High-ROI automation opportunities: (1) Route optimization AI: 8-12% fuel savings = 156,000 PLN/year, investment 25,000 PLN, payback 2 months. (2) Automated dispatch: 30% faster order processing, 2 FTE reduction = 120,000 PLN/year, investment 35,000 PLN, payback 3.5 months. (3) Predictive maintenance: 25% reduction in breakdowns = 85,000 PLN/year, investment 18,000 PLN, payback 2.5 months. Total investment: 78,000 PLN. Total annual savings: 361,000 PLN. ROI: 463%.',
 'recommendation', 3),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'Digital Maturity Benchmark - EU Logistics Sector',
 'Digital maturity assessment (scale 1-5): Big Trucking Corp Ltd. score: 2.1 (below average). EU logistics average: 3.2. Top performers: 4.3. Key gaps: Cloud adoption (score 1.5), data analytics (1.8), automation (2.0), cybersecurity (1.5). Industry leaders invest 4-6% of revenue in technology. Big Trucking Corp Ltd. current: 1.8%. Recommended increase: 3.5% = 682,000 PLN/year. Expected outcomes: 15% operational cost reduction, 25% faster delivery times, 40% better compliance, 20% revenue growth.',
 'benchmark', 4);
