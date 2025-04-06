from typing import Dict, Any, Union
import json
import os
from datetime import datetime

def format_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format and clean resume data."""
    if not data:
        return {}
    
    formatted_data = {}
    
    # Format contact information
    if "contact" in data:
        formatted_data["contact"] = {
            k: v.strip().lower() if k == "email" else v.strip()
            for k, v in data["contact"].items() if v
        }
    
    # Format education entries
    if "education" in data:
        formatted_data["education"] = [
            {k: v.strip() for k, v in edu.items() if v}
            for edu in data["education"]
        ]
    
    # Format experience entries
    if "experience" in data:
        formatted_data["experience"] = [
            {
                "company": exp.get("company", "").strip(),
                "title": exp.get("title", "").strip(),
                "duration": exp.get("duration", "").strip(),
                "responsibilities": [r.strip() for r in exp.get("responsibilities", []) if r.strip()]
            }
            for exp in data["experience"]
        ]
    
    return formatted_data

def validate_resume_data(data: Dict[str, Any]) -> bool:
    """Validate resume data structure and content."""
    if not isinstance(data, dict):
        raise ValueError("Resume data must be a dictionary")
    
    # Check required sections
    required_sections = ["contact", "education", "experience"]
    missing_sections = [section for section in required_sections if section not in data]
    if missing_sections:
        raise ValueError(f"Missing required sections: {', '.join(missing_sections)}")
    
    # Validate contact information
    contact = data.get("contact", {})
    required_contact_fields = ["email", "phone"]
    missing_fields = [field for field in required_contact_fields if not contact.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required contact fields: {', '.join(missing_fields)}")
    
    return True

def save_analysis_results(data: Dict[str, Any], filename: str = None) -> str:
    """Save analysis results with timestamp."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_results_{timestamp}.json"
    
    output_dir = os.path.join("uploads", "analysis_results")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)
    
    return filepath

def format_analysis_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Format analysis results for display."""
    formatted = {
        "score": results.get("score", 0),
        "summary": {
            "strengths": len(results.get("strengths", [])),
            "improvements_needed": len(results.get("improvements", [])),
            "missing_elements": len(results.get("missing_elements", []))
        },
        "details": {
            "strengths": results.get("strengths", []),
            "improvements": results.get("improvements", []),
            "missing_elements": results.get("missing_elements", [])
        }
    }
    
    return formatted