from datetime import datetime, timedelta
from enum import Enum
import random


class TrackingEventType(str, Enum):
    VESSEL_DEPARTED = 'vessel_departed'
    VESSEL_AT_TRANSSHIPMENT = 'transshipment_arrived'
    VESSEL_ARRIVED = 'vessel_arrived'
    CONTAINER_DISCHARGED = 'container_discharged'
    CONTAINER_GATE_OUT = 'container_gate_out'


class MockTrackingService:
    """
    Phase 1: Returns mocked tracking events.
    Phase 2: Will integrate real 3PL tracking API + webhooks.
    """

    async def get_container_status(self, container_number: str) -> dict:
        """Get current status of a container."""
        statuses = ['in_transit', 'at_port', 'discharged', 'in_warehouse', 'delivered']
        current_status = random.choice(statuses)

        return {
            'container_number': container_number,
            'status': current_status,
            'vessel_name': 'MSC GULSUN',
            'current_location': 'Atlantic Ocean' if current_status == 'in_transit' else 'Port of Newark',
            'last_update': datetime.utcnow().isoformat(),
            'eta': (datetime.utcnow() + timedelta(days=random.randint(5, 30))).isoformat(),
            'last_free_day': (datetime.utcnow() + timedelta(days=random.randint(7, 14))).isoformat(),
        }

    async def get_tracking_events(self, container_number: str) -> list:
        """Get all tracking events for a container."""
        return [
            {
                'event_type': 'vessel_departed',
                'timestamp': (datetime.utcnow() - timedelta(days=10)).isoformat(),
                'location': 'Port of Mumbai',
                'details': 'Vessel departed origin port',
            },
            {
                'event_type': 'vessel_in_transit',
                'timestamp': (datetime.utcnow() - timedelta(days=5)).isoformat(),
                'location': 'Atlantic Ocean',
                'details': 'Container in transit',
            },
            {
                'event_type': 'vessel_arrived',
                'timestamp': (datetime.utcnow() - timedelta(days=1)).isoformat(),
                'location': 'Port of Newark',
                'details': 'Vessel arrived at discharge port',
            },
        ]


mock_tracking_service = MockTrackingService()
