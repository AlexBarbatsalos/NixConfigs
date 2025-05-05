from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.spinner import Spinner
from contextlib import contextmanager
import time

console = Console()


## loading animation
@contextmanager
def loading_spinner(text: str = "Working..."):
    with console.status(f"[bold green]{text}[/bold green]", spinner="dots") as status:
        yield



## color formatting
def print_colored_title(title: str):
    console.print(f"\n[bold cyan]{title}[/bold cyan]")

def print_section_divider(label: str):
    console.print(f"[bold green]\n{label}[/bold green]\n" + "=" * 60)


    
def print_error(error: str):
    console.print((f"\n[bold red]{error}[/bold red]"))
    
def print_cancel(message: str):
    console.print((f"\n[bold yellow]{message}[/bold yellow]"))
    
    
## padding/structural formatting

def print_summary_row(label, value, label_color="cyan", value_color="white", pad=22):
    """Prints a summary row with aligned columns and color."""
    label_text = Text(label.ljust(pad), style=label_color)
    value_text = Text(value, style=value_color)
    console.print(label_text + value_text)
