import typer
from RDS.commands import rds_app

app = typer.Typer(help="AWS Management CLI")
app.add_typer(rds_app, name="rds")

if __name__ == "__main__":
    app()