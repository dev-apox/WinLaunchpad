import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
import threading
import ctypes
from ctypes import wintypes

class LaunchpadDefinitivo:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg='#050505')
        self.root.attributes("-alpha", 0.98)
        
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(self.base_path, "icons")
        
        if not os.path.exists(self.icons_dir):
            os.makedirs(self.icons_dir)

        self.all_apps = []
        self.pages = []
        self.current_page = 0
        self.apps_per_page = 24
        
        self.icon_cache = {}
        self.colors = ["#FF3B30", "#FF9500", "#FFCC00", "#4CD964", "#5AC8FA", "#007AFF", "#5856D6", "#FF2D55"]

        self.root.bind("<Escape>", lambda e: self.root.withdraw())
        self.root.bind("<MouseWheel>", self.on_mousewheel)
        
        self.setup_ui()
        
        threading.Thread(target=self.load_apps, daemon=True).start()
        self.start_hotkey_listener()

    def start_hotkey_listener(self):
        def listener():
            user32 = ctypes.windll.user32
            if not user32.RegisterHotKey(None, 99, 1, 0x51): # ALT+Q
                return
                
            msg = wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == 0x0312:
                    self.root.after(0, self.toggle_visibility)
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
                
        threading.Thread(target=listener, daemon=True).start()

    def toggle_visibility(self):
        if self.root.winfo_viewable():
            self.root.withdraw()
        else:
            self.root.deiconify()
            self.root.attributes("-topmost", True)
            self.root.focus_force()
            self.search_entry.delete(0, tk.END)
            self.search_entry.focus_set()

    def get_icon(self, app_name, size=90):
        app_name_lower = app_name.lower().strip()
        if app_name_lower in self.icon_cache:
            return self.icon_cache[app_name_lower]

        words = app_name_lower.split()
        names_to_try = [app_name_lower]
        if len(words) >= 2: names_to_try.append(f"{words[0]} {words[1]}")
        if len(words) >= 1: names_to_try.append(words[0])

        for name in names_to_try:
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_', '+'))
            for ext in [".png", ".icns", ".jpg"]:
                path = os.path.join(self.icons_dir, safe_name + ext)
                if os.path.exists(path):
                    try:
                        img = Image.open(path).convert("RGBA")
                        img = img.resize((size, size), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.icon_cache[app_name_lower] = photo
                        return photo
                    except:
                        continue
        return None

    def load_apps(self):
        # Percorsi standard Windows
        paths = [
            os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["AppData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["USERPROFILE"], "Desktop"),
            os.path.join(os.environ["PUBLIC"], "Desktop")
        ]
        
        # AGGIUNGI QUI I TUOI DISCHI (D:, E:, ecc.)
        cartelle_extra = [
            r"D:\Giochi", 
            r"D:\Programmi",
            r"D:\SteamLibrary\steamapps\common"
        ]
        
        for cp in cartelle_extra:
            if os.path.exists(cp):
                paths.append(cp)
        
        bad_words = ["uninstall", "disinstalla", "help", "manual", "readme", "setup", "update"]
        temp_apps = []
        seen_names = set()
        
        for p in paths:
            if not os.path.exists(p): continue
            for root, dirs, files in os.walk(p):
                if root[len(p):].count(os.sep) > 3:
                    dirs.clear()
                    continue
                
                for f in files:
                    if f.lower().endswith((".lnk", ".url", ".exe")):
                        name = f.rsplit('.', 1)[0]
                        name_lower = name.lower()
                        
                        if any(bw in name_lower for bw in bad_words): continue
                        if name_lower in seen_names: continue
                        
                        temp_apps.append({'name': name, 'path': os.path.join(root, f)})
                        seen_names.add(name_lower)
        
        self.all_apps = sorted(temp_apps, key=lambda x: x['name'].lower())
        self.pages = [self.all_apps[i:i + self.apps_per_page] for i in range(0, len(self.all_apps), self.apps_per_page)]
        self.root.after(0, self.render_page)

    def setup_ui(self):
        self.header = tk.Frame(self.root, bg='#050505', pady=30)
        self.header.pack(fill="x")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        self.search_entry = tk.Entry(self.header, textvariable=self.search_var, font=("Segoe UI", 22),
                                   bg="#1a1a1a", fg="white", bd=0, justify="center", width=25, insertbackground="white")
        self.search_entry.pack()
        self.grid_container = tk.Frame(self.root, bg='#050505')
        self.grid_container.pack(expand=True)
        self.footer = tk.Frame(self.root, bg='#050505', pady=20)
        self.footer.pack(fill="x")
        
        # Frecce laterali
        self.btn_prev = tk.Label(self.root, text="<", font=("Segoe UI Bold", 50), bg="#050505", fg="#444", cursor="hand2")
        self.btn_prev.place(relx=0.04, rely=0.5, anchor="center")
        self.btn_prev.bind("<Button-1>", lambda e: self.change_page(-1))
        
        self.btn_next = tk.Label(self.root, text=">", font=("Segoe UI Bold", 50), bg="#050505", fg="#444", cursor="hand2")
        self.btn_next.place(relx=0.96, rely=0.5, anchor="center")
        self.btn_next.bind("<Button-1>", lambda e: self.change_page(1))
        
        self.close_btn = tk.Label(self.root, text="Close", font=("Segoe UI", 12, "bold"), bg="#050505", fg="#444444", cursor="hand2")
        self.close_btn.place(relx=0.98, rely=0.02, anchor="ne")
        self.close_btn.bind("<Button-1>", lambda e: self.quit_app())
        
        self.firma = tk.Label(self.root, text="made by DenisDev", font=("Segoe UI", 11, "italic"), bg="#050505", fg="#555555")
        self.firma.place(relx=0.99, rely=0.99, anchor="se")

    def render_page(self, filtered_list=None):
        for w in self.grid_container.winfo_children(): w.destroy()
        for w in self.footer.winfo_children(): w.destroy()
        
        display_list = filtered_list if filtered_list is not None else (self.pages[self.current_page] if self.pages else [])
        
        if not display_list:
            tk.Label(self.grid_container, text="Nessuna app trovata", fg="#444", bg="#050505", font=("Segoe UI", 20)).pack()
            return

        for i, app in enumerate(display_list):
            r, c = divmod(i, 6)
            frame = tk.Frame(self.grid_container, bg='#050505', padx=25, pady=20)
            frame.grid(row=r, column=c)
            
            img = self.get_icon(app['name'])
            if img:
                icon = tk.Label(frame, image=img, bg="#050505", cursor="hand2")
                icon.image = img
            else:
                iniziale = app['name'][0].upper()
                colore_bg = self.colors[sum(ord(char) for char in app['name']) % len(self.colors)]
                icon = tk.Label(frame, text=iniziale, font=("Segoe UI Bold", 36), bg=colore_bg, fg="white", width=3, height=1, cursor="hand2")
            
            icon.pack()
            lbl = tk.Label(frame, text=app['name'][:14], font=("Segoe UI", 10), bg="#050505", fg="#aaa")
            lbl.pack(pady=10)
            
            for w in [frame, icon, lbl]:
                w.bind("<Button-1>", lambda e, p=app['path']: self.launch(p))
                w.bind("<Enter>", lambda e, f=frame: f.config(bg="#151515"))
                w.bind("<Leave>", lambda e, f=frame: f.config(bg="#050505"))

        if filtered_list is None:
            dot_f = tk.Frame(self.footer, bg='#050505')
            dot_f.pack(expand=True)
            for i in range(len(self.pages)):
                color = "white" if i == self.current_page else "#333"
                tk.Label(dot_f, text="•", fg=color, bg="#050505", font=("Arial", 24)).pack(side="left", padx=10)

    def change_page(self, step):
        new_page = self.current_page + step
        if 0 <= new_page < len(self.pages):
            self.current_page = new_page
            self.render_page()

    def on_mousewheel(self, event):
        if self.search_var.get(): return
        if event.delta < 0: self.change_page(1)
        elif event.delta > 0: self.change_page(-1)

    def on_search(self, *args):
        q = self.search_var.get().lower().strip()
        if not q: 
            self.render_page()
            self.btn_prev.place(relx=0.04, rely=0.5, anchor="center")
            self.btn_next.place(relx=0.96, rely=0.5, anchor="center")
        else:
            filtered = [a for a in self.all_apps if q in a['name'].lower()]
            self.render_page(filtered[:24])
            self.btn_prev.place_forget()
            self.btn_next.place_forget()

    def launch(self, path):
        try:
            os.startfile(path)
            self.root.withdraw()
        except: pass

    def quit_app(self):
        try: ctypes.windll.user32.UnregisterHotKey(None, 99)
        except: pass
        self.root.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaunchpadDefinitivo(root)
    root.mainloop()