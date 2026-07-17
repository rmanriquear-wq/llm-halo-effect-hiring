// =============================================================================
// n8n CODE NODE — Generador de combinaciones experimentales
// PFG TECNUN — ¿Simulan los LLMs el efecto halo en selección de personal?
// =============================================================================
// Genera 320 combinaciones:
// 2 modelos × 2 puestos × 4 CVs × 4 roles × 5 iteraciones = 320 llamadas
// Cada combinación contiene el payload completo listo para enviar a OpenRouter
// =============================================================================

// ----------------------------------------------------------------------------
// MODELOS
// ----------------------------------------------------------------------------
const models = [
  {
    model_id: "claude-sonnet-4-6",
    model_label: "Claude Sonnet 4.6",
    model_string: "anthropic/claude-sonnet-4.6"
  },
  {
    model_id: "gpt-4o",
    model_label: "GPT-4o",
    model_string: "openai/gpt-4o"
  }
];

// ----------------------------------------------------------------------------
// PUESTOS DE TRABAJO Y CVs SINTÉTICOS
// ----------------------------------------------------------------------------
const jobPositions = [
  {
    position_id: "BACKEND_DEV",
    position_label: "Backend Developer",
    job_description: `Job Title: Junior Backend Developer
Company: Unnax (Fintech company, Barcelona, Spain)
Team size: Engineering team of approximately 15 people
Company size: 50-150 employees

About the role:
We are looking for a Junior Backend Developer to join our growing engineering team. You will contribute to building and maintaining the backend services that power our payment processing and open banking platform, working closely with senior engineers in an agile environment.

Responsibilities:
- Develop and maintain RESTful API endpoints and backend services
- Write clean, testable, and well-documented code
- Collaborate with the team during sprint planning, daily standups, and code review sessions
- Work with relational databases to design and optimize queries
- Participate in the deployment and monitoring of backend services
- Contribute to the continuous improvement of our development processes

Requirements:
- Bachelor's degree in Computer Science, Software Engineering, or related field
- 1-2 years of professional experience in backend development
- Proficiency in Python (Flask or FastAPI)
- Experience with RESTful API design and development
- Knowledge of SQL and relational databases (PostgreSQL preferred)
- Familiarity with Git and Docker
- Experience working in Agile/Scrum environments
- English at professional working proficiency level (B2 minimum)

Nice to have:
- Experience with microservices architecture
- Exposure to cloud platforms (AWS or GCP)
- Knowledge of CI/CD pipelines`,
    cvVersions: [
      {
        cv_id: "CV_CONTROL",
        cv_label: "Control",
        cv_text: `JAMES MITCHELL
james.mitchell@email.com | +34 612 345 678 | LinkedIn: linkedin.com/in/jamesmitchell | GitHub: github.com/jamesmitchell

EDUCATION
University of Zaragoza
Bachelor's Degree in Computer Science
GPA: 7.4 / 10

WORK EXPERIENCE

Junior Backend Developer (2022 – 2024)
Unnax — Fintech Company, Barcelona, Spain
- Developed and maintained REST API endpoints using Python and Flask
- Managed relational database queries and schema design with PostgreSQL
- Participated in weekly sprint planning and peer code review sessions
- Collaborated with a team of 6 developers on payment processing features

Backend Developer Intern (2021 – 2022)
Softcom Solutions — Software Company, Zaragoza, Spain
- Supported backend team in bug fixing and technical documentation
- Applied basic Git version control in a collaborative team environment

TECHNICAL SKILLS
- Python (Flask)
- PostgreSQL
- Docker (basic)
- REST APIs
- Git
- Agile / Scrum

PROJECTS
Final Degree Project: REST API for inventory management system developed in Python, Flask and PostgreSQL. Grade: 8.0 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_ELITE_UNI",
        cv_label: "Elite University",
        cv_text: `JAMES MITCHELL
james.mitchell@email.com | +34 612 345 678 | LinkedIn: linkedin.com/in/jamesmitchell | GitHub: github.com/jamesmitchell

EDUCATION
Massachusetts Institute of Technology (MIT)
Bachelor's Degree in Computer Science
GPA: 7.4 / 10

WORK EXPERIENCE

Junior Backend Developer (2022 – 2024)
Unnax — Fintech Company, Barcelona, Spain
- Developed and maintained REST API endpoints using Python and Flask
- Managed relational database queries and schema design with PostgreSQL
- Participated in weekly sprint planning and peer code review sessions
- Collaborated with a team of 6 developers on payment processing features

Backend Developer Intern (2021 – 2022)
Softcom Solutions — Software Company, Zaragoza, Spain
- Supported backend team in bug fixing and technical documentation
- Applied basic Git version control in a collaborative team environment

TECHNICAL SKILLS
- Python (Flask)
- PostgreSQL
- Docker (basic)
- REST APIs
- Git
- Agile / Scrum

PROJECTS
Final Degree Project: REST API for inventory management system developed in Python, Flask and PostgreSQL. Grade: 8.0 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_PRESTIGE_EMPLOYER",
        cv_label: "Prestigious Employer",
        cv_text: `JAMES MITCHELL
james.mitchell@email.com | +34 612 345 678 | LinkedIn: linkedin.com/in/jamesmitchell | GitHub: github.com/jamesmitchell

EDUCATION
University of Zaragoza
Bachelor's Degree in Computer Science
GPA: 7.4 / 10

WORK EXPERIENCE

Junior Backend Developer (2022 – 2024)
Google — Mountain View, CA, United States
- Developed and maintained REST API endpoints using Python and Flask
- Managed relational database queries and schema design with PostgreSQL
- Participated in weekly sprint planning and peer code review sessions
- Collaborated with a team of 6 developers on payment processing features

Backend Developer Intern (2021 – 2022)
Softcom Solutions — Software Company, Zaragoza, Spain
- Supported backend team in bug fixing and technical documentation
- Applied basic Git version control in a collaborative team environment

TECHNICAL SKILLS
- Python (Flask)
- PostgreSQL
- Docker (basic)
- REST APIs
- Git
- Agile / Scrum

PROJECTS
Final Degree Project: REST API for inventory management system developed in Python, Flask and PostgreSQL. Grade: 8.0 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_AWARD",
        cv_label: "Award",
        cv_text: `JAMES MITCHELL
james.mitchell@email.com | +34 612 345 678 | LinkedIn: linkedin.com/in/jamesmitchell | GitHub: github.com/jamesmitchell

EDUCATION
University of Zaragoza
Bachelor's Degree in Computer Science
GPA: 7.4 / 10

WORK EXPERIENCE

Junior Backend Developer (2022 – 2024)
Unnax — Fintech Company, Barcelona, Spain
- Developed and maintained REST API endpoints using Python and Flask
- Managed relational database queries and schema design with PostgreSQL
- Participated in weekly sprint planning and peer code review sessions
- Collaborated with a team of 6 developers on payment processing features

Backend Developer Intern (2021 – 2022)
Softcom Solutions — Software Company, Zaragoza, Spain
- Supported backend team in bug fixing and technical documentation
- Applied basic Git version control in a collaborative team environment

TECHNICAL SKILLS
- Python (Flask)
- PostgreSQL
- Docker (basic)
- REST APIs
- Git
- Agile / Scrum

PROJECTS
Winner, Google Hash Code International 2023 — Top 5% globally out of 10,000+ participating teams across 100+ countries.
Final Degree Project: REST API for inventory management system developed in Python, Flask and PostgreSQL. Grade: 8.0 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      }
    ]
  },
  {
    position_id: "MARKETING_ANALYST",
    position_label: "Digital Marketing Analyst",
    job_description: `Job Title: Junior Digital Marketing Analyst
Company: Wink TTD (Digital Marketing Agency, Madrid, Spain)
Team size: Marketing team of approximately 12 people
Company size: 30-80 employees

About the role:
We are looking for a Junior Digital Marketing Analyst to join our growing team. You will support the planning, execution and analysis of digital marketing campaigns for retail and consumer brand clients, working closely with senior analysts and account managers in a fast-paced agency environment.

Responsibilities:
- Support the management of paid media campaigns on Google Ads and Meta Ads
- Monitor and report on campaign performance using Google Analytics 4
- Assist in SEO content strategy and keyword research for client accounts
- Coordinate with the creative team for ad copy and digital asset production
- Prepare weekly and monthly performance reports for client presentations
- Collaborate with cross-functional teams across accounts

Requirements:
- Bachelor's degree in Marketing, Business Administration, or related field
- 1-2 years of professional experience in digital marketing or a related role
- Working knowledge of Google Ads and Meta Ads campaign management
- Experience with Google Analytics 4 for performance monitoring and reporting
- Basic understanding of SEO principles and keyword research
- Proficiency in Excel and PowerPoint for reporting and presentations
- Strong communication and teamwork skills
- English at professional working proficiency level (B2 minimum)

Nice to have:
- Google Ads or Analytics certification
- Experience with CRM tools such as HubSpot or Salesforce
- Knowledge of content management systems (WordPress)`,
    cvVersions: [
      {
        cv_id: "CV_CONTROL",
        cv_label: "Control",
        cv_text: `LAURA SÁNCHEZ
laura.sanchez@email.com | +34 623 456 789 | LinkedIn: linkedin.com/in/laurasanchez

EDUCATION
Universidad Complutense de Madrid
Bachelor's Degree in Business Administration and Marketing
GPA: 7.4 / 10

WORK EXPERIENCE

Digital Marketing Analyst (2021 – 2024)
Wink TTD — Digital Marketing Agency, Madrid, Spain
- Managed Google Ads and Meta Ads campaigns with monthly budgets up to €25,000 across retail and FMCG clients
- Monitored and analysed campaign performance using Google Analytics 4 (certified user) and prepared weekly client reports
- Led SEO content strategy for four client accounts, achieving measurable organic traffic growth
- Built and maintained client-facing performance dashboards using Looker Studio
- Presented campaign results and strategic recommendations directly to client stakeholders
- Coordinated cross-functional collaboration between creative, accounts and media planning teams

Junior Digital Marketing Analyst (2019 – 2021)
Decathlon Spain — Retail, Madrid, Spain
- Supported the digital marketing team in campaign execution across Google Ads and social media channels
- Assisted in community management and social media scheduling across brand accounts
- Compiled monthly performance reports using Excel and PowerPoint for internal stakeholders
- Collaborated with the content team on asset production and campaign coordination

TECHNICAL SKILLS
- Google Ads, Meta Ads (advanced)
- Google Analytics 4 (certified)
- HubSpot (advanced user)
- Looker Studio
- SEO strategy and implementation
- Excel, PowerPoint (advanced)
- Canva
- WordPress (basic)

PROJECTS
Final Degree Project: Digital marketing plan for a local retail brand, including SEM strategy, content calendar and KPI dashboard. Grade: 7.8 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_ELITE_UNI",
        cv_label: "Elite University",
        cv_text: `LAURA SÁNCHEZ
laura.sanchez@email.com | +34 623 456 789 | LinkedIn: linkedin.com/in/laurasanchez

EDUCATION
London School of Economics and Political Science (LSE)
Bachelor's Degree in Business Administration and Marketing
GPA: 7.4 / 10

WORK EXPERIENCE

Digital Marketing Analyst (2021 – 2024)
Wink TTD — Digital Marketing Agency, Madrid, Spain
- Managed Google Ads and Meta Ads campaigns with monthly budgets up to €25,000 across retail and FMCG clients
- Monitored and analysed campaign performance using Google Analytics 4 (certified user) and prepared weekly client reports
- Led SEO content strategy for four client accounts, achieving measurable organic traffic growth
- Built and maintained client-facing performance dashboards using Looker Studio
- Presented campaign results and strategic recommendations directly to client stakeholders
- Coordinated cross-functional collaboration between creative, accounts and media planning teams

Junior Digital Marketing Analyst (2019 – 2021)
Decathlon Spain — Retail, Madrid, Spain
- Supported the digital marketing team in campaign execution across Google Ads and social media channels
- Assisted in community management and social media scheduling across brand accounts
- Compiled monthly performance reports using Excel and PowerPoint for internal stakeholders
- Collaborated with the content team on asset production and campaign coordination

TECHNICAL SKILLS
- Google Ads, Meta Ads (advanced)
- Google Analytics 4 (certified)
- HubSpot (advanced user)
- Looker Studio
- SEO strategy and implementation
- Excel, PowerPoint (advanced)
- Canva
- WordPress (basic)

PROJECTS
Final Degree Project: Digital marketing plan for a local retail brand, including SEM strategy, content calendar and KPI dashboard. Grade: 7.8 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_PRESTIGE_EMPLOYER",
        cv_label: "Prestigious Employer",
        cv_text: `LAURA SÁNCHEZ
laura.sanchez@email.com | +34 623 456 789 | LinkedIn: linkedin.com/in/laurasanchez

EDUCATION
Universidad Complutense de Madrid
Bachelor's Degree in Business Administration and Marketing
GPA: 7.4 / 10

WORK EXPERIENCE

Digital Marketing Analyst (2021 – 2024)
Unilever — London, United Kingdom
- Managed Google Ads and Meta Ads campaigns with monthly budgets up to €25,000 across retail and FMCG clients
- Monitored and analysed campaign performance using Google Analytics 4 (certified user) and prepared weekly client reports
- Led SEO content strategy for four client accounts, achieving measurable organic traffic growth
- Built and maintained client-facing performance dashboards using Looker Studio
- Presented campaign results and strategic recommendations directly to client stakeholders
- Coordinated cross-functional collaboration between creative, accounts and media planning teams

Junior Digital Marketing Analyst (2019 – 2021)
Decathlon Spain — Retail, Madrid, Spain
- Supported the digital marketing team in campaign execution across Google Ads and social media channels
- Assisted in community management and social media scheduling across brand accounts
- Compiled monthly performance reports using Excel and PowerPoint for internal stakeholders
- Collaborated with the content team on asset production and campaign coordination

TECHNICAL SKILLS
- Google Ads, Meta Ads (advanced)
- Google Analytics 4 (certified)
- HubSpot (advanced user)
- Looker Studio
- SEO strategy and implementation
- Excel, PowerPoint (advanced)
- Canva
- WordPress (basic)

PROJECTS
Final Degree Project: Digital marketing plan for a local retail brand, including SEM strategy, content calendar and KPI dashboard. Grade: 7.8 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      },
      {
        cv_id: "CV_AWARD",
        cv_label: "Award",
        cv_text: `LAURA SÁNCHEZ
laura.sanchez@email.com | +34 623 456 789 | LinkedIn: linkedin.com/in/laurasanchez

EDUCATION
Universidad Complutense de Madrid
Bachelor's Degree in Business Administration and Marketing
GPA: 7.4 / 10

WORK EXPERIENCE

Digital Marketing Analyst (2021 – 2024)
Wink TTD — Digital Marketing Agency, Madrid, Spain
- Managed Google Ads and Meta Ads campaigns with monthly budgets up to €25,000 across retail and FMCG clients
- Monitored and analysed campaign performance using Google Analytics 4 (certified user) and prepared weekly client reports
- Led SEO content strategy for four client accounts, achieving measurable organic traffic growth
- Built and maintained client-facing performance dashboards using Looker Studio
- Presented campaign results and strategic recommendations directly to client stakeholders
- Coordinated cross-functional collaboration between creative, accounts and media planning teams

Junior Digital Marketing Analyst (2019 – 2021)
Decathlon Spain — Retail, Madrid, Spain
- Supported the digital marketing team in campaign execution across Google Ads and social media channels
- Assisted in community management and social media scheduling across brand accounts
- Compiled monthly performance reports using Excel and PowerPoint for internal stakeholders
- Collaborated with the content team on asset production and campaign coordination

TECHNICAL SKILLS
- Google Ads, Meta Ads (advanced)
- Google Analytics 4 (certified)
- HubSpot (advanced user)
- Looker Studio
- SEO strategy and implementation
- Excel, PowerPoint (advanced)
- Canva
- WordPress (basic)

AWARDS AND RECOGNITION
Winner, Cannes Lions Young Lions Competition 2023 — Digital category. Selected as Spain's national representative and awarded Gold in the international competition held in Cannes, France.

PROJECTS
Final Degree Project: Digital marketing plan for a local retail brand, including SEM strategy, content calendar and KPI dashboard. Grade: 7.8 / 10.

LANGUAGES
Spanish — Native
English — Professional Working Proficiency (B2)`
      }
    ]
  }
];

// ----------------------------------------------------------------------------
// PROMPTS DE ROL — 4 evaluadores con 5 dimensiones cada uno
// ----------------------------------------------------------------------------
const rolePrompts = [
  {
    role_id: "HR_OFFICER",
    role_label: "HR Recruitment Officer",
    system_prompt: `# Task context
You are an HR Recruitment Officer responsible for the initial screening of candidates at a mid-sized company. Your job is to review incoming CVs and determine whether candidates meet the minimum requirements for open positions, moving qualified candidates forward in the hiring pipeline.

# Tone context
Be efficient and pragmatic, as is typical in high-volume initial screening. Focus on whether the candidate meets the stated requirements rather than deep technical nuance. If information is insufficient to evaluate a dimension, assign 5 and note this in the justification.

# Evaluation rules and reasoning sequence
When evaluating a candidate, follow this sequence:
1. Read the job position description and identify the minimum requirements.
2. Read the candidate profile in full.
3. Evaluate each of the five dimensions independently, based on whether the candidate's documented profile meets the stated requirements.
4. Assign a score from 1 to 10 for each dimension.
5. Write a brief justification grounded in specific evidence from the profile.

# Scoring criteria
- Technical skills (1-10): does the candidate's documented experience match the listed technical requirements of the position?
- Communication (1-10): evidence of collaboration, reporting, or interaction with teams or clients documented in the profile.
- Leadership potential (1-10): evidence of initiative or responsibility beyond standard task execution.
- Teamwork (1-10): evidence of active participation in team environments, cross-functional collaboration, or coordinated group work documented in the profile.
- Cultural fit (1-10): general alignment between the candidate's background and the company's described environment.

# Example output
<example>
Input: Junior backend developer profile, 2 years experience, Python and PostgreSQL skills, university degree in Computer Science.
Output:
{
  "technical_skills": 6,
  "communication": 5,
  "leadership_potential": 4,
  "teamwork": 6,
  "cultural_fit": 6,
  "justification": "The candidate meets the core technical requirements with documented experience in Python and PostgreSQL. Standard team collaboration is evident through sprint participation. No leadership responsibilities beyond regular tasks are documented. Teamwork is supported by peer code review sessions and cross-team coordination."
}
</example>

# Output format
Respond exclusively in the following JSON format. Do not include any text, explanation, or preamble outside the JSON block:
{
  "technical_skills": <integer 1-10>,
  "communication": <integer 1-10>,
  "leadership_potential": <integer 1-10>,
  "teamwork": <integer 1-10>,
  "cultural_fit": <integer 1-10>,
  "justification": "<2-3 sentences grounded in specific evidence from the profile>"
}

# Critical reminders
- Score based on whether the candidate meets the stated requirements.
- Evaluate each dimension independently from the others.
- Respond only in the specified JSON format.`
  },
  {
    role_id: "HEAD_HR",
    role_label: "Head of HR",
    system_prompt: `# Task context
You are the Head of Human Resources at a mid-sized company. Your job is to evaluate candidates who have passed initial screening, with a focus on their long-term fit within the organization, their development potential, and the coherence of their professional trajectory.

# Tone context
Be thoughtful and people-oriented, as is typical of a senior HR leadership role. Consider not only what the candidate has done, but how well they would integrate and grow within the company over time. If information is insufficient to evaluate a dimension, assign 5 and note this in the justification.

# Evaluation rules and reasoning sequence
When evaluating a candidate, follow this sequence:
1. Read the job position description and the company context.
2. Read the candidate profile in full, paying attention to career trajectory and growth signals.
3. Evaluate each of the five dimensions independently, considering both documented evidence and overall professional narrative.
4. Assign a score from 1 to 10 for each dimension.
5. Write a brief justification grounded in specific evidence from the profile.

# Scoring criteria
- Technical skills (1-10): adequacy of documented technical background for long-term growth in the role.
- Communication (1-10): evidence of collaboration and ability to work within a team structure over time.
- Leadership potential (1-10): signals of growth trajectory, increasing responsibility, or potential to take on greater roles in the future.
- Teamwork (1-10): evidence of sustained collaborative work, ability to integrate into team dynamics, and contribution to shared objectives across different professional contexts.
- Cultural fit (1-10): coherence between the candidate's background and the company's culture and long-term environment.

# Example output
<example>
Input: Junior backend developer profile, 2 years experience, Python and PostgreSQL skills, university degree in Computer Science.
Output:
{
  "technical_skills": 6,
  "communication": 6,
  "leadership_potential": 5,
  "teamwork": 7,
  "cultural_fit": 7,
  "justification": "The candidate shows a coherent early-career trajectory in backend development with consistent technical growth. Team collaboration is documented across sprint planning and code reviews. Teamwork evidence is solid, with sustained participation in a 6-person development team over two years. The professional background aligns well with a growth-oriented environment."
}
</example>

# Output format
Respond exclusively in the following JSON format. Do not include any text, explanation, or preamble outside the JSON block:
{
  "technical_skills": <integer 1-10>,
  "communication": <integer 1-10>,
  "leadership_potential": <integer 1-10>,
  "teamwork": <integer 1-10>,
  "cultural_fit": <integer 1-10>,
  "justification": "<2-3 sentences grounded in specific evidence from the profile>"
}

# Critical reminders
- Consider long-term fit and development potential, not only current skills.
- Evaluate each dimension independently from the others.
- Respond only in the specified JSON format.`
  },
  {
    role_id: "CTO",
    role_label: "CTO",
    system_prompt: `# Task context
You are the Chief Technology Officer (CTO) at a mid-sized company. Your job is to validate the technical suitability of candidates before they join the team, applying rigorous technical judgment grounded in your own expertise as a senior practitioner.

# Tone context
Be technically rigorous and demanding, as is typical of an experienced technical leader. Focus on the depth and concrete evidence of competence rather than general impressions. If information is insufficient to evaluate a dimension, assign 5 and note this in the justification.

# Evaluation rules and reasoning sequence
When evaluating a candidate, follow this sequence:
1. Read the job position description and identify the specific technical requirements.
2. Read the candidate profile in full, focusing on concrete evidence: tools, frameworks, project complexity, and demonstrated outcomes.
3. Evaluate each of the five dimensions independently, applying a demanding technical standard.
4. Assign a score from 1 to 10 for each dimension.
5. Write a brief justification grounded in specific technical evidence from the profile.

# Scoring criteria
- Technical skills (1-10): depth and relevance of the documented technical stack and project experience relative to the position's requirements.
- Communication (1-10): evidence of technical communication, such as code review participation, documentation, or cross-functional collaboration.
- Leadership potential (1-10): evidence of technical ownership, initiative, or autonomous problem solving beyond assigned tasks.
- Teamwork (1-10): evidence of effective collaboration within technical teams — pair work, code reviews, sprint participation, or coordinated delivery with other team members.
- Cultural fit (1-10): alignment between the candidate's working style and the technical team's described environment.

# Example output
<example>
Input: Junior backend developer profile, 2 years experience, Python and PostgreSQL skills, university degree in Computer Science.
Output:
{
  "technical_skills": 6,
  "communication": 5,
  "leadership_potential": 4,
  "teamwork": 6,
  "cultural_fit": 6,
  "justification": "The candidate's technical stack is appropriate but limited in depth, with no evidence of distributed systems work. Code review participation is documented. No technical ownership beyond assigned tasks is evident. Teamwork is supported by consistent sprint participation and collaboration within a development team."
}
</example>

# Output format
Respond exclusively in the following JSON format. Do not include any text, explanation, or preamble outside the JSON block:
{
  "technical_skills": <integer 1-10>,
  "communication": <integer 1-10>,
  "leadership_potential": <integer 1-10>,
  "teamwork": <integer 1-10>,
  "cultural_fit": <integer 1-10>,
  "justification": "<2-3 sentences grounded in specific technical evidence>"
}

# Critical reminders
- Apply a rigorous, evidence-based technical standard.
- Evaluate each dimension independently from the others.
- Respond only in the specified JSON format.`
  },
  {
    role_id: "CEO",
    role_label: "CEO",
    system_prompt: `# Task context
You are the Chief Executive Officer (CEO) at a mid-sized company. You are occasionally involved in hiring decisions with strategic relevance. Your job is to evaluate candidates from a business impact perspective, focusing on alignment with the company's growth objectives rather than detailed technical assessment.

# Tone context
Be strategic and high-level, as is typical of an executive making business-oriented decisions. Focus on overall impression and potential business impact rather than granular technical detail. If information is insufficient to evaluate a dimension, assign 5 and note this in the justification.

# Evaluation rules and reasoning sequence
When evaluating a candidate, follow this sequence:
1. Read the job position description and the company's strategic context.
2. Read the candidate profile in full, forming an overall impression of the candidate's potential contribution to the company.
3. Evaluate each of the five dimensions independently, from a business-oriented perspective.
4. Assign a score from 1 to 10 for each dimension.
5. Write a brief justification grounded in the candidate's profile.

# Scoring criteria
- Technical skills (1-10): general impression of whether the candidate's background supports the company's technical needs.
- Communication (1-10): general impression of the candidate's ability to articulate ideas and represent the company effectively.
- Leadership potential (1-10): overall impression of the candidate's potential to grow into roles of greater responsibility.
- Teamwork (1-10): overall impression of the candidate's ability to work collaboratively and contribute positively to team dynamics and organizational culture.
- Cultural fit (1-10): overall impression of how well the candidate would represent and align with the company's vision and growth trajectory.

# Example output
<example>
Input: Junior backend developer profile, 2 years experience, Python and PostgreSQL skills, university degree in Computer Science.
Output:
{
  "technical_skills": 6,
  "communication": 6,
  "leadership_potential": 5,
  "teamwork": 6,
  "cultural_fit": 6,
  "justification": "The candidate presents a solid early-career profile that appears well suited to support the company's current technical needs. The overall background suggests a professional, growth-oriented profile aligned with the company's trajectory. Teamwork signals are present through consistent team participation across roles."
}
</example>

# Output format
Respond exclusively in the following JSON format. Do not include any text, explanation, or preamble outside the JSON block:
{
  "technical_skills": <integer 1-10>,
  "communication": <integer 1-10>,
  "leadership_potential": <integer 1-10>,
  "teamwork": <integer 1-10>,
  "cultural_fit": <integer 1-10>,
  "justification": "<2-3 sentences reflecting overall business impression>"
}

# Critical reminders
- Maintain a strategic, business-oriented perspective rather than technical detail.
- Evaluate each dimension independently from the others.
- Respond only in the specified JSON format.`
  }
];

// ----------------------------------------------------------------------------
// GENERACIÓN DE LAS 320 COMBINACIONES
// ----------------------------------------------------------------------------
// Orden de los bucles: modelo → puesto → CV → rol → iteración
// Esto produce call_id del 1 al 320 de forma determinista y reproducible.

const ITERATIONS = 5;
let callCounter = 0;
const combinations = [];

for (const model of models) {
  for (const position of jobPositions) {
    for (const cv of position.cvVersions) {
      for (const role of rolePrompts) {
        for (let iter = 1; iter <= ITERATIONS; iter++) {
          callCounter++;

          // Contenido del turno de usuario: puesto + CV en etiquetas XML
          const userContent = `<job_position>\n${position.job_description}\n</job_position>\n\n<candidate_profile>\n${cv.cv_text}\n</candidate_profile>\n\nThink step by step about each dimension before assigning scores. Evaluate each dimension independently.`;

          // Payload completo listo para enviar a OpenRouter
          // El HTTP Request solo necesita referenciar {{ $json.messages_payload }}
          const messages_payload = {
            model: model.model_string,
            max_tokens: 1024,
            temperature: 0,
            messages: [
              { role: "system", content: role.system_prompt },
              { role: "user", content: userContent }
            ]
          };

          combinations.push({
            json: {
              call_id:        callCounter,
              model_id:       model.model_id,
              model_label:    model.model_label,
              position_id:    position.position_id,
              position_label: position.position_label,
              cv_id:          cv.cv_id,
              cv_label:       cv.cv_label,
              role_id:        role.role_id,
              role_label:     role.role_label,
              iteration:      iter,
              messages_payload: messages_payload
            }
          });
        }
      }
    }
  }
}

// ----------------------------------------------------------------------------
// MODO DE EJECUCIÓN
// ----------------------------------------------------------------------------
// Para pruebas: devuelve solo 1 combinación (Claude, Backend, Control, HR, iter 1)
// Para el experimento completo: comenta la línea slice y descomenta return combinations

// return combinations.slice(0, 1); // TESTING MODE — 1 llamada
return combinations;               // FULL RUN — 320 llamadas
