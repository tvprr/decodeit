import base64
import urllib.parse
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def decode_base64(s):
    try:
        return base64.b64decode(s).decode('utf-8'), None
    except Exception:
        return None, "❌ Invalid Base64!"

def decode_hex(s):
    try:
        return bytes.fromhex(s).decode('utf-8'), None
    except Exception:
        return None, "❌ Invalid Hex!"

def decode_url(s):
    try:
        decoded = urllib.parse.unquote(s)
        # Próba zakodowania do utf-8 żeby zweryfikować poprawność
        decoded.encode('utf-8')
        return decoded, None
    except Exception:
        return None, "❌ Invalid URL encoding!"

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
            result, error = decode_base64(data)
        elif choice == "2":
            result, error = decode_hex(data)
        else:
            result, error = decode_url(data)

        if error:
            clear_screen()
            console.print(Panel(f"[bold red]{error}[/bold red]", border_style="red"))
            console.print("[yellow]Press Enter to return to menu...[/yellow]")
            input()
            clear_screen()
            console.print(Panel("[bold cyan]Welcome to DecodeIt - Easy decoding tool[/bold cyan]", expand=False))
            continue

        console.print(Panel("[cyan]➡️ Result:[/cyan]", border_style="cyan"))

        for char in result:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()

if __name__ == "__main__":
    main()
