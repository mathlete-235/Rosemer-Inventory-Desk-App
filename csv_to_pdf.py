import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def csv_to_pdf(csv_file, pdf_file):
    """Convert a CSV file into a formatted PDF document."""
    try:
        # Read CSV
        df = pd.read_csv(csv_file)

        # Create PDF Canvas
        pdf = canvas.Canvas(pdf_file, pagesize=landscape(letter))
        pdf.setTitle("CSV Data Report")

        # Convert DataFrame to List of Lists (For Table)
        data = [df.columns.tolist()] + df.values.tolist()

        # Create Table
        table = Table(data)

        # Apply Styling
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header Background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header Text Color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center Align Text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header Font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header Padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row Background
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table Grid
        ])
        table.setStyle(style)

        # Draw Table
        table.wrapOn(pdf, 50, 500)
        table.drawOn(pdf, 50, 500)

        # Save PDF
        pdf.save()

        #print(f"PDF saved successfully: {pdf_file}")

    except Exception as e:
        print(f"Error: {e}")
