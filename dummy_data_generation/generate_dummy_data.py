from pathlib import Path
import csv
import random
from datetime import datetime, timedelta
import os
import sys
import django

from generate_dummy_data_choices import FIRST_NAMES, LAST_NAMES, COMPANY_NAMES, EXPERIENCE_LEVELS, JOB_TITLES, SKILLS, DESCRIPTIONS, SERVICES, MESSAGES
from industry_mappings import INDUSTRY_CATEGORIES  # Import from separate file

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Setup paths for importing listings/choices.py
project_root = Path(__file__).parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from listings.choices import industry_choices, budget_choices, duration_choices

from django.contrib.auth.hashers import make_password

# Import CV generation function
from generate_pdf import generate_cv_pdf

# Configuration
Multipler = 30
NUM_COMPANY_USERS = 1 * Multipler  # Company users (1:1 with companies)
NUM_INDIVIDUAL_USERS = 10 * Multipler  # Individual users (job seekers)
NUM_COMPANIES = NUM_COMPANY_USERS  # Same as company users
NUM_LISTINGS = 4 * Multipler
NUM_APPLIES = 60 * Multipler

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

def categorize_industry(industry_name):
    """Categorize an industry into one of the predefined categories"""
    # Direct mapping since we're using the same industry names
    return industry_name

def filter_by_industry(items, industry, item_type="company"):
    """Filter items by industry category"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    if item_type == "company":
        keywords = category_data.get("company_keywords", [])
    elif item_type == "job_title":
        keywords = category_data.get("job_titles", [])
    elif item_type == "skill":
        keywords = category_data.get("skills_keywords", [])
    elif item_type == "service":
        keywords = category_data.get("service_keywords", [])
    elif item_type == "description":
        keywords = category_data.get("description_keywords", [])
    else:
        keywords = []
    
    # If no keywords, return random items
    if not keywords:
        return random.sample(items, min(len(items), 5))
    
    # Filter items that contain any of the keywords
    filtered_items = []
    for item in items:
        item_lower = str(item).lower()
        for keyword in keywords:
            if keyword in item_lower:
                filtered_items.append(item)
                break
    
    # If no items match, return some random items
    if not filtered_items:
        return random.sample(items, min(len(items), 5))
    
    return filtered_items

def get_industry_specific_job_title(industry):
    """Get a job title specific to the industry"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    # Get job title keywords for this industry
    job_title_keywords = category_data.get("job_titles", [])
    
    if job_title_keywords:
        # Filter job titles that contain these keywords
        filtered_titles = []
        for title in JOB_TITLES:
            title_lower = title.lower()
            for keyword in job_title_keywords:
                if keyword.lower() in title_lower:
                    filtered_titles.append(title)
                    break
        
        if filtered_titles:
            return random.choice(filtered_titles)
    
    # Fallback: return a random job title
    return random.choice(JOB_TITLES)

def get_industry_specific_company_name(industry):
    """Get a company name specific to the industry"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    # Get company name keywords for this industry
    company_keywords = category_data.get("company_keywords", [])
    
    if company_keywords:
        # Filter company names that contain these keywords
        filtered_companies = []
        for company in COMPANY_NAMES:
            company_lower = company.lower()
            for keyword in company_keywords:
                if keyword in company_lower:
                    filtered_companies.append(company)
                    break
        
        if filtered_companies:
            return random.choice(filtered_companies)
    
    # Fallback: return a random company name
    return random.choice(COMPANY_NAMES)

def get_industry_specific_skills(industry, num_skills=5):
    """Get skills specific to the industry"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    # Get skill keywords for this industry
    skill_keywords = category_data.get("skills_keywords", [])
    
    if skill_keywords:
        # Filter skills that contain these keywords
        filtered_skills = []
        for skill in SKILLS:
            skill_lower = skill.lower()
            for keyword in skill_keywords:
                if keyword in skill_lower:
                    filtered_skills.append(skill)
                    break
        
        if filtered_skills:
            # Take a sample, but ensure we don't request more than available
            sample_size = min(num_skills, len(filtered_skills))
            if sample_size > 0:
                return random.sample(filtered_skills, sample_size)
    
    # Fallback: return random skills
    return random.sample(SKILLS, min(num_skills, len(SKILLS)))

def get_industry_specific_services(industry):
    """Get services specific to the industry"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    # Get service keywords for this industry
    service_keywords = category_data.get("service_keywords", [])
    
    if service_keywords:
        # Filter services that contain these keywords
        filtered_services = []
        for service in SERVICES:
            service_lower = service.lower()
            for keyword in service_keywords:
                if keyword in service_lower:
                    filtered_services.append(service)
                    break
        
        if filtered_services:
            return random.choice(filtered_services)
    
    # Fallback: return a random service
    return random.choice(SERVICES)

def get_industry_specific_description(industry, job_title=""):
    """Get a description specific to the industry and optionally job title"""
    category = categorize_industry(industry)
    category_data = INDUSTRY_CATEGORIES.get(category, {})
    
    # Get description keywords for this industry
    description_keywords = category_data.get("description_keywords", [])
    
    if description_keywords:
        # Filter descriptions that contain these keywords
        filtered_descriptions = []
        for desc in DESCRIPTIONS:
            desc_lower = desc.lower()
            for keyword in description_keywords:
                if keyword in desc_lower:
                    filtered_descriptions.append(desc)
                    break
        
        if filtered_descriptions:
            return random.choice(filtered_descriptions)
    
    # Fallback: return a random description
    return random.choice(DESCRIPTIONS)

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

def generate_datetime(start_date, end_date):
    """Generate a random datetime between start and end with randomized time"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    
    random_date = start_date + timedelta(days=random_days)
    return datetime(
        random_date.year,
        random_date.month,
        random_date.day,
        random_hours,
        random_minutes,
        random_seconds
    )

def generate_message():
    """Generate application message"""
    return random.choice(MESSAGES)

def generate_auth_user_data():
    """Generate auth_user data with properly hashed passwords"""
    data = []
    
    # Store generated user data for later reference
    company_users = []
    individual_users = []
    
    # Generate company users
    for i in range(NUM_COMPANY_USERS):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"company_user_{i+1}"
        email = generate_email(first_name, last_name, company=True)
        
        # Hash password using Django's make_password
        hashed_password = make_password(PASSWORD["company"])
        
        user = {
            "id": i + 1,  # User ID starting from 1
            "password": hashed_password,
            "last_login": generate_datetime(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            "is_superuser": "false",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": "false",
            "is_active": "true",
            "date_joined": generate_datetime(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(user)
        company_users.append(user)
    
    # Generate individual users
    for i in range(NUM_INDIVIDUAL_USERS):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"user_{i+1}"
        email = generate_email(first_name, last_name)
        
        # Hash password using Django's make_password
        hashed_password = make_password(PASSWORD['user'])
        
        user = {
            "id": NUM_COMPANY_USERS + i + 1,  # Continue IDs after company users
            "password": hashed_password, 
            "last_login": generate_datetime(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            "is_superuser": "false",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": "false",
            "is_active": "true",
            "date_joined": generate_datetime(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(user)
        individual_users.append(user)
    
    return data, company_users, individual_users

def hsl_to_hex(h, s, l):
    """Convert HSL to HEX color"""
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}".upper()  

def download_logo_from_placehold(company_name, company_id, create_date):
    """Download and save logo from placehold.co based on company name"""
    import urllib.request
    import urllib.error
    
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
    
    # Generate the URL for placehold.co
    logo_url = f"https://placehold.co/150x150/{bg_hex}/{text_hex}/png?text={initials}"
    
    # Parse the create_date to get year and month
    try:
        # create_date is a string in format "YYYY-MM-DD HH:MM:SS"
        create_datetime = datetime.strptime(create_date, "%Y-%m-%d %H:%M:%S")
        logo_year = create_datetime.year
        logo_month = create_datetime.month
        logo_day = create_datetime.day
    except (ValueError, TypeError):
        # Fallback to current date if parsing fails
        logo_year = 2024
        logo_month = 1
        logo_day = 1
    
    # Create logo filename
    logo_filename = f"logo_{company_name.lower().replace(' ', '_')}_{company_id}.png"
    logo_relative_path = f"photos/{logo_year}/{logo_month:02d}/{logo_day:02d}/{logo_filename}"
    # Save to project root photos directory instead of dummy_data_generation subdirectory
    project_root = Path(__file__).parent.parent
    logo_full_path = project_root / logo_relative_path
    
    # Ensure directory exists
    logo_dir = os.path.dirname(logo_full_path)
    os.makedirs(logo_dir, exist_ok=True)
    
    # Download and save the logo
    try:
        urllib.request.urlretrieve(logo_url, logo_full_path)
        print(f"  Downloaded logo for {company_name}: {logo_relative_path}")
        return logo_relative_path
    except urllib.error.URLError as e:
        print(f"Error downloading logo for {company_name}: {e}")
        # Fallback to placeholder path
        return f"photos/{logo_year}/{logo_month:02d}/{logo_day:02d}/logo_{company_id}.png"
    except Exception as e:
        print(f"Error saving logo for {company_name}: {e}")
        # Fallback to placeholder path
        return f"photos/{logo_year}/{logo_month:02d}/{logo_day:02d}/logo_{company_id}.png"

def generate_logo_from_name(company_name, company_id, create_date):
    """Generate logo with colors based on company name - downloads and saves locally"""
    return download_logo_from_placehold(company_name, company_id, create_date)

def generate_company_data(company_users):
    """Generate company data with downloaded logos - uses matching user data and aligns company name with industry"""
    data = []
    
    print("Generating company logos...")
    
    for i, user in enumerate(company_users):
        user_id = user["id"]
        
        # First choose an industry
        industry = random.choice(INDUSTRIES)
        
        # Get a company name that aligns with the industry
        company_name = get_industry_specific_company_name(industry)
        
        # Use the email from the corresponding user
        email = user["email"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        
        # Generate create date for the company (use user's date_joined)
        create_date_str = user["date_joined"]
        
        # Generate and download logo
        logo_path = generate_logo_from_name(company_name, user_id, create_date_str)
        
        # Get industry-specific services
        services = get_industry_specific_services(industry)
        
        # Get industry-specific description
        description = get_industry_specific_description(industry)
        
        company = {
            "name": company_name,
            "logo": logo_path,
            "industry": industry,
            "serivces": services,
            "description": description,
            "phone": generate_phone(),
            "email": email,  # Use the same email as the user
            "create_date": create_date_str,
            "user_id": user_id
        }
        data.append(company)
        
        # Show progress for logos
        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1} logos...")
    
    print(f"Completed generating {NUM_COMPANIES} company logos")
    return data

def generate_listing_data(company_data):
    """Generate listing data that aligns with company industry"""
    data = []
    
    for i in range(NUM_LISTINGS):
        # Pick a company and get its industry
        company = random.choice(company_data)
        company_id = company_data.index(company) + 1
        company_industry = company["industry"]
        
        # Generate random publish datetime with randomized time
        publish_datetime = generate_datetime(datetime(2023, 1, 1), datetime(2024, 12, 31))
        
        # Ensure is_active is boolean
        is_active = "1" if random.random() > 0.2 else "0"  # 80% active
        
        # Get industry-specific job title
        job_title = get_industry_specific_job_title(company_industry)
        
        # Add experience level to job title
        experience_level = random.choice(EXPERIENCE_LEVELS)
        full_job_title = f"{experience_level} {job_title}"
        
        # Get industry-specific skills
        skills = get_industry_specific_skills(company_industry, random.randint(3, 6))
        
        # Get industry-specific description
        description = get_industry_specific_description(company_industry, job_title)
        
        listing = {
            "company_id": company_id,
            "title": full_job_title,
            "industry": company_industry,  # Same as company industry
            "budget": random.choice(BUDGET_RANGES),
            "duration": random.choice(DURATIONS),
            "description": description,
            "requirement": ", ".join(skills),
            "publish_date": publish_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "is_active": is_active
        }
        data.append(listing)
    
    return data

def generate_apply_data(individual_users, listing_data):
    """Generate apply data with actual PDF CVs - uses matching user data"""
    data = []
    
    print("Generating CV PDFs for applicants...")
    
    # Create a copy of individual users to track which ones have applied
    available_users = individual_users.copy()
    applied_users = []
    
    for i in range(NUM_APPLIES):
        # Pick a listing
        listing = random.choice(listing_data)
        listing_id = listing_data.index(listing) + 1
        
        # Get listing industry for CV alignment
        listing_industry = listing["industry"]
        listing_job_title = listing["title"]
        
        # Get listing to ensure apply date is after publish date
        publish_datetime = datetime.strptime(listing["publish_date"], "%Y-%m-%d %H:%M:%S")
        
        # Select a user - prioritize users who haven't applied yet
        if available_users and random.random() > 0.3:  # 70% chance to use new user
            user = random.choice(available_users)
            available_users.remove(user)
            applied_users.append(user)
        else:
            # Use a user who already applied (reuse)
            user = random.choice(applied_users if applied_users else individual_users)
        
        user_id = user["id"]
        
        # Use the name and email from the user
        first_name = user["first_name"]
        last_name = user["last_name"]
        full_name = f"{first_name} {last_name}"
        email = user["email"]
        
        # Generate apply datetime after listing publish date (with randomized time)
        max_apply_date = min(datetime(2024, 12, 31, 23, 59, 59), publish_datetime + timedelta(days=180))
        apply_datetime = generate_datetime(publish_datetime, max_apply_date)
        
        # Generate CV path based on apply date (matching Django's upload_to pattern)
        cv_year = apply_datetime.year
        cv_month = apply_datetime.month
        cv_day = apply_datetime.day
        
        # Create CV filename with applicant name and ID
        cv_filename = f"cv_{full_name.lower().replace(' ', '_')}_{user_id}.pdf"
        cv_relative_path = f"cv/{cv_year}/{cv_month:02d}/{cv_day:02d}/{cv_filename}"
        # Save to project root cv directory instead of dummy_data_generation subdirectory
        project_root = Path(__file__).parent.parent
        cv_full_path = project_root / cv_relative_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(cv_full_path), exist_ok=True)
        
        # Get industry-specific skills for the CV
        cv_skills = get_industry_specific_skills(listing_industry, random.randint(5, 10))
        
        # Generate applicant information for CV
        experience_level = random.choice(EXPERIENCE_LEVELS)
        message = generate_message()
        description = get_industry_specific_description(listing_industry, listing_job_title)
        
        # Create applicant info dictionary for CV generation
        applicant_info = {
            'name': full_name,
            'email': email,  # Use the same email as the user
            'phone': generate_phone(),
            'skills': ", ".join(cv_skills),
            'experience_level': experience_level,
            'job_title': listing_job_title,  # Use the listing job title
            'description': description,
            'message': message
        }
        
        # Generate actual PDF CV
        try:
            generate_cv_pdf(applicant_info, cv_full_path)
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1} CVs...")
        except Exception as e:
            print(f"Error generating CV for applicant {i+1}: {e}")
            # Fallback to placeholder path if CV generation fails
            cv_relative_path = f"cv/{cv_year}/{cv_month:02d}/{cv_day:02d}/cv_{user_id}.pdf"
            # Also update the full path for the fallback
            cv_full_path = project_root / cv_relative_path
        
        apply_record = {
            "listing_id": listing_id,
            "name": full_name,  # Use the same name as the user
            "email": email,  # Use the same email as the user
            "phone": generate_phone(),
            "message": message,
            "cv": cv_relative_path,
            "apply_date": apply_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id
        }
        data.append(apply_record)
    
    print(f"Completed generating {NUM_APPLIES} CV PDFs")
    return data

def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    # Go one level up to project root, then create dummy_data directory
    project_root = script_dir.parent
    dummy_dir = project_root / 'dummy_data'
    
    # Create directory
    dummy_dir.mkdir(exist_ok=True)
    
    # Create full filepath
    filepath = dummy_dir / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} records in {filepath}")

def main():
    print("Generating dummy data for Django project...")
    print("Aligning data by industry: company names, job titles, skills, descriptions, and services...")
    print("Randomizing datetime with hours, minutes, and seconds...")
    
    # Generate and save auth_user data
    auth_user_fields = [
        "id", "password", "last_login", "is_superuser", "username", "first_name",
        "last_name", "email", "is_staff", "is_active", "date_joined"
    ]
    
    # Generate auth_user data and get user lists
    auth_user_data, company_users, individual_users = generate_auth_user_data()
    write_csv('auth_user.csv', auth_user_data, auth_user_fields)
    
    # Generate and save company data (using company users' emails and aligning with industry)
    company_fields = [
        "name", "logo", "industry", "serivces", "description", 
        "phone", "email", "create_date", "user_id"
    ]
    company_data = generate_company_data(company_users)
    write_csv('companies_company.csv', company_data, company_fields)
    
    # Generate and save listing data (aligning with company industry)
    listing_fields = [
        "company_id", "title", "industry", "budget", "duration",
        "description", "requirement", "publish_date", "is_active"
    ]
    listing_data = generate_listing_data(company_data)
    write_csv('listings_listing.csv', listing_data, listing_fields)
    
    # Generate and save apply data (using individual users' names and emails)
    apply_fields = [
        "name", "email", "phone", "message",
        "cv", "apply_date", "listing_id", "user_id"
    ]
    apply_data = generate_apply_data(individual_users, listing_data)
    write_csv('applies_apply.csv', apply_data, apply_fields)
    
    print("\n" + "="*50)
    print("DATA GENERATION COMPLETE!")
    print("="*50)
    print(f"Total auth_user records: {NUM_COMPANY_USERS + NUM_INDIVIDUAL_USERS}")
    print(f"Total company records: {NUM_COMPANIES}")
    print(f"Total listing records: {NUM_LISTINGS}")
    print(f"Total apply records: {NUM_APPLIES}")
    print("\nData alignment ensured:")
    print("1. Company names align with their industry")
    print("2. Job titles align with listing industry")
    print("3. Skills align with industry requirements")
    print("4. Descriptions align with industry context")
    print("5. Services align with company industry")
    print("6. Company emails match their user emails")
    print("7. Apply emails and names match individual user emails and names")
    print("8. Datetimes include randomized hours, minutes, and seconds")
    print("\nFiles saved in 'dummy_data/' directory:")
    print("1. auth_user.csv")
    print("2. companies_company.csv")
    print("3. listings_listing.csv")
    print("4. applies_apply.csv")
    print("\n" + "="*50)
    print("IMPORTANT: Files have been generated in the following directories:")
    print("1. CV PDFs in 'cv/' directory:")
    print("     cv/YYYY/MM/DD/cv_firstname_lastname_id.pdf")
    print("2. Company logos in 'photos/' directory:")
    print("     photos/YYYY/MM/DD/logo_company_name_id.png")
    print("\nThe file paths in the CSV files reference these generated files.")
    print("="*50)
    print("\nIMPORT INSTRUCTIONS:")
    print("1. Make sure Django project is set up and migrations are applied")
    print("2. Use Django's loaddata command or write a script to import CSV")
    print("3. Note: Passwords are already hashed using Django's make_password")
    print("   Company users: company123, Individual users: user123")
    print("4. The CV and logo files are already generated and placed in the")
    print("   correct directory structure for Django's FileField upload_to pattern")
    print("5. Data consistency: Company emails match user emails, Apply emails/names match user data")
    print("6. Industry alignment: All data is aligned by industry category")
    print("="*50)

if __name__ == "__main__":
    main()