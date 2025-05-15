import typer


from rich.progress import Progress, SpinnerColumn, TextColumn

rds_app = typer.Typer(help="Commands for managing AWS EC2 instances.")