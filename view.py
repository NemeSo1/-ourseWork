import tkinter as tk
from tkinter import ttk

TRANSLATIONS = {
    "uk": {
        "title": "Книга рецептів",
        "tab_search": "Пошук страв", "tab_manage": "Керування базою",
        "lang_menu": "Мова", "theme_menu": "Тема",
        "light_theme": "Світла", "dark_theme": "Темна",
        "search_btn": "Знайти рецепти", "add_btn": "Додати рецепт", "del_btn": "Видалити",
        "name_lbl": "Назва:", "cat_lbl": "Категорія:", "ing_lbl": "Інгредієнти:",
        "inst_lbl": "Інструкції:", "time_lbl": "Час (хв):", "diff_lbl": "Складність:",
        "easy": "Легко", "medium": "Середньо", "hard": "Складно",
        "avail_ing_lbl": "Включити:", "excl_ing_lbl": "Виключити:",
        "max_time_lbl": "Макс. час:", "search_res_lbl": "Результати",
        "update_btn": "Оновити",
        "save_btn": "Зберегти",
        "cancel_btn": "Скасувати",
        "confirm_del_title": "Підтвердження",
        "confirm_del_msg": "Ви впевнені, що хочете видалити цей рецепт?",
        "error_title": "Помилка",
        "fields_error": "Будь ласка, заповніть всі обов'язкові поля!",
        "categories": ["Сніданок", "Обід", "Вечеря", "Десерт"],
        "app_title": "КНИГА РЕЦЕПТІВ",
        "menu_lang": "Мова",
        "menu_theme": "Тема"
    },
    "en": {
        "title": "Recipe Book",
        "tab_search": "Search", "tab_manage": "Manage DB",
        "lang_menu": "Language", "theme_menu": "Theme",
        "light_theme": "Light", "dark_theme": "Dark",
        "search_btn": "Find Recipes", "add_btn": "Add Recipe", "del_btn": "Delete",
        "name_lbl": "Name:", "cat_lbl": "Category:", "ing_lbl": "Ingredients:",
        "inst_lbl": "Instructions:", "time_lbl": "Time (min):", "diff_lbl": "Difficulty:",
        "easy": "Easy", "medium": "Medium", "hard": "Hard",
        "avail_ing_lbl": "Available:", "excl_ing_lbl": "Exclude:",
        "max_time_lbl": "Max time:", "search_res_lbl": "Results",
        "update_btn": "Update",
        "save_btn": "Save",
        "cancel_btn": "Cancel",
        "confirm_del_title": "Confirm",
        "confirm_del_msg": "Are you sure you want to delete this recipe?",
        "error_title": "Error",
        "fields_error": "Please fill in all fields!",
        "categories": ["Breakfast", "Lunch", "Dinner", "Dessert"],
        "app_title": "RECIPE BOOK",
        "menu_lang": "Language",
        "menu_theme": "Theme"
    }
}

INGREDIENTS_DATA = [
    "курка", "картопля", "помідор", "сир", "яйце", "молоко", "борошно", "цибуля", "часник",
    "огірок", "перець", "морква", "капуста", "гриби", "яловичина", "свинина", "риба", "креветки",
    "рис", "гречка", "макарони", "олія", "масло", "сметана", "вершки", "цукор", "сіль", "мед",
    "яблуко", "банан", "лимон", "зелень", "авокадо", "бекон", "баклажан", "кабачок", "горіхи"
]

class CustomFrame(tk.Frame): pass

class RecipeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = "uk"
        self.t = TRANSLATIONS[self.current_lang]
        self.title(self.t["title"])
        
        self.selected_avail = set()
        self.selected_excl = set()
        self.search_hidden = True 
        
        self.themes = {
            "light": {
                "bg": "#E2E8F0",          
                "surface": "#FFFFFF",     
                "header": "#0F172A",      
                "header_fg": "#FFFFFF",
                "fg": "#1E293B",          
                "fg_muted": "#64748B",    
                "accent": "#4F46E5",      
                "accent_hover": "#4338CA",
                "border": "#CBD5E1",      
                "input_bg": "#F8FAFC",    
                "danger": "#E11D48"       
            },
            "dark": {
                "bg": "#0B0F19",          
                "surface": "#111827",     
                "header": "#080B12",      
                "header_fg": "#FFFFFF",
                "fg": "#F1F5F9",          
                "fg_muted": "#94A3B8",    
                "accent": "#6366F1",      
                "accent_hover": "#4F46E5",
                "border": "#1F2937",      
                "input_bg": "#1F2937",    
                "danger": "#F43F5E"
            }
        }
        self.current_theme = "light"
        
        self._manage_sort_col = None
        self._manage_sort_asc = True
        self._search_sort_col = None
        self._search_sort_asc = True

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_fonts_and_styles()

        self._center_window(1100, 780)
        self.create_menu()
        self._build_header()
        self.create_notebook()
        self.update_ui_text()
        self.apply_theme()

    def _configure_fonts_and_styles(self):
        self.fonts = {
            "main": ("Segoe UI", 10),
            "bold": ("Segoe UI", 10, "bold"),
            "heading": ("Segoe UI", 15, "bold"),
            "logo": ("Segoe UI", 18, "bold"),
            "small": ("Segoe UI", 9)
        }
        
        self.style.configure(".", font=self.fonts["main"])
        
        self.style.configure("TNotebook", borderwidth=0, tabmargins=[20, 10, 0, 0])
        self.style.configure("TNotebook.Tab", font=self.fonts["bold"], padding=[25, 8], borderwidth=0, relief="flat")
        
        self.style.configure("TButton", font=self.fonts["bold"], padding=8, borderwidth=0)
        self.style.configure("Accent.TButton", font=self.fonts["bold"], padding=10, borderwidth=0)
        
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        self.style.configure("Treeview", font=self.fonts["main"], rowheight=35, borderwidth=0)
        self.style.configure("Treeview.Heading", font=self.fonts["bold"], padding=8, borderwidth=0)
        
        self.style.configure("TLabel", font=self.fonts["main"])
        self.style.configure("TEntry", padding=6, borderwidth=0)
        self.style.configure("TCombobox", padding=6, borderwidth=0)

    def create_menu(self):
        menubar = tk.Menu(self, borderwidth=0)
        self.config(menu=menubar)
        
        self.lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🌍 " + self.t["lang_menu"], menu=self.lang_menu)
        
        self.theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎨 " + self.t["theme_menu"], menu=self.theme_menu)

    def _build_header(self):
        c = self.themes[self.current_theme]
        
        self.header_frame = tk.Frame(self, height=60, bg=c["header"])
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        self.lbl_logo = tk.Label(
            self.header_frame, 
            text="🍽  " + self.t["app_title"], 
            font=self.fonts["logo"],
            bg=c["header"],
            fg=c["header_fg"]
        )
        self.lbl_logo.pack(side=tk.LEFT, padx=30, pady=10)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=(10, 20))
        
        self.tab_search = CustomFrame(self.notebook)
        self.tab_manage = CustomFrame(self.notebook)
        
        self.notebook.add(self.tab_search, text=self.t["tab_search"])
        self.notebook.add(self.tab_manage, text=self.t["tab_manage"])
        
        self._build_search_tab()
        self._build_manage_tab()

    # --- Вкладка: ПОШУК (Компактна версія) ---
    def _build_search_tab(self):
        # Зменшено відступи: padx=15, pady=15
        self.search_side_frame = CustomFrame(self.tab_search, padx=15, pady=15)
        self.search_side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=10)

        tk.Label(self.search_side_frame, text="Фільтри", font=self.fonts["heading"]).pack(anchor="w", pady=(0, 10))

        # Маю
        tk.Label(self.search_side_frame, text=self.t["avail_ing_lbl"], font=self.fonts["bold"]).pack(anchor="w")
        self.filter_avail_var = tk.StringVar()
        self.entry_filter_avail = ttk.Entry(self.search_side_frame, textvariable=self.filter_avail_var)
        self.entry_filter_avail.pack(fill=tk.X, pady=(2, 2))
        self.entry_filter_avail.bind("<KeyRelease>", lambda e: self.filter_ingredients("avail"))
        
        self.ing_listbox = tk.Listbox(self.search_side_frame, selectmode=tk.MULTIPLE, exportselection=0, height=3)
        self.ing_listbox.pack(fill=tk.X, pady=(0, 10))

        # Не маю
        tk.Label(self.search_side_frame, text=self.t["excl_ing_lbl"], font=self.fonts["bold"]).pack(anchor="w")
        self.filter_excl_var = tk.StringVar()
        self.entry_filter_excl = ttk.Entry(self.search_side_frame, textvariable=self.filter_excl_var)
        self.entry_filter_excl.pack(fill=tk.X, pady=(2, 2))
        self.entry_filter_excl.bind("<KeyRelease>", lambda e: self.filter_ingredients("excl"))
        
        self.excl_listbox = tk.Listbox(self.search_side_frame, selectmode=tk.MULTIPLE, exportselection=0, height=3)
        self.excl_listbox.pack(fill=tk.X, pady=(0, 10))

        # Повзунок часу
        tk.Label(self.search_side_frame, text=self.t["max_time_lbl"], font=self.fonts["bold"]).pack(anchor="w")
        self.search_time_scale = tk.Scale(self.search_side_frame, from_=5, to=120, orient=tk.HORIZONTAL, resolution=5, sliderlength=15, width=12)
        self.search_time_scale.set(120)
        self.search_time_scale.pack(fill=tk.X, pady=(0, 10))

        # Складність
        tk.Label(self.search_side_frame, text=self.t["diff_lbl"], font=self.fonts["bold"]).pack(anchor="w")
        diff_f = CustomFrame(self.search_side_frame)
        diff_f.pack(fill=tk.X, pady=(2, 10))
        
        self.search_diff_easy, self.search_diff_med, self.search_diff_hard = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
        tk.Checkbutton(diff_f, text="Легко", variable=self.search_diff_easy).pack(side=tk.LEFT, padx=(0,5))
        tk.Checkbutton(diff_f, text="Середньо", variable=self.search_diff_med).pack(side=tk.LEFT, padx=(0,5))
        tk.Checkbutton(diff_f, text="Складно", variable=self.search_diff_hard).pack(side=tk.LEFT)
        
        # --- Фільтр категорій ---
        self.lbl_search_cat_title = tk.Label(self.search_side_frame, text=self.t.get("cat_lbl", "Категорія:"), font=self.fonts["bold"])
        self.lbl_search_cat_title.pack(anchor="w", pady=(10, 0))

        # Фрейм, де будуть з'являтися галочки
        self.cat_checks_frame = tk.Frame(self.search_side_frame, bg=self.themes[self.current_theme]["surface"])
        self.cat_checks_frame.pack(fill=tk.X, pady=5)
        
        # Тут ми будемо зберігати змінні та самі віджети галочок
        self.cat_vars = {}
        
        # Кнопка Знайти прикріплена до НИЗУ (BOTTOM)
        self.btn_search = ttk.Button(self.search_side_frame, text=self.t["search_btn"], style="Accent.TButton")
        self.btn_search.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Права панель
        self.search_main_frame = CustomFrame(self.tab_search, padx=20, pady=20)
        self.search_main_frame.pack(side=tk.LEFT, expand=True, fill="both", pady=10)
        tk.Label(self.search_main_frame, text=self.t["search_res_lbl"], font=self.fonts["heading"]).pack(anchor="w", pady=(0, 10))

        # Додаємо "cat" у список колонок
        self.search_tree = ttk.Treeview(self.search_main_frame, columns=("name", "cat", "time", "diff"), show="headings")
        
        # Налаштовуємо нову колонку
        self.search_tree.heading("name", text=self.t["name_lbl"]); self.search_tree.column("name", width=250)
        self.search_tree.heading("cat", text=self.t["cat_lbl"]); self.search_tree.column("cat", width=120, anchor="center")
        self.search_tree.heading("time", text=self.t["time_lbl"]); self.search_tree.column("time", width=80, anchor="center")
        self.search_tree.heading("diff", text=self.t["diff_lbl"]); self.search_tree.column("diff", width=120, anchor="center")
        
        scr = ttk.Scrollbar(self.search_main_frame, command=self.search_tree.yview); self.search_tree.configure(yscrollcommand=scr.set)
        self.search_tree.pack(side=tk.LEFT, expand=True, fill="both"); scr.pack(side=tk.LEFT, fill=tk.Y)
        
    # --- Вкладка: КЕРУВАННЯ ---
    def _build_manage_tab(self):
        self.form_frame = CustomFrame(self.tab_manage, padx=20, pady=20)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=10)

        # ДОДАНО self.lbl_form_title
        self.lbl_form_title = tk.Label(self.form_frame, text="Додати / Редагувати", font=self.fonts["heading"])
        self.lbl_form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Налаштування відступів для полів форми
        grid_p = {"sticky": "w", "pady": 8}
        
        # ДОДАНО self.lbl_name
        self.lbl_name = tk.Label(self.form_frame, text=self.t['name_lbl'], font=self.fonts["bold"])
        self.lbl_name.grid(row=1, column=0, **grid_p)
        self.entry_name = ttk.Entry(self.form_frame, width=32)
        self.entry_name.grid(row=1, column=1, **grid_p, padx=(10,0))

        # ДОДАНО self.lbl_time
        self.lbl_time = tk.Label(self.form_frame, text=self.t['time_lbl'], font=self.fonts["bold"])
        self.lbl_time.grid(row=2, column=0, **grid_p)
        self.time_scale = tk.Scale(self.form_frame, from_=5, to=120, orient=tk.HORIZONTAL, resolution=5, sliderlength=15, width=12)
        self.time_scale.grid(row=2, column=1, sticky="ew", padx=(10,0))

        # ДОДАНО self.lbl_diff
        self.lbl_diff = tk.Label(self.form_frame, text=self.t['diff_lbl'], font=self.fonts["bold"])
        self.lbl_diff.grid(row=3, column=0, **grid_p)
        
        self.diff_var = tk.StringVar(value="easy")
        radio_f = CustomFrame(self.form_frame)
        radio_f.grid(row=3, column=1, sticky="w", padx=(10,0))
        
        # ДОДАНО self.rb_easy, self.rb_med, self.rb_hard
        self.rb_easy = tk.Radiobutton(radio_f, text=self.t["easy"], variable=self.diff_var, value="easy")
        self.rb_easy.pack(side=tk.LEFT, padx=(0,5))
        self.rb_med = tk.Radiobutton(radio_f, text=self.t["medium"], variable=self.diff_var, value="medium")
        self.rb_med.pack(side=tk.LEFT, padx=(0,5))
        self.rb_hard = tk.Radiobutton(radio_f, text=self.t["hard"], variable=self.diff_var, value="hard")
        self.rb_hard.pack(side=tk.LEFT)

        # ДОДАНО self.lbl_cat
        self.lbl_cat = tk.Label(self.form_frame, text=self.t['cat_lbl'], font=self.fonts["bold"])
        self.lbl_cat.grid(row=4, column=0, **grid_p)
        
        # ВИПРАВЛЕНО: беремо значення зі словника (self.t["categories"])
        self.combo_cat = ttk.Combobox(self.form_frame, values=self.t.get("categories", ["Сніданок", "Обід", "Вечеря", "Десерт"]), state="readonly", width=30)
        self.combo_cat.current(0)
        self.combo_cat.grid(row=4, column=1, **grid_p, padx=(10,0))

        # ДОДАНО self.lbl_ing
        self.lbl_ing = tk.Label(self.form_frame, text=self.t['ing_lbl'], font=self.fonts["bold"])
        self.lbl_ing.grid(row=5, column=0, sticky="nw", pady=(8,0))
        self.entry_ing = ttk.Entry(self.form_frame, width=32)
        self.entry_ing.grid(row=5, column=1, sticky="ew", padx=(10,0), pady=(8,0))

        # ДОДАНО self.lbl_inst
        self.lbl_inst = tk.Label(self.form_frame, text=self.t['inst_lbl'], font=self.fonts["bold"])
        self.lbl_inst.grid(row=6, column=0, sticky="nw", pady=(15,0))
        self.text_inst_frame = CustomFrame(self.form_frame)
        self.text_inst_frame.grid(row=6, column=1, sticky="ew", padx=(10,0), pady=(15,0))
        
        self.text_inst = tk.Text(self.text_inst_frame, height=5, width=30, wrap="word", font=self.fonts["main"])
        scr_t = ttk.Scrollbar(self.text_inst_frame, command=self.text_inst.yview); self.text_inst.configure(yscrollcommand=scr_t.set)
        self.text_inst.pack(side=tk.LEFT, expand=True, fill="both"); scr_t.pack(side=tk.LEFT, fill=tk.Y)

        act_f = CustomFrame(self.form_frame)
        act_f.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        self.btn_add = ttk.Button(act_f, text=self.t["add_btn"], style="Accent.TButton")
        self.btn_add.pack(fill=tk.X, pady=(0, 8))
        self.btn_update = ttk.Button(act_f, text=self.t["update_btn"])
        self.btn_update.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        
        self.btn_delete = ttk.Button(act_f, text=self.t["del_btn"])
        self.btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        
        self.btn_cancel = ttk.Button(act_f, text=self.t.get("cancel_btn", "Скасувати"), command=self.clear_form)
        self.btn_cancel.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Права панель з таблицею
        self.manage_main_frame = CustomFrame(self.tab_manage, padx=20, pady=20)
        self.manage_main_frame.pack(side=tk.LEFT, expand=True, fill="both", pady=10)

        list_header = CustomFrame(self.manage_main_frame)
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        # ДОДАНО self.lbl_base_title
        self.lbl_base_title = tk.Label(list_header, text="База страв", font=self.fonts["heading"])
        self.lbl_base_title.pack(side=tk.LEFT)
        
        self.btn_toggle_search = ttk.Button(list_header, text="🔍 Пошук", command=self._toggle_search_bar)
        self.btn_toggle_search.pack(side=tk.RIGHT)

        self.hidden_search_frame = CustomFrame(self.manage_main_frame)
        
        self.search_ing_var = tk.StringVar()
        self.search_ing_entry = ttk.Entry(self.hidden_search_frame, textvariable=self.search_ing_var, font=self.fonts["main"])
        self.search_ing_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        
        # ДОДАНО self.lbl_search_hint
        self.lbl_search_hint = tk.Label(self.hidden_search_frame, text="Почніть вводити назву...", font=self.fonts["small"], fg="#94A3B8")
        self.lbl_search_hint.pack(side=tk.LEFT)

        # Замість старих 2-х колонок робимо 4
        self.manage_tree = ttk.Treeview(self.manage_main_frame, columns=("name", "cat", "time", "diff"), show="headings")

        # Налаштовуємо заголовки та ширину
        self.manage_tree.heading("name", text=self.t["name_lbl"]); self.manage_tree.column("name", width=200)
        self.manage_tree.heading("cat", text=self.t["cat_lbl"]); self.manage_tree.column("cat", width=120, anchor="center")
        self.manage_tree.heading("time", text=self.t["time_lbl"]); self.manage_tree.column("time", width=80, anchor="center")
        self.manage_tree.heading("diff", text=self.t["diff_lbl"]); self.manage_tree.column("diff", width=100, anchor="center")
        
        scr_m = ttk.Scrollbar(self.manage_main_frame, command=self.manage_tree.yview); self.manage_tree.configure(yscrollcommand=scr_m.set)
        self.manage_tree.pack(side=tk.LEFT, expand=True, fill="both"); scr_m.pack(side=tk.LEFT, fill=tk.Y)
    
    def _toggle_search_bar(self):
        if self.search_hidden:
            self.hidden_search_frame.pack(fill=tk.X, before=self.manage_tree, pady=(0, 10))
            self.search_ing_entry.focus()
            self.btn_toggle_search.config(text="✕ Закрити пошук")
        else:
            self.search_ing_var.set("") 
            self.hidden_search_frame.pack_forget()
            self.btn_toggle_search.config(text="🔍 Пошук")
        self.search_hidden = not self.search_hidden

    def set_tree_heading(self, tree_key, col, text, command):
        tree = self.manage_tree if tree_key == "manage" else self.search_tree
        cur_col = self._manage_sort_col if tree_key == "manage" else self._search_sort_col
        cur_asc = self._manage_sort_asc if tree_key == "manage" else self._search_sort_asc
        arrow = " ▲" if cur_asc else " ▼" if col == cur_col else ""
        tree.heading(col, text=text + arrow, command=command)

    def apply_theme(self):
        c = self.themes[self.current_theme]
        
        # Основний фон вікна
        self.config(bg=c["bg"])
        
        # Верхня панель (Header) та Логотип
        if hasattr(self, 'header_frame'):
            self.header_frame.config(bg=c["header"])
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.config(bg=c["header"], fg=c["header_fg"])
        
        # Налаштування стилів ttk (Notebook, Treeview, Buttons)
        self.style.configure("TNotebook", background=c["bg"])
        self.style.configure("TNotebook.Tab", background=c["border"], foreground=c["fg"])
        self.style.map("TNotebook.Tab", 
                       background=[("selected", c["surface"])], 
                       foreground=[("selected", c["accent"])])
        
        self.style.configure("Treeview", 
                             background=c["surface"], 
                             fieldbackground=c["surface"], 
                             foreground=c["fg"])
        self.style.map("Treeview", 
                       background=[("selected", c["accent"])], 
                       foreground=[("selected", c["header_fg"])])
        self.style.configure("Treeview.Heading", background=c["bg"], foreground=c["fg_muted"])
        
        self.style.configure("TLabel", foreground=c["fg"], background=c["surface"])
        self.style.configure("TCheckbutton", foreground=c["fg"], background=c["surface"])
        self.style.configure("TRadiobutton", foreground=c["fg"], background=c["surface"])
        
        # Кнопки
        self.style.configure("TButton", background=c["border"], foreground=c["fg"])
        self.style.map("TButton", background=[("active", c["input_bg"])])
        
        # Акцентна кнопка (твоя фіолетова "Add/Save")
        self.style.configure("Accent.TButton", background=c["accent"], foreground=c["header_fg"])
        self.style.map("Accent.TButton", background=[("active", c["accent_hover"])])
        
        # Рекурсивне оновлення звичайних віджетів (Entry, Text і т.д.)
        self._style_widgets(self)

    def _style_widgets(self, widget, current_bg=None):
        c = self.themes[self.current_theme]
        
        if isinstance(widget, CustomFrame): bg = c["surface"]
        elif widget == self.header_frame: bg = c["header"]
        elif isinstance(widget, (tk.Tk, ttk.Notebook)) or (isinstance(widget, tk.Frame) and not current_bg): bg = c["bg"]
        else: bg = current_bg

        try:
            if isinstance(widget, (tk.Frame, CustomFrame)) and widget != self.header_frame:
                widget.config(bg=bg)
            elif isinstance(widget, (tk.Label, tk.Radiobutton, tk.Checkbutton)) and widget not in (self.lbl_logo, self.lbl_subtitle):
                widget.config(bg=bg, fg=c["fg"], selectcolor=bg, activebackground=bg, activeforeground=c["fg"])
            elif isinstance(widget, tk.Scale):
                widget.config(bg=bg, fg=c["fg"], highlightthickness=0, troughcolor=c["input_bg"], activebackground=c["accent"])
            elif isinstance(widget, (tk.Listbox, tk.Text)):
                widget.config(bg=c["input_bg"], fg=c["fg"], borderwidth=0, highlightthickness=1, 
                              highlightbackground=c["border"], highlightcolor=c["accent"],
                              selectbackground=c["accent"], selectforeground=c["header_fg"], relief="flat", padx=3, pady=3)
        except: pass
        
        for child in widget.winfo_children():
            self._style_widgets(child, bg)
            

    def update_ui_text(self):
        self.t = TRANSLATIONS[self.current_lang]
        self.title(self.t["title"])
        self.lang_menu.entryconfig(0, label="Українська"); self.lang_menu.entryconfig(1, label="English")
        self.theme_menu.entryconfig(0, label=self.t["light_theme"]); self.theme_menu.entryconfig(1, label=self.t["dark_theme"])
        self.notebook.tab(0, text=self.t["tab_search"]); self.notebook.tab(1, text=self.t["tab_manage"])
        
        # 1. Оновлюємо головний заголовок (лого)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.config(text="🍽  " + self.t["app_title"])
            
        # 2. Оновлюємо верхнє меню (Мова та Тема)
        # У Tkinter індекси меню зазвичай починаються з 1
        if hasattr(self, 'menu_bar'):
            try:
                self.menu_bar.entryconfig(1, label=self.t["menu_lang"])
                self.menu_bar.entryconfig(2, label=self.t["menu_theme"])
            except:
                # Якщо індекси інші, спробуй 0 та 1
                self.menu_bar.entryconfig(0, label=self.t["menu_lang"])
                self.menu_bar.entryconfig(1, label=self.t["menu_theme"])

        # Статичні заголовки
        self.lbl_form_title.config(text="Додати / Редагувати" if self.current_lang == "uk" else "Add / Edit")
        self.lbl_base_title.config(text="База страв" if self.current_lang == "uk" else "Recipe Base")
        self.btn_toggle_search.config(text="🔍 Пошук" if self.current_lang == "uk" else "🔍 Search")
        self.lbl_search_hint.config(text="Почніть вводити назву..." if self.current_lang == "uk" else "Start typing name...")
        
        # Поля форми
        self.lbl_name.config(text=self.t["name_lbl"])
        self.lbl_time.config(text=self.t["time_lbl"])
        self.lbl_diff.config(text=self.t["diff_lbl"])
        self.lbl_cat.config(text=self.t["cat_lbl"])
        self.lbl_ing.config(text=self.t["ing_lbl"])
        self.lbl_inst.config(text=self.t["inst_lbl"])
        
        # Кнопки
        current_add_text = self.btn_add.cget("text")
        if current_add_text in ["Зберегти", "Save"]:
            self.btn_add.config(text=self.t["save_btn"])
        else:
            self.btn_add.config(text=self.t["add_btn"])
            
        self.btn_update.config(text=self.t["update_btn"])
        self.btn_delete.config(text=self.t["del_btn"])
        
        # Радіокнопки
        self.rb_easy.config(text=self.t["easy"])
        self.rb_med.config(text=self.t["medium"])
        self.rb_hard.config(text=self.t["hard"])

        # --- Комбобокс категорій (ВИПРАВЛЕНО ТУТ) ---
        current_idx = self.combo_cat.current()
        # Безпечно беремо список категорій, якщо його раптом немає у словнику - даємо дефолтний
        self.combo_cat['values'] = self.t.get("categories", ["Сніданок", "Обід", "Вечеря", "Десерт"])
        if current_idx >= 0:
            self.combo_cat.current(current_idx)
        
        # Оновлення списків
        self.ing_listbox.delete(0, tk.END); self.excl_listbox.delete(0, tk.END)
        for ing in INGREDIENTS_DATA:
            self.ing_listbox.insert(tk.END, ing); self.excl_listbox.insert(tk.END, ing)
                      
    def filter_ingredients(self, mode):
        query = self.filter_avail_var.get().lower() if mode == "avail" else self.filter_excl_var.get().lower()
        lb = self.ing_listbox if mode == "avail" else self.excl_listbox
        selected_set = self.selected_avail if mode == "avail" else self.selected_excl
        
        for i in lb.curselection(): selected_set.add(lb.get(i))
            
        lb.delete(0, tk.END)
        for ing in INGREDIENTS_DATA:
            if query in ing.lower():
                lb.insert(tk.END, ing)
                if ing in selected_set: lb.selection_set(tk.END)
                
    def update_category_widgets(self, categories):
        # Очищаємо фрейм
        for widget in self.cat_checks_frame.winfo_children():
            widget.destroy()
        
        self.cat_vars = {}
        
        # Використовуємо .grid() замість .pack() для створення 2-х колонок
        for i, cat in enumerate(categories):
            var = tk.BooleanVar(value=False)
            self.cat_vars[cat] = var
            
            cb = tk.Checkbutton(
                self.cat_checks_frame, 
                text=cat, 
                variable=var,
                bg=self.themes[self.current_theme]["surface"],
                fg=self.themes[self.current_theme]["fg"],
                selectcolor=self.themes[self.current_theme]["input_bg"],
                activebackground=self.themes[self.current_theme]["surface"]
            )
            # row=i//2 (ціла частина) дає номер рядка, column=i%2 (залишок) дає 0 або 1
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=5, pady=2)

    def fill_form(self, r):
        self.clear_form()
        self.entry_name.insert(0, r["name"]); self.time_scale.set(r["time"]); self.diff_var.set(r["difficulty"])
        self.combo_cat.set(r["category"]); self.entry_ing.insert(0, ", ".join(r["ingredients"]))
        self.text_inst.insert("1.0", r["instructions"])
        self.btn_add.config(text=self.t["save_btn"]) 

    def get_form_data(self):
        return {
            "name": self.entry_name.get().strip(), "time": self.time_scale.get(),
            "difficulty": self.diff_var.get(), "category": self.combo_cat.get(),
            "ingredients": self.entry_ing.get().strip(), "instructions": self.text_inst.get("1.0", tk.END).strip()
        }

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_ing.delete(0, tk.END)
        self.text_inst.config(state="normal")
        self.text_inst.delete("1.0", tk.END)
        self.time_scale.set(30)
        self.combo_cat.set("") # Очищаємо комбобокс категорії
        self.diff_var.set("Easy")
        
        # Повертаємо кнопці оригінальний текст "Додати" через словник
        self.btn_add.config(text=self.t.get("add_btn", "Додати рецепт"))
        
    def _center_window(self, width, height):
        self.geometry(f"{width}x{height}+{int((self.winfo_screenwidth()/2)-(width/2))}+{int((self.winfo_screenheight()/2)-(height/2))}")

    def show_custom_details_dialog(self, r):
        c = self.themes[self.current_theme]
        d = tk.Toplevel(self)
        d.title(r["name"]); d.geometry("450x600"); d.config(bg=c["surface"])
        
        tk.Label(d, text=r["name"], font=self.fonts["logo"], fg=c["accent"], bg=c["surface"]).pack(pady=(25, 5))
        
        # --- Спрощена логіка (в базі тепер завжди українська) ---
        saved_cat = r.get('category', 'Інше')
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Other"]
        
        if self.current_lang == "en" and saved_cat in cats_uk:
            display_cat = cats_en[cats_uk.index(saved_cat)]
        else:
            display_cat = saved_cat
        # --------------------------------------------------------
        
        time_text = "хв" if self.current_lang == "uk" else "min"
        
        tk.Label(d, text=f"⏱ {r['time']} {time_text}   •   📊 {self.t.get(r['difficulty'], r['difficulty'])}   •   🍽 {display_cat}", 
                 font=self.fonts["bold"], bg=c["surface"], fg=c["fg_muted"]).pack(pady=(0, 20))
        
        tk.Label(d, text=self.t['ing_lbl'], font=self.fonts["heading"], bg=c["surface"], fg=c["fg"]).pack(anchor="w", padx=30)
        
        ing_text = " • " + "\n • ".join(r['ingredients'])
        tk.Label(d, text=ing_text, wraplength=400, justify="left", font=self.fonts["main"], bg=c["surface"], fg=c["fg"]).pack(anchor="w", padx=40, pady=(10, 20))
        
        tk.Label(d, text=self.t['inst_lbl'], font=self.fonts["heading"], bg=c["surface"], fg=c["fg"]).pack(anchor="w", padx=30)
        
        t_frame = CustomFrame(d, padx=30, pady=10)
        t_frame.pack(fill=tk.BOTH, expand=True)
        tbox = tk.Text(t_frame, bg=c["input_bg"], fg=c["fg"], wrap="word", height=8, borderwidth=0, font=self.fonts["main"], padx=10, pady=10)
        
        scr_d = ttk.Scrollbar(t_frame, command=tbox.yview); tbox.configure(yscrollcommand=scr_d.set)
        tbox.insert("1.0", r["instructions"]); tbox.config(state="disabled")
        tbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); scr_d.pack(side=tk.LEFT, fill=tk.Y)
        
        # Переклали і кнопку "Закрити"
        close_text = "Закрити" if self.current_lang == "uk" else "Close"
        ttk.Button(d, text=close_text, style="Accent.TButton", command=d.destroy).pack(pady=20, padx=30, fill=tk.X)