from decimal import Decimal


class DDRiskLevel:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class DDRiskService:
    """
    D&D Risk Management Service.
    Calculates demurrage & detention costs, risk levels, and escalations.
    """

    DEMURRAGE_RATE = Decimal('150')  # USD per day per container
    DETENTION_RATE = Decimal('100')  # USD per day per container

    @staticmethod
    def calculate_risk_level(days_remaining: int) -> tuple[str, int | None]:
        """
        Returns (risk_level, sla_hours) based on days until LFD.
        sla_hours is None when risk is low.
        """
        if days_remaining > 5:
            return (DDRiskLevel.LOW, None)
        elif 3 <= days_remaining <= 5:
            return (DDRiskLevel.MEDIUM, 48)
        elif 1 <= days_remaining < 3:
            return (DDRiskLevel.HIGH, 24)
        else:
            return (DDRiskLevel.CRITICAL, 4)

    @staticmethod
    def calculate_dd_cost(
        days_overdue: int,
        num_containers: int,
        demurrage_rate: Decimal = DEMURRAGE_RATE,
        detention_rate: Decimal = DETENTION_RATE,
    ) -> dict:
        """Calculate demurrage + detention costs."""
        if days_overdue <= 0:
            return {
                'demurrage_cost': Decimal('0'),
                'detention_cost': Decimal('0'),
                'total_cost': Decimal('0'),
                'days_overdue': 0,
                'num_containers': num_containers,
            }

        demurrage = demurrage_rate * Decimal(days_overdue) * Decimal(num_containers)
        detention = detention_rate * Decimal(days_overdue) * Decimal(num_containers)

        return {
            'demurrage_cost': demurrage,
            'detention_cost': detention,
            'total_cost': demurrage + detention,
            'days_overdue': days_overdue,
            'num_containers': num_containers,
        }

    @staticmethod
    def get_escalation_recipients(risk_level: str) -> dict:
        """Determine who should be notified based on risk level."""
        escalations = {
            DDRiskLevel.MEDIUM: {
                'email_recipients': ['ops_manager@company.com'],
                'channels': ['email'],
                'urgency': 'high',
            },
            DDRiskLevel.HIGH: {
                'email_recipients': ['director@company.com', 'ops_manager@company.com'],
                'channels': ['email', 'sms'],
                'urgency': 'critical',
            },
            DDRiskLevel.CRITICAL: {
                'email_recipients': ['owner@company.com', 'director@company.com'],
                'channels': ['email', 'sms', 'slack'],
                'urgency': 'emergency',
            },
        }
        return escalations.get(risk_level, {})
