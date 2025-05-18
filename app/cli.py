# app/cli.py
import os

import typer
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal
from .enums import UserRole

app_cli = typer.Typer()


@app_cli.command()
def create_admin_user(
    email: str = typer.Option(
        ..., prompt="Email do Administrador", help="Email para o superusuário."
    ),
    password: str = typer.Option(
        ...,
        prompt="Senha",
        confirmation_prompt=True,
        hide_input=True,
        help="Senha para o superusuário.",
    ),
    nome_completo: str = typer.Option(
        "Admin Padrão", prompt="Nome Completo", help="Nome completo do superusuário."
    ),
):
    """
    Cria um usuário administrador inicial no sistema.
    """
    typer.echo(f"Tentando criar usuário admin: {email}")  # type: ignore[attr-defined]
    db: Session = SessionLocal()
    try:
        existing_user = crud.get_user_by_email(db, email=email)
        if existing_user:
            typer.secho(f"Email '{email}' já existe.")  # type: ignore[attr-defined]
            raise typer.Exit(code=1)

        user_in = schemas.UserCreate(
            email=email,
            nome_completo=nome_completo,
            password=password,
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True,
        )

        new_admin = crud.create_user(db=db, user=user_in)
        typer.secho(f"Admin '{new_admin.email}' criado!")  # type: ignore[attr-defined]
    except ValueError as e:
        typer.secho(f"Erro ao criar admin: {e}")  # type: ignore[attr-defined]
        raise typer.Exit(code=1)
    finally:
        db.close()


@app_cli.command()
def run_migrations():
    """Roda as migrações do Alembic."""
    typer.echo("Executando migrações do Alembic...")  # type: ignore[attr-defined]
    os.system("alembic upgrade head")
    typer.echo("Migrações concluídas.")  # type: ignore[attr-defined]


if __name__ == "__main__":
    app_cli()
