from fpdf import FPDF
from datetime import datetime

class SalesReceiptPDF(FPDF):
    def header(self):
        # Add company logo
        self.image("/mnt/data/rosemer.jpg", 10, 8, 80)
        self.set_font("Arial", "B", 12)
        self.ln(25)  # Move below the logo

    def generate_sales_receipt(self, receipt_data,  logged_in_user):
        self.add_page()
        self.set_font("Arial", "", 10)
        
        # Unpack receipt data
        trans_id, customer, location, contact, items, unit_price, quantity, bulk_discounted_price, total_owed, paid, remaining_debt, payment_mode, cheque_bank = receipt_data
        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Transaction details
        self.cell(0, 10, f"Transaction ID: {trans_id}", ln=True)
        self.cell(0, 10, f"Date: {sale_date}", ln=True)
        self.cell(0, 10, f"Customer: {customer}", ln=True)
        self.ln(5)
        
        # Items table
        self.set_font("Arial", "B", 10)
        self.cell(70, 10, "Item", border=1)
        self.cell(30, 10, "Quantity", border=1, align="C")
        self.cell(40, 10, "Unit Price (GHS)", border=1, align="C")
        self.cell(40, 10, "Discounted Price (GHS)", border=1, align="C")
        self.ln()
        
        self.set_font("Arial", "", 10)
        items = items.split(", ")
        unit_price = list(map(float, unit_price.split(", ")))
        quantity = list(map(int, quantity.split(", ")))
        bulk_discounted_price = list(map(float, bulk_discounted_price.split(", ")))
        
        for i in range(len(items)):
            self.cell(70, 10, items[i], border=1)
            self.cell(30, 10, str(quantity[i]), border=1, align="C")
            self.cell(40, 10, f"{unit_price[i]:.2f}", border=1, align="C")
            self.cell(40, 10, f"{bulk_discounted_price[i]:.2f}" if bulk_discounted_price[i] > 0 else "-", border=1, align="C")
            self.ln()
        
        # Totals
        self.ln(5)
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, f"Total Cost: GHS {total_owed:.2f}", ln=True)
        self.cell(0, 10, f"Amount Paid: GHS {paid:.2f}", ln=True)
        self.cell(0, 10, f"Remaining Debt: GHS {remaining_debt:.2f}", ln=True)
        self.cell(0, 10, f"Payment Mode: {payment_mode}", ln=True)
        
        if payment_mode == "Cheque":
            self.cell(0, 10, f"Cheque Bank: {cheque_bank}", ln=True)
        
        self.ln(10)
        self.cell(0, 10, f"Served by: {logged_in_user}", ln=True)
        self.cell(0, 10, "Thank you for your business!", ln=True, align="C")
        
        return self
