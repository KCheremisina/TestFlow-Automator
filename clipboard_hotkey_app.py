import tkinter as tk
import keyboard
import pyperclip

class HotkeyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Магия буфера обмена")
        self.root.geometry("320x160")
        self.root.resizable(False, False)
        
        # Центрируем окно
        self.root.eval('tk::PlaceWindow . center')

        #  Интерфейс 
        self.label1 = tk.Label(root, text="Alt + 1:", font=("Arial", 10, "bold"))
        self.label1.grid(row=0, column=0, padx=15, pady=15, sticky="e")
        
        self.entry1 = tk.Entry(root, width=20, font=("Arial", 10))
        self.entry1.grid(row=0, column=1, padx=10, pady=15)

        self.label2 = tk.Label(root, text="Alt + 2:", font=("Arial", 10, "bold"))
        self.label2.grid(row=1, column=0, padx=15, pady=5, sticky="e")
        
        self.entry2 = tk.Entry(root, width=20, font=("Arial", 10))
        self.entry2.grid(row=1, column=1, padx=10, pady=5)

        self.status = tk.Label(root, text="Ожидание нажатия...", fg="gray", font=("Arial", 9))
        self.status.grid(row=2, column=0, columnspan=2, pady=10)

        self.entry1.insert(0, "admin")
        self.entry2.insert(0, "Admin1!111")
        self.setup_hotkeys()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_status(self, text, color):
        #Обновление статуса (выполняется в главном потоке)
        self.status.config(text=text, fg=color)
        self.root.after(2000, lambda: self.status.config(text="Ожидание нажатия...", fg="gray"))

    def setup_hotkeys(self):
        #Регистрируем горячие клавиши БЕЗОПАСНО
        # ГЛАВНОЕ ИЗМЕНЕНИЕ: мы не читаем поля здесь. 
        # Мы просто отправляем запрос в главный поток через root.after.
        keyboard.add_hotkey('alt+1', lambda: self.root.after(0, self.process_hotkey, self.entry1, "Alt+1"))
        keyboard.add_hotkey('alt+2', lambda: self.root.after(0, self.process_hotkey, self.entry2, "Alt+2"))

    def process_hotkey(self, entry_widget, hotkey_name):
        #Эта функция теперь гарантированно выполняется в главном потоке Tkinter
        # Теперь мы можем безопасно читать текст и работать с буфером
        text = entry_widget.get()
        if text:
            pyperclip.copy(text)
            self.update_status(f"✓ Скопировано ({hotkey_name})", "green")
        else:
            self.update_status(f"✗ Поле {hotkey_name} пустое!", "red")

    def on_closing(self):
        #Чистим хуки при закрытии
        keyboard.unhook_all_hotkeys()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotkeyApp(root)
    root.mainloop()