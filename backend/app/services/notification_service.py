import os
from datetime import datetime
from typing import List, Dict
from app.services.dd_risk_service import DDRiskService


class NotificationService:
    """
    Send email notifications for shipment events.
    Requires SENDGRID_API_KEY env var to actually send — otherwise logs and skips.
    """

    def __init__(self):
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'alerts@ewms.company.com')
        self._sg = None

    @property
    def sg(self):
        if self._sg is None and self.sendgrid_key:
            from sendgrid import SendGridAPIClient
            self._sg = SendGridAPIClient(self.sendgrid_key)
        return self._sg

    def _build_dd_html(self, shipment_number: str, risk_level: str, days_remaining: int, estimated_cost: float) -> str:
        return f"""
        <html><body style="font-family:Arial,sans-serif;">
          <div style="max-width:600px;margin:0 auto;padding:20px;border:1px solid #ddd;border-radius:8px;">
            <h2 style="color:#EF4444;">⚠️ {risk_level.upper()} D&D Risk Alert — {shipment_number}</h2>
            <div style="background:#FEE2E2;padding:16px;border-radius:4px;margin:16px 0;">
              <p><strong>Shipment:</strong> {shipment_number}</p>
              <p><strong>Risk Level:</strong> <span style="color:#B91C1C;font-weight:bold;">{risk_level.upper()}</span></p>
              <p><strong>Days Until LFD:</strong> {days_remaining}</p>
              <p><strong>Estimated D&D Cost:</strong> ${estimated_cost:,.2f}</p>
            </div>
            <h3>Required Actions:</h3>
            <ul>
              <li>Review shipment status immediately</li>
              <li>Contact 3PL for gate-out confirmation</li>
              <li>Arrange expedited customs clearance if needed</li>
              <li>Update shipment status in EWMS</li>
            </ul>
            <p><a href="https://ewms.company.com/dashboard"
               style="background:#22C55E;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block;">
               View in EWMS</a></p>
            <hr style="margin-top:30px;border:none;border-top:1px solid #ddd;">
            <p style="color:#666;font-size:12px;">Automated alert from EWMS. Do not reply.</p>
          </div>
        </body></html>
        """

    async def send_dd_risk_alert(
        self,
        shipment_number: str,
        risk_level: str,
        days_remaining: int,
        estimated_cost: float,
        recipients: List[str],
    ) -> Dict:
        """Send D&D risk alert email"""
        if not self.sg:
            return {'status': 'skipped', 'reason': 'SendGrid not configured'}

        from sendgrid.helpers.mail import Mail, Email, To, Subject, PlainTextContent, HtmlContent

        try:
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=[To(e) for e in recipients],
                subject=Subject(f'⚠️ {risk_level.upper()} D&D Risk Alert - {shipment_number}'),
                plain_text_content=PlainTextContent(f'D&D Risk Alert: {shipment_number}'),
                html_content=HtmlContent(self._build_dd_html(shipment_number, risk_level, days_remaining, estimated_cost)),
            )
            self.sg.send(message)
            return {
                'status': 'sent',
                'shipment': shipment_number,
                'risk_level': risk_level,
                'recipients': len(recipients),
                'timestamp': datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

    async def send_sla_breach_alert(
        self,
        shipment_number: str,
        stage: str,
        due_date: str,
        recipients: List[str],
    ) -> Dict:
        """Send SLA breach alert"""
        if not self.sg:
            return {'status': 'skipped', 'reason': 'SendGrid not configured'}

        from sendgrid.helpers.mail import Mail, Email, To, Subject, HtmlContent

        html = f"""
        <html><body style="font-family:Arial,sans-serif;">
          <h2 style="color:#EF4444;">⚠️ SLA BREACHED — {shipment_number} ({stage})</h2>
          <p><strong>Shipment:</strong> {shipment_number}</p>
          <p><strong>Stage:</strong> {stage}</p>
          <p><strong>Due Date:</strong> {due_date}</p>
          <p style="color:#EF4444;font-weight:bold;">This stage has exceeded its SLA deadline.</p>
          <p><a href="https://ewms.company.com/shipments/{shipment_number}">View Shipment</a></p>
        </body></html>
        """
        try:
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=[To(e) for e in recipients],
                subject=Subject(f'⚠️ SLA BREACHED - {shipment_number} ({stage})'),
                html_content=HtmlContent(html),
            )
            self.sg.send(message)
            return {'status': 'sent', 'shipment': shipment_number}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

    async def send_invoice_approval_reminder(
        self,
        invoice_number: str,
        days_pending: int,
        recipient: str,
    ) -> Dict:
        """Reminder email for pending invoice HITL review"""
        if not self.sg:
            return {'status': 'skipped', 'reason': 'SendGrid not configured'}

        from sendgrid.helpers.mail import Mail, Email, To, Subject, HtmlContent

        html = f"""
        <html><body style="font-family:Arial,sans-serif;">
          <h2>📋 Invoice Awaiting HITL Review</h2>
          <p><strong>Invoice:</strong> {invoice_number}</p>
          <p><strong>Pending For:</strong> {days_pending} days</p>
          <p>Please review and approve or reject this invoice.</p>
          <p><a href="https://ewms.company.com/hitl-review">Review Now</a></p>
        </body></html>
        """
        try:
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=To(recipient),
                subject=Subject(f'📋 Invoice Awaiting Review - {invoice_number}'),
                html_content=HtmlContent(html),
            )
            self.sg.send(message)
            return {'status': 'sent'}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
