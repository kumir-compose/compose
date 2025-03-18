import click


def err_exit(text: str) -> None:
    """Print error and exit."""
    click.echo(
        click.style(text, fg="red"),
        err=True,
        color=True
    )
    raise click.exceptions.Exit(1)
