# utils/pdf_export.py
# PDF generation functions
# This file will contain:
# 1. Imports for PDF creation libraries (e.g., FPDF, reportlab).
# 2. A `save_summary_to_pdf` function.
# 3. Logic to format the summary text, headers, and bullet points into a readable PDF document.
# 4. Saving the generated PDF to the output path (potentially in the assets folder).

import os
from fpdf import FPDF
from utils.logger import get_logger

# Initialize logger
logger = get_logger("PDFExport")

class MeetingPDF(FPDF):
    """
    Custom PDF class to handle consistent headers and footers across pages.
    """
    def header(self):
        # Set font for the header: Helvetica, Bold, size 15
        self.set_font('helvetica', 'B', 15)
        # Add a centered title to the top of every page
        self.cell(0, 10, 'Meeting Summary & Transcript', border=False, ln=True, align='C')
        # Add a small vertical space after the header title
        self.ln(5)

    def footer(self):
        # Position the footer at 15mm from the bottom of the page
        self.set_y(-15)
        # Set font for the footer: Helvetica, Italic, size 8
        self.set_font('helvetica', 'I', 8)
        # Print "Page X/{total_pages}" centered in the footer
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def export_to_pdf(summary, transcript, output_path="assets/meeting_report.pdf"):
    """
    Creates a professional PDF report containing both the meeting summary and the full transcript.
    """
    logger.info(f"Generating PDF report at: {output_path}")
    
    try:
        # Step 1: Create the 'assets' directory if it doesn't already exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Step 2: Initialize the custom PDF object
        pdf = MeetingPDF()
        pdf.alias_nb_pages() # Required to calculate the total page count for the footer
        pdf.add_page()
        
        # --- Meeting Summary Section ---
        # Define a high-level header style for the summary section
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(44, 62, 80) # Use a professional dark blue/gray shade
        pdf.cell(0, 10, "Meeting Summary", ln=True)
        pdf.ln(2) # Extra spacing
        
        # Switch to the body font style for the summary itself
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(0, 0, 0) # Basic black text
        # Write the summary. Note: We strip '#' to remove basic markdown headers for a cleaner look.
        pdf.multi_cell(0, 7, summary.replace('#', '')) 
        pdf.ln(10) # Add a larger gap before starting the transcript section
        
        # --- Full Transcript Section ---
        # Set up a new section header for the transcript
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, "Full Transcript", ln=True)
        pdf.ln(2)
        
        # Use a slightly smaller font for the transcript to fit more content per page
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(30, 30, 30) # Dark gray text
        # Write the full, multi-line transcript
        pdf.multi_cell(0, 6, transcript)
        
        # Step 3: Write the finalized content to the PDF file
        pdf.output(output_path)
        logger.info("PDF document generated successfully.")
        return output_path
    
    except Exception as e:
        # Capture and log any issues during PDF creation (e.g., file permissions)
        error_msg = f"Failed to generate PDF: {str(e)}"
        logger.error(error_msg)
        return None
