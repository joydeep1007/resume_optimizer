from typing import Dict, List, Any

def analyze_resume(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze resume data and provide optimization suggestions."""
    suggestions = {
        "score": 0,
        "improvements": [],
        "strengths": [],
        "missing_elements": []
    }
    
    # Check contact information
    analyze_contact_info(resume_data.get("contact", {}), suggestions)
    
    # Analyze education section
    analyze_education(resume_data.get("education", []), suggestions)
    
    # Analyze work experience
    analyze_experience(resume_data.get("experience", []), suggestions)
    
    # Calculate overall score
    calculate_score(suggestions)
    
    return suggestions

def analyze_contact_info(contact: Dict[str, str], suggestions: Dict[str, Any]) -> None:
    required_fields = ["email", "phone", "linkedin"]
    missing = [field for field in required_fields if not contact.get(field)]
    
    if missing:
        suggestions["missing_elements"].extend([f"Missing {field}" for field in missing])
    else:
        suggestions["strengths"].append("Complete contact information provided")

def analyze_education(education: List[Dict[str, str]], suggestions: Dict[str, Any]) -> None:
    if not education:
        suggestions["missing_elements"].append("No education history provided")
        return
    
    for edu in education:
        if not edu.get("degree"):
            suggestions["improvements"].append("Add degree specifications")
        if not edu.get("year"):
            suggestions["improvements"].append("Add graduation years")
        if edu.get("gpa") and float(edu.get("gpa", 0)) > 3.5:
            suggestions["strengths"].append(f"Strong academic performance (GPA: {edu['gpa']})")

def analyze_experience(experience: List[Dict[str, str]], suggestions: Dict[str, Any]) -> None:
    if not experience:
        suggestions["missing_elements"].append("No work experience provided")
        return
    
    for exp in experience:
        responsibilities = exp.get("responsibilities", [])
        
        if len(responsibilities) < 3:
            suggestions["improvements"].append(f"Add more details about your role at {exp.get('company', 'company')}")
        
        # Check for action verbs
        action_verbs = ["developed", "implemented", "managed", "led", "created", "designed", "improved"]
        has_action_verbs = any(verb in ' '.join(responsibilities).lower() for verb in action_verbs)
        
        if not has_action_verbs:
            suggestions["improvements"].append("Use more action verbs in experience descriptions")
        
        # Check for metrics and achievements
        has_metrics = any(any(char.isdigit() for char in resp) for resp in responsibilities)
        if not has_metrics:
            suggestions["improvements"].append("Add quantifiable achievements and metrics")

def calculate_score(suggestions: Dict[str, Any]) -> None:
    """Calculate overall resume score based on various factors."""
    base_score = 100
    deductions = len(suggestions["improvements"]) * 5 + len(suggestions["missing_elements"]) * 10
    additions = len(suggestions["strengths"]) * 5
    
    final_score = max(0, min(100, base_score - deductions + additions))
    suggestions["score"] = final_score