from fpdf import FPDF
import os
from datetime import datetime

class CVGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Logo or header content
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'Curriculum Vitae', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'C')
        
    def add_personal_info(self, name, email, phone, skills, experience_level):
        """Add personal information section"""
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, name, 0, 1, 'L')
        
        self.set_font('helvetica', '', 10)
        self.cell(0, 5, f'Email: {email}', 0, 1, 'L')
        self.cell(0, 5, f'Phone: {phone}', 0, 1, 'L')
        self.cell(0, 5, f'Experience Level: {experience_level}', 0, 1, 'L')
        self.ln(5)
        
    def add_skills_section(self, skills):
        """Add skills section"""
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Skills', 0, 1, 'L')
        self.set_font('helvetica', '', 10)
        
        # Split skills into chunks for better formatting
        skills_list = skills.split(', ')
        chunk_size = 3
        for i in range(0, len(skills_list), chunk_size):
            chunk = skills_list[i:i + chunk_size]
            # Use a simple dash instead of bullet to avoid encoding issues
            skills_text = ' - '.join(chunk)
            self.cell(0, 5, skills_text, 0, 1, 'L')
        self.ln(5)
        
    def add_experience_section(self, job_title, description):
        """Add experience section"""
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Professional Experience', 0, 1, 'L')
        
        self.set_font('helvetica', 'B', 10)
        self.cell(0, 5, job_title, 0, 1, 'L')
        
        self.set_font('helvetica', '', 10)
        # Wrap text for description
        self.multi_cell(0, 5, description)
        self.ln(5)
        
    def add_summary_section(self, message):
        """Add summary/objective section"""
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Professional Summary', 0, 1, 'L')
        
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, message)
        self.ln(5)

def generate_cv_pdf(applicant_info, output_path):
    """
    Generate a CV PDF for an applicant
    
    Args:
        applicant_info (dict): Dictionary containing applicant information
            Required keys: name, email, phone, skills, experience_level, 
                          job_title, description, message
        output_path (str): Path where to save the PDF file
    """
    # Create CV generator
    pdf = CVGenerator()
    pdf.add_page()
    
    # Add personal information
    pdf.add_personal_info(
        name=applicant_info.get('name', ''),
        email=applicant_info.get('email', ''),
        phone=applicant_info.get('phone', ''),
        skills=applicant_info.get('skills', ''),
        experience_level=applicant_info.get('experience_level', '')
    )
    
    # Add skills section
    pdf.add_skills_section(applicant_info.get('skills', ''))
    
    # Add experience section
    pdf.add_experience_section(
        job_title=applicant_info.get('job_title', ''),
        description=applicant_info.get('description', '')
    )
    
    # Add summary section
    pdf.add_summary_section(applicant_info.get('message', ''))
    
    # Ensure directory exists (only if output_path has a directory component)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Save PDF
    pdf.output(output_path)
    return output_path

def generate_simple_pdf(text, filename, font="helvetica", size=12):
    """Simple PDF generation function (backward compatible)"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(font, size=size)
    pdf.cell(text=text)
    
    # Ensure directory exists
    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    pdf.output(filename)
    return filename

if __name__ == "__main__":
    # Test the CV generator
    test_applicant = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '123-456-7890',
        'skills': 'Python, Django, React, PostgreSQL, AWS',
        'experience_level': 'Senior',
        'job_title': 'Senior Full Stack Developer',
        'description': 'Experienced full-stack developer with 8+ years in web application development. Specialized in Python/Django backend and React frontend.',
        'message': 'Looking for challenging opportunities to apply my skills in building scalable web applications.'
    }
    
    generate_cv_pdf(test_applicant, 'test_cv.pdf')
    print("Test CV generated as 'test_cv.pdf'")
