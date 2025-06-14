import tkinter as tk
import keyboard
from collections import Counter
import threading

# GUI setup
root = tk.Tk()
root.title("Keyboard Analyser")
root.geometry("700x450")
root.configure(bg="#fdf6f0")

# Variablen
keys = []
strgpressed = False
function_keys_enabled = False

sonderzeichen = {
    "space": " ",
    "enter": "\n",
    "tab": "\t",
    "backspace": "⌫",
    "linke windows": "[WIN]",
}

def toggle_function_keys():
    global keys, function_keys_enabled

    function_keys_enabled = not function_keys_enabled

    if function_keys_enabled:
        onoroff_btn.config(bg="#63cd0d", text="Function Keys enabled")
    else:
        onoroff_btn.config(bg="#e51e1e", text="Function Keys disabled")

        # Sonderzeichen aus der Liste entfernen
        keys = [k for k in keys if k not in sonderzeichen]

        # Anzeige aktualisieren
        update_analysis()

def update_analysis():
    analyse = Counter(keys)
    top3 = analyse.most_common(3)

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Tastenanalyse:\n\n")
    for taste, anzahl in analyse.items():
        text_output.insert(tk.END, f"{taste}: {anzahl}\n")

    label_top3_text = "Top 3 meistgedrückte Tasten:\n"
    for taste, anzahl in top3:
        label_top3_text += f"{taste}: {anzahl} Mal\n"
    label_top3.config(text=label_top3_text)

def pressed():
    global strgpressed
    strgpressed = True

def tastenerkennung():
    global strgpressed
    while not strgpressed:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if not function_keys_enabled and event.name in sonderzeichen:
                continue
            keys.append(event.name)
            update_analysis()

# GUI-Elemente
label_info = tk.Label(root, text="Key Analyser", bg="#fdf6f0", font=("Arial", 15, "bold"))
label_info.pack(pady=10)

text_output = tk.Text(root, height=10, width=60, font=("Courier", 12))
text_output.pack(pady=10)

onoroff_btn = tk.Button(root, text="Function Keys disabled", bg="#e51e1e",
                        font=("Arial", 14, "bold"), command=toggle_function_keys)
onoroff_btn.pack(pady=5)

label_top3 = tk.Label(root, text="", bg="#fdf6f0", font=("Arial", 14, "bold"))
label_top3.pack(pady=10)

# STRG+1 als Stop-Hotkey
keyboard.add_hotkey("ctrl+1", pressed)

# Thread starten für Tastenerkennung
threading.Thread(target=tastenerkennung, daemon=True).start()

# GUI starten
root.mainloop()
