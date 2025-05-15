import typer
from RDS.commands import rds_app
from ECS.commands import ecs_app

app = typer.Typer(help="AWS Management CLI")
app.add_typer(rds_app, name="rds")
app.add_typer(ecs_app, name="ecs")

if __name__ == "__main__":
    app()