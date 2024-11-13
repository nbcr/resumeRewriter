from fpdf import FPDF
from file_utils import sanitize_filename
from datetime import datetime

def save_cover_letter_as_pdf(cover_letter_content, job, contact_info, company_details):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add the header with contact info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"{contact_info['name']}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"{contact_info['email']} | {contact_info['phone']}", ln=True)
    pdf.cell(0, 10, "North Bay, Ontario", ln=True)
    pdf.cell(0, 10, "", ln=True)  # Blank line
    
    # Company details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, job['company'], ln=True)
    pdf.cell(0, 10, company_details['address'], ln=True)
    pdf.cell(0, 10, job['location'], ln=True)
    pdf.cell(0, 10, "", ln=True)  # Blank line
    
    # Date
    pdf.cell(0, 10, datetime.now().strftime("%B %d, %Y"), ln=True)
    pdf.cell(0, 10, "", ln=True)  # Blank line
    
    # Body of the letter
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cover_letter_content)
    
    # Save the PDF
    file_path = f"output/{sanitize_filename(job['company'])}_{sanitize_filename(job['title'])}_cover_letter.pdf"
    pdf.output(file_path)
    return file_path
