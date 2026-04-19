from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id')),
        sa.Column('email', sa.String(255), unique=True),
        sa.Column('name', sa.String(255)),
        sa.Column('role', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'sales_invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('invoice_number', sa.String(50)),
        sa.Column('exporter_name', sa.String(255)),
        sa.Column('buyer_name', sa.String(255)),
        sa.Column('invoice_date', sa.Date()),
        sa.Column('total_value', sa.Numeric(12, 2)),
        sa.Column('currency', sa.String(3)),
        sa.Column('ocr_status', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'shipments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_number', sa.String(50), unique=True),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id')),
        sa.Column('phase', sa.String(50)),
        sa.Column('status', sa.String(50)),
        sa.Column('invoice_ids', postgresql.ARRAY(postgresql.UUID(as_uuid=True))),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('shipments.id')),
        sa.Column('document_type', sa.String(50)),
        sa.Column('status', sa.String(50)),
        sa.Column('file_url', sa.String(500)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('shipments.id')),
        sa.Column('task_type', sa.String(100)),
        sa.Column('status', sa.String(50)),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('due_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'sla_timelines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('shipments.id')),
        sa.Column('stage', sa.String(100)),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('due_at', sa.DateTime()),
        sa.Column('status', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'accounting_tickets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('shipments.id')),
        sa.Column('ticket_number', sa.String(50), unique=True),
        sa.Column('trigger_event', sa.String(100)),
        sa.Column('entry_type', sa.String(50)),
        sa.Column('amount', sa.Numeric(12, 2)),
        sa.Column('currency', sa.String(3)),
        sa.Column('status', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('accounting_tickets')
    op.drop_table('sla_timelines')
    op.drop_table('tasks')
    op.drop_table('documents')
    op.drop_table('shipments')
    op.drop_table('sales_invoices')
    op.drop_table('users')
    op.drop_table('organizations')
