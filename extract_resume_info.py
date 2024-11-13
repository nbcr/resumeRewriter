from docx import Document
import re

def extract_info_from_resume(file_path):
    doc = Document(file_path)
    info = {
        'name': None,
        'email': None,
        'phone': None,
        'address': None,
        'skills': [],
        'experience': [],
    }
    
    # Define regex patterns for email and phone number
    email_pattern = r'\S+@\S+\.\S+'
    phone_pattern = r'(\(?\d{3}\)?\s?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Flags to track section parsing
    in_skills_section = False
    in_experience_section = False

    # Extract text from each paragraph
    for para in doc.paragraphs:
        text = para.text.strip()

        # Extract Name (Assuming the name is the first non-empty paragraph)
        if info['name'] is None and text:
            info['name'] = text
            continue

        # Extract email
        if info['email'] is None:
            email_match = re.search(email_pattern, text)
            if email_match:
                info['email'] = email_match.group()

        # Extract phone number
        if info['phone'] is None:
            phone_match = re.search(phone_pattern, text)
            if phone_match:
                info['phone'] = phone_match.group()

        # Check for Skills section
        if 'Abilities:' in text:
            in_skills_section = True
            in_experience_section = False
            continue  # Move to the next paragraph to get skills

        # Check for Experience section
        if 'Experience:' in text:
            in_experience_section = True
            in_skills_section = False
            continue  # Move to the next paragraph to get experience

        # Collect skills
        if in_skills_section and text:
            if text.startswith("Experience:"):  # End of Skills section
                in_skills_section = False
            else:
                info['skills'].append(text)

        # Collect experience entries
        if in_experience_section and text:
            if any(keyword in text for keyword in ["Objective", "Hobbies"]):  # End of Experience section
                in_experience_section = False
            else:
                info['experience'].append(text)

    return info

# Test the function with your master resume file path
if __name__ == "__main__":
    file_path = 'C:/Users/Yot/Downloads/Work/Master Resume.docx'  # Update with the actual path to your master resume if running locally
    extracted_info = extract_info_from_resume(file_path)
    
    # Display the extracted information
    print("Name:", extracted_info['name'])
    print("Email:", extracted_info['email'])
    print("Phone:", extracted_info['phone'])
    print("Skills:", ", ".join(extracted_info['skills']))
    print("Experience:", "\n".join(extracted_info['experience']))
