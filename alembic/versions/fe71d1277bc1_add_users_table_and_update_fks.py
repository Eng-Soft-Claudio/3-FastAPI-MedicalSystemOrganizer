# alembic/versions/fe71d1277bc1_add_users_table_and_update_fks.py

"""add_users_table_and_update_fks

Revision ID: fe71d1277bc1
Revises:
Create Date: 2025-05-16 20:23:42.838021

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "fe71d1277bc1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "medicos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.VARCHAR(), nullable=False),
        sa.Column("especialidade", sa.VARCHAR(), nullable=False),
        sa.Column("telefone", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("medicos_pkey")),
        sa.UniqueConstraint("nome", name=op.f("medicos_nome_key")),
    )
    op.create_index(op.f("ix_medicos_id"), "medicos", ["id"], unique=False)
    op.create_index(op.f("ix_medicos_nome"), "medicos", ["nome"], unique=True)

    op.create_table(
        "pacientes",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("nome_completo", sa.VARCHAR(), nullable=False),
        sa.Column("data_nascimento", sa.DATE(), nullable=False),
        sa.Column("nome_da_mae", sa.VARCHAR(), nullable=False),
        sa.Column("cpf", sa.VARCHAR(), nullable=False),
        sa.Column("cns", sa.VARCHAR(), nullable=True),
        sa.Column("telefone", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pacientes_pkey")),
    )
    op.create_index(op.f("ix_pacientes_id"), "pacientes", ["id"], unique=False)
    op.create_index(
        op.f("ix_pacientes_nome_completo"), "pacientes", ["nome_completo"], unique=False
    )
    op.create_index(op.f("ix_pacientes_cpf"), "pacientes", ["cpf"], unique=True)
    op.create_index(op.f("ix_pacientes_cns"), "pacientes", ["cns"], unique=True)

    op.create_table(
        "enderecos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("rua", sa.VARCHAR(), nullable=False),
        sa.Column("numero", sa.VARCHAR(), nullable=True),
        sa.Column("bairro", sa.VARCHAR(), nullable=False),
        sa.Column("cidade", sa.VARCHAR(), nullable=False),
        sa.Column("estado", sa.VARCHAR(length=2), nullable=False),
        sa.Column("cep", sa.VARCHAR(length=9), nullable=False),
        sa.Column("paciente_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["paciente_id"], ["pacientes.id"], name=op.f("enderecos_paciente_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("enderecos_pkey")),
        sa.UniqueConstraint("paciente_id", name=op.f("enderecos_paciente_id_key")),
    )
    op.create_index(op.f("ix_enderecos_id"), "enderecos", ["id"], unique=False)
    op.create_index(op.f("ix_enderecos_rua"), "enderecos", ["rua"], unique=False)
    op.create_index(op.f("ix_enderecos_bairro"), "enderecos", ["bairro"], unique=False)
    op.create_index(op.f("ix_enderecos_cidade"), "enderecos", ["cidade"], unique=False)
    op.create_index(op.f("ix_enderecos_cep"), "enderecos", ["cep"], unique=False)

    user_role_enum = postgresql.ENUM(
        "ADMIN", "SECRETARIA", "MEDICO", name="user_role_enum"
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(), nullable=False),
        sa.Column("nome_completo", sa.VARCHAR(), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "ADMIN",
                "SECRETARIA",
                "MEDICO",
                name="user_role_enum",
                inherit_schema=True,
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.BOOLEAN(), nullable=False, server_default=sa.true()),
        sa.Column(
            "is_superuser", sa.BOOLEAN(), nullable=False, server_default=sa.false()
        ),
        sa.Column("medico_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["medico_id"], ["medicos.id"], name=op.f("users_medico_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
        sa.UniqueConstraint("email", name=op.f("users_email_key")),
        sa.UniqueConstraint("medico_id", name=op.f("users_medico_id_key")),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "agendamentos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("especialidade", sa.VARCHAR(), nullable=False),
        sa.Column("data_primeira_consulta", sa.DATE(), nullable=False),
        sa.Column("data_proxima_consulta", sa.DATE(), nullable=True),
        sa.Column(
            "valor_consulta",
            sa.NUMERIC(precision=10, scale=2),  # type: ignore[arg-type]
            nullable=False,
        ),
        sa.Column("descricao", sa.VARCHAR(), nullable=True),
        sa.Column("receituario", sa.VARCHAR(), nullable=True),
        sa.Column("paciente_id", sa.INTEGER(), nullable=False),
        sa.Column("medico_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["medico_id"], ["medicos.id"], name=op.f("agendamentos_medico_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["paciente_id"],
            ["pacientes.id"],
            name=op.f("agendamentos_paciente_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("agendamentos_pkey")),
    )
    op.create_index(op.f("ix_agendamentos_id"), "agendamentos", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_agendamentos_id"), table_name="agendamentos")
    op.drop_table("agendamentos")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    user_role_enum = postgresql.ENUM(
        "ADMIN", "SECRETARIA", "MEDICO", name="user_role_enum"
    )
    user_role_enum.drop(op.get_bind(), checkfirst=True)

    op.drop_index(op.f("ix_enderecos_cep"), table_name="enderecos")
    op.drop_index(op.f("ix_enderecos_cidade"), table_name="enderecos")
    op.drop_index(op.f("ix_enderecos_bairro"), table_name="enderecos")
    op.drop_index(op.f("ix_enderecos_rua"), table_name="enderecos")
    op.drop_index(op.f("ix_enderecos_id"), table_name="enderecos")
    op.drop_table("enderecos")

    op.drop_index(op.f("ix_pacientes_cns"), table_name="pacientes")
    op.drop_index(op.f("ix_pacientes_cpf"), table_name="pacientes")
    op.drop_index(op.f("ix_pacientes_nome_completo"), table_name="pacientes")
    op.drop_index(op.f("ix_pacientes_id"), table_name="pacientes")
    op.drop_table("pacientes")

    op.drop_index(op.f("ix_medicos_nome"), table_name="medicos")
    op.drop_index(op.f("ix_medicos_id"), table_name="medicos")
    op.drop_table("medicos")
