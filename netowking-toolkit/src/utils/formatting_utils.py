from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

def print_colored_title(title: str):
    console.print(f"\n[bold cyan]{title}[/bold cyan]")

def print_section_divider(label: str):
    console.print(f"[bold green]\n{label}[/bold green]\n" + "=" * 60)

def print_table(headers, rows):
    table = Table(show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*row)
    console.print(table)
    
def print_error(error: str):
    console.print((f"\n[bold red]{error}[/bold red]"))
