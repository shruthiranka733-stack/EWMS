from datetime import datetime
from io import BytesIO
from typing import Dict, List


class ReportService:
    """Generate PDF reports for shipments and financials using ReportLab."""

    @staticmethod
    def generate_shipment_report(shipment_data: Dict) -> BytesIO:
        """Generate detailed shipment report PDF"""
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(
            f"<b>Shipment Report</b><br/>{shipment_data.get('shipment_number', '')}",
            styles['Heading1'],
        ))
        elements.append(Spacer(1, 0.3 * inch))

        rows = [
            ['Field', 'Value'],
            ['Shipment #', shipment_data.get('shipment_number', '')],
            ['Phase', shipment_data.get('phase', '')],
            ['Status', shipment_data.get('status', '')],
            ['Created', shipment_data.get('created_at', '')],
            ['Invoice Count', str(shipment_data.get('invoice_count', 0))],
        ]

        table = Table(rows, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_financial_report(tickets: List[Dict]) -> BytesIO:
        """Generate accounting entries report PDF"""
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(
            f"<b>Accounting Entries Report</b><br/>{datetime.now().strftime('%Y-%m-%d')}",
            styles['Heading1'],
        ))
        elements.append(Spacer(1, 0.3 * inch))

        rows = [['Ticket #', 'Event', 'Type', 'Amount', 'Status']]
        total = 0.0
        for t in tickets:
            amount = float(t.get('amount', 0))
            total += amount
            rows.append([
                t.get('ticket_number', ''),
                t.get('trigger_event', ''),
                t.get('entry_type', ''),
                f'${amount:,.2f}',
                t.get('status', ''),
            ])
        rows.append(['', '', 'TOTAL', f'${total:,.2f}', ''])

        table = Table(rows, colWidths=[1.2 * inch, 1.5 * inch, 1.2 * inch, 1.2 * inch, 1 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer
