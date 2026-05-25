# This file is a CLI wrapper for the modpack_changelogger function in main.py
# It provides a CLI interface for the package

import aiohttp
import click

from modpack_changelogger.main import generate_changelog
from modpack_changelogger.utils import (
    ConfigValidationError,
    DifferentModpackFormatError,
    ModpackFormatError,
    UnsupportedModpackFormatError,
    create_config,
)
from modpack_changelogger.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-?"])


def handle_error(error, message=None):
    """Centralized error handler for CLI errors."""
    if message:
        click.secho(f"Error: {message}", err=True, fg="bright_red")
        click.secho(f"Details: {error}", err=True, fg="red")
    else:
        click.secho(f"Error: {error}", err=True, fg="bright_red")


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--version", is_flag=True, help="Show the version and exit")
@click.option("-o", "--old", help="First pack to compare")
@click.option("-n", "--new", help="The pack to compare against")
@click.option("-c", "--config", help="Use a config file")
@click.option("-f", "--file", help="Specify the output file for the changelog")
@click.pass_context
def cli(ctx, version, old, new, config, file):
    """CLI wrapper for Modpack Changelogger."""
    if ctx.invoked_subcommand is not None:
        return

    if version:
        click.echo(f"Modpack Changelogger {__version__}")
        return

    # Show help and exit if no arguments are provided
    if not any([old, new, config, file]):
        click.echo(ctx.get_help())
        ctx.exit(0)

    if not (old and new):
        raise click.UsageError(
            "Provide both --old and --new modpacks for comparison",
        )

    try:
        generate_changelog(old, new, config, file)
        click.secho(f"Changelog successfully generated in '{file}'.", fg="green")
    except FileNotFoundError as error:
        handle_error(error)
    except PermissionError as error:
        handle_error(error)
    except (
        TimeoutError,
        aiohttp.ClientConnectionError,
        aiohttp.ClientResponseError,
    ) as error:
        handle_error(
            error,
            "Unable to connect to the API. This could be due to internet connection issues, API downtime, or incorrect URLs. Please verify and try again.",
        )
    except (
        UnsupportedModpackFormatError,
        DifferentModpackFormatError,
        ModpackFormatError,
        ConfigValidationError,
    ) as error:
        handle_error(error, str(error))
    except Exception as error:
        handle_error(error, f"Unhandled error: {error!r}")


@cli.command(context_settings=CONTEXT_SETTINGS)
def newconfig():
    """Create a new configuration file."""
    try:
        create_config()
        click.secho(
            "A new configuration file has been created successfully.",
            fg="green",
        )
    except Exception as error:
        handle_error(error, "Unable to create a new configuration file.")


if __name__ == "__main__":
    cli()
