import PyPDF2
from docx import Document
import re
import os
import logging
from typing import Dict, List, Any

def parse_resume(file_path: str) -> Dict[str, Any]:
    """Parse resume file and extract information."""
    file_ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if file_ext == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        elif file_ext in ['.docx', '.doc']:
            doc = Document(file_path)
            text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
        
        return {
            "name": extract_name(text),
            "contact": extract_contact_details(text),
            "education": extract_education(text),
            "experience": extract_experience(text)
        }
    except Exception as e:
        logging.error(f"Error parsing resume: {str(e)}")
        return {"error": str(e)}

def extract_name(text: str) -> str:
    """Extract name from resume text."""
    # Look for name at the beginning of the resume
    lines = text.split('\n')
    for line in lines[:3]:  # Check first 3 lines
        # Remove special characters and extra spaces
        clean_line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        # Look for 2-3 word combinations that could be names
        if len(clean_line.split()) in [2, 3] and all(word.istitle() for word in clean_line.split()):
            return clean_line
    return ""

def extract_contact_details(text: str) -> Dict[str, str]:
    """Extract contact information using regex patterns."""
    contact = {
        "email": "",
        "phone": "",
        "linkedin": "",
        "location": ""
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact["email"] = email_match.group()
    
    # Phone pattern (various formats)
    phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact["phone"] = phone_match.group()
    
    # LinkedIn URL pattern
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group()
    
    return contact

def extract_education(text: str) -> List[Dict[str, str]]:
    """Extract education information."""
    education_list = []
    
    # Common education keywords
    edu_keywords = r'education|university|college|school|bachelor|master|phd|b\.?tech|m\.?tech|b\.?e|m\.?e'
    
    # Find education section
    edu_section = ""
    sections = re.split(r'\n\s*\n', text)
    for section in sections:
        if re.search(edu_keywords, section.lower()):
            edu_section = section
            break
    
    if edu_section:
        # Extract individual education entries
        entries = re.split(r'\n(?=[A-Z])', edu_section)
        for entry in entries:
            if len(entry.strip()) > 0:
                edu_info = {
                    "degree": "",
                    "institution": "",
                    "year": "",
                    "gpa": ""
                }
                
                # Extract degree
                degree_pattern = r'(B\.?Tech|M\.?Tech|PhD|Bachelor|Master|B\.?E|M\.?E|B\.?S|M\.?S)[^\n]*'
                degree_match = re.search(degree_pattern, entry, re.IGNORECASE)
                if degree_match:
                    edu_info["degree"] = degree_match.group().strip()
                
                # Extract year
                year_pattern = r'20\d{2}|19\d{2}'
                year_match = re.search(year_pattern, entry)
                if year_match:
                    edu_info["year"] = year_match.group()
                
                # Extract GPA
                gpa_pattern = r'(?:GPA|CGPA):\s*(\d+\.\d+)'
                gpa_match = re.search(gpa_pattern, entry)
                if gpa_match:
                    edu_info["gpa"] = gpa_match.group(1)
                
                education_list.append(edu_info)
    
    return education_list

def extract_experience(text: str) -> List[Dict[str, str]]:
    """Extract work experience information."""
    experience_list = []
    
    # Find experience section
    exp_keywords = r'experience|work|employment|career'
    exp_section = ""
    sections = re.split(r'\n\s*\n', text)
    for section in sections:
        if re.search(exp_keywords, section.lower()):
            exp_section = section
            break
    
    if exp_section:
        # Split into individual roles
        entries = re.split(r'\n(?=[A-Z])', exp_section)
        for entry in entries:
            if len(entry.strip()) > 0:
                exp_info = {
                    "company": "",
                    "title": "",
                    "duration": "",
                    "responsibilities": []
                }
                
                # Extract company and title
                lines = entry.split('\n')
                for line in lines[:2]:  # Usually in first two lines
                    if not exp_info["company"]:
                        company_match = re.search(r'^[A-Z][A-Za-z\s&]+', line)
                        if company_match:
                            exp_info["company"] = company_match.group().strip()
                    elif not exp_info["title"]:
                        exp_info["title"] = line.strip()
                
                # Extract duration
                duration_pattern = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-]+\d{4}(?:\s*(?:-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-]+\d{4}))?'
                duration_match = re.search(duration_pattern, entry, re.IGNORECASE)
                if duration_match:
                    exp_info["duration"] = duration_match.group()
                
                # Extract responsibilities
                resp_lines = [line.strip() for line in lines[2:] if line.strip()]
                exp_info["responsibilities"] = [line for line in resp_lines if len(line) > 10]
                
                if exp_info["company"] or exp_info["title"]:
                    experience_list.append(exp_info)
    
    return experience_list