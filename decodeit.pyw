import customtkinter as ctk
import tkinter.messagebox
import pyperclip
import base64
import binascii
import urllib.parse
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x520")
app.title("DecodeIt v2.5")

# ------------------------- Decode & Encode Logic ----------------------------
def decode_base64(s):
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return None

def decode_hex(s):
    try:
        return bytes.fromhex(s).decode('utf-8')
    except Exception:
        return None

def decode_url(s):
    try:
        return urllib.parse.unquote(s)
    except Exception:
        return None

def encode_base64(s):
    try:
        return base64.b64encode(s.encode()).decode('utf-8')
    except Exception:
        return None

def encode_hex(s):
    try:
        return s.encode('utf-8').hex()
    except Exception:
        return None

def encode_url(s):
    try:
        return urllib.parse.quote(s)
    except Exception:
        return None

def smart_decode(s):
    for func in [decode_base64, decode_hex, decode_url]:
        result = func(s)
        if result: return result
    return None

# ------------------------- GUI Callbacks ----------------------------
history_items = []

def update_result(result):
    result_box.configure(state="normal")
    result_box.delete("0.0", "end")
    result_box.insert("0.0", result)
    result_box.configure(state="disabled")
    pyperclip.copy(result)
    update_history(result)

def handle_decode(func):
    input_text = input_box.get("0.0", "end").strip()
    result = func(input_text)
    if result:
        update_result(result)
    else:
        tkinter.messagebox.showerror("Decode Error", "Invalid encoded input!")
        clear_all()

def handle_encode(func):
    input_text = input_box.get("0.0", "end").strip()
    result = func(input_text)
    if result:
        update_result(result)
    else:
        tkinter.messagebox.showerror("Encode Error", "Invalid input for encoding!")
        clear_all()

def handle_smart():
    input_text = input_box.get("0.0", "end").strip()
    result = smart_decode(input_text)
    if result:
        update_result(result)
    else:
        tkinter.messagebox.showerror("Smart Decode", "Could not determine the encoding type!")
        clear_all()

def clear_all():
    input_box.delete("0.0", "end")
    result_box.configure(state="normal")
    result_box.delete("0.0", "end")
    result_box.configure(state="disabled")

def update_history(result):
    if result and result not in history_items:
        history_items.insert(0, result)
        if len(history_items) > 10:
            history_items.pop()
        refresh_history()

def refresh_history():
    history_box.configure(state="normal")
    history_box.delete("0.0", "end")
    for item in history_items:
        history_box.insert("end", f"- {item}\n")
    history_box.configure(state="disabled")

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "dark" else "dark")

# ------------------------- Tabs ----------------------------
tabs = ctk.CTkTabview(master=app)
tabs.pack(padx=20, pady=20, fill="both", expand=True)

tab_decode = tabs.add("🔓 Decode")
tab_encode = tabs.add("🔒 Encode")
tab_history = tabs.add("🕘 History")
tab_settings = tabs.add("⚙️ Settings")

# ------------------------- Decode Tab ----------------------------
input_label = ctk.CTkLabel(master=tab_decode, text="🔤 Input Text")
input_label.pack(anchor="w")

input_box = ctk.CTkTextbox(master=tab_decode, height=100)
input_box.pack(fill="x", padx=10)

decode_btn_frame = ctk.CTkFrame(master=tab_decode)
decode_btn_frame.pack(pady=10)

ctk.CTkButton(decode_btn_frame, text="Base64", command=lambda: handle_decode(decode_base64)).grid(row=0, column=0, padx=5)
ctk.CTkButton(decode_btn_frame, text="Hex", command=lambda: handle_decode(decode_hex)).grid(row=0, column=1, padx=5)
ctk.CTkButton(decode_btn_frame, text="URL", command=lambda: handle_decode(decode_url)).grid(row=0, column=2, padx=5)
ctk.CTkButton(decode_btn_frame, text="Smart Decode", command=handle_smart).grid(row=0, column=3, padx=5)

result_label = ctk.CTkLabel(master=tab_decode, text="✅ Output")
result_label.pack(anchor="w")

result_box = ctk.CTkTextbox(master=tab_decode, height=100, state="disabled")
result_box.pack(fill="x", padx=10)

# ------------------------- Encode Tab ----------------------------
encode_label = ctk.CTkLabel(master=tab_encode, text="🔤 Input Text")
encode_label.pack(anchor="w")

encode_input = ctk.CTkTextbox(master=tab_encode, height=100)
encode_input.pack(fill="x", padx=10)

encode_btn_frame = ctk.CTkFrame(master=tab_encode)
encode_btn_frame.pack(pady=10)

ctk.CTkButton(encode_btn_frame, text="Base64", command=lambda: handle_encode(encode_base64)).grid(row=0, column=0, padx=5)
ctk.CTkButton(encode_btn_frame, text="Hex", command=lambda: handle_encode(encode_hex)).grid(row=0, column=1, padx=5)
ctk.CTkButton(encode_btn_frame, text="URL", command=lambda: handle_encode(encode_url)).grid(row=0, column=2, padx=5)
ctk.CTkButton(encode_btn_frame, text="Reset", command=clear_all).grid(row=0, column=3, padx=5)

# ------------------------- History Tab ----------------------------
history_box = ctk.CTkTextbox(master=tab_history, state="disabled")
history_box.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------------- Settings Tab ----------------------------
ctk.CTkButton(tab_settings, text="🌓 Toggle Theme", command=toggle_theme).pack(pady=10)
ctk.CTkLabel(tab_settings, text=f"DecodeIt v2.5\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", text_color="gray").pack(pady=10)

app.mainloop()
