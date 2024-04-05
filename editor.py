import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import json

class WordProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("PAGE MAKER")
        self.root.geometry("680x535")

        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menu de arquivos
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Export", accelerator="Ctrl+E", command=self.export_text_to_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

        # Menu de editar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Change Text Color", command=self.change_text_color)
        self.edit_menu.add_command(label="Change Background Color", command=self.change_bg_color)

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_configure("text_color", foreground=color)
            self.text_area.tag_add("text_color", self.text_area.index(tk.SEL_FIRST), self.text_area.index(tk.SEL_LAST))

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(bg=color)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.root.title(f"Word Processor - {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Word Processor - {file_path}")

    def export_text_to_file(self):
        try:
            # Pede pelo nome e tipo dod arquivo
            export_file = filedialog.asksaveasfilename(
                title="Export File As",
                defaultextension=".json",
                initialfile="Exported_Text.json",
                filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
            )

            # Lista para guardar as informações
            export_data = []

            lines = self.text_area.get("1.0", tk.END).split('\n')[:-1]
            for line_number, line in enumerate(lines, start=1):
                # Extracting color and background color from the tag
                tags = self.text_area.tag_names(f"{line_number}.0")
                color = self.text_area.tag_cget(tags[0], "foreground") if "text_color" in tags else "white"
                background_color = self.text_area.cget("bg")

                export_data.append({
                    "text": line,
                    "color": color,
                    "background_color": background_color
                })

            # Fazendo o JSON
            with open(export_file, "w", encoding="utf-8") as outfile:
                json.dump({"content": export_data}, outfile, ensure_ascii=False, indent=2)

            messagebox.showinfo("Export Successful", "Text exported successfully in JSON format!")
        except Exception as e:
            messagebox.showerror("Export Error", e)

    def exit(self):
        self.root.destroy()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'

if __name__ == "__main__":
    root = tk.Tk()
    text_editor_instance = WordProcessor(root)
    root.mainloop()
