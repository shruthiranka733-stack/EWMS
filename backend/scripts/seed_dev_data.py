import os
import sys
from uuid import uuid4
from datetime import date
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# Ensure app package is importable when run from backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://ewms_user:password@localhost:5432/ewms_dev')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_organizations():
    from app.models import Organization

    india_logistics = Organization(id=uuid4(), name='India Logistics Team', type='india_logistics')
    us_logistics = Organization(id=uuid4(), name='US Logistics Team', type='us_logistics')
    management = Organization(id=uuid4(), name='Management', type='management')
    finance = Organization(id=uuid4(), name='Finance Team', type='finance')

    db.add_all([india_logistics, us_logistics, management, finance])
    db.commit()
    print('✅ Organizations created')
    return india_logistics, us_logistics, management, finance


def seed_users(india_logistics, us_logistics, management, finance):
    from app.models import User

    user1 = User(id=uuid4(), org_id=india_logistics.id, email='india_coordinator@example.com', name='India Logistics Coordinator', role='user')
    user2 = User(id=uuid4(), org_id=us_logistics.id, email='us_coordinator@example.com', name='US Logistics Coordinator', role='user')
    user3 = User(id=uuid4(), org_id=management.id, email='manager@example.com', name='Operations Manager', role='admin')
    user4 = User(id=uuid4(), org_id=finance.id, email='finance@example.com', name='Finance Analyst', role='user')

    db.add_all([user1, user2, user3, user4])
    db.commit()
    print('✅ Users created')
    return user1, user2, user3, user4


def seed_sales_invoices(india_logistics):
    from app.models import SalesInvoice

    invoice1 = SalesInvoice(
        id=uuid4(),
        invoice_number='EXP/2025/001',
        exporter_name='INZETMAN Private Limited',
        buyer_name='UNIMACTS GLOBAL LLC',
        invoice_date=date(2025, 4, 18),
        total_value=Decimal('150000.00'),
        currency='USD',
        ocr_status='pending_hitl',
    )
    invoice2 = SalesInvoice(
        id=uuid4(),
        invoice_number='EXP/2025/002',
        exporter_name='INZETMAN Private Limited',
        buyer_name='ANOTHER BUYER LLC',
        invoice_date=date(2025, 4, 19),
        total_value=Decimal('200000.00'),
        currency='USD',
        ocr_status='pending_hitl',
    )

    db.add_all([invoice1, invoice2])
    db.commit()
    print('✅ Sales Invoices created')
    return invoice1, invoice2


def main():
    try:
        print('Starting seed...')
        india_logistics, us_logistics, management, finance = seed_organizations()
        seed_users(india_logistics, us_logistics, management, finance)
        seed_sales_invoices(india_logistics)
        print('✅ All seed data created successfully!')
        print('   - 4 organizations')
        print('   - 4 users')
        print('   - 2 sales invoices')
    except Exception as e:
        print(f'❌ Error: {str(e)}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    main()
