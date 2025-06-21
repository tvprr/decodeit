import base64
import urllib.parse
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

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
        return Result.err("❌ Invalid Base64!")

def decode_hex(s):
    try:
        return Result.ok(bytes.fromhex(s).decode('utf-8'))
    except Exception:
        return Result.err("❌ Invalid Hex!")

def decode_url(s):
    try:
        decoded = urllib.parse.unquote(s)
        decoded.encode('utf-8')  # Ensure it's valid UTF-8
        return Result.ok(decoded)
    except Exception:
        return Result.err("❌ Invalid URL encoding!")

def main():
    clear_screen()
    console.print(Panel("[bold cyan]Welcome to DecodeIt - Easy decoding tool[/bold cyan]", expand=False))

    while True:
        console.print(Panel.fit(
            "\n[bold yellow]Select an option:[/bold yellow]\n"
            "[green]1)[/green] Base64 decode\n"
            "[green]2)[/green] Hex decode\n"
            "[green]3)[/green] URL decode\n"
            "[green]0)[/green] Exit\n",
            title="[bold magenta]Menu[/bold magenta]",
            border_style="magenta",
        ))

        choice = Prompt.ask("[bold green]Your choice[/bold green]", choices=["0", "1", "2", "3"])

        if choice == "0":
            console.print("\n[bold magenta]👋 Goodbye![/bold magenta]")
            break

        data = Prompt.ask("[bold blue]Paste your encoded text[/bold blue]")

        if choice == "1":
            result = decode_base64(data)
        elif choice == "2":
            result = decode_hex(data)
        else:
            result = decode_url(data)

        if result.is_err():
            clear_screen()
            console.print(Panel(f"[bold red]{result.err}[/bold red]", border_style="red"))
            console.print("[yellow]Press Enter to return to menu...[/yellow]")
            input()
            clear_screen()
            console.print(Panel("[bold cyan]Welcome to DecodeIt - Easy decoding tool[/bold cyan]", expand=False))
            continue

        # Display result with nice animation
        console.print(Panel("[cyan]➡️ Result:[/cyan]", border_style="cyan"))
        for char in result.ok:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()

if __name__ == "__main__":
    main()
