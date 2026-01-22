import csv
import random
from datetime import datetime, timedelta
import os
import sys
import django
from listings.choices import industry_choices, budget_choices, duration_choices

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password

# Configuration
NUM_COMPANY_USERS = 30  # Company users (1:1 with companies)
NUM_INDIVIDUAL_USERS = 300  # Individual users (job seekers)
NUM_COMPANIES = NUM_COMPANY_USERS  # Same as company users
NUM_LISTINGS = 120
NUM_APPLIES = 1800

# Individual user password and company user password
PASSWORD = {
    "user": "user123",
    "company": "company123"
}

# Industry categories for companies and listings
INDUSTRIES = [value for value in industry_choices]

# Budget ranges
BUDGET_RANGES = [value for value in budget_choices]

# Duration options
DURATIONS = [value for value in duration_choices]

# First and last names for individuals
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Margaret", "Anthony", "Sandra", "Donald", "Ashley", "Mark", "Kimberly",
    "Paul", "Emily", "Steven", "Donna", "Andrew", "Michelle", "Kenneth", "Carol",
    "Joshua", "Amanda", "Kevin", "Dorothy", "Brian", "Melissa", "George", "Deborah",
    "Edward", "Stephanie", "Ronald", "Rebecca", "Timothy", "Sharon", "Jason", "Laura",
    "Jeffrey", "Cynthia", "Ryan", "Kathleen", "Jacob", "Amy", "Gary", "Shirley",
    "Nicholas", "Angela", "Eric", "Helen", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Nicole", "Scott", "Emma", "Brandon", "Samantha"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts"
]

# Company names
COMPANY_NAMES = [
    # Two-Word Tech Names (Modern)
    "SparkLogic", "Nimbus Cloud", "Aether Works", "Circuit Stream",
    "Byte Forge", "Pulse Digital", "Nexus Grid", "Vertex Labs",
    "Quantum Path", "Synapse Systems", "Orbit Tech", "Zenith Digital",
    
    # Founder Name Based (Traditional)
    "Anderson & Sons Tech", "Miller Digital Solutions", "Chang Innovations",
    "Patel Technology Group", "Rodriguez Systems", "Kim Consulting",
    "Nguyen Development", "Schmidt & Partners", "Yamamoto Tech",
    "Garcia Creative", "Johnson Analytics", "Chen Solutions",
    
    # Geographic + Industry
    "Silicon Valley Dynamics", "Bay Area Innovations", "Austin Tech Works",
    "Boston Digital Labs", "Seattle Cloud Solutions", "London Tech Group",
    "Toronto Development Co.", "Singapore Systems", "Berlin Code Factory",
    "Sydney Digital Partners", "Bangalore Tech Hub", "Tel Aviv Innovations",
    
    # Action-Oriented Names
    "BuildRight Solutions", "CreateSpace Digital", "LaunchPad Tech",
    "ScaleFast Systems", "GrowSmart Consulting", "DesignBuild Co.",
    "MakeIt Digital", "CodeCreate Labs", "ThinkBuild Solutions",
    "PlanExecute Partners", "ImagineCreate Studio", "DreamBuild Tech",
    
    # Nature-Inspired Tech
    "OakTree Solutions", "Mountain Peak Tech", "RiverFlow Digital",
    "Skyline Systems", "Horizon Labs", "ForestPath Innovations",
    "OceanDepth Analytics", "DesertWind Tech", "MeadowCode",
    "Summit Digital", "Valley View Tech", "CreekSide Solutions",
    
    # Minimalist Modern
    "Apex", "Vertex", "Nova", "Synapse", "Pulse", "Grid", "Sphere",
    "Core", "Shift", "Spark", "Flow", "Base", "Root", "Edge", "Node",
    
    # Industry-Specific
    "HealthTech Solutions", "FinTech Builders", "EdTech Innovators",
    "RetailTech Systems", "PropTech Labs", "AgriTech Solutions",
    "CleanTech Works", "MedTech Developers", "LegalTech Partners",
    "TravelTech Co.", "FoodTech Innovations", "SportsTech Systems",
    
    # Quirky & Memorable
    "Code Monkeys Inc", "Pixel Pushers", "Binary Bakers", "Algorithm Alchemists",
    "Data Wizards", "Cloud Crafters", "App Architects", "Digital Dreamers",
    "Tech Tinkerers", "Software Sculptors", "Web Weavers", "Mobile Makers",
    
    # Professional Services
    "Strategic Solutions Group", "Professional Partners LLC",
    "Enterprise Excellence Inc", "Corporate Consultants International",
    "Business Development Associates", "Management Advisory Services",
    "Executive Solutions Group", "Performance Partners Ltd"
]

# Job titles and experience for listings
EXPERIENCE_LEVELS = ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]
JOB_TITLES = [
    # Technology & Development (35)
    "Frontend Developer", "Backend Developer", "Full Stack Developer", "React Developer",
    "Python Developer", "Java Developer", "JavaScript Developer", "Node.js Developer",
    "iOS Developer", "Android Developer", "Flutter Developer", "React Native Developer",
    "WordPress Developer", "Shopify Developer", "PHP Developer", "Ruby on Rails Developer",
    "Go Developer", "C# Developer", "ASP.NET Developer", "API Developer",
    "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "AWS Engineer",
    "Azure Cloud Architect", "Google Cloud Engineer", "Kubernetes Specialist", "Docker Specialist",
    "Database Administrator", "PostgreSQL Specialist", "MySQL Developer", "MongoDB Developer",
    "Data Engineer", "ETL Developer", "Big Data Engineer",
    
    # Data Science & AI (10)
    "Data Scientist", "Machine Learning Engineer", "AI Developer", "Computer Vision Engineer",
    "NLP Specialist", "Business Intelligence Analyst", "Data Analyst", "Quantitative Analyst",
    "Research Scientist", "Predictive Modeler",
    
    # Design & Creative (15)
    "UI Designer", "UX Designer", "UI/UX Designer", "Product Designer",
    "Graphic Designer", "Visual Designer", "Motion Graphics Designer", "3D Artist",
    "Illustrator", "Brand Identity Designer", "Packaging Designer", "Web Designer",
    "Game Designer", "AR/VR Designer", "Character Designer",
    
    # Marketing & Content (15)
    "Digital Marketing Manager", "Content Marketing Specialist", "SEO Specialist",
    "SEM Specialist", "Social Media Manager", "Email Marketing Specialist",
    "Content Writer", "Copywriter", "Technical Writer", "Blog Writer",
    "Video Editor", "Video Producer", "Photographer", "Podcast Producer",
    "Influencer Marketing Manager",
    
    # Business & Management (15)
    "Project Manager", "Product Manager", "Scrum Master", "Agile Coach",
    "Business Analyst", "Systems Analyst", "Process Consultant", "Operations Manager",
    "Business Development Manager", "Sales Executive", "Account Manager",
    "Customer Success Manager", "HR Manager", "Recruitment Specialist",
    "Executive Assistant",
    
    # Finance & Legal (5)
    "Financial Analyst", "Accountant", "Bookkeeper", "Tax Consultant",
    "Legal Consultant",
    
    # Specialized Technical (5)
    "Blockchain Developer", "Smart Contract Developer", "Cybersecurity Analyst",
    "Penetration Tester", "IoT Developer"
]

# Skills for services/requirements
SKILLS = [
    # Programming Languages (25)
    "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Ruby",
    "Go", "Swift", "Kotlin", "Rust", "Scala", "Perl", "R", "MATLAB", "Dart",
    "Objective-C", "Shell Scripting", "Bash", "PowerShell", "SQL", "NoSQL",
    "GraphQL", "Assembly",
    
    # Web Frontend (15)
    "React", "Angular", "Vue.js", "Next.js", "Nuxt.js", "Svelte", "Gatsby",
    "HTML5", "CSS3", "SASS/SCSS", "Tailwind CSS", "Bootstrap", "Material-UI",
    "Webpack", "Vite",
    
    # Web Backend (20)
    "Node.js", "Express.js", "Django", "Flask", "FastAPI", "Spring Boot",
    "ASP.NET", "Laravel", "Ruby on Rails", "Symfony", "NestJS", "Koa.js",
    "GraphQL", "REST API", "Microservices", "Serverless", "WebSockets",
    "API Development", "API Integration", "API Design",
    
    # Mobile Development (10)
    "React Native", "Flutter", "iOS Development", "Android Development",
    "Xamarin", "Ionic", "Cordova", "Mobile UI/UX", "App Store Deployment",
    "Google Play Store",
    
    # Databases (15)
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Elasticsearch",
    "SQLite", "Oracle", "SQL Server", "Firebase", "Supabase", "DynamoDB",
    "Neo4j", "MariaDB", "Cosmos DB",
    
    # Cloud & DevOps (25)
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
    "Ansible", "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI",
    "CI/CD", "Infrastructure as Code", "Serverless", "Lambda",
    "EC2", "S3", "RDS", "CloudFormation", "CloudFront", "Load Balancing",
    "Monitoring", "Logging", "Alerting", "Site Reliability Engineering",
    
    # Data Science & AI (20)
    "Machine Learning", "Deep Learning", "Data Science", "Data Analysis",
    "Data Visualization", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Tableau",
    "Power BI", "Natural Language Processing", "Computer Vision",
    "Big Data", "Hadoop",
    
    # Design & Creative (15)
    "UI Design", "UX Design", "Figma", "Adobe XD", "Sketch", "Adobe Creative Suite",
    "Photoshop", "Illustrator", "InDesign", "After Effects", "Premiere Pro",
    "Blender", "3D Modeling", "Motion Graphics", "Prototyping",
    
    # Testing & QA (10)
    "Unit Testing", "Integration Testing", "End-to-End Testing", "Selenium",
    "Cypress", "Jest", "Mocha", "Chai", "Test Automation", "Quality Assurance",
    
    # Project Management (10)
    "Agile", "Scrum", "Kanban", "Jira", "Confluence", "Trello", "Asana",
    "Project Management", "Product Management", "Waterfall",
    
    # Cybersecurity (10)
    "Cybersecurity", "Penetration Testing", "Ethical Hacking", "OWASP",
    "Network Security", "Application Security", "Cryptography", "SSL/TLS",
    "VPN", "Firewall",
    
    # Business & Soft Skills (15)
    "Communication", "Problem Solving", "Team Leadership", "Project Coordination",
    "Client Management", "Technical Writing", "Documentation", "Presentation",
    "Requirements Analysis", "Stakeholder Management", "Time Management",
    "Critical Thinking", "Collaboration", "Mentoring", "Public Speaking",
    
    # E-commerce & CMS (10)
    "WordPress", "Shopify", "WooCommerce", "Magento", "BigCommerce",
    "SquareSpace", "Webflow", "Content Management", "Payment Gateway Integration",
    "E-commerce Development",
    
    # Blockchain & Web3 (8)
    "Blockchain", "Smart Contracts", "Solidity", "Web3", "Ethereum",
    "NFT Development", "DeFi", "Cryptocurrency",
    
    # IoT & Embedded (7)
    "IoT", "Embedded Systems", "Arduino", "Raspberry Pi", "Microcontrollers",
    "Firmware", "Hardware Programming"
]

DESCRIPTIONS = [
        # Tech/Development Projects (15)
        "We need a full-stack developer to build a responsive web application from scratch. The project includes frontend with React, backend with Node.js, and MongoDB database. Experience with REST APIs and cloud deployment required.",
        "Looking for an experienced mobile app developer to create a cross-platform application for iOS and Android. Must have experience with React Native or Flutter, and integrating third-party APIs for payment processing.",
        "Seeking a Python developer to build data pipelines and automate reporting processes. Experience with pandas, NumPy, and data visualization libraries is essential. Knowledge of machine learning is a plus.",
        "Need a WordPress expert to redesign our corporate website with custom theme development. Must have experience with WooCommerce integration and page speed optimization.",
        "Looking for a DevOps engineer to set up CI/CD pipelines and containerize our applications using Docker and Kubernetes. Experience with AWS or Azure cloud services required.",
        "We need a UI/UX designer to create wireframes and prototypes for our new SaaS platform. Must have experience with Figma or Adobe XD and understanding of user-centered design principles.",
        "Seeking a blockchain developer to build a smart contract for an Ethereum-based application. Experience with Solidity, Web3.js, and cryptocurrency wallet integrations required.",
        "Looking for a QA engineer to develop and execute comprehensive test plans for our web application. Must have experience with automated testing frameworks like Selenium or Cypress.",
        "Need a cybersecurity specialist to conduct vulnerability assessment and penetration testing for our network infrastructure. Relevant certifications (CEH, OSCP) are preferred.",
        "Seeking a machine learning engineer to develop predictive models for customer behavior analysis. Experience with TensorFlow, PyTorch, and data preprocessing techniques required.",
        "Looking for a chatbot developer to create an AI-powered customer service assistant using natural language processing. Experience with Dialogflow or Rasa framework is essential.",
        "We need an API developer to design and implement RESTful services for our microservices architecture. Must have experience with API documentation (Swagger/OpenAPI) and security best practices.",
        "Looking for an e-commerce specialist to optimize our online store for conversion rate improvement. Experience with A/B testing, analytics, and customer journey mapping required.",
        "Seeking a video game developer to create a 2D mobile game using Unity or Unreal Engine. Experience with game physics, animation, and monetization strategies is essential.",
        "Need a technical writer to create comprehensive documentation for our software products. Must have experience with Markdown, Git, and ability to explain complex technical concepts clearly.",
        
        # Marketing/Creative Projects (10)
        "We need a digital marketing specialist to develop and execute a comprehensive social media strategy across Facebook, Instagram, and LinkedIn. Must have experience with content planning and performance analytics.",
        "Looking for a content writer to create blog articles and whitepapers for our B2B technology company. Must have strong research skills and ability to write about complex technical topics.",
        "Seeking a graphic designer to create marketing collateral including brochures, presentations, and social media graphics. Proficiency in Adobe Creative Suite required.",
        "Need a video editor to produce promotional videos and tutorials for our product line. Experience with Adobe Premiere Pro, After Effects, and color grading required.",
        "Looking for an SEO specialist to improve our website's organic search rankings. Must have experience with keyword research, on-page optimization, and backlink strategy.",
        "We need a copywriter to craft compelling product descriptions and email marketing campaigns. Experience with persuasive writing and conversion optimization techniques required.",
        "Seeking a social media manager to handle daily posting, community engagement, and influencer partnerships. Experience with social media management tools and analytics required.",
        "Looking for a brand identity designer to create a complete visual identity system including logo, color palette, typography, and brand guidelines.",
        "Need a PR specialist to develop media relations strategy and secure coverage in industry publications. Experience with press release writing and media pitching required.",
        "Seeking a marketing analytics expert to set up tracking dashboards and provide insights for campaign optimization. Experience with Google Analytics, Google Tag Manager, and data visualization tools essential.",
        
        # Business/Consulting Projects (8)
        "We need a business consultant to analyze our current operations and recommend process improvements. Experience with Lean Six Sigma or similar methodologies preferred.",
        "Looking for a financial analyst to create financial models and projections for our startup. Must have experience with Excel modeling, valuation techniques, and investor presentations.",
        "Seeking a project manager to oversee the development of our new product launch. Experience with Agile methodology, JIRA, and cross-functional team coordination required.",
        "Need a HR consultant to develop employee onboarding programs and performance management systems. Experience with HR best practices and compliance requirements essential.",
        "Looking for a sales strategist to design and implement a B2B sales process for our SaaS product. Experience with CRM systems and sales pipeline management required.",
        "We need a market researcher to conduct competitive analysis and customer interviews for our new product concept. Experience with survey design and qualitative research methods required.",
        "Seeking a business plan writer to create a comprehensive business plan for investor funding. Must have experience with financial projections, market analysis, and executive summaries.",
        "Looking for an operations specialist to optimize our supply chain and inventory management processes. Experience with logistics and warehouse management systems preferred.",
        
        # Design/Creative Projects (7)
        "We need an interior designer to create 3D renderings and floor plans for our office renovation project. Experience with AutoCAD, SketchUp, and client presentations required.",
        "Looking for a packaging designer to create innovative and sustainable packaging solutions for our consumer products. Experience with structural design and material selection essential.",
        "Seeking a fashion designer to develop a new clothing line for our brand. Must have experience with pattern making, fabric selection, and fashion illustration.",
        "Need an architectural designer to create concept designs for residential building projects. Proficiency in Revit and 3D visualization software required.",
        "Looking for a product designer to develop ergonomic furniture concepts from ideation to prototyping. Experience with CAD software and material testing required.",
        "We need an industrial designer to create consumer electronics products with focus on user experience and manufacturability. Experience with 3D printing and prototyping essential.",
        "Seeking a motion graphics designer to create animated explainer videos and title sequences. Proficiency in After Effects and understanding of animation principles required.",
        
        # Writing/Translation Projects (5)
        "Looking for a technical translator to translate software documentation from English to Japanese. Must have native-level proficiency in both languages and technical background.",
        "We need a legal writer to draft contracts and terms of service for our online platform. Experience with legal terminology and attention to detail essential.",
        "Seeking a medical writer to create patient education materials and clinical study summaries. Background in healthcare and ability to simplify complex medical information required.",
        "Need an academic writer to help with research papers and literature reviews. Experience with academic formatting (APA/MLA) and plagiarism-free writing required.",
        "Looking for a grant writer to prepare funding proposals for our non-profit organization. Experience with foundation research and persuasive proposal writing required.",
        
        # Miscellaneous Projects (5)
        "We need a virtual assistant to handle administrative tasks including email management, calendar scheduling, and data entry. Strong organizational skills and attention to detail required.",
        "Looking for a language tutor to provide one-on-one English lessons via video conferencing. Teaching certification and experience with online teaching platforms preferred.",
        "Seeking a fitness coach to create personalized workout programs and provide virtual training sessions. Certified personal trainer with online coaching experience required.",
        "Need an event planner to coordinate a virtual conference with multiple speakers and breakout sessions. Experience with webinar platforms and attendee engagement strategies essential.",
        "Looking for a data entry specialist to digitize and organize large volumes of paper documents. High accuracy rate and experience with database management required."
    ]

SERVICES = [
        # Technology & Development Services (15)
        "Full-Stack Web Development, Responsive Design, Progressive Web Apps",
        "Mobile App Development (iOS & Android), Cross-Platform Solutions",
        "Custom Software Development, Enterprise Applications, System Architecture",
        "Cloud Migration Services, AWS Consulting, Azure Implementation",
        "DevOps Engineering, CI/CD Pipeline Setup, Containerization",
        "Blockchain Development, Smart Contracts, DApp Creation",
        "E-commerce Solutions, Shopify Development, WooCommerce Customization",
        "API Development & Integration, Microservices Architecture",
        "Quality Assurance Testing, Automated Testing Solutions",
        "Technical Support, IT Helpdesk, System Maintenance",
        "Database Design & Optimization, Data Migration Services",
        "IoT Solutions, Embedded Systems, Hardware Integration",
        "Game Development, Unity 3D, Mobile Gaming Solutions",
        "CRM Implementation, Salesforce Consulting, Business Process Automation",
        "Legacy System Modernization, Code Refactoring, Technical Debt Reduction",
        
        # Design & Creative Services (10)
        "UI/UX Design, Wireframing, User Research & Testing",
        "Brand Identity Design, Logo Creation, Visual Identity Systems",
        "Graphic Design, Marketing Collateral, Print & Digital Media",
        "Motion Graphics, Animated Explainer Videos, 2D/3D Animation",
        "Product Design, Industrial Design, Prototyping Services",
        "Architectural Visualization, 3D Rendering, Interior Design",
        "Packaging Design, Structural Design, Sustainable Solutions",
        "Video Production, Editing, Corporate Video Creation",
        "Photography Services, Product Photography, Commercial Shoots",
        "Illustration Services, Digital Art, Character Design",
        
        # Marketing & Business Services (10)
        "Digital Marketing Strategy, Campaign Management, Performance Analysis",
        "Search Engine Optimization (SEO), Local SEO, Technical SEO Audits",
        "Social Media Marketing, Community Management, Influencer Partnerships",
        "Content Marketing, Blog Writing, Content Strategy Development",
        "Pay-Per-Click Advertising, Google Ads Management, Social Media Ads",
        "Email Marketing, Newsletter Campaigns, Marketing Automation",
        "Public Relations, Media Outreach, Press Release Distribution",
        "Market Research, Competitive Analysis, Consumer Insights",
        "Business Consulting, Strategic Planning, Operational Excellence",
        "Sales Enablement, CRM Strategy, Sales Process Optimization",
        
        # Data & Analytics Services (5)
        "Data Analytics, Business Intelligence, Dashboard Development",
        "Big Data Solutions, Data Warehousing, ETL Pipeline Development",
        "Machine Learning Solutions, Predictive Analytics, AI Integration",
        "Data Visualization, Interactive Reports, KPI Monitoring",
        "Data Strategy, Governance, Compliance Consulting",
        
        # Specialized Professional Services (5)
        "Legal Consulting, Contract Review, Intellectual Property Protection",
        "Financial Advisory, Investment Analysis, Financial Modeling",
        "HR Consulting, Talent Acquisition, Performance Management Systems",
        "Supply Chain Optimization, Logistics Management, Inventory Control",
        "Healthcare IT Solutions, Medical Software, HIPAA Compliance",
        
        # Miscellaneous Services (5)
        "Virtual Assistant Services, Administrative Support, Calendar Management",
        "Translation Services, Localization, Multilingual Content Creation",
        "Online Education Platforms, E-learning Solutions, Course Development",
        "Sustainability Consulting, Environmental Impact Assessment",
        "Event Planning, Virtual Conference Management, Webinar Production"
    ]

MESSAGES = [
        # Technical Projects (15)
        "With 5+ years of experience in full-stack development, I have successfully delivered similar projects using React and Node.js. I'm excited about your tech stack and ready to contribute immediately.",
        "As a certified AWS Solutions Architect, I've helped multiple companies migrate to cloud infrastructure. Your project requirements align perfectly with my expertise in scalable cloud solutions.",
        "Having developed 10+ mobile apps on both iOS and Android, I'm confident I can deliver a high-quality application for your project. I'm particularly impressed with your app concept.",
        "Your need for API integration matches my specialization. I've built robust REST APIs for enterprise clients and can ensure seamless connectivity with your existing systems.",
        "As a DevOps engineer with Kubernetes certification, I can optimize your deployment pipeline and implement best practices for container orchestration, reducing costs by 30% typically.",
        "My portfolio includes several e-commerce platforms with payment gateway integrations. I understand the security and performance requirements for online transactions.",
        "With expertise in Python data science libraries, I can help you build the predictive models you need. I've attached case studies showing 25% improvement in similar projects.",
        "Your cybersecurity requirements are exactly what I specialize in. I hold CEH certification and have conducted penetration testing for financial institutions.",
        "As a blockchain developer with 3 years of Solidity experience, I can build secure smart contracts for your Ethereum project. I'm familiar with the gas optimization techniques you'll need.",
        "I've been following your company's work in the AI space and would be thrilled to contribute. My ML models have achieved 95% accuracy in similar classification tasks.",
        "Your WordPress customization project requires the specific WooCommerce expertise I've developed over 50+ successful implementations.",
        "Having led QA teams for software companies, I can establish comprehensive testing protocols that will ensure your product launches with minimal bugs.",
        "My experience with microservices architecture and Docker containerization can help you achieve the scalability goals mentioned in your project description.",
        "I specialize in legacy system modernization and have successfully migrated several companies from outdated platforms to modern tech stacks.",
        "Your IoT project requires the embedded systems experience I've gained through 8+ years in hardware-software integration.",
        
        # Design & Creative (10)
        "Your branding project caught my eye! I've developed visual identities for 20+ companies in your industry and understand what resonates with your target audience.",
        "As a UI/UX designer with a psychology background, I focus on creating intuitive user experiences. Your project goals align with my human-centered design approach.",
        "I've created motion graphics for major brands and can bring your explainer video concept to life with engaging animations that increase viewer retention.",
        "Your packaging design requirements match my sustainable design philosophy. I specialize in eco-friendly materials and minimalist aesthetics.",
        "Having designed user interfaces for SaaS platforms, I can create the clean, functional design your web application needs to stand out in the market.",
        "My architectural visualization work has helped clients secure millions in funding. I can create photorealistic renders that showcase your project's potential.",
        "Your need for a comprehensive brand identity system is exactly what I excel at. I create cohesive visual systems that work across all touchpoints.",
        "I specialize in conversion-focused web design and have increased conversion rates by up to 40% for previous clients with similar target markets.",
        "Your video production project requires the storytelling expertise I've developed through film school and commercial production experience.",
        "As a product designer with manufacturing experience, I can create designs that are both beautiful and production-ready, saving you time and costs.",
        
        # Marketing & Content (10)
        "Your content marketing strategy could benefit from my SEO writing expertise. I've helped companies achieve first-page rankings for competitive keywords.",
        "Having managed social media campaigns with 500% ROI, I can develop a strategy that engages your audience and drives meaningful conversions.",
        "Your SEO audit needs match my technical SEO specialization. I've identified and fixed critical issues that improved organic traffic by 200%+ for clients.",
        "I've written successful grant proposals securing over $2M in funding for nonprofits. I understand how to craft compelling narratives for funders.",
        "Your email marketing campaign could achieve better results with my segmentation and personalization strategies that typically increase open rates by 35%.",
        "As a bilingual content creator, I can help you expand into new markets with culturally adapted messaging that resonates with local audiences.",
        "I specialize in B2B marketing content and have written whitepapers that generated qualified leads for technology companies like yours.",
        "Your PR campaign needs the media relations skills I've developed through years of securing coverage in top industry publications.",
        "Having created successful influencer marketing campaigns, I can identify and partner with influencers who authentically represent your brand.",
        "I develop comprehensive marketing strategies that align sales and marketing efforts, typically increasing marketing-sourced revenue by 50%.",
        
        # Business & Consulting (8)
        "Your business process optimization project requires the Lean Six Sigma expertise I've applied to save companies an average of $500K annually.",
        "As a financial analyst with CFA certification, I can build the valuation models and investor presentations you need for your funding round.",
        "Having managed Agile teams for 8 years, I can implement the Scrum framework to keep your project on track and within budget.",
        "Your HR system implementation matches my experience with HRIS platforms. I've successfully transitioned companies to automated systems.",
        "I specialize in market entry strategies and have helped 15+ companies successfully expand into new geographic markets.",
        "Your sales process could benefit from the CRM optimization strategies I've implemented, typically increasing sales team productivity by 30%.",
        "Having written 50+ business plans that secured funding, I understand what investors look for and how to present your opportunity compellingly.",
        "I've optimized supply chains for manufacturing companies, reducing lead times by 40% and inventory costs by 25% on average.",
        
        # General & Enthusiastic (7)
        "I'm genuinely excited about this opportunity! Your project combines several areas where I excel, and I'm confident I can deliver exceptional results.",
        "This project aligns perfectly with both my skills and personal interests. I've been looking for exactly this type of challenge to apply my expertise.",
        "Having reviewed your company's portfolio, I'm impressed by your work and would be honored to contribute to your team's success.",
        "Your project timeline fits perfectly with my availability, and I can dedicate the focused attention needed to exceed your expectations.",
        "I bring not just technical skills but also a collaborative mindset that helps teams work more effectively together toward common goals.",
        "This opportunity represents the next logical step in my career progression, and I'm eager to bring my growing expertise to your organization.",
        "I appreciate your detailed project description and believe my approach to problem-solving matches what you're looking for in a candidate."
    ]


def generate_phone():
    """Generate a random phone number"""
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_email(first_name, last_name, company=False):
    """Generate a random email address"""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    company_domains = ["tech.com", "solutions.com", "corp.com", "inc.com", "digital.com"]
    
    if company:
        domain = random.choice(company_domains)
        return f"{first_name.lower()}.{last_name.lower()}@{domain}"
    else:
        domain = random.choice(domains)
        variations = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{random.randint(1, 99)}"
        ]
        return f"{random.choice(variations)}@{domain}"

def generate_date(start_date, end_date):
    """Generate a random date between start and end"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def generate_description():
    """Generate a random description"""
    return random.choice(DESCRIPTIONS)

def generate_services():
    """Generate company services"""
    return random.choice(SERVICES)

def generate_message():
    """Generate application message"""
    return random.choice(MESSAGES)

def generate_auth_user_data():
    """Generate auth_user data with properly hashed passwords"""
    data = []
    
    # Generate company users
    for i in range(NUM_COMPANY_USERS):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"company_user_{i+1}"
        email = generate_email(first_name, last_name, company=True)
        
        # Hash password using Django's make_password
        hashed_password = make_password(PASSWORD["company"])
        
        user = {
            "password": hashed_password,
            "last_login": generate_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            "is_superuser": "false",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": "false",
            "is_active": "true",
            "date_joined": generate_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(user)
    
    # Generate individual users
    for i in range(NUM_INDIVIDUAL_USERS):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"user_{i+1}"
        email = generate_email(first_name, last_name)
        
        # Hash password using Django's make_password
        hashed_password = make_password(PASSWORD['user'])
        
        user = {
            "password": hashed_password, 
            "last_login": generate_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            "is_superuser": "false",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": "false",
            "is_active": "true",
            "date_joined": generate_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(user)
    
    return data

def hsl_to_hex(h, s, l):
    """Convert HSL to HEX color"""
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}".upper()  

def generate_logo_from_name(company_name, company_id):
    """Generate logo with colors based on company name"""
    
    # Generate hash from company name
    name_hash = hash(company_name) % 360  # 0-359 for hue
    
    # Use HSL color model for consistent schemes
    # Background: Main color
    hue = name_hash
    saturation = random.randint(40, 80)
    lightness = random.randint(30, 60)
    
    bg_color = hsl_to_hex(hue, saturation, lightness)
    
    # Text: Complementary or monochromatic
    if random.choice([True, False]):
        # Complementary color (opposite on color wheel)
        text_hue = (hue + 180) % 360
        text_color = hsl_to_hex(text_hue, saturation, lightness)
    else:
        # White or black based on background brightness
        if lightness < 45:
            text_color = "#FFFFFF"
        else:
            text_color = "#000000"
    
    bg_hex = bg_color[1:]
    text_hex = text_color[1:]
    
    # Use company initials as text
    initials = ''.join([word[0].upper() for word in company_name.split()])[:3]
    if not initials:
        initials = f"C{company_id}"
    
    return f"https://placehold.co/150x150/{bg_hex}/{text_hex}/png?text={initials}"

def generate_company_data():
    """Generate company data"""
    data = []
    
    for i in range(NUM_COMPANIES):
        # Get corresponding user (first NUM_COMPANY_USERS are company users)
        user_id = i + 1  # User IDs start from 1
        company_name = COMPANY_NAMES[i % len(COMPANY_NAMES)]
        
        # Get user info from auth_user to match email
        # In real scenario, you'd fetch this, but here we'll generate
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        company = {
            "name": company_name,
            # "logo": f"photos/2024/01/{random.randint(1, 31):02d}/logo_{i+1}.jpg",
            "logo": generate_logo_from_name(company_name, user_id),
            "industry": random.choice(INDUSTRIES),
            "serivces": generate_services(),  # Note: Typo in field name 'serivces' from your model
            "description": generate_description(),
            "phone": generate_phone(),
            "email": generate_email(first_name, last_name, company=True),
            "create_date": generate_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id
        }
        data.append(company)
    
    return data

def generate_listing_data():
    """Generate listing data"""
    data = []
    
    for i in range(NUM_LISTINGS):
        company_id = random.randint(1, NUM_COMPANIES)
        publish_date = generate_date(datetime(2023, 1, 1), datetime(2024, 12, 31))
        
        # Ensure is_active is boolean
        is_active = "1" if random.random() > 0.2 else "0"  # 80% active
        
        listing = {
            "company_id": company_id,
            "title": f"{random.choice(EXPERIENCE_LEVELS)} {random.choice(JOB_TITLES)}",
            "industry": random.choice(INDUSTRIES),
            "budget": random.choice(BUDGET_RANGES),
            "duration": random.choice(DURATIONS),
            "description": generate_description(),
            "requirement": ", ".join(random.sample(SKILLS, random.randint(3, 6))),
            "publish_date": publish_date.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": is_active
        }
        data.append(listing)
    
    return data

def generate_apply_data():
    """Generate apply data"""
    data = []
    
    for i in range(NUM_APPLIES):
        listing_id = random.randint(1, NUM_LISTINGS)
        
        # User must be an individual user (IDs after company users)
        user_id = random.randint(NUM_COMPANY_USERS + 1, NUM_COMPANY_USERS + NUM_INDIVIDUAL_USERS)
        
        # Generate applicant info
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        # Generate apply date after listing publish date
        # We'll assume listing publish dates are between 2023-2024
        apply_date = generate_date(datetime(2023, 6, 1), datetime(2024, 12, 31))
        
        apply_record = {
            "listing_id": listing_id,
            "name": f"{first_name} {last_name}",
            "email": generate_email(first_name, last_name),
            "phone": generate_phone(),
            "message": generate_message(),
            "cv": f"cv/2024/01/{random.randint(1, 31):02d}/cv_{i+1}.pdf",
            "apply_date": apply_date.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id
        }
        data.append(apply_record)
    
    return data

def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    os.makedirs('dummy_data', exist_ok=True)
    filepath = f'dummy_data/{filename}'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} records in {filepath}")

def main():
    print("Generating dummy data for Django project...")
    
    # Generate and save auth_user data
    auth_user_fields = [
        "password", "last_login", "is_superuser", "username", "first_name",
        "last_name", "email", "is_staff", "is_active", "date_joined"
    ]
    auth_user_data = generate_auth_user_data()
    write_csv('auth_user.csv', auth_user_data, auth_user_fields)
    
    # Generate and save company data
    company_fields = [
        "name", "logo", "industry", "serivces", "description", 
        "phone", "email", "create_date", "user_id"
    ]
    company_data = generate_company_data()
    write_csv('companies_company.csv', company_data, company_fields)
    
    # Generate and save listing data
    listing_fields = [
        "company_id", "title", "industry", "budget", "duration",
        "description", "requirement", "publish_date", "is_active"
    ]
    listing_data = generate_listing_data()
    write_csv('listings_listing.csv', listing_data, listing_fields)
    
    # Generate and save apply data
    apply_fields = [
        "name", "email", "phone", "message",
        "cv", "apply_date", "listing_id", "user_id"
    ]
    apply_data = generate_apply_data()
    write_csv('applies_apply.csv', apply_data, apply_fields)
    
    print("\n" + "="*50)
    print("DATA GENERATION COMPLETE!")
    print("="*50)
    print(f"Total auth_user records: {NUM_COMPANY_USERS + NUM_INDIVIDUAL_USERS}")
    print(f"Total company records: {NUM_COMPANIES}")
    print(f"Total listing records: {NUM_LISTINGS}")
    print(f"Total apply records: {NUM_APPLIES}")
    print("\nFiles saved in 'dummy_data/' directory:")
    print("1. auth_user.csv")
    print("2. companies_company.csv")
    print("3. listings_listing.csv")
    print("4. applies_apply.csv")
    print("\n" + "="*50)
    print("IMPORT INSTRUCTIONS:")
    print("1. Make sure Django project is set up and migrations are applied")
    print("2. Use Django's loaddata command or write a script to import CSV")
    print("3. Note: Passwords are already hashed using Django's make_password")
    print("   Company users: company123, Individual users: user123")
    print("="*50)

if __name__ == "__main__":
    main()