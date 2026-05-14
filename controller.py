import tkinter as tk
from tkinter import messagebox, filedialog
class RecipeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self._manage_recipes = []
        self._search_results = []
        
        self.setup_bindings()
        self.update_manage_list()
        self.refresh_category_filters()
        
        self.view.clear_form()
        

    def setup_bindings(self):
        v = self.view
        
        
        if hasattr(v, 'btn_cancel'):
            v.btn_cancel.config(command=self.cancel_edit_action)
            
        # Меню (збережено)
        v.btn_lang_uk.config(command=lambda: self.change_language("uk"))
        v.btn_lang_en.config(command=lambda: self.change_language("en"))
        v.help_menu.add_command(label=v.t["help_about"], command=self.show_about)
        v.help_menu.add_command(label=v.t["help_shortcuts"], command=self.show_shortcuts)
        v.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        v.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        # Кнопки дій (збережено)
        v.btn_add.config(command=self.add_recipe_action)
        v.btn_update.config(command=self.prepare_update)
        v.btn_delete.config(command=self.delete_recipe_action)
        v.btn_search.config(command=self.search_dishes_action)

        # Treeview (вбудовані дії)
        v.manage_tree.bind("<Double-Button-1>", lambda e: self.on_tree_double_click("manage"))
        v.search_tree.bind("<Double-Button-1>", lambda e: self.on_tree_double_click("search"))
        
        # --- Сортування при клацанні на заголовок
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
        
        self.view.menubar.add_command(label=self.view.t["menu_fav"], command=self.show_favorites_list)
        
        for tree in [v.search_tree, v.manage_tree]:
            for col in ("name", "cat", "time", "diff"):
                tree.heading(col, command=lambda t=tree, c=col: self.sort_column(t, c, False))

        # Вбудований пошук Керування
        v.search_ing_entry.bind("<KeyRelease>", lambda e: self.update_manage_list())
        
        if hasattr(v, 'manage_tree'):
            v.manage_tree.bind("<Delete>", lambda event: self.delete_recipe_action())
            v.manage_tree.bind("<BackSpace>", lambda event: self.delete_recipe_action())
            # Замініть `self.delete_recipe_action` на вашу точну назву методу для видалення

        # 2. Пошук рецепту клавішею Enter
        if hasattr(v, 'search_dishes_action'):
            v.search_dishes_action.bind("<Return>", lambda event: self.search_dishes_action())
            
        if hasattr(v, 'root'):
            v.root.bind("<Return>", self._handle_enter)
            
    def show_about(self):
        from tkinter import messagebox
        messagebox.showinfo(self.view.t["help_about"], self.view.t["about_text"])

    def show_shortcuts(self):
        from tkinter import messagebox
        messagebox.showinfo(self.view.t["help_shortcuts"], self.view.t["shortcuts_text"])
            
    def _handle_enter(self, event):
        if hasattr(self.view, 'notebook'):
            current_tab_id = self.view.notebook.select()
            current_tab_index = self.view.notebook.index(current_tab_id)
            if current_tab_index == 0:
                self.search_dishes_action()

    # --- ЗАГАЛЬНІ ДІЇ ---
    def change_language(self, lang):
        self.view.current_lang = lang
        self.view.update_ui_text()
        
        self.view.help_menu.entryconfig(0, label=self.view.t["help_about"])
        self.view.help_menu.entryconfig(1, label=self.view.t["help_shortcuts"])
    
        self.view.clear_form()
        self.update_manage_list()
    

        self.refresh_category_filters()
    
        if self._search_results:
            self._fill_tree(self._search_results, self.view.search_tree, "search")

    def change_theme(self, theme_name):
        self.view.current_theme = theme_name
        self.view.apply_theme()
        
    
        
    def export_to_txt(self, r):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile=f"{r['name']}.txt",
            title="Зберегти рецепт"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"РЕЦЕПТ: {r['name']}\n")
                    f.write(f"Категорія: {r.get('category', 'Інше')}\n")
                    f.write(f"Час: {r['time']} хв | Складність: {r['difficulty']}\n")
                    f.write("-" * 30 + "\n")
                    f.write("ІНГРЕДІЄНТИ:\n")
                    for ing in r['ingredients']:
                        f.write(f" - {ing}\n")
                    f.write("-" * 30 + "\n")
                    f.write("ІНСТРУКЦІЇ:\n")
                    f.write(r['instructions'])
                
                messagebox.showinfo("Успіх", "Рецепт успішно збережено у файл!")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")
                
    # УПРАВЛІННЯ ДАНИМИ Treeview
    def update_manage_list(self):
        self._manage_recipes = self.model.get_all_recipes()
        
        search_query = self.view.search_ing_var.get().strip().lower()
        if search_query:
            self._manage_recipes = [
                r for r in self._manage_recipes 
                if any(word.startswith(search_query) for word in r["name"].lower().split())
            ]
            
        display_recipes = []
        
        for r in self._manage_recipes:
            r_copy = r.copy()
            
            raw_cat = r_copy.get("category", "Інше")
            raw_diff = r_copy.get("difficulty", "easy")
            
            r_copy["category"] = self.view.t.get(raw_cat, raw_cat)
            r_copy["difficulty"] = self.view.t.get(raw_diff, raw_diff)
            
            display_recipes.append(r_copy)

        self._fill_tree(display_recipes, self.view.manage_tree, "manage")
        
        self.update_manage_tree_ui()
        
    def update_manage_tree_ui(self):
        v = self.view
        v.set_tree_heading("manage", "name", v.t["name_lbl"], self._cmd_sort_mname)
        v.set_tree_heading("manage", "cat", v.t["cat_lbl"], self._cmd_sort_mcat)
        v.set_tree_heading("manage", "time", v.t["time_lbl"], self._cmd_sort_mtime)
        v.set_tree_heading("manage", "diff", v.t["diff_lbl"], self._cmd_sort_mdiff)

    # УПРАВЛІННЯ ДАНИМИ Treeview (Пошук)
    def search_dishes_action(self):
        v = self.view
        
        # 1. ЗБІР ІНГРЕДІЄНТІВ
        v.selected_avail.clear()
        v.selected_excl.clear()

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
        
        # 3. ФІЛЬТРИ КАТЕГОРІЙ
        allowed_cats = [cat for cat, var in v.cat_vars.items() if var.get()]
        
        # 4. ВИКЛИК МОДЕЛІ
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

    # ДОПОМІЖНІ ФУНКЦІЇ ЗАПОВНЕННЯ/СОРТУВАННЯ Treeview
    def _fill_tree(self, data, tree, tree_key):
        for item in tree.get_children(): 
            tree.delete(item)
        
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Закуска", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"]
        
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
        is_asc = self.view._manage_sort_asc if tree_key == "manage" else self.view._search_sort_asc
        data.sort(key=key_func, reverse=not is_asc)
        self._fill_tree(data, tree, tree_key)

    # ДІЇ НАД РЕЦЕПТАМИ
    def add_recipe_action(self):
        v = self.view
        if self.view.btn_add.cget("text") == self.view.t["save_btn"]:
            if self._editing_recipe_name:
                self.save_update(self._editing_recipe_name)
            return
        

        d = self.view.get_form_data()
        
        # МАПІНГ
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Закуска", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"]
        
        if self.view.current_lang == "en" and d["category"] in cats_en:
            idx = cats_en.index(d["category"])
            d["category"] = cats_uk[idx]


        if not d["name"] or not d["ingredients"]:
            messagebox.showerror("Помилка", self.view.t.get("err_fill", "Заповніть обов'язкові поля!"))
            return
        
        diff_value = d.get("difficulty")
        if not diff_value or diff_value == "none" or diff_value == "0":
            err_title = v.t.get("error_title", "Помилка")
            err_msg = v.t.get("error_diff", "Будь ласка, оберіть складність страви!")
            messagebox.showerror(err_title, err_msg)
            return
        
        # Перевірка на існування
        existing_names = [r["name"].lower() for r in self.model.get_all_recipes()]
        if d["name"].lower() in existing_names:
            messagebox.showerror("Помилка", self.view.t.get("err_exists", "Рецепт з такою назвою вже існує!")); return
            
            
        # Додаємо рецепт
        self.model.add_recipe(d["name"], d["category"], d["ingredients"], d["instructions"], d["time"], d["difficulty"])
        self.update_manage_list()
        self.view.clear_form()
        
        success_msg = "Recipe added!" if self.view.current_lang == "en" else f"Рецепт '{d['name']}' додано!"
        messagebox.showinfo("Успіх", success_msg)
        
    def prepare_update(self):
        sel = self.view.manage_tree.selection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для редагування!")
            return
        
        recipe_name = self.view.manage_tree.item(sel[0], "tags")[0]
        
        recipe = next((r for r in self._manage_recipes if r["name"] == recipe_name), None)
        if recipe:
            self.view.fill_form(recipe)
            self._editing_recipe_name = recipe_name

    def show_favorites_list(self):
        all_recipes = self.model.get_all_recipes()
        
        favs = [r for r in all_recipes if r.get("is_favorite") == True]
        
        fav_win = tk.Toplevel(self.view)
        fav_win.title(self.view.t["fav_win_title"])
        fav_win.geometry("400x500")
        fav_win.minsize(300, 400)
        c = self.view.themes[self.view.current_theme]
        fav_win.config(bg=c["surface"])
        
        tk.Label(fav_win, text=self.view.t["fav_win_header"], font=self.view.fonts["logo"], 
                 bg=c["surface"], fg=c["accent"]).pack(pady=15)
        
        if not favs:
            tk.Label(fav_win, text=self.view.t["fav_empty"], font=self.view.fonts["main"], 
                     bg=c["surface"], fg=c["fg_muted"]).pack(pady=20)
            return

        lb = tk.Listbox(fav_win, bg=c["input_bg"], fg=c["fg"], 
                        font=self.view.fonts["main"], borderwidth=0, 
                        selectbackground=c["accent"], highlightthickness=0)
        lb.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for r in favs:
            lb.insert(tk.END, r["name"])
            
        def open_fav(event):
            selection = lb.curselection()
            if selection:
                name = lb.get(selection[0])
                recipe = next((rc for rc in favs if rc["name"] == name), None)
                if recipe:
                    self.view.show_custom_details_dialog(recipe, self.toggle_favorite_action, self.export_to_txt)
        
        lb.bind("<Double-1>", open_fav)
        
    def save_update(self, old_name):
        d = self.view.get_form_data()
        
        # МАПІНГ: Завжди зберігаємо категорію українською
        cats_uk = ["Сніданок", "Обід", "Вечеря", "Десерт", "Закуска", "Інше"]
        cats_en = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Other"]
        
        if self.view.current_lang == "en" and d["category"] in cats_en:
            idx = cats_en.index(d["category"])
            d["category"] = cats_uk[idx]

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
            
    def toggle_favorite_action(self, name, label_widget):
        new_status = self.model.toggle_favorite(name)
        
        star_symbol = "★" if new_status else "☆"
        fav_color = "#3498db" if new_status else self.view.themes[self.view.current_theme]["fg_muted"]
        
        label_widget.config(text=star_symbol, fg=fav_color)
        
        self.update_manage_list()

    # --- ДІЇ Treeview ---
    def on_tree_double_click(self, tree_key):
        tree = self.view.manage_tree if tree_key == "manage" else self.view.search_tree
        sel = tree.selection()
        if sel:
            recipe_name = tree.item(sel[0], "tags")[0]
            cur_data = self._manage_recipes if tree_key == "manage" else self._search_results
            r = next((rc for rc in cur_data if rc["name"] == recipe_name), None)
            if r:
                self.view.show_custom_details_dialog(r, self.toggle_favorite_action, self.export_to_txt)
                
    def refresh_category_filters(self):
        recipes = self.model.get_all_recipes()
        categories = sorted(list(set(r.get("category", "Other") for r in recipes)))
        self.view.update_category_widgets(categories)
        
    def cancel_edit_action(self):
        self.view.clear_form()
        
        self._editing_recipe_name = None
        
        if hasattr(self.view, 'manage_tree'):
            sel = self.view.manage_tree.selection()
            if sel:
                self.view.manage_tree.selection_remove(sel)
                
    def sort_column(self, tree, col, reverse):
        data = [(tree.set(k, col), k) for k in tree.get_children('')]
    
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)

        for index, (val, k) in enumerate(data):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))
        
