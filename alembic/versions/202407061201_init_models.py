"""init models

Revision ID: 202407061201
Revises: 
Create Date: 2024-07-06 12:01:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '202407061201'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'properties',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('unit_count', sa.Integer, nullable=False),
    )

    unitsize = sa.Enum('STUDIO', '1BR', '2BR', '3BR', name='unitsize')
    unitsize.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'apartment_units',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('unit_number', sa.String, nullable=False),
        sa.Column('size', unitsize, nullable=False),
        sa.Column('rent', sa.Integer, nullable=False),
        sa.Column('property_id', sa.Integer, sa.ForeignKey('properties.id'), nullable=False),
    )

    op.create_table(
        'residents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('phone', sa.String, nullable=False),
        sa.Column('income', sa.Integer),
        sa.Column('occupation', sa.String),
        sa.Column('num_occupants', sa.Integer, nullable=False, server_default='1'),
        sa.Column('unit_id', sa.Integer, sa.ForeignKey('apartment_units.id'), nullable=False),
    )

    paymentstatus = sa.Enum('ON_TIME', 'LATE', 'OUTSTANDING', name='paymentstatus')
    paymentstatus.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('status', paymentstatus, nullable=False),
        sa.Column('resident_id', sa.Integer, sa.ForeignKey('residents.id'), nullable=False),
    )

    repairstatus = sa.Enum('NEW', 'IN_PROGRESS', 'DONE', name='repairstatus')
    repairstatus.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'repairs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('status', repairstatus, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('unit_id', sa.Integer, sa.ForeignKey('apartment_units.id'), nullable=False),
        sa.Column('resident_id', sa.Integer, sa.ForeignKey('residents.id')),    )

    op.create_table(
        'pets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('breed', sa.String),
        sa.Column('weight', sa.Float),
        sa.Column('resident_id', sa.Integer, sa.ForeignKey('residents.id'), nullable=False),
    )

    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('make', sa.String, nullable=False),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('plate', sa.String, nullable=False),
        sa.Column('resident_id', sa.Integer, sa.ForeignKey('residents.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('vehicles')
    op.drop_table('pets')
    op.drop_table('repairs')
    op.drop_table('payments')
    op.drop_table('residents')
    op.drop_table('apartment_units')
    op.drop_table('properties')
    sa.Enum(name='unitsize').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='paymentstatus').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='repairstatus').drop(op.get_bind(), checkfirst=False)
