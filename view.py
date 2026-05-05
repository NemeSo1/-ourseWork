import tkinter as tk
from tkinter import ttk, messagebox

TRANSLATIONS = {
    "uk": {
        "title": "Книга рецептів",
        "tab_search": "Пошук", "tab_manage": "Керування",
        "lang_menu": "Мова", "theme_menu": "Тема",
        "light_theme": "Світла", "dark_theme": "Темна",
        "search_btn": "Знайти", "add_btn": "Додати рецепт", "del_btn": "Видалити",
        "name_lbl": "Назва:", "cat_lbl": "Категорія:", "ing_lbl": "Інгредієнти:",
        "inst_lbl": "Інструкції:", "time_lbl": "Час (хв):", "diff_lbl": "Складність:",
        "easy": "Легко", "medium": "Середньо", "hard": "Складно",
        "avail_ing_lbl": "Що є:", "excl_ing_lbl": "Без чого:",
        "max_time_lbl": "Макс. час:", "search_res_lbl": "Результати:",
        "update_btn": "Оновити"
    },
    "en": {
        "title": "Recipe Book",
        "tab_search": "Search", "tab_manage": "Manage",
        "lang_menu": "Language", "theme_menu": "Theme",
        "light_theme": "Light", "dark_theme": "Dark",
        "search_btn": "Search", "add_btn": "Add Recipe", "del_btn": "Delete",
        "name_lbl": "Name:", "cat_lbl": "Category:", "ing_lbl": "Ingredients:",
        "inst_lbl": "Instructions:", "time_lbl": "Time (min):", "diff_lbl": "Difficulty:",
        "easy": "Easy", "medium": "Medium", "hard": "Hard",
        "avail_ing_lbl": "Have:", "excl_ing_lbl": "Exclude:",
        "max_time_lbl": "Max time:", "search_res_lbl": "Results:",
        "update_btn": "Update"
    }
}

INGREDIENTS_DATA = [
    "курка", "картопля", "помідор", "сир", "яйце", "молоко", "борошно", "цибуля", "часник",
    "огірок", "перець", "морква", "капуста", "гриби", "яловичина", "свинина", "риба", "креветки",
    "рис", "гречка", "макарони", "олія", "масло", "сметана", "вершки", "цукор", "сіль", "мед",
    "яблуко", "банан", "лимон", "зелень", "авокадо", "бекон", "баклажан", "кабачок", "горіхи"
]
class RecipeView:
    def __init__(self, root):
        self.root = root
        self.current_lang = "uk"
        self.t = TRANSLATIONS[self.current_lang]
        
        # Налаштування тем
        self.themes = {
            "light": {"bg": "#f0f0f0", "fg": "black", "list_bg": "white"},
            "dark": {"bg": "#2d2d2d", "fg": "white", "list_bg": "#3d3d3d"}
        }
        self.current_theme = "light"

        self.center_window(self.root, 900, 700)
        self.create_menu()
        self.create_notebook()
        self.update_ui_text()
        self.apply_theme()

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Мова", menu=self.lang_menu)
        
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Тема", menu=self.theme_menu)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        self.tab_search = tk.Frame(self.notebook)
        self.tab_manage = tk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text="Пошук")
        self.notebook.add(self.tab_manage, text="Керування")
        self.build_search_tab()
        self.build_manage_tab()

    def build_search_tab(self):
        # 3 колонки для списків
        for i in range(3): self.tab_search.columnconfigure(i, weight=1)
        
        self.lbl_avail = tk.Label(self.tab_search, text="")
        self.lbl_avail.grid(row=0, column=0)
        self.ing_listbox = tk.Listbox(self.tab_search, selectmode=tk.MULTIPLE, exportselection=0)
        self.ing_listbox.grid(row=1, column=0, sticky="nsew", padx=5)

        self.lbl_excl = tk.Label(self.tab_search, text="")
        self.lbl_excl.grid(row=0, column=1)
        self.excl_listbox = tk.Listbox(self.tab_search, selectmode=tk.MULTIPLE, exportselection=0)
        self.excl_listbox.grid(row=1, column=1, sticky="nsew", padx=5)

        self.lbl_res = tk.Label(self.tab_search, text="")
        self.lbl_res.grid(row=0, column=2)
        self.res_listbox = tk.Listbox(self.tab_search)
        self.res_listbox.grid(row=1, column=2, sticky="nsew", padx=5)

        # Фільтр по часу (Scale)
        self.lbl_max_time = tk.Label(self.tab_search, text="")
        self.lbl_max_time.grid(row=2, column=0, columnspan=2, pady=(10,0))
        self.search_time_scale = tk.Scale(self.tab_search, from_=5, to=120, orient=tk.HORIZONTAL)
        self.search_time_scale.set(120)
        self.search_time_scale.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20)
        
        # Фільтр по складності (Checkbuttons)
        self.lbl_diff_search = tk.Label(self.tab_search, text="")
        self.lbl_diff_search.grid(row=2, column=2, pady=(10,0))
        
        self.diff_frame_search = tk.Frame(self.tab_search)
        self.diff_frame_search.grid(row=3, column=2)
        
        self.search_diff_easy = tk.BooleanVar(value=True)
        self.search_diff_med = tk.BooleanVar(value=True)
        self.search_diff_hard = tk.BooleanVar(value=True)
        
        self.cb_easy = tk.Checkbutton(self.diff_frame_search, variable=self.search_diff_easy)
        self.cb_med = tk.Checkbutton(self.diff_frame_search, variable=self.search_diff_med)
        self.cb_hard = tk.Checkbutton(self.diff_frame_search, variable=self.search_diff_hard)
        
        self.cb_easy.pack(side=tk.LEFT)
        self.cb_med.pack(side=tk.LEFT)
        self.cb_hard.pack(side=tk.LEFT)
        
        self.btn_search = tk.Button(self.tab_search, text="", bg="#4CAF50", fg="white")
        self.btn_search.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

    def build_manage_tab(self):
        self.tab_manage.columnconfigure(1, weight=1)
        
        # Поля вводу
        tk.Label(self.tab_manage, text="Назва:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(self.tab_manage)
        self.entry_name.grid(row=0, column=1, sticky="ew")

        # Час приготування (Scale)
        self.lbl_time_manage = tk.Label(self.tab_manage, text="Час (хв):")
        self.lbl_time_manage.grid(row=1, column=0, sticky="w")
        self.time_scale = tk.Scale(self.tab_manage, from_=5, to=120, orient=tk.HORIZONTAL)
        self.time_scale.grid(row=1, column=1, sticky="ew")

        # Складність (Radiobuttons)
        self.lbl_diff_manage = tk.Label(self.tab_manage, text="Складність:")
        self.lbl_diff_manage.grid(row=2, column=0, sticky="nw")
        self.diff_var = tk.StringVar(value="easy")
        self.radio_frame = tk.Frame(self.tab_manage)
        self.radio_frame.grid(row=2, column=1, sticky="w")
        
        self.rb_easy = tk.Radiobutton(self.radio_frame, text="Easy", variable=self.diff_var, value="easy")
        self.rb_med = tk.Radiobutton(self.radio_frame, text="Medium", variable=self.diff_var, value="medium")
        self.rb_hard = tk.Radiobutton(self.radio_frame, text="Hard", variable=self.diff_var, value="hard")
        self.rb_easy.pack(side=tk.LEFT)
        self.rb_med.pack(side=tk.LEFT)
        self.rb_hard.pack(side=tk.LEFT)

        # Категорія
        tk.Label(self.tab_manage, text="Категорія:").grid(row=3, column=0, sticky="w")
        self.combo_cat = ttk.Combobox(self.tab_manage, values=["Сніданок", "Обід", "Вечеря", "Десерт"], state="readonly")
        self.combo_cat.current(0)
        self.combo_cat.grid(row=3, column=1, sticky="ew")

        tk.Label(self.tab_manage, text="Інгредієнти:").grid(row=4, column=0, sticky="w")
        self.entry_ing = tk.Entry(self.tab_manage)
        self.entry_ing.grid(row=4, column=1, sticky="ew")

        tk.Label(self.tab_manage, text="Інструкції:").grid(row=5, column=0, sticky="nw")
        self.text_inst = tk.Text(self.tab_manage, height=5)
        self.text_inst.grid(row=5, column=1, sticky="ew")

        self.btn_add = tk.Button(self.tab_manage, text="Додати", bg="#2196F3", fg="white")
        self.btn_add.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Створюємо рамку для списку і скролбару
        list_frame = tk.Frame(self.tab_manage)
        list_frame.grid(row=7, column=0, columnspan=2, sticky="nsew") # row=7 або той, що у тебе
        
        # Створюємо скролбар
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Створюємо Listbox і прив'язуємо до скролбару
        self.recipes_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.recipes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.recipes_listbox.yview)
        
        # Створюємо фрейм-контейнер для кнопок дій
        actions_frame = tk.Frame(self.tab_manage, bg=self.themes[self.current_theme]["bg"])
        actions_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Налаштовуємо колонки фрейму, щоб кнопки були однакової ширини
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        # Кнопка Оновити (тепер зліва)
        self.btn_update = tk.Button(actions_frame, text="Оновити", bg="#FF9800", fg="white")
        self.btn_update.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        # Кнопка Видалити (тепер справа)
        self.btn_delete = tk.Button(actions_frame, text="Видалити", bg="#f44336", fg="white")
        self.btn_delete.grid(row=0, column=1, sticky="ew", padx=(2, 0))

    def apply_theme(self):
        colors = self.themes[self.current_theme]
        # Застосування кольорів до всіх основних елементів
        widgets_to_style = [self.root, self.tab_search, self.tab_manage, self.radio_frame, self.diff_frame_search]
        for w in widgets_to_style: w.config(bg=colors["bg"])
        
        for widget in self.root.winfo_children():
            self._recursive_style(widget, colors)

    def _recursive_style(self, widget, colors):
        try:
            if isinstance(widget, (tk.Label, tk.Radiobutton, tk.Scale)):
                widget.config(bg=colors["bg"], fg=colors["fg"])
            elif isinstance(widget, (tk.Listbox, tk.Text, tk.Entry)):
                widget.config(bg=colors["list_bg"], fg=colors["fg"])
        except: pass
        for child in widget.winfo_children():
            self._recursive_style(child, colors)

    def update_ui_text(self):
        self.root.title(self.t["title"])
        self.t = TRANSLATIONS[self.current_lang]
        self.menubar.entryconfig(1, label=self.t["lang_menu"])
        self.menubar.entryconfig(2, label=self.t["theme_menu"])
        self.notebook.tab(0, text=self.t["tab_search"])
        self.notebook.tab(1, text=self.t["tab_manage"])
        self.lbl_avail.config(text=self.t["avail_ing_lbl"])
        self.lbl_excl.config(text=self.t["excl_ing_lbl"])
        self.lbl_res.config(text=self.t["search_res_lbl"])
        self.lbl_max_time.config(text=self.t["max_time_lbl"])
        self.btn_search.config(text=self.t["search_btn"])
        self.btn_add.config(text=self.t["add_btn"])
        self.btn_delete.config(text=self.t["del_btn"])
        self.rb_easy.config(text=self.t["easy"])
        self.rb_med.config(text=self.t["medium"])
        self.rb_hard.config(text=self.t["hard"])
        self.lbl_diff_search.config(text=self.t["diff_lbl"])
        self.cb_easy.config(text=self.t["easy"])
        self.cb_med.config(text=self.t["medium"])
        self.cb_hard.config(text=self.t["hard"])
        
        # Оновлення списку інгредієнтів (можна розширити словником як раніше)
        self.ing_listbox.delete(0, tk.END)
        self.excl_listbox.delete(0, tk.END)
        for ing in INGREDIENTS_DATA:
            self.ing_listbox.insert(tk.END, ing)
            self.excl_listbox.insert(tk.END, ing)

    def show_custom_details_dialog(self, recipe):
        dialog = tk.Toplevel(self.root)
        dialog.title(recipe["name"])
        dialog.geometry("400x550") # Трохи збільшив висоту для інгредієнтів
        dialog.config(bg=self.themes[self.current_theme]["bg"])
        
        fg = self.themes[self.current_theme]["fg"]
        bg = self.themes[self.current_theme]["bg"]

        # Назва
        tk.Label(dialog, text=recipe["name"], font=("Arial", 14, "bold"), fg="#2196F3", bg=bg).pack(pady=5)
        
        # Час і складність
        tk.Label(dialog, text=f"{self.t['time_lbl']} {recipe['time']} | {self.t['diff_lbl']} {self.t.get(recipe['difficulty'], recipe['difficulty'])}", bg=bg, fg=fg).pack()
        
        # Інгредієнти
        tk.Label(dialog, text=self.t['ing_lbl'], font=("Arial", 10, "bold"), bg=bg, fg=fg).pack(anchor="w", padx=20, pady=(10, 0))
        ing_text = ", ".join(recipe['ingredients'])
        tk.Label(dialog, text=ing_text, bg=bg, fg=fg, wraplength=350, justify="left").pack(anchor="w", padx=20)
        
        # Інструкції
        tk.Label(dialog, text=self.t['inst_lbl'], font=("Arial", 10, "bold"), bg=bg, fg=fg).pack(anchor="w", padx=20, pady=(10, 0))
        tbox = tk.Text(dialog, height=10, bg=self.themes[self.current_theme]["list_bg"], fg=fg, wrap="word")
        tbox.insert("1.0", recipe["instructions"])
        tbox.config(state="disabled")
        tbox.pack(padx=20, pady=5, fill="both", expand=True)
        
        # Кнопка ОК
        tk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=10)
        
    def show_loading(self):
        self.root.withdraw()
        
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Завантаження")
        loading_window.overrideredirect(True)
        self.center_window(loading_window, 300, 100) 
        
        tk.Label(loading_window, text="Завантаження бази даних...", font=("Arial", 10, "bold")).pack(pady=(15, 10))
        
        progress = ttk.Progressbar(loading_window, orient="horizontal", length=250, mode="determinate")
        progress.pack()
        
        # Імітуємо завантаження
        for i in range(0, 201, 2):
            progress["value"] = i
            loading_window.update()
            self.root.after(10) # пауза
            
        # Знищуємо віконце завантаження
        loading_window.destroy()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
    def center_window(self, window, width, height):
        # Отримуємо розміри екрану користувача
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Вираховуємо координати X та Y для центру
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Встановлюємо розмір і позицію вікна на екрані
        window.geometry(f"{width}x{height}+{x}+{y}")