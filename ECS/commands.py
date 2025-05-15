import typer
from ServiceRestart import ServiceRestart
from rich.progress import Progress, SpinnerColumn, TextColumn

ecs_app = typer.Typer(help="Commands for managing AWS ECS Service.")

@ecs_app.command(name="RestartService")
def RestartService(
    ClusterName: str = typer.Option(..., help="ECS Cluster Name"),
    Servicearn: str = typer.Option(..., help="Service ARN"),
    awsRegion: str = typer.Option(..., help="AWS Region")
):  
    rds_change = ServiceRestart(ClusterName, Servicearn, awsRegion)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("[cyan]Restarting ECS Service...", total=100)
        progress.start_task(task)
        try:
            rds_change.ServiceRestart()
            progress.update(task, description="[green]ECS Service Restarted Successfully!")
        except Exception as e:
            progress.update(task, description=f"[red]Error: {str(e)}")
            raise
    print(f"Service Restart.")
