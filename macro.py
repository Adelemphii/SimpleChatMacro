from pynput import keyboard
import tkinter as tk
from tkinter import messagebox

import time

class ChatMacroApp:
    def __init__(self, root):
        super().__init__()

        self.root = root
        self.root.title("Adele's Simple Chat Macro")
        self.kb_controller = keyboard.Controller()
        self.macro_trigger = keyboard.Key.f3  # Default trigger
        self.exit_combination = set([keyboard.Key.alt_l, keyboard.Key.right])
        self.held_keys = set()
        self.uwu_pastes = set([
            "uwu", "UwU", "owo", "OwO", ">.>", "<.<", "-_-",
            "^-^", "v.v", "UwO", ":*", ":3", "~-~", "x3", "X3",
            ":)"
        ])
        self.recent_pastes = set()
        self.send_shift_enter = tk.BooleanVar(value=False)  # Toggle to send Shift + Enter at the beginning of the paste

        # Set the window icon and taskbar icon
        self.set_window_icon("icon.png")
        self.set_taskbar_icon("icon.ico")

        self.setup_gui()
        self.setup_keyboard_listener()

    def set_window_icon(self, icon_path):
        try:
            icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Failed to set window icon: {str(e)}")

    def set_taskbar_icon(self, icon_path):
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set taskbar icon: {str(e)}")

    def setup_gui(self):
        # Set minimum window size
        self.root.minsize(500, 500)

        # Styling
        self.root.geometry("500x500")  # Set the window size
        self.root.configure(bg="#f0f0f0")  # Set background color

        # GUI elements for current uwu_pastes
        self.current_pastes_label = tk.Label(
            self.root,
            text="Current chat pastes:",
            font=("Arial", 12),
            bg="#f0f0f0",
        )
        self.current_pastes_label.pack(pady=10)

        self.current_pastes_display = tk.Label(
            self.root,
            text=", ".join(self.uwu_pastes),
            font=("Arial", 10),
            bg="#f0f0f0",
        )
        self.current_pastes_display.pack()

        # GUI elements for pastes
        self.paste_label = tk.Label(
            self.root,
            text="Enter new pastes (comma-separated):",
            font=("Arial", 12),
            bg="#f0f0f0",
        )
        self.paste_label.pack(pady=10)

        self.paste_entry = tk.Entry(
            self.root,
            font=("Arial", 10),
        )
        self.paste_entry.pack()

        self.update_button = tk.Button(
            self.root,
            text="Update Pastes",
            command=self.update_pastes,
            font=("Arial", 10),
            bg="#007acc",
            fg="white",
        )
        self.update_button.pack(pady=10)

        # GUI elements for current macro_trigger
        self.current_trigger_label = tk.Label(
            self.root,
            text="Current macro_trigger:",
            font=("Arial", 12),
            bg="#f0f0f0",
        )
        self.current_trigger_label.pack(pady=10)

        self.current_trigger_display = tk.Label(
            self.root,
            text=str("(" + self.macro_trigger.name + ")"),
            font=("Arial", 10),
            bg="#f0f0f0",
        )
        self.current_trigger_display.pack()

        # GUI elements for trigger key
        self.trigger_label = tk.Label(
            self.root,
            text="Enter trigger key (e.g., shift_r):",
            font=("Arial", 12),
            bg="#f0f0f0",
        )
        self.trigger_label.pack(pady=10)

        self.trigger_entry = tk.Entry(
            self.root,
            font=("Arial", 10),
        )
        self.trigger_entry.pack()

        self.trigger_button = tk.Button(
            self.root,
            text="Update Trigger",
            command=self.update_trigger,
            font=("Arial", 10),
            bg="#007acc",
            fg="white",
        )
        self.trigger_button.pack(pady=10)

        # GUI elements for the UwU speak button
        self.uwu_button = tk.Button(
            self.root,
            text="Convert to UwU",
            command=self.update_uwu_speak,
            font=("Arial", 10),
            bg="#007acc",
            fg="white",
        )
        self.uwu_button.pack(pady=10)

        # Toggle button for Shift + Enter combo
        self.toggle_shift_enter = tk.Checkbutton(
            self.root,
            text="Send paste into ALL chat",
            variable=self.send_shift_enter,
            font=("Arial", 10),
            bg="#f0f0f0",
            onvalue=True,
            offvalue=False,
        )
        self.toggle_shift_enter.pack(pady=10)

    def setup_keyboard_listener(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()

    def matches_exit_combination(self):
        if self.exit_combination.issubset(self.held_keys):
            print("Exiting!")
            self.root.quit()

    def on_press(self, key):
        if not key in self.held_keys:
            self.held_keys.add(key)
        if self.matches_exit_combination():
            return False

    def on_release(self, key):
        if key == self.macro_trigger:
            self.triggerMacro()
        if key in self.held_keys:
            self.held_keys.remove(key)

    def triggerMacro(self):
        random_paste = self.selectRandomPaste()
        print(random_paste)
        self.sendPaste(random_paste)

    def selectRandomPaste(self):
        if not self.uwu_pastes:
            for value in self.recent_pastes:
                self.uwu_pastes.add(value)
            self.recent_pastes.clear()
        random_phrase = self.uwu_pastes.pop()
        self.recent_pastes.add(random_phrase)
        return random_phrase

    def sendPaste(self, paste: str):
        if self.send_shift_enter.get():
            self.kb_controller.press(keyboard.Key.shift)
            self.kb_controller.press(keyboard.Key.enter)
            self.kb_controller.release(keyboard.Key.shift)
        else:
            self.kb_controller.press(keyboard.Key.enter)
        time.sleep(0.09)
        self.kb_controller.type(paste + "\n")
        print("Pasted {0}!".format(paste))

    def update_pastes(self):
        new_pastes = self.paste_entry.get().split(',')
        if not new_pastes or not self.paste_entry.get():
            messagebox.showerror("Empty Field", "Please enter new pastes.")
        else:
            self.uwu_pastes.clear()
            self.uwu_pastes.update(new_pastes)
            self.current_pastes_display.config(text=", ".join(self.uwu_pastes))

    def update_trigger(self):
        trigger_key = self.trigger_entry.get()
        try:
            self.macro_trigger = getattr(keyboard.Key, trigger_key)
            self.current_trigger_display.config(text=str("(" + self.macro_trigger.name + ")"))
        except AttributeError:
            messagebox.showerror("Invalid Key", "Invalid key name: {0}".format(trigger_key))

    def update_uwu_speak(self):
        self.convert_widgets_to_uwu(self.root)

    def convert_widgets_to_uwu(self, widget):
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Button):
            text = widget.cget("text")
            widget.config(text=self.uwu_speak(text))
        for child in widget.winfo_children():
            self.convert_widgets_to_uwu(child)

    def uwu_speak(self, text):
        # Define UwU replacements
        uwu_replacements = {
            'r': 'w',
            'l': 'w',
            'th': 'f',
        }

        # Split text by spaces
        words = text.split()

        # Apply UwU replacements to words outside of parentheses
        for i, word in enumerate(words):
            if '(' not in word and ')' not in word:
                for key, value in uwu_replacements.items():
                    word = word.replace(key, value)
                words[i] = word

        # Join the words back into a single string
        return ' '.join(words)

if __name__ == "__main__":
    window = tk.Tk()  # Create the Tkinter window here
    app = ChatMacroApp(window)
    window.mainloop()