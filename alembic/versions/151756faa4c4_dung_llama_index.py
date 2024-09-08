"""dung llama_index

Revision ID: 151756faa4c4
Revises: 0845b103e03a
Create Date: 2024-09-07 23:32:57.968315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '151756faa4c4'
down_revision: Union[str, None] = '0845b103e03a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('data_vector_embedding_idx', table_name='data_vector', postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.drop_table('data_vector')
    op.drop_index('ix_document_embeddings_id', table_name='document_embeddings')
    op.drop_table('document_embeddings')
    op.drop_table('ChatSession')
    op.drop_table('Documents')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Documents',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Documents_pkey')
    )
    op.create_table('ChatSession',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('response', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='ChatSession_pkey')
    )
    op.create_table('document_embeddings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='document_embeddings_pkey')
    )
    op.create_index('ix_document_embeddings_id', 'document_embeddings', ['id'], unique=False)
    op.create_table('data_vector',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_vector_pkey')
    )
    op.create_index('data_vector_embedding_idx', 'data_vector', ['embedding'], unique=False, postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    # ### end Alembic commands ###
