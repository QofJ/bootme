"""CLI entry point for bootme."""

import typer
from enum import Enum
from . import autohotkey
from bootme.colemak import start_colemak_for_oyrx_win, start_colemak_for_qwerty_win

app = typer.Typer(context_settings={'help_option_names': ['-h', '--help']})

class KeyboardType(str, Enum):
    qwerty = 'qwerty'
    oyrx = 'oyrx'

class Platform(str, Enum):
    win = 'win'


@app.command(name="autohotkey")
def autohotkey_cmd() -> None:
    """Install AutoHotkey scripts via TUI."""
    autohotkey.main()

@app.command()
def colemak(
    keyboard: KeyboardType = typer.Argument(KeyboardType.qwerty, help="键盘布局"),
    platform: Platform = typer.Argument(Platform.win, help="操作系统平台")
):
    """使用Colemak键盘字母布局，并相应调整输入"""
    if keyboard == 'qwerty' and platform == 'win':
        start_colemak_for_qwerty_win()
    elif keyboard == 'oyrx' and platform == 'win':
        start_colemak_for_oyrx_win()
    else:
        typer.secho('不支持的keyboard或platform', fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Bootme - AutoHotkey script installation manager."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
