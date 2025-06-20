import base64
import binascii
import urllib.parse

def decode_base64(s):
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return "❌ Invalid Base64!"

def decode_hex(s):
    try:
        return bytes.fromhex(s).decode('utf-8')
    except Exception:
        return "❌ Invalid Hex!"

def decode_url(s):
    try:
        return urllib.parse.unquote(s)
    except Exception:
        return "❌ Invalid URL encoding!"

def main():
    print("🔓 DecodeIt - easy application to decode")
    while True:
        print("\nselect options:")
        print("1) Base64 decode")
        print("2) Hex decode")
        print("3) URL decode")
        print("0) leave")

        choice = input("> ").strip()

        if choice == "0":
            print("Bye")
            break

        if choice not in {"1", "2", "3"}:
            print("❌ Invalid selection, please try again.")
            continue

        data = input("paste encoded text:\n> ").strip()

        if choice == "1":
            print("➡️ result:", decode_base64(data))
        elif choice == "2":
            print("➡️ result:", decode_hex(data))
        elif choice == "3":
            print("➡️ result:", decode_url(data))

if __name__ == "__main__":
    main()
