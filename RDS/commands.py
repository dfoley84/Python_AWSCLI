
import typer
from ChangeType import ChangeType
from ChangeEngineType import ChangeEngine
from rich.progress import Progress, SpinnerColumn, TextColumn

rds_app = typer.Typer(help="Commands for managing AWS RDS instances.")

@rds_app.command(name="ChangeInstanceType")
def ChangeType(
    InstanceName: str = typer.Option(..., help="RDS Instance Name"),
    InstanceType: str = typer.Option(..., help="RDS Instance Type"),
    awsRegion: str = typer.Option(..., help="AWS Region")
):  
    rds_change = ChangeType(InstanceName, InstanceType, awsRegion)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("[cyan]Changing RDS instance type...", total=100)
        progress.start_task(task)
        try:
            rds_change.ChangeType(apply_immediately=True, wait=True)
            progress.update(task, description="[green]RDS instance type changed successfully!")
        except Exception as e:
            progress.update(task, description=f"[red]Error: {str(e)}")
            raise
    print(f"Changed {InstanceName} to {InstanceType} in {awsRegion}.")


@rds_app.command(name="ChangeEngineVersion")
def ChangeVersion(
    InstanceName: str = typer.Option(..., help="RDS Instance Name"),
    EngineVersion: str = typer.Option(..., help="RDS Engine Version"),
    awsRegion: str = typer.Option(..., help="AWS Region")
):  
    rds_change = ChangeEngine(InstanceName, EngineVersion, awsRegion)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("[cyan]Changing RDS Engine Version...", total=100)
        progress.start_task(task)
        try:
            rds_change.ChangeEngine(apply_immediately=True, wait=True)
            progress.update(task, description="[green]RDS instance type changed successfully!")
        except Exception as e:
            progress.update(task, description=f"[red]Error: {str(e)}")
            raise
    print(f"Changed {InstanceName} to Engine Verison: {EngineVersion} in {awsRegion}.")