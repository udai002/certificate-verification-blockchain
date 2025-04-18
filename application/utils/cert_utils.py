import pdfplumber
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
import re


def generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, logo_path):
    """Generate a PDF certificate with a professional design."""
    signature_path = r"C:\Users\mvams\Downloads\MySignNorm.png"
    slide_design_path = r"C:\Users\mvams\Downloads\slideDesign.jpg"
    award_logo_path = r"C:\Users\mvams\Downloads\AwardLogo.png"
    
    c = canvas.Canvas(pdf_file_path, pagesize=landscape(letter))
    width, height = landscape(letter)

    border_color = HexColor("#001f3f")
    text_color = HexColor("#2E2E2E")

    border_margin = 20
    c.setStrokeColor(border_color)
    c.setLineWidth(4)
    c.rect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin)

    c.drawImage(award_logo_path, width - 320, height - 300, width=300, height=280)
    c.drawImage(slide_design_path, border_margin, height - 520, width=500, height=500)
    c.drawImage(logo_path, (width - 200) / 2, height - 540, width=200, height=100)

    c.setFont("Helvetica-Bold", 50)
    c.setFillColor(text_color)
    c.drawCentredString(width / 2, height - 140, "CERTIFICATE")
    c.setFont("Helvetica", 25)
    c.drawCentredString(width / 2, height - 180, "OF ACHIEVEMENT")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 260, "THIS IS TO CERTIFY THAT")
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height - 330, candidate_name)

    c.setFont("Helvetica", 14)
    c.drawString(border_margin + 60, height - 370, f"has successfully completed the course {course_name} with a duration of 6 months.")
    c.drawString(border_margin + 60, height - 390, "In recognition of outstanding performance and commitment, this certificate is awarded.")

    c.drawImage(signature_path, 55, 120, width=170, height=50)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(95, 120, "(Vamsi Mandala)")
    c.line(border_margin + 60, 115, 195, 115)
    c.setFont("Helvetica", 14)
    c.drawString(95, 95, "Manager")

    current_date = datetime.now().strftime("%d %B %Y")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 185, 120, current_date)
    c.line(width - 195, 115, width - 80, 115)
    c.setFont("Helvetica", 14)
    c.drawString(width - 165, 95, "Issue Date")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(width / 2 - 180, height - 560, "Certificate ID:")
    c.setFont("Helvetica", 10)
    c.drawString(width / 2 - 100, height - 560, f"{uid}")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(width / 2 + 30, height - 560, "Issued by:")
    c.setFont("Helvetica", 10)
    c.drawString(width / 2 + 90, height - 560, f"{org_name}")

    c.save()


def extract_certificate(pdf_path):
    """Extract certificate details using pdfplumber for more reliable text extraction."""
    extracted_text = ""

    # Open PDF with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"  # Extract text page by page

    lines = extracted_text.splitlines()

    # Debugging: Print extracted text (Only enable during testing)
    # print("\nExtracted Text:\n", extracted_text)

    # Extract Certificate ID
    uid_match = re.search(r"Certificate ID:\s*([\w\d]+)", extracted_text)
    uid = uid_match.group(1).strip() if uid_match else "Not Found"

    # Extract Organization Name
    org_match = re.search(r"Issued by:\s*(.+)", extracted_text)
    org_name = org_match.group(1).strip() if org_match else "Not Found"

    # Extract Candidate Name
    try:
        name_index = lines.index("THIS IS TO CERTIFY THAT") + 1
        candidate_name = lines[name_index].strip()
    except (ValueError, IndexError):
        candidate_name = "Not Found"

    # Extract Course Name
    course_match = re.search(r"has successfully completed the course\s+(.+?)\s+with a duration", extracted_text)
    course_name = course_match.group(1).strip() if course_match else "Not Found"

    return (uid, candidate_name, course_name, org_name)
