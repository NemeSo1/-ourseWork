import tkinter as tk
from tkinter import messagebox

class RecipeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Стан сортування таблиці керування
        self._manage_recipes = [] # Зберігаємо завантажені рецепти
        self._search_results = []
        
        self.setup_bindings()
        self.update_manage_list() # Перше завантаження
        self.refresh_category_filters()
        

    def setup_bindings(self):
        v = self.view
        
        if hasattr(v, 'btn_cancel'):  # Або як у тебе називається ця кнопка
            v.btn_cancel.config(command=self.cancel_edit_action)
            
        # Меню (збережено)
        v.lang_menu.add_command(label="Українська", command=lambda: self.change_language("uk"))
        v.lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        v.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        v.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        # Кнопки дій (збережено)
        v.btn_add.config(command=self.add_recipe_action) # Спочатку це Add
        v.btn_update.config(command=self.prepare_update)
        v.btn_delete.config(command=self.delete_recipe_action)
        v.btn_search.config(command=self.search_dishes_action)

        # Treeview (вбудовані дії)
        v.manage_tree.bind("<Double-Button-1>", lambda e: self.on_tree_double_click("manage"))
        v.search_tree.bind("<Double-Button-1>", lambda e: self.on_tree_double_click("search"))
        
        # --- Сортування при клацанні на заголовок (NEW) ---
        # Керування: Назва, Категорія
        def make_manage_sort(col, key_func):
            def sort_command():
                if v._manage_sort_col == col: v._manage_sort_asc = not v._manage_sort_asc
                else: v._manage_sort_col = col; v._manage_sort_asc = True
                self._sort_tree_data(self._manage_recipes, v.manage_tree, "manage", key_func)
                self.update_manage_tree_ui() # Перемалювати заголовки
            return sort_command

        # Прив'язка заголовків Керування
        self._cmd_sort_mname = make_manage_sort("name", lambda r: r["name"].lower())
        self._cmd_sort_mcat = make_manage_sort("cat", lambda r: r.get("category", "").lower())
        self._cmd_sort_mtime = make_manage_sort("time", lambda r: float(r.get("time", 0)))
        self._cmd_sort_mdiff = make_manage_sort("diff", lambda r: r.get("difficulty", "").lower())
        
        # Пошук страв: Назва, Час, Складність
        def make_search_sort(col, key_func):
            def sort_command():
                if v._search_sort_col == col: v._search_sort_asc = not v._search_sort_asc
                else: v._search_sort_col = col; v._search_sort_asc = True
                self._sort_tree_data(self._search_results, v.search_tree, "search", key_func)
                self.update_search_tree_ui()
            return sort_command

        # Прив'язка заголовків Пошуку
        diff_weights = {"easy": 1, "medium": 2, "hard": 3}
        self._cmd_sort_sname = make_search_sort("name", lambda r: r["name"].lower())
        self._cmd_sort_scat = make_search_sort("cat", lambda r: r.get("category", "").lower()) # ДОДАНО!
        self._cmd_sort_stime = make_search_sort("time", lambda r: float(r.get("time", 0)))
        self._cmd_sort_sdiff = make_search_sort("diff", lambda r: diff_weights.get(r.get("difficulty", "easy").lower(), 0))
        
        # Додай це в кінець методу setup_bindings
        for tree in [v.search_tree, v.manage_tree]:
            for col in ("name", "cat", "time", "diff"):
                tree.heading(col, command=lambda t=tree, c=col: self.sort_column(t, c, False))

        # --- Вбудований пошук Керування (NEW) ---
        v.search_ing_entry.bind("<KeyRelease>", lambda e: self.update_manage_list())

    # --- ЗАГАЛЬНІ ДІЇ ---
    def change_language(self, lang):
        self.view.current_lang = lang
        self.view.update_ui_text()
        self.view.clear_form() # Очистити форму при зміні мови
        self.update_manage_list() # Перезавантажити списки

    def change_theme(self, theme_name):
        self.view.current_theme = theme_name
        self.view.apply_theme()

    # --- УПРАВЛІННЯ ДАНИМИ Treeview (Керування) ---
    # --- УПРАВЛІННЯ ДАНИМИ Treeview (Керування) ---
    def update_manage_list(self):
        # 1. Завантажити дані з моделі
        self._manage_recipes = self.model.get_all_recipes()
        
        # 2. Фільтрація: перевіряємо, чи починається назва з введених літер
        search_query = self.view.search_ing_var.get().strip().lower()
        if search_query:
            self._manage_recipes = [
                r for r in self._manage_recipes 
                if any(word.startswith(search_query) for word in r["name"].lower().split())
            ]
            
        # --- 3. ПІДГОТОВКА ДАНИХ ДЛЯ ВІДОБРАЖЕННЯ (Переклад категорій) ---
        display_recipes = []
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Other"]
        
        for r in self._manage_recipes:
            # Робимо копію рецепта, щоб не змінювати оригінальні дані в моделі
            r_copy = r.copy()
            if self.view.current_lang == "en" and r_copy["category"] in cats_uk:
                idx = cats_uk.index(r_copy["category"])
                r_copy["category"] = cats_en[idx]
            elif self.view.current_lang == "uk" and r_copy["category"] in cats_en:
                idx = cats_en.index(r_copy["category"])
                r_copy["category"] = cats_uk[idx]
            display_recipes.append(r_copy)
        # ---------------------------------------------------------------

        # 4. Вивести в таблицю (використовуємо display_recipes замість оригіналу)
        self._fill_tree(display_recipes, self.view.manage_tree, "manage")
        
        # Оновити заголовки (скинути стрілки)
        self.update_manage_tree_ui()

    def update_manage_tree_ui(self):
        v = self.view
        v.set_tree_heading("manage", "name", v.t["name_lbl"], self._cmd_sort_mname)
        v.set_tree_heading("manage", "cat", v.t["cat_lbl"], self._cmd_sort_mcat)
        v.set_tree_heading("manage", "time", v.t["time_lbl"], self._cmd_sort_mtime)
        v.set_tree_heading("manage", "diff", v.t["diff_lbl"], self._cmd_sort_mdiff)

    # --- УПРАВЛІННЯ ДАНИМИ Treeview (Пошук) ---
    def search_dishes_action(self):
        v = self.view
        
        # 1. ЗБІР ІНГРЕДІЄНТІВ
        v.selected_avail.clear()
        v.selected_excl.clear()

        # Збираємо тільки те, що ВИДІЛЕНО в списках зараз
        for i in v.ing_listbox.curselection():
            v.selected_avail.add(v.ing_listbox.get(i))
        for i in v.excl_listbox.curselection():
            v.selected_excl.add(v.excl_listbox.get(i))

        sel = list(v.selected_avail)
        excl = list(v.selected_excl)
        
        # 2. ФІЛЬТРИ СКЛАДНОСТІ
        allowed_diffs = []
        if v.search_diff_easy.get(): allowed_diffs.append("easy")
        if v.search_diff_med.get(): allowed_diffs.append("medium")
        if v.search_diff_hard.get(): allowed_diffs.append("hard")
        
        # 3. ФІЛЬТРИ КАТЕГОРІЙ (Нове!)
        # Збираємо назви категорій, де стоїть галочка (var.get() == True)
        allowed_cats = [cat for cat, var in v.cat_vars.items() if var.get()]
        
        # 4. ВИКЛИК МОДЕЛІ
        # Додаємо allowed_cats як новий аргумент
        self._search_results = self.model.search_recipes(
            sel, 
            excl, 
            v.search_time_scale.get(), 
            allowed_diffs,
            allowed_cats  # <-- Передаємо список вибраних категорій
        )
        
        # 5. ОНОВЛЕННЯ ТАБЛИЦІ
        self._fill_tree(self._search_results, v.search_tree, "search")
        self.update_search_tree_ui()

    def update_search_tree_ui(self):
        v = self.view
        v.set_tree_heading("search", "name", v.t["name_lbl"], self._cmd_sort_sname)
        v.set_tree_heading("search", "cat", v.t["cat_lbl"], self._cmd_sort_scat) # ДОДАНО!
        v.set_tree_heading("search", "time", v.t["time_lbl"], self._cmd_sort_stime)
        v.set_tree_heading("search", "diff", v.t["diff_lbl"], self._cmd_sort_sdiff)

    # --- ДОПОМІЖНІ ФУНКЦІЇ ЗАПОВНЕННЯ/СОРТУВАННЯ Treeview ---
    def _fill_tree(self, data, tree, tree_key):
        for item in tree.get_children(): 
            tree.delete(item)
        
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Other"]
        
        for r in data:
            # 1. Переклад категорії
            display_cat = r.get("category", "Інше")
            if self.view.current_lang == "en" and display_cat in cats_uk:
                display_cat = cats_en[cats_uk.index(display_cat)]
            elif self.view.current_lang == "uk" and display_cat in cats_en:
                display_cat = cats_uk[cats_en.index(display_cat)]
            
            # 2. Переклад складності
            display_diff = self.view.t.get(r.get("difficulty", ""), r.get("difficulty", ""))
            
            # 3. Вставляємо однакові 4 колонки для обох таблиць
            values = (r["name"], display_cat, r["time"], display_diff)
            tree.insert("", tk.END, values=values, tags=(r["name"],))

    def _sort_tree_data(self, data, tree, tree_key, key_func):
        # Сортування списку даних
        is_asc = self.view._manage_sort_asc if tree_key == "manage" else self.view._search_sort_asc
        data.sort(key=key_func, reverse=not is_asc)
        # Перемалювати таблицю
        self._fill_tree(data, tree, tree_key)

    # --- ДІЇ НАД РЕЦЕПТАМИ (збережено та адаптовано) ---
    def add_recipe_action(self):
        v = self.view
        # Якщо ми в режимі Save, це функція Update. Якщо в Add — функція Add.
        if self.view.btn_add.cget("text") == self.view.t["save_btn"]:
            if self._editing_recipe_name:
                self.save_update(self._editing_recipe_name)
            return

        # Отримуємо дані з форми
        d = self.view.get_form_data()
        
        # --- МАПІНГ: Завжди зберігаємо категорію українською ---
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Other"]
        
        if self.view.current_lang == "en" and d["category"] in cats_en:
            idx = cats_en.index(d["category"])
            d["category"] = cats_uk[idx]
        # --------------------------------------------------------

        if not d["name"] or not d["ingredients"]:
            messagebox.showerror("Помилка", self.view.t.get("err_fill", "Заповніть обов'язкові поля!"))
            return
        
        # Перевірка на існування
        existing_names = [r["name"].lower() for r in self.model.get_all_recipes()]
        if d["name"].lower() in existing_names:
            messagebox.showerror("Помилка", self.view.t.get("err_exists", "Рецепт з такою назвою вже існує!")); return

        # Додаємо рецепт (тепер у d["category"] гарантовано українська назва)
        self.model.add_recipe(d["name"], d["category"], d["ingredients"], d["instructions"], d["time"], d["difficulty"])
        self.update_manage_list()
        self.view.clear_form()
        
        success_msg = "Recipe added!" if self.view.current_lang == "en" else f"Рецепт '{d['name']}' додано!"
        messagebox.showinfo("Успіх", success_msg)
        
    def prepare_update(self):
        # Адаптовано для Treeview
        sel = self.view.manage_tree.selection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для редагування!")
            return
        
        # Отримуємо ім'я з tags (збережено при вставці)
        recipe_name = self.view.manage_tree.item(sel[0], "tags")[0]
        
        # Знайти рецепт
        recipe = next((r for r in self._manage_recipes if r["name"] == recipe_name), None)
        if recipe:
            self.view.fill_form(recipe) # Заповнити форму, змінити кнопку на Save
            self._editing_recipe_name = recipe_name # Зберегти старе ім'я для оновлення

    def save_update(self, old_name):
        d = self.view.get_form_data()
        
        # --- МАПІНГ: Завжди зберігаємо категорію українською ---
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Other"]
        
        if self.view.current_lang == "en" and d["category"] in cats_en:
            idx = cats_en.index(d["category"])
            d["category"] = cats_uk[idx]
        # --------------------------------------------------------

        # Перевірка на порожні поля
        if not d["name"] or not d["ingredients"]:
            messagebox.showerror("Помилка", self.view.t.get("err_fill", "Заповніть обов'язкові поля!"))
            return

        # Перевірка, чи не змінили ми назву на таку, що вже існує (щоб не затерти інший рецепт)
        if d["name"].lower() != old_name.lower():
            existing_names = [r["name"].lower() for r in self.model.get_all_recipes()]
            if d["name"].lower() in existing_names:
                messagebox.showerror("Помилка", self.view.t.get("err_exists", "Рецепт з такою назвою вже існує!"))
                return

        # Оновлення рецепта
        if self.model.update_recipe(old_name, d):
            success_msg = "Recipe updated!" if self.view.current_lang == "en" else "Рецепт оновлено!"
            messagebox.showinfo("Успіх", success_msg)
            
            self.update_manage_list()
            self.view.clear_form() # Очищаємо форму, кнопка повертається до Add
            self._editing_recipe_name = None

    def delete_recipe_action(self):
        # Адаптовано для Treeview
        sel = self.view.manage_tree.selection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для видалення!")
            return
        
        # Отримуємо ім'я
        recipe_name = self.view.manage_tree.item(sel[0], "tags")[0]
        
        confirm = messagebox.askyesno(
            self.view.t["confirm_del_title"], 
            self.view.t["confirm_del_msg"].format(recipe_name)
        )
        
        if confirm:
            self.model.delete_recipe(recipe_name)
            self.update_manage_list()
            messagebox.showinfo("Успіх", f"Рецепт '{recipe_name}' видалено!")

    # --- ДІЇ Treeview ---
    def on_tree_double_click(self, tree_key):
        # Адаптовано для Treeview (показ діалогу деталей)
        tree = self.view.manage_tree if tree_key == "manage" else self.view.search_tree
        sel = tree.selection()
        if sel:
            recipe_name = tree.item(sel[0], "tags")[0]
            # Шукаємо рецепт у поточному списку
            cur_data = self._manage_recipes if tree_key == "manage" else self._search_results
            r = next((rc for rc in cur_data if rc["name"] == recipe_name), None)
            if r:
                self.view.show_custom_details_dialog(r)
                
    def refresh_category_filters(self):
        # Отримуємо всі унікальні категорії з моделі
        recipes = self.model.get_all_recipes()
        categories = sorted(list(set(r.get("category", "Other") for r in recipes)))
        # Кажемо в'юшці намалювати галочки
        self.view.update_category_widgets(categories)
        
    def cancel_edit_action(self):
        # Очищаємо форму
        self.view.clear_form()
        
        # Скидаємо змінну, щоб контролер забув, що ми щось редагували
        self._editing_recipe_name = None
        
        # І ось ТУТ знімаємо фіолетове виділення з таблиці
        if hasattr(self.view, 'manage_tree'):
            sel = self.view.manage_tree.selection()
            if sel:
                self.view.manage_tree.selection_remove(sel)
                
    def sort_column(self, tree, col, reverse):
        data = [(tree.set(k, col), k) for k in tree.get_children('')]
    
        # Сортуємо: числа як числа, текст як текст
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)

        for index, (val, k) in enumerate(data):
            tree.move(k, '', index)

        # При наступному кліку сортуємо навпаки
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))
        