import tkinter as tk
from tkinter import ttk, messagebox

TRANSLATIONS = {
    "uk": {
        "title": "Книга рецептів",
        "tab_search": "Пошук страв",
        "tab_manage": "Мої рецепти",
        "lang_menu": "Мова",
        "search_btn": "Знайти рецепти",
        "add_btn": "Додати рецепт",
        "del_btn": "Видалити обране",
        "name_lbl": "Назва страви:",
        "cat_lbl": "Категорія:",
        "ing_lbl": "Інгредієнти (через кому):",
        "inst_lbl": "Спосіб приготування:",
        "avail_ing_lbl": "Що є в холодильнику:",
        "excl_ing_lbl": "Чого НЕ повинно бути:",
        "search_res_lbl": "Результати пошуку (2-клік):",
        "all_rec_lbl": "Список рецептів (2-клік):"
    },
    "en": {
        "title": "Recipe Book",
        "tab_search": "Search Dishes",
        "tab_manage": "My Recipes",
        "lang_menu": "Language",
        "search_btn": "Search Recipes",
        "add_btn": "Add Recipe",
        "del_btn": "Delete Selected",
        "name_lbl": "Dish Name:",
        "cat_lbl": "Category:",
        "ing_lbl": "Ingredients (comma separated):",
        "inst_lbl": "Cooking Method:",
        "avail_ing_lbl": "Available ingredients:",
        "excl_ing_lbl": "Must NOT include:",
        "search_res_lbl": "Search Results (Double-click):",
        "all_rec_lbl": "Recipe List (Double-click):"
    }
}

class RecipeView:
    def __init__(self, root):
        self.root = root
        self.current_lang = "uk"
        self.t = TRANSLATIONS[self.current_lang]
        
        self.root.title(self.t["title"])
        self.root.geometry("850x600") # Розширюємо вікно для 3 колонок
        self.center_window()
        
        self.header_font = ("Helvetica", 11, "bold")
        self.normal_font = ("Helvetica", 10)
        
        self.create_menu()
        self.create_notebook()
        self.update_ui_text()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.t["lang_menu"], menu=self.lang_menu)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.tab_search = ttk.Frame(self.notebook)
        self.tab_manage = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text=self.t["tab_search"])
        self.notebook.add(self.tab_manage, text=self.t["tab_manage"])
        self.build_search_tab()
        self.build_manage_tab()

    def build_search_tab(self):
        self.tab_search.columnconfigure(0, weight=1)
        self.tab_search.columnconfigure(1, weight=1)
        self.tab_search.columnconfigure(2, weight=2)
        self.tab_search.rowconfigure(1, weight=1)

        # Колонка 1: Бажані інгредієнти
        self.lbl_avail_ing = tk.Label(self.tab_search, text=self.t["avail_ing_lbl"], font=self.header_font)
        self.lbl_avail_ing.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.ing_listbox = tk.Listbox(self.tab_search, selectmode=tk.MULTIPLE, font=self.normal_font, exportselection=False)
        self.ing_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Колонка 2: Заборонені інгредієнти
        self.lbl_excl_ing = tk.Label(self.tab_search, text=self.t["excl_ing_lbl"], font=self.header_font, fg="#f44336")
        self.lbl_excl_ing.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.excl_listbox = tk.Listbox(self.tab_search, selectmode=tk.MULTIPLE, font=self.normal_font, exportselection=False)
        self.excl_listbox.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        
        ing_list = ["курка", "картопля", "помідор", "сир", "яйце", "молоко", "борошно", "цибуля", "часник", "гриби"]
        for ing in ing_list:
            self.ing_listbox.insert(tk.END, ing)
            self.excl_listbox.insert(tk.END, ing)

        # Кнопка пошуку (на дві колонки)
        self.btn_search = tk.Button(self.tab_search, text=self.t["search_btn"], bg="#4CAF50", fg="white", font=self.header_font)
        self.btn_search.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Колонка 3: Результати
        self.lbl_search_res = tk.Label(self.tab_search, text=self.t["search_res_lbl"], font=self.header_font)
        self.lbl_search_res.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.res_listbox = tk.Listbox(self.tab_search, font=self.normal_font)
        self.res_listbox.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=5)

    def build_manage_tab(self):
        self.tab_manage.columnconfigure(1, weight=1)
        self.tab_manage.rowconfigure(4, weight=1)

        self.lbl_name = tk.Label(self.tab_manage, text=self.t["name_lbl"])
        self.lbl_name.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.entry_name = tk.Entry(self.tab_manage)
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        self.lbl_cat = tk.Label(self.tab_manage, text=self.t["cat_lbl"])
        self.lbl_cat.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.combo_cat = ttk.Combobox(self.tab_manage, values=["Сніданок", "Обід", "Вечеря", "Десерт"], state="readonly")
        self.combo_cat.current(0)
        self.combo_cat.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        self.lbl_ing = tk.Label(self.tab_manage, text=self.t["ing_lbl"])
        self.lbl_ing.grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.entry_ing = tk.Entry(self.tab_manage)
        self.entry_ing.grid(row=2, column=1, sticky="ew", padx=10, pady=2)

        self.lbl_inst = tk.Label(self.tab_manage, text=self.t["inst_lbl"])
        self.lbl_inst.grid(row=3, column=0, sticky="nw", padx=10, pady=2)
        self.text_inst = tk.Text(self.tab_manage, height=5, font=("Arial", 9))
        self.text_inst.grid(row=3, column=1, sticky="ew", padx=10, pady=2)

        self.btn_add = tk.Button(self.tab_manage, text=self.t["add_btn"], bg="#2196F3", fg="white", font=self.header_font)
        self.btn_add.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.lbl_all_rec = tk.Label(self.tab_manage, text=self.t["all_rec_lbl"], font=self.header_font)
        self.lbl_all_rec.grid(row=5, column=0, sticky="nw", padx=10, pady=5)
        
        list_frame = tk.Frame(self.tab_manage)
        list_frame.grid(row=5, column=1, sticky="nsew", padx=10, pady=5)
        
        self.recipes_listbox = tk.Listbox(list_frame)
        self.recipes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.config(command=self.recipes_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipes_listbox.config(yscrollcommand=scrollbar.set)

        self.btn_delete = tk.Button(self.tab_manage, text=self.t["del_btn"], bg="#f44336", fg="white")
        self.btn_delete.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def update_ui_text(self):
        self.t = TRANSLATIONS[self.current_lang]
        self.root.title(self.t["title"])
        self.menubar.entryconfig(1, label=self.t["lang_menu"])
        self.notebook.tab(self.tab_search, text=self.t["tab_search"])
        self.notebook.tab(self.tab_manage, text=self.t["tab_manage"])
        self.lbl_avail_ing.config(text=self.t["avail_ing_lbl"])
        self.lbl_excl_ing.config(text=self.t["excl_ing_lbl"])
        self.btn_search.config(text=self.t["search_btn"])
        self.lbl_search_res.config(text=self.t["search_res_lbl"])
        self.lbl_name.config(text=self.t["name_lbl"])
        self.lbl_cat.config(text=self.t["cat_lbl"])
        self.lbl_ing.config(text=self.t["ing_lbl"])
        self.lbl_inst.config(text=self.t["inst_lbl"])
        self.btn_add.config(text=self.t["add_btn"])
        self.lbl_all_rec.config(text=self.t["all_rec_lbl"])
        self.btn_delete.config(text=self.t["del_btn"])

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_custom_details_dialog(self, recipe):
        dialog = tk.Toplevel(self.root)
        dialog.title(recipe["name"])
        dialog.geometry("400x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 225
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text=recipe["name"], font=("Arial", 14, "bold"), fg="#2196F3").pack(pady=10)
        tk.Label(dialog, text=f"Категорія: {recipe['category']}", font=self.normal_font).pack()
        
        tk.Label(dialog, text="Інгредієнти:", font=self.header_font).pack(anchor="w", padx=20, pady=(10,0))
        tk.Label(dialog, text=", ".join(recipe['ingredients']), font=self.normal_font, wraplength=350, justify="left").pack(anchor="w", padx=20)
        
        tk.Label(dialog, text="Спосіб приготування:", font=self.header_font).pack(anchor="w", padx=20, pady=(10,0))
        
        inst_box = tk.Text(dialog, wrap="word", height=10, font=("Arial", 10), bg="#f9f9f9")
        inst_box.insert("1.0", recipe.get("instructions", "Інструкції відсутні."))
        inst_box.config(state="disabled")
        inst_box.pack(padx=20, pady=5, fill="both", expand=True)
        
        tk.Button(dialog, text="Закрити", command=dialog.destroy, width=15).pack(pady=10)