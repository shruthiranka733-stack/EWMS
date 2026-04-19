import os
from typing import List, Dict


class SMSAlertService:
    """
    Send SMS alerts via Twilio for critical shipment events.
    Requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER env vars.
    """

    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER')
        self._client = None

    @property
    def client(self):
        if self._client is None and self.account_sid:
            from twilio.rest import Client
            self._client = Client(self.account_sid, self.auth_token)
        return self._client

    async def send_critical_dd_alert(
        self,
        shipment_number: str,
        days_remaining: int,
        to_numbers: List[str],
    ) -> Dict:
        """Send SMS for CRITICAL D&D risk"""
        if not self.client:
            return {'status': 'skipped', 'reason': 'Twilio not configured'}

        body = (
            f'🚨 CRITICAL D&D ALERT: {shipment_number} — '
            f'{days_remaining}d remaining. Action required NOW.'
        )

        results = []
        for phone in to_numbers:
            try:
                msg = self.client.messages.create(body=body, from_=self.from_number, to=phone)
                results.append({'phone': phone, 'status': 'sent', 'sid': msg.sid})
            except Exception as e:
                results.append({'phone': phone, 'status': 'failed', 'error': str(e)})

        return {
            'shipment': shipment_number,
            'alerts_sent': sum(1 for r in results if r['status'] == 'sent'),
            'alerts_failed': sum(1 for r in results if r['status'] == 'failed'),
            'details': results,
        }

    async def send_sla_breach_sms(
        self,
        shipment_number: str,
        to_numbers: List[str],
    ) -> Dict:
        """Send SMS for SLA breach"""
        if not self.client:
            return {'status': 'skipped', 'reason': 'Twilio not configured'}

        body = f'⚠️ SLA BREACHED: {shipment_number}. Check EWMS dashboard immediately.'

        results = []
        for phone in to_numbers:
            try:
                self.client.messages.create(body=body, from_=self.from_number, to=phone)
                results.append({'phone': phone, 'status': 'sent'})
            except Exception as e:
                results.append({'phone': phone, 'status': 'failed', 'error': str(e)})

        return {'shipment': shipment_number, 'results': results}
