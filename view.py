import tkinter as tk
from tkinter import ttk

TRANSLATIONS = {
    "uk": {
        "title": "Книга рецептів",
        "app_title": "КНИГА РЕЦЕПТІВ",
        "tab_search": "Пошук страв", "tab_manage": "Керування базою",
        "menu_lang": "Мова", "menu_theme": "Тема",
        "lang_menu": "Мова", "theme_menu": "Тема",
        "light_theme": "Світла", "dark_theme": "Темна",
        "menu_fav": "⭐ Улюблені",
        "fav_win_title": "Мої улюблені страви",
        "fav_win_header": "⭐ Улюблені рецепти",
        "fav_empty": "Список порожній",
        
        "menu_help": "Довідка",
        "help_about": "Про програму",
        "help_shortcuts": "Гарячі клавіші",
        "about_text": "📖 Книга рецептів\nВерсія 1.0",
        "shortcuts_text": "Ctrl+S — зберегти рецепт\nCtrl+N — очистити форму\nDelete — видалити вибраний рецепт\nПодвійний клік — відкрити деталі рецепту",

        
        "search_btn": "Знайти рецепти", "add_btn": "Додати рецепт", "del_btn": "Видалити",
        "update_btn": "Оновити", "save_btn": "Зберегти", "cancel_btn": "Скасувати",
        
        "name_lbl": "Назва:", "cat_lbl": "Категорія:", "ing_lbl": "Інгредієнти:",
        "inst_lbl": "Інструкції:", "time_lbl": "Час (хв):", "diff_lbl": "Складність:",
        
        "easy": "Легко", "medium": "Середньо", "hard": "Складно",
        "avail_ing_lbl": "Включити:", "excl_ing_lbl": "Виключити:",
        "max_time_lbl": "Макс. час:", 
        
        "filters_lbl": "Фільтри", "search_res_lbl": "Результати",
        "add_edit_lbl": "Додати / Редагувати", "base_title_lbl": "База страв",
        "search_toggle_lbl": "🔍 Пошук", "search_hint_lbl": "Почніть вводити назву...",
        
        "confirm_del_title": "Підтвердження",
        "confirm_del_msg": "Ви впевнені, що хочете видалити цей рецепт?",
        "error_title": "Помилка",
        "fields_error": "Будь ласка, заповніть всі обов'язкові поля!",
        "error_diff": "Будь ласка, оберіть складність страви!",
        
        "categories": ["Сніданок", "Обід", "Вечеря", "Десерт", "Закуска", "Інше"],
        "Сніданок": "Сніданок", "Обід": "Обід", "Вечеря": "Вечеря", 
        "Десерт": "Десерт", "Закуска": "Закуска", "Інше": "Інше"
    },
    "en": {
        "title": "Recipe Book",
        "app_title": "RECIPE BOOK",
        "tab_search": "Search", "tab_manage": "Manage DB",
        "menu_lang": "Language", "menu_theme": "Theme",
        "lang_menu": "Language", "theme_menu": "Theme",
        "light_theme": "Light", "dark_theme": "Dark",
        "menu_fav": "⭐ Favorites",
        "fav_win_title": "My Favorite Dishes",
        "fav_win_header": "⭐ Favorite Recipes",
        "fav_empty": "The list is empty",
        
        "menu_help": "Help",
        "help_about": "About",
        "help_shortcuts": "Keyboard Shortcuts",
        "about_text": "📖 Recipe Book\nVersion 1.0",
        "shortcuts_text": "Ctrl+S — save recipe\nCtrl+N — clear form\nDelete — delete selected recipe\nDouble click — open recipe details",        
        "search_btn": "Find Recipes", "add_btn": "Add Recipe", "del_btn": "Delete",
        "update_btn": "Update", "save_btn": "Save", "cancel_btn": "Cancel",
        
        "name_lbl": "Name:", "cat_lbl": "Category:", "ing_lbl": "Ingredients:",
        "inst_lbl": "Instructions:", "time_lbl": "Time (min):", "diff_lbl": "Difficulty:",
        
        "easy": "Easy", "medium": "Medium", "hard": "Hard",
        "avail_ing_lbl": "Include:", "excl_ing_lbl": "Exclude:",
        "max_time_lbl": "Max time:", 
        
        "filters_lbl": "Filters", "search_res_lbl": "Results",
        "add_edit_lbl": "Add / Edit", "base_title_lbl": "Recipe Base",
        "search_toggle_lbl": "🔍 Search", "search_hint_lbl": "Start typing name...",
        
        "confirm_del_title": "Confirm",
        "confirm_del_msg": "Are you sure you want to delete this recipe?",
        "error_title": "Error",
        "fields_error": "Please fill in all fields!",
        "error_diff": "Please select the difficulty level!",
        
        "categories": ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"],
        "Сніданок": "Breakfast", "Обід": "Lunch", "Вечеря": "Dinner", 
        "Десерт": "Dessert", "Закуска": "Snack", "Інше": "Other"
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
        self._center_window(1100, 780)
        self.minsize(1000, 700)
        
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
                "bg": "#030712",         
                "surface": "#2D3748",     
                "header": "#111827",    
                "header_fg": "#FFFFFF",
                "fg": "#F9FAFB",          
                "fg_muted": "#9CA3AF",   
                "accent": "#6366F1",      
                "accent_hover": "#818CF8",
                "border": "#374151",      
                "input_bg": "#111827",    
                "danger": "#EF4444"
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
               
        # Прив'язка до всього головного вікна (виправляємо self.root на self)
        self.bind("<Control-s>", lambda event: self.btn_add.invoke())
        self.bind("<Control-n>", lambda event: self.clear_form())
        
       
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
        # Додаємо self., щоб меню було доступне всюди в коді
        self.menubar = tk.Menu(self, borderwidth=0, tearoff=0)
        self.config(menu=self.menubar)
        
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
    
        self.menubar.add_cascade(label="Довідка", menu=self.help_menu)
        self.menubar.add_cascade(label="Тема", menu=self.theme_menu)
        

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

    # Кнопки EN / UK справа
        self.btn_lang_en = tk.Button(
        self.header_frame, text="EN",
        font=self.fonts["bold"],
        bg=c["header"], fg=c["header_fg"],
        bd=0, relief="flat", cursor="hand2",
        activebackground=c["accent"], activeforeground="#fff",
        padx=8, pady=4
    )
        self.btn_lang_en.pack(side=tk.RIGHT, padx=(0, 15))

        self.btn_lang_uk = tk.Button(
        self.header_frame, text="UK",
        font=self.fonts["bold"],
        bg=c["header"], fg=c["header_fg"],
        bd=0, relief="flat", cursor="hand2",
        activebackground=c["accent"], activeforeground="#fff",
        padx=8, pady=4
    )
        self.btn_lang_uk.pack(side=tk.RIGHT, padx=(0, 4))

    # Глобус
        tk.Label(
            self.header_frame, text="🌐",
            font=self.fonts["main"],
            bg=c["header"], fg=c["header_fg"]
        ).pack(side=tk.RIGHT, padx=(0, 4))    
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

    # Вкладка: ПОШУК 
    def _build_search_tab(self):
        # Ліва панель фільтрів
        self.search_side_frame = CustomFrame(self.tab_search) 
        self.search_side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=10)

        # Фрейм кнопки Знайти (завжди внизу)
        self.bottom_action_frame = tk.Frame(self.search_side_frame, bg=self.themes[self.current_theme]["surface"])
        self.bottom_action_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_search = ttk.Button(self.bottom_action_frame, text=self.t["search_btn"], style="Accent.TButton")
        self.btn_search.pack(fill=tk.X, padx=15, pady=15)

        # Зона прокрутки фільтрів
        self.canvas = tk.Canvas(self.search_side_frame, bg=self.themes[self.current_theme]["surface"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.search_side_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.filters_frame = CustomFrame(self.canvas, padx=15, pady=15)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.filters_frame, anchor="nw")
        self.filters_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        # Заголовок Фільтри
        self.lbl_filter_header = tk.Label(self.filters_frame, text=self.t["filters_lbl"], font=self.fonts["heading"])
        self.lbl_filter_header.pack(anchor="w", pady=(0, 10))

        # Інгредієнти Включити
        self.lbl_search_avail = tk.Label(self.filters_frame, text=self.t["avail_ing_lbl"], font=self.fonts["bold"])
        self.lbl_search_avail.pack(anchor="w")
        self.filter_avail_var = tk.StringVar()
        self.entry_filter_avail = ttk.Entry(self.filters_frame, textvariable=self.filter_avail_var)
        self.entry_filter_avail.pack(fill=tk.X, pady=(2, 2))
        self.entry_filter_avail.bind("<KeyRelease>", lambda e: self.filter_ingredients("avail"))
        self.ing_listbox = tk.Listbox(self.filters_frame, selectmode=tk.MULTIPLE, exportselection=0, height=3)
        self.ing_listbox.pack(fill=tk.X, pady=(0, 10))

        # Інгредієнти Виключити
        self.lbl_search_excl = tk.Label(self.filters_frame, text=self.t["excl_ing_lbl"], font=self.fonts["bold"])
        self.lbl_search_excl.pack(anchor="w")
        self.filter_excl_var = tk.StringVar()
        self.entry_filter_excl = ttk.Entry(self.filters_frame, textvariable=self.filter_excl_var)
        self.entry_filter_excl.pack(fill=tk.X, pady=(2, 2))
        self.entry_filter_excl.bind("<KeyRelease>", lambda e: self.filter_ingredients("excl"))
        self.excl_listbox = tk.Listbox(self.filters_frame, selectmode=tk.MULTIPLE, exportselection=0, height=3)
        self.excl_listbox.pack(fill=tk.X, pady=(0, 10))

        # Макс. Час
        self.lbl_search_time = tk.Label(self.filters_frame, text=self.t["max_time_lbl"], font=self.fonts["bold"])
        self.lbl_search_time.pack(anchor="w")
        self.search_time_scale = tk.Scale(self.filters_frame, from_=5, to=120, orient=tk.HORIZONTAL, resolution=5, sliderlength=15, width=12)
        self.search_time_scale.set(120)
        self.search_time_scale.pack(fill=tk.X, pady=(0, 10))

        # Складність
        self.lbl_search_diff_title = tk.Label(self.filters_frame, text=self.t["diff_lbl"], font=self.fonts["bold"])
        self.lbl_search_diff_title.pack(anchor="w")
        diff_f = CustomFrame(self.filters_frame)
        diff_f.pack(fill=tk.X, pady=(2, 10))
        
        self.search_diff_easy, self.search_diff_med, self.search_diff_hard = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
        self.ch_easy = tk.Checkbutton(diff_f, text=self.t["easy"], variable=self.search_diff_easy)
        self.ch_easy.pack(side=tk.LEFT, padx=(0,5))
        self.ch_med = tk.Checkbutton(diff_f, text=self.t["medium"], variable=self.search_diff_med)
        self.ch_med.pack(side=tk.LEFT, padx=(0,5))
        self.ch_hard = tk.Checkbutton(diff_f, text=self.t["hard"], variable=self.search_diff_hard)
        self.ch_hard.pack(side=tk.LEFT)
        
        # Категорії
        self.lbl_search_cat_title = tk.Label(self.filters_frame, text=self.t["cat_lbl"], font=self.fonts["bold"])
        self.lbl_search_cat_title.pack(anchor="w", pady=(10, 0))
        self.cat_checks_frame = tk.Frame(self.filters_frame, bg=self.themes[self.current_theme]["surface"])
        self.cat_checks_frame.pack(fill=tk.X, pady=5)
        self.cat_vars = {}

        # Права панель результатів
        self.search_main_frame = CustomFrame(self.tab_search, padx=20, pady=20)
        self.search_main_frame.pack(side=tk.LEFT, expand=True, fill="both", pady=10)
        self.lbl_search_results_header = tk.Label(self.search_main_frame, text=self.t["search_res_lbl"], font=self.fonts["heading"])
        self.lbl_search_results_header.pack(anchor="w", pady=(0, 10))

        # Таблиця
        self.search_tree = ttk.Treeview(self.search_main_frame, columns=("name", "cat", "time", "diff"), show="headings")
        self.search_tree.heading("name", text=self.t["name_lbl"]); self.search_tree.column("name", width=250)
        self.search_tree.heading("cat", text=self.t["cat_lbl"]); self.search_tree.column("cat", width=120, anchor="center")
        self.search_tree.heading("time", text=self.t["time_lbl"]); self.search_tree.column("time", width=80, anchor="center")
        self.search_tree.heading("diff", text=self.t["diff_lbl"]); self.search_tree.column("diff", width=120, anchor="center")
        
        scr = ttk.Scrollbar(self.search_main_frame, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scr.set)
        self.search_tree.pack(side=tk.LEFT, expand=True, fill="both")
        scr.pack(side=tk.LEFT, fill=tk.Y)
        
    # Вкладка: КЕРУВАННЯ
    def _build_manage_tab(self):
        # Ліва панель (Форма)
        self.form_frame = CustomFrame(self.tab_manage, padx=20, pady=20)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=10)

        self.lbl_form_title = tk.Label(self.form_frame, text=self.t["add_edit_lbl"], font=self.fonts["heading"])
        self.lbl_form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        grid_p = {"sticky": "w", "pady": 8}
        
        # Поле Назва
        self.lbl_name = tk.Label(self.form_frame, text=self.t['name_lbl'], font=self.fonts["bold"])
        self.lbl_name.grid(row=1, column=0, **grid_p)
        self.entry_name = ttk.Entry(self.form_frame, width=32)
        self.entry_name.grid(row=1, column=1, **grid_p, padx=(10,0))

        # Поле Час
        self.lbl_time = tk.Label(self.form_frame, text=self.t['time_lbl'], font=self.fonts["bold"])
        self.lbl_time.grid(row=2, column=0, **grid_p)
        self.time_scale = tk.Scale(self.form_frame, from_=5, to=120, orient=tk.HORIZONTAL, resolution=5, sliderlength=15, width=12)
        self.time_scale.grid(row=2, column=1, sticky="ew", padx=(10,0))

        # Поле Складність (Радіокнопки)
        self.lbl_diff = tk.Label(self.form_frame, text=self.t['diff_lbl'], font=self.fonts["bold"])
        self.lbl_diff.grid(row=3, column=0, **grid_p)
        
        self.diff_var = tk.StringVar(value="easy")
        radio_f = CustomFrame(self.form_frame)
        radio_f.grid(row=3, column=1, sticky="w", padx=(10,0))
        
        self.rb_easy = tk.Radiobutton(radio_f, text=self.t["easy"], variable=self.diff_var, value="easy")
        self.rb_easy.pack(side=tk.LEFT, padx=(0,5))
        self.rb_med = tk.Radiobutton(radio_f, text=self.t["medium"], variable=self.diff_var, value="medium")
        self.rb_med.pack(side=tk.LEFT, padx=(0,5))
        self.rb_hard = tk.Radiobutton(radio_f, text=self.t["hard"], variable=self.diff_var, value="hard")
        self.rb_hard.pack(side=tk.LEFT)

        # Комбобокс Категорія
        self.lbl_cat = tk.Label(self.form_frame, text=self.t['cat_lbl'], font=self.fonts["bold"])
        self.lbl_cat.grid(row=4, column=0, **grid_p)
        self.combo_cat = ttk.Combobox(self.form_frame, values=self.t.get("categories", []), state="readonly", width=30)
        self.combo_cat.current(0)
        self.combo_cat.grid(row=4, column=1, **grid_p, padx=(10,0))

        # Поле Інгредієнти
        self.lbl_ing = tk.Label(self.form_frame, text=self.t['ing_lbl'], font=self.fonts["bold"])
        self.lbl_ing.grid(row=5, column=0, sticky="nw", pady=(8,0))
        self.entry_ing = ttk.Entry(self.form_frame, width=32)
        self.entry_ing.grid(row=5, column=1, sticky="ew", padx=(10,0), pady=(8,0))

        # Поле Інструкції
        self.lbl_inst = tk.Label(self.form_frame, text=self.t['inst_lbl'], font=self.fonts["bold"])
        self.lbl_inst.grid(row=6, column=0, sticky="nw", pady=(15,0))
        self.text_inst_frame = CustomFrame(self.form_frame)
        self.text_inst_frame.grid(row=6, column=1, sticky="ew", padx=(10,0), pady=(15,0))
        
        self.text_inst = tk.Text(self.text_inst_frame, height=5, width=30, wrap="word", font=self.fonts["main"])
        scr_t = ttk.Scrollbar(self.text_inst_frame, command=self.text_inst.yview)
        self.text_inst.configure(yscrollcommand=scr_t.set)
        self.text_inst.pack(side=tk.LEFT, expand=True, fill="both")
        scr_t.pack(side=tk.LEFT, fill=tk.Y)

        # Кнопки дій (Зберегти, Видалити і т.д.)
        act_f = CustomFrame(self.form_frame)
        act_f.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        self.btn_add = ttk.Button(act_f, text=self.t["add_btn"], style="Accent.TButton")
        self.btn_add.pack(fill=tk.X, pady=(0, 8))
        self.btn_update = ttk.Button(act_f, text=self.t["update_btn"])
        self.btn_update.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        self.btn_delete = ttk.Button(act_f, text=self.t["del_btn"])
        self.btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        self.btn_cancel = ttk.Button(act_f, text=self.t["cancel_btn"], command=self.clear_form)
        self.btn_cancel.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Права панель (Таблиця бази)
        self.manage_main_frame = CustomFrame(self.tab_manage, padx=20, pady=20)
        self.manage_main_frame.pack(side=tk.LEFT, expand=True, fill="both", pady=10)

        # Шапка таблиці з пошуком
        list_header = CustomFrame(self.manage_main_frame)
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_base_title = tk.Label(list_header, text=self.t["base_title_lbl"], font=self.fonts["heading"])
        self.lbl_base_title.pack(side=tk.LEFT)
        self.btn_toggle_search = ttk.Button(list_header, text=self.t["search_toggle_lbl"], command=self._toggle_search_bar)
        self.btn_toggle_search.pack(side=tk.RIGHT)

        self.hidden_search_frame = CustomFrame(self.manage_main_frame)
        self.search_ing_var = tk.StringVar()
        self.search_ing_entry = ttk.Entry(self.hidden_search_frame, textvariable=self.search_ing_var, font=self.fonts["main"])
        self.search_ing_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        self.lbl_search_hint = tk.Label(self.hidden_search_frame, text=self.t["search_hint_lbl"], font=self.fonts["small"], fg="#94A3B8")
        self.lbl_search_hint.pack(side=tk.LEFT)

        # Таблиця
        self.manage_tree = ttk.Treeview(self.manage_main_frame, columns=("name", "cat", "time", "diff"), show="headings")
        self.manage_tree.heading("name", text=self.t["name_lbl"])
        self.manage_tree.column("name", width=200)
        self.manage_tree.heading("cat", text=self.t["cat_lbl"])
        self.manage_tree.column("cat", width=120, anchor="center")
        self.manage_tree.heading("time", text=self.t["time_lbl"])
        self.manage_tree.column("time", width=80, anchor="center")
        self.manage_tree.heading("diff", text=self.t["diff_lbl"])
        self.manage_tree.column("diff", width=100, anchor="center")
        
        scr_m = ttk.Scrollbar(self.manage_main_frame, command=self.manage_tree.yview)
        self.manage_tree.configure(yscrollcommand=scr_m.set)
        self.manage_tree.pack(side=tk.LEFT, expand=True, fill="both")
        scr_m.pack(side=tk.LEFT, fill=tk.Y)

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
        
        # Головний фон вікна
        self.config(bg=c["bg"])
        
        # 1. Верхня панель (Header)
        if hasattr(self, 'header_frame'):
            self.header_frame.config(bg=c["header"])
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.config(bg=c["header"], fg=c["header_fg"])
        
        # 2. Стилі Notebook (вкладки)
        self.style.configure("TNotebook", background=c["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=c["border"], foreground=c["fg"])
        self.style.map("TNotebook.Tab", 
                       background=[("selected", c["surface"])], 
                       foreground=[("selected", c["accent"])])
        
        # 3. Стилі Treeview (таблиці)
        self.style.configure("Treeview", 
                             background=c["input_bg"], 
                             fieldbackground=c["input_bg"], 
                             foreground=c["fg"],
                             borderwidth=0)
        self.style.map("Treeview", 
                       background=[("selected", c["accent"])], 
                       foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", background=c["surface"], foreground=c["fg"], borderwidth=1)
        
        # 4. Стилі стандартних ttk віджетів
        self.style.configure("TLabel", foreground=c["fg"], background=c["surface"])
        self.style.configure("TEntry", fieldbackground=c["input_bg"], foreground=c["fg"])
        self.style.configure("TCombobox", fieldbackground=c["input_bg"], foreground=c["fg"])
        
        # 5. Кнопки
        self.style.configure("TButton", background=c["border"], foreground=c["fg"])
        self.style.map("TButton", background=[("active", c["input_bg"])])
        
        # Акцентна кнопка (наприклад, "Знайти" або "Додати")
        self.style.configure("Accent.TButton", background=c["accent"], foreground="#FFFFFF")
        self.style.map("Accent.TButton", background=[("active", c["accent_hover"])])
        
        # 6. Запускаємо рекурсивне оновлення для всіх tk-віджетів (Label, Frame, Checkbutton)
        self._style_widgets(self)

    def _style_widgets(self, widget, current_bg=None):
        c = self.themes[self.current_theme]
        
        # Визначаємо колір фону для поточного рівня
        if isinstance(widget, CustomFrame): 
            bg = c["surface"]
        elif widget == getattr(self, 'header_frame', None): 
            bg = c["header"]
        elif isinstance(widget, (tk.Tk, ttk.Notebook)) or (isinstance(widget, tk.Frame) and not current_bg): 
            bg = c["bg"]
        else: 
            bg = current_bg

        try:
            if isinstance(widget, (tk.Frame, CustomFrame)) and widget != getattr(self, 'header_frame', None):
                widget.config(bg=bg)
            
            elif isinstance(widget, (tk.Label, tk.Radiobutton, tk.Checkbutton)):
                if widget != getattr(self, 'lbl_logo', None):
                    widget.config(
                        bg=bg, 
                        fg=c["fg"], 
                        activebackground=bg, 
                        activeforeground=c["fg"],
                        selectcolor=c["input_bg"]
                    )
            
            # Повзунок (Scale)
            elif isinstance(widget, tk.Scale):
                widget.config(bg=bg, fg=c["fg"], troughcolor=c["input_bg"], highlightthickness=0)
            
            # Списки та текстові поля (Listbox, Text)
            elif isinstance(widget, (tk.Listbox, tk.Text)):
                widget.config(
                    bg=c["input_bg"], 
                    fg=c["fg"], 
                    insertbackground=c["fg"],
                    highlightbackground=c["border"],
                    highlightcolor=c["accent"]
                )
            
            # Спеціально для Canvas (якщо є прокрутка)
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=bg, highlightthickness=0)
                
        except Exception:
            pass # Деякі віджети можуть не підтримувати певні параметри
        
        # Йдемо вглиб до дочірніх елементів
        for child in widget.winfo_children():
            self._style_widgets(child, bg)
            

    def update_ui_text(self):
        self.t = TRANSLATIONS[self.current_lang]
        self.title(self.t["title"])
        
        # 1. ВКЛАДКИ ТА ПІДМЕНЮ
        if hasattr(self, 'btn_lang_uk') and hasattr(self, 'btn_lang_en'):
            c = self.themes[self.current_theme]
        if self.current_lang == "uk":
            self.btn_lang_uk.config(bg=c["accent"], fg="#fff")
            self.btn_lang_en.config(bg=c["header"], fg=c["header_fg"])
        else:
            self.btn_lang_en.config(bg=c["accent"], fg="#fff")
            self.btn_lang_uk.config(bg=c["header"], fg=c["header_fg"])

        self.theme_menu.entryconfig(0, label=self.t["light_theme"])
        self.theme_menu.entryconfig(1, label=self.t["dark_theme"])
        self.notebook.tab(0, text=self.t["tab_search"])
        self.notebook.tab(1, text=self.t["tab_manage"])
        
        # 2. ГОЛОВНЕ ЛОГО ТА ВЕРХНЄ МЕНЮ
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.config(text="🍽  " + self.t["app_title"])
            
        if hasattr(self, 'menubar'):
            last_idx = self.menubar.index("end")
            if last_idx >= 0:
                self.menubar.entryconfig(0, label=self.t["menu_help"])
                
            if last_idx >= 1:
                self.menubar.entryconfig(1, label="🎨 " + self.t["menu_theme"])
                
            if last_idx >= 2:
                self.menubar.entryconfig(2, label=self.t["menu_fav"])  

        # ВКЛАДКА "КЕРУВАННЯ БАЗОЮ"
        if hasattr(self, 'lbl_form_title'):
            # Заголовки та підказки
            self.lbl_form_title.config(text=self.t["add_edit_lbl"])
            self.lbl_base_title.config(text=self.t["base_title_lbl"])
            self.btn_toggle_search.config(text=self.t["search_toggle_lbl"])
            self.lbl_search_hint.config(text=self.t["search_hint_lbl"])
            
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
            self.btn_cancel.config(text=self.t["cancel_btn"])
            self.btn_update.config(text=self.t["update_btn"])
            self.btn_delete.config(text=self.t["del_btn"])
            
            # Радіокнопки
            self.rb_easy.config(text=self.t["easy"])
            self.rb_med.config(text=self.t["medium"])
            self.rb_hard.config(text=self.t["hard"])

            # Комбобокс категорій
            if hasattr(self, 'combo_cat'):
                current_val = self.combo_cat.get() # Беремо поточне слово (напр. "Сніданок")
                self.combo_cat['values'] = self.t.get("categories", [])
                
                # Перекладаємо це слово на нову мову і вставляємо назад у поле
                translated_val = self.t.get(current_val, current_val)
                self.combo_cat.set(translated_val)
        

            # Заголовки таблиці
            self.manage_tree.heading("name", text=self.t["name_lbl"])
            self.manage_tree.heading("cat", text=self.t["cat_lbl"])
            self.manage_tree.heading("time", text=self.t["time_lbl"])
            self.manage_tree.heading("diff", text=self.t["diff_lbl"])

        # ВКЛАДКА ПОШУК
        if hasattr(self, 'lbl_filter_header'):

            # Заголовки фільтрів
            self.lbl_filter_header.config(text=self.t["filters_lbl"])
            self.lbl_search_avail.config(text=self.t["avail_ing_lbl"])
            self.lbl_search_excl.config(text=self.t["excl_ing_lbl"])
            self.lbl_search_time.config(text=self.t["max_time_lbl"])
            self.lbl_search_diff_title.config(text=self.t["diff_lbl"])
            self.lbl_search_cat_title.config(text=self.t["cat_lbl"])
            self.lbl_search_results_header.config(text=self.t["search_res_lbl"])

            
            # Галочки складності та кнопка
            self.ch_easy.config(text=self.t["easy"])
            self.ch_med.config(text=self.t["medium"])
            self.ch_hard.config(text=self.t["hard"])
            self.btn_search.config(text=self.t["search_btn"])

            # Заголовки таблиці пошуку
            self.search_tree.heading("name", text=self.t["name_lbl"])
            self.search_tree.heading("cat", text=self.t["cat_lbl"])
            self.search_tree.heading("time", text=self.t["time_lbl"])
            self.search_tree.heading("diff", text=self.t["diff_lbl"])
            
        # Списки інгредієнтів
        if hasattr(self, 'ing_listbox') and hasattr(self, 'excl_listbox'):
            self.ing_listbox.delete(0, tk.END)
            self.excl_listbox.delete(0, tk.END)
            try:
                for ing in INGREDIENTS_DATA:
                    self.ing_listbox.insert(tk.END, ing)
                    self.excl_listbox.insert(tk.END, ing)
            except NameError:
                pass

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
        for widget in self.cat_checks_frame.winfo_children():
            widget.destroy()
    
        self.cat_vars = {}

        num_columns = 4 
    
        for i, cat in enumerate(categories):
            var = tk.BooleanVar(value=True) 
            self.cat_vars[cat] = var
        
            display_name = self.t.get(cat, cat)
        
            cb = tk.Checkbutton(
                self.cat_checks_frame, 
                text=display_name,
                variable=var,
                bg=self.themes[self.current_theme]["surface"],
                fg=self.themes[self.current_theme]["fg"],
                selectcolor=self.themes[self.current_theme]["input_bg"],
                activebackground=self.themes[self.current_theme]["surface"],
                font=self.fonts["main"]
            )
        
            row_idx = i // num_columns
            col_idx = i % num_columns
        
            cb.grid(row=row_idx, column=col_idx, sticky="w", padx=10, pady=2)

        for c in range(num_columns):
            self.cat_checks_frame.columnconfigure(c, weight=1)

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
        self.combo_cat.set("")
        self.diff_var.set("none")
        
        self.btn_add.config(text=self.t.get("add_btn", "Додати рецепт"))
        
    def _center_window(self, width, height):
        self.geometry(f"{width}x{height}+{int((self.winfo_screenwidth()/2)-(width/2))}+{int((self.winfo_screenheight()/2)-(height/2))}")

    def show_custom_details_dialog(self, r, toggle_fav_cb=None, export_cb=None):
        c = self.themes[self.current_theme]
        d = tk.Toplevel(self)
        d.title(r["name"])
        d.geometry("450x700")
        d.minsize(400, 600)
        d.config(bg=c["surface"])
        
        header_frame = tk.Frame(d, bg=c["surface"])
        header_frame.pack(pady=(25, 5))

        tk.Label(header_frame, text=r["name"], font=self.fonts["logo"], 
                 fg=c["accent"], bg=c["surface"]).pack(side=tk.LEFT)
        
        is_fav = r.get("is_favorite", False)
        star_symbol = "★" if is_fav else "☆"
        fav_color = "#3498db" if is_fav else c["fg_muted"]

        star_lbl = tk.Label(header_frame, text=star_symbol, font=("Arial", 24), 
                            fg=fav_color, bg=c["surface"], cursor="hand2")
        star_lbl.pack(side=tk.LEFT, padx=10)

        if toggle_fav_cb:
            star_lbl.bind("<Button-1>", lambda e: toggle_fav_cb(r["name"], star_lbl))
        
        saved_cat = r.get('category', 'Інше')
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Закуска", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"]
        
        display_cat = cats_en[cats_uk.index(saved_cat)] if self.current_lang == "en" and saved_cat in cats_uk else saved_cat
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
        
        export_text = "💾 Зберегти рецепт (.txt)" if self.current_lang == "uk" else "💾 Save recipe (.txt)"
        btn_export = ttk.Button(d, text=export_text, style="Accent.TButton", 
                                command=lambda: export_cb(r) if export_cb else None)
        btn_export.pack(pady=(15, 0), padx=30, fill=tk.X)

        close_text = "Закрити" if self.current_lang == "uk" else "Close"
        ttk.Button(d, text=close_text, command=d.destroy).pack(pady=15, padx=30, fill=tk.X)