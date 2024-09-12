"""moi

Revision ID: 00cd5f85e528
Revises: 1d6149e75389
Create Date: 2024-09-12 20:20:42.598960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '00cd5f85e528'
down_revision: Union[str, None] = '1d6149e75389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('data_metagpt_vector_embedding_idx', table_name='data_metagpt_vector', postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.drop_table('data_metagpt_vector')
    op.drop_index('ix_document_embeddings_id', table_name='document_embeddings')
    op.drop_table('document_embeddings')
    op.drop_index('data_selfrag_vector_embedding_idx', table_name='data_selfrag_vector', postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.drop_table('data_selfrag_vector')
    op.drop_index('data_attention_vector_embedding_idx', table_name='data_attention_vector', postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.drop_table('data_attention_vector')
    op.drop_index('data_longlora_vector_embedding_idx', table_name='data_longlora_vector', postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.drop_table('data_longlora_vector')
    op.drop_table('ChatSession')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ChatSession',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('response', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='ChatSession_pkey')
    )
    op.create_table('data_longlora_vector',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_longlora_vector_pkey')
    )
    op.create_index('data_longlora_vector_embedding_idx', 'data_longlora_vector', ['embedding'], unique=False, postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.create_table('data_attention_vector',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_attention_vector_pkey')
    )
    op.create_index('data_attention_vector_embedding_idx', 'data_attention_vector', ['embedding'], unique=False, postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.create_table('data_selfrag_vector',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_selfrag_vector_pkey')
    )
    op.create_index('data_selfrag_vector_embedding_idx', 'data_selfrag_vector', ['embedding'], unique=False, postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    op.create_table('document_embeddings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='document_embeddings_pkey')
    )
    op.create_index('ix_document_embeddings_id', 'document_embeddings', ['id'], unique=False)
    op.create_table('data_metagpt_vector',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_metagpt_vector_pkey')
    )
    op.create_index('data_metagpt_vector_embedding_idx', 'data_metagpt_vector', ['embedding'], unique=False, postgresql_with={'m': '16', 'ef_construction': '64'}, postgresql_using='hnsw')
    # ### end Alembic commands ###
