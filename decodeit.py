import base64
import urllib.parse
import time
import os
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

VERSION = "1.9"

class Result:
    def __init__(self, ok=None, err=None):
        self.ok = ok
        self.err = err

    @staticmethod
    def ok(value):
        return Result(ok=value)

    @staticmethod
    def err(error_msg):
        return Result(err=error_msg)

    def is_ok(self):
        return self.err is None

    def is_err(self):
        return self.err is not None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def decode_base64(s):
    try:
        return Result.ok(base64.b64decode(s).decode('utf-8'))
    except Exception:
        return Result.err("Invalid Base64 input.")

def decode_hex(s):
    try:
        return Result.ok(bytes.fromhex(s).decode('utf-8'))
    except Exception:
        return Result.err("Invalid Hex input.")

def decode_url(s):
    try:
        decoded = urllib.parse.unquote(s)
        decoded.encode('utf-8')  # Verify UTF-8
        return Result.ok(decoded)
    except Exception:
        return Result.err("Invalid URL encoding.")

def display_header():
    console.print(Panel(f"[bold cyan]DecodeIt v{VERSION}[/bold cyan]", expand=False))

def display_menu():
    console.print(Panel.fit(
        "[bold yellow]Select an option:[/bold yellow]\n"
        "[green]1)[/green] Base64 decode\n"
        "[green]2)[/green] Hex decode\n"
        "[green]3)[/green] URL decode\n"
        "[green]r)[/green] Repeat last input\n"
        "[green]0)[/green] Exit",
        title="[bold magenta]Menu[/bold magenta]",
        border_style="magenta",
    ))

def main():
    clear_screen()
    display_header()

    last_choice = None
    last_data = None

    while True:
        display_menu()
        choice = Prompt.ask("[bold green]Your choice[/bold green]", choices=["0", "1", "2", "3", "r"])

        if choice == "0":
            console.print("\n[bold magenta]Goodbye![/bold magenta]")
            break

        if choice == "r":
            if not last_choice or not last_data:
                console.print("[red]No previous input to repeat.[/red]")
                continue
            choice = last_choice
            data = last_data
        else:
            data = Prompt.ask("[bold blue]Paste your encoded text[/bold blue]")
            last_choice = choice
            last_data = data

        # Decode based on choice
        if choice == "1":
            result = decode_base64(data)
        elif choice == "2":
            result = decode_hex(data)
        elif choice == "3":
            result = decode_url(data)
        else:
            result = Result.err("Invalid option.")

        if result.is_err():
            clear_screen()
            display_header()
            console.print(Panel(f"[bold red]{result.err}[/bold red]", border_style="red"))
            console.print("[yellow]Press Enter to return to menu...[/yellow]")
            input()
            clear_screen()
            display_header()
            continue

        clear_screen()
        display_header()
        console.print(Panel("[cyan]Decoded Result:[/cyan]", border_style="cyan"))

        for c in result.ok:
            print(c, end='', flush=True)
            time.sleep(0.008)
        print()

        pyperclip.copy(result.ok)
        console.print("\n[green]✔️ Result copied to clipboard.[/green]")

        console.print("\n[yellow]Press Enter to continue...[/yellow]")
        input()
        clear_screen()
        display_header()

if __name__ == "__main__":
    main()
