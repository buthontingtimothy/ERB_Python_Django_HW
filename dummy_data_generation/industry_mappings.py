"""
Industry mappings for data generation alignment
"""

# Define industry categories and their associated data
INDUSTRY_CATEGORIES = {
    # Technology & IT
    "Technology": {
        "company_keywords": ["tech", "digital", "software", "code", "data", "cloud", "ai", "mobile", "web", "network", "cyber", "system"],
        "job_titles": ["Developer", "Engineer", "Architect", "Analyst", "Specialist", "Administrator", "Consultant", "Manager"],
        "skills_keywords": ["python", "javascript", "java", "react", "node", "aws", "azure", "docker", "kubernetes", "devops", "api", "sql", "nosql", "git"],
        "service_keywords": ["development", "software", "cloud", "mobile", "web", "api", "devops", "cybersecurity", "data", "analytics"],
        "description_keywords": ["software", "application", "platform", "system", "cloud", "mobile", "web", "api", "database", "security"]
    },
    
    # Finance & Banking
    "Finance": {
        "company_keywords": ["finance", "bank", "capital", "wealth", "investment", "fund", "financial", "trust", "equity", "risk", "payment"],
        "job_titles": ["Analyst", "Manager", "Advisor", "Consultant", "Specialist", "Officer", "Banker", "Accountant", "Auditor"],
        "skills_keywords": ["financial", "analysis", "accounting", "excel", "modeling", "valuation", "risk", "compliance", "quickbooks", "tax", "audit"],
        "service_keywords": ["financial", "investment", "accounting", "tax", "audit", "compliance", "wealth", "banking", "payment"],
        "description_keywords": ["financial", "investment", "accounting", "tax", "audit", "banking", "wealth", "portfolio", "risk"]
    },
    
    # Healthcare & Medical
    "Healthcare": {
        "company_keywords": ["health", "medical", "care", "clinic", "hospital", "bio", "life", "patient", "therapy", "clinical", "pharma"],
        "job_titles": ["Coordinator", "Specialist", "Analyst", "Writer", "Engineer", "Consultant", "Administrator", "Coder", "Researcher"],
        "skills_keywords": ["medical", "healthcare", "clinical", "patient", "hipaa", "ehr", "pharmaceutical", "research", "compliance", "telemedicine"],
        "service_keywords": ["medical", "healthcare", "clinical", "patient", "telemedicine", "pharmaceutical", "research", "compliance"],
        "description_keywords": ["medical", "healthcare", "patient", "clinical", "research", "treatment", "therapy", "diagnostic", "pharmaceutical"]
    },
    
    # Consulting
    "Consulting": {
        "company_keywords": ["consulting", "business", "strategy", "solution", "partner", "corporate", "enterprise", "operational", "process", "advisory"],
        "job_titles": ["Manager", "Analyst", "Consultant", "Specialist", "Coordinator", "Director", "Officer", "Assistant", "Strategist"],
        "skills_keywords": ["management", "project", "business", "analysis", "agile", "scrum", "jira", "process", "operations", "strategy", "planning"],
        "service_keywords": ["consulting", "business", "management", "strategy", "process", "operations", "project", "corporate"],
        "description_keywords": ["business", "management", "process", "operations", "strategy", "consulting", "project", "corporate", "enterprise"]
    },
    
    # Design & Creative
    "Marketing": {
        "company_keywords": ["marketing", "advertising", "media", "brand", "digital", "social", "content", "creative", "agency", "pr", "strategy"],
        "job_titles": ["Manager", "Specialist", "Analyst", "Strategist", "Consultant", "Writer", "Editor", "Director", "Coordinator"],
        "skills_keywords": ["marketing", "seo", "social", "content", "google", "analytics", "ads", "email", "campaign", "brand", "strategy"],
        "service_keywords": ["marketing", "digital", "social", "content", "seo", "advertising", "brand", "pr", "campaign"],
        "description_keywords": ["marketing", "campaign", "brand", "content", "social", "digital", "advertising", "strategy", "audience"]
    },
    
    # Education & Training
    "Education": {
        "company_keywords": ["education", "learning", "academy", "school", "university", "training", "instruction", "curriculum", "e-learning", "tutor"],
        "job_titles": ["Developer", "Designer", "Specialist", "Coordinator", "Writer", "Tutor", "Consultant", "Manager", "Researcher"],
        "skills_keywords": ["education", "learning", "curriculum", "instruction", "e-learning", "lms", "training", "assessment", "research", "teaching"],
        "service_keywords": ["education", "learning", "training", "e-learning", "curriculum", "instruction", "tutoring", "educational"],
        "description_keywords": ["education", "learning", "training", "curriculum", "instruction", "e-learning", "educational", "teaching", "assessment"]
    },
    
    # Energy & Utilities
    "Energy": {
        "company_keywords": ["energy", "utility", "power", "renewable", "sustainable", "environmental", "oil", "gas", "electric", "grid", "solar", "wind"],
        "job_titles": ["Analyst", "Engineer", "Specialist", "Manager", "Consultant", "Coordinator", "Researcher"],
        "skills_keywords": ["energy", "renewable", "power", "environmental", "utility", "grid", "oil", "gas", "efficiency", "compliance"],
        "service_keywords": ["energy", "renewable", "power", "utility", "environmental", "sustainable", "oil", "gas"],
        "description_keywords": ["energy", "power", "renewable", "utility", "sustainable", "environmental", "grid", "oil", "gas"]
    },
    
    # Entertainment & Media
    "Entertainment": {
        "company_keywords": ["entertainment", "production", "film", "television", "music", "gaming", "broadcast", "content", "studio", "creative"],
        "job_titles": ["Producer", "Editor", "Writer", "Manager", "Director", "Analyst", "Specialist", "Coordinator", "Creator"],
        "skills_keywords": ["entertainment", "video", "production", "audio", "editing", "content", "broadcast", "film", "music", "gaming"],
        "service_keywords": ["entertainment", "production", "video", "content", "broadcast", "film", "music", "gaming"],
        "description_keywords": ["entertainment", "production", "video", "content", "film", "music", "gaming", "broadcast"]
    },
    
    # Government
    "Government": {
        "company_keywords": ["government", "public", "social", "aid", "environmental", "education", "healthcare", "cultural", "justice"],
        "job_titles": ["Coordinator", "Manager", "Analyst", "Writer", "Specialist", "Consultant", "Director", "Researcher"],
        "skills_keywords": ["government", "grant", "fundraising", "program", "community", "policy", "public", "administration", "outreach"],
        "service_keywords": ["government", "community", "public", "grant", "fundraising", "program", "policy"],
        "description_keywords": ["government", "community", "public", "program", "grant", "fundraising", "policy", "social"]
    },
    
    # Hospitality & Tourism
    "Hospitality": {
        "company_keywords": ["hospitality", "tourism", "hotel", "restaurant", "travel", "event", "catering", "resort", "vacation", "culinary"],
        "job_titles": ["Manager", "Planner", "Specialist", "Coordinator", "Consultant", "Director", "Analyst"],
        "skills_keywords": ["hospitality", "tourism", "hotel", "event", "customer", "restaurant", "food", "safety", "revenue", "travel"],
        "service_keywords": ["hospitality", "tourism", "hotel", "event", "travel", "restaurant", "catering", "vacation"],
        "description_keywords": ["hospitality", "tourism", "hotel", "travel", "event", "restaurant", "vacation", "customer", "experience"]
    },
    
    # Legal Services
    "Legal": {
        "company_keywords": ["legal", "law", "attorney", "corporate", "intellectual", "property", "contract", "justice", "rights", "defense"],
        "job_titles": ["Consultant", "Analyst", "Writer", "Specialist", "Manager", "Researcher", "Coordinator"],
        "skills_keywords": ["legal", "law", "contract", "intellectual", "property", "corporate", "research", "compliance", "regulation", "litigation"],
        "service_keywords": ["legal", "law", "corporate", "intellectual", "property", "contract", "compliance", "litigation"],
        "description_keywords": ["legal", "law", "contract", "corporate", "intellectual property", "compliance", "litigation", "regulation", "rights"]
    },
    
    # Manufacturing & Engineering
    "Manufacturing": {
        "company_keywords": ["manufacturing", "engineering", "industrial", "production", "factory", "machinery", "quality", "supply", "logistics", "assembly"],
        "job_titles": ["Engineer", "Manager", "Supervisor", "Analyst", "Coordinator", "Specialist", "Consultant", "Planner"],
        "skills_keywords": ["manufacturing", "engineering", "quality", "lean", "six", "supply", "production", "process", "safety", "cad", "industrial"],
        "service_keywords": ["manufacturing", "engineering", "industrial", "production", "quality", "supply", "logistics", "assembly"],
        "description_keywords": ["manufacturing", "production", "engineering", "industrial", "quality", "supply", "logistics", "assembly", "factory"]
    },
    
    # Media
    "Media": {
        "company_keywords": ["media", "entertainment", "production", "film", "television", "music", "gaming", "broadcast", "content", "studio", "creative"],
        "job_titles": ["Producer", "Editor", "Writer", "Manager", "Director", "Analyst", "Specialist", "Coordinator", "Creator"],
        "skills_keywords": ["media", "entertainment", "video", "production", "audio", "editing", "content", "broadcast", "film", "music", "gaming"],
        "service_keywords": ["media", "entertainment", "production", "video", "content", "broadcast", "film", "music", "gaming"],
        "description_keywords": ["media", "entertainment", "production", "video", "content", "film", "music", "gaming", "broadcast"]
    },
    
    # Non-Profit
    "Non-Profit": {
        "company_keywords": ["non-profit", "community", "public", "social", "aid", "environmental", "education", "healthcare", "cultural", "justice"],
        "job_titles": ["Coordinator", "Manager", "Analyst", "Writer", "Specialist", "Consultant", "Director", "Researcher"],
        "skills_keywords": ["non-profit", "grant", "fundraising", "program", "community", "policy", "public", "administration", "outreach"],
        "service_keywords": ["non-profit", "community", "public", "grant", "fundraising", "program", "policy"],
        "description_keywords": ["non-profit", "community", "public", "program", "grant", "fundraising", "policy", "social"]
    },
    
    # Real Estate & Construction
    "Real Estate": {
        "company_keywords": ["real estate", "property", "construction", "building", "development", "architectural", "infrastructure", "home", "commercial", "residential"],
        "job_titles": ["Agent", "Manager", "Analyst", "Designer", "Engineer", "Estimator", "Coordinator", "Consultant", "Planner"],
        "skills_keywords": ["real estate", "property", "construction", "autocad", "revit", "building", "codes", "estimation", "contract", "architectural"],
        "service_keywords": ["real estate", "property", "construction", "development", "architectural", "building", "commercial", "residential"],
        "description_keywords": ["real estate", "property", "construction", "building", "development", "architectural", "commercial", "residential", "infrastructure"]
    },
    
    # Retail & E-commerce
    "Retail": {
        "company_keywords": ["retail", "shop", "store", "market", "commerce", "e-commerce", "merchandise", "consumer", "product", "boutique", "shopping"],
        "job_titles": ["Manager", "Specialist", "Analyst", "Coordinator", "Buyer", "Merchandiser", "Planner", "Consultant"],
        "skills_keywords": ["retail", "e-commerce", "inventory", "merchandising", "customer", "pos", "supply", "sales", "crm", "shopping"],
        "service_keywords": ["retail", "e-commerce", "shopping", "merchandising", "inventory", "customer", "store", "marketplace"],
        "description_keywords": ["retail", "e-commerce", "store", "product", "shopping", "customer", "inventory", "merchandise", "sales"]
    },
    
    # Transportation & Logistics
    "Transportation": {
        "company_keywords": ["transportation", "logistics", "shipping", "freight", "supply", "chain", "fleet", "distribution", "delivery", "warehouse"],
        "job_titles": ["Manager", "Analyst", "Coordinator", "Specialist", "Consultant", "Planner", "Engineer"],
        "skills_keywords": ["logistics", "transportation", "supply", "chain", "fleet", "warehouse", "inventory", "import", "export", "distribution"],
        "service_keywords": ["logistics", "transportation", "shipping", "supply", "chain", "fleet", "distribution", "warehouse"],
        "description_keywords": ["logistics", "transportation", "shipping", "supply chain", "distribution", "warehouse", "fleet", "delivery", "inventory"]
    },
    
    # Agriculture & Food
    "Agriculture": {
        "company_keywords": ["agriculture", "food", "farm", "organic", "sustainable", "harvest", "produce", "agricultural", "farming", "crop"],
        "job_titles": ["Scientist", "Manager", "Specialist", "Analyst", "Developer", "Coordinator", "Consultant", "Researcher"],
        "skills_keywords": ["agriculture", "food", "sustainable", "farming", "crop", "livestock", "safety", "processing", "soil", "agricultural"],
        "service_keywords": ["agriculture", "food", "farming", "sustainable", "organic", "produce", "crop", "livestock"],
        "description_keywords": ["agriculture", "farming", "food", "sustainable", "organic", "crop", "livestock", "harvest", "produce"]
    },
    
    # Construction
    "Construction": {
        "company_keywords": ["construction", "building", "development", "architectural", "infrastructure", "home", "commercial", "residential"],
        "job_titles": ["Manager", "Engineer", "Supervisor", "Estimator", "Coordinator", "Consultant", "Planner", "Architect"],
        "skills_keywords": ["construction", "building", "autocad", "revit", "codes", "estimation", "contract", "architectural", "safety"],
        "service_keywords": ["construction", "building", "development", "architectural", "infrastructure", "commercial", "residential"],
        "description_keywords": ["construction", "building", "development", "architectural", "infrastructure", "commercial", "residential", "project"]
    },
    
    # Telecommunications
    "Telecommunications": {
        "company_keywords": ["telecom", "communications", "wireless", "fiber", "optic", "satellite", "network", "mobile", "voice", "data", "internet"],
        "job_titles": ["Engineer", "Manager", "Analyst", "Specialist", "Consultant", "Coordinator", "Technician"],
        "skills_keywords": ["telecommunications", "network", "wireless", "fiber", "voip", "satellite", "mobile", "security", "administration"],
        "service_keywords": ["telecommunications", "wireless", "network", "fiber", "voip", "satellite", "internet", "mobile"],
        "description_keywords": ["telecommunications", "network", "wireless", "fiber", "internet", "mobile", "satellite", "voice", "data"]
    }
}