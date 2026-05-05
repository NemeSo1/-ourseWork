import tkinter as tk
from tkinter import messagebox

class RecipeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.show_loading()
        self.setup_bindings()
        self.update_recipe_lists()

    def setup_bindings(self):
        # Меню мови
        self.view.lang_menu.add_command(label="Українська", command=lambda: self.change_language("uk"))
        self.view.lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        
        # Меню тем
        self.view.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        self.view.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        self.view.btn_add.config(command=self.add_recipe)
        self.view.btn_delete.config(command=self.delete_recipe)
        self.view.btn_update.config(command=self.prepare_update)
        self.view.btn_search.config(command=self.search_recipes)
        self.view.recipes_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)
        self.view.res_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)

        self.view.recipes_listbox.bind("<Delete>", lambda event: self.delete_recipe())

    def change_language(self, lang):
        self.view.current_lang = lang
        self.view.update_ui_text()

    def change_theme(self, theme_name):
        self.view.current_theme = theme_name
        self.view.apply_theme()

    def add_recipe(self):
        name = self.view.entry_name.get().strip()
        time = self.view.time_scale.get()
        diff = self.view.diff_var.get()
        cat = self.view.combo_cat.get()
        ings = self.view.entry_ing.get().strip()
        inst = self.view.text_inst.get("1.0", tk.END).strip()

        if not name or not ings:
            messagebox.showerror("Помилка", "Заповніть назву та інгредієнти!")
            return
        
        existing_recipes = [r["name"].lower() for r in self.model.get_all_recipes()]
        if name.lower() in existing_recipes:
            messagebox.showerror("Помилка", f"Рецепт '{name}' вже існує!")
            return

        self.model.add_recipe(name, cat, ings, inst, time, diff)
        self.update_recipe_lists()
        
        self.view.entry_name.delete(0, tk.END)
        self.view.entry_ing.delete(0, tk.END) # Не забудь очистити і поле інгредієнтів
        self.view.text_inst.delete("1.0", tk.END)
        
        messagebox.showinfo("Успіх", f"Рецепт '{name}' успішно додано!")
        
    def delete_recipe(self):
        sel = self.view.recipes_listbox.curselection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для видалення!")
            return

        recipe_name = self.view.recipes_listbox.get(sel[0])
        
        confirm = messagebox.askyesno(
            "Підтвердження видалення", 
            f"Ви впевнені, що хочете видалити рецепт '{recipe_name}'?"
        )
        
        # 3. Якщо користувач натиснув "Так" (True) — видаляємо
        if confirm:
            self.model.delete_recipe(recipe_name)
            self.update_recipe_lists()
            messagebox.showinfo("Успіх", f"Рецепт '{recipe_name}' видалено!")

    def prepare_update(self):
        sel = self.view.recipes_listbox.curselection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для редагування!")
            return
            
        name = self.view.recipes_listbox.get(sel[0])
        recipe = next((r for r in self.model.get_all_recipes() if r["name"] == name), None)
        
        if recipe:
            # Заповнюємо поля даними з рецепта
            self.view.entry_name.delete(0, tk.END)
            self.view.entry_name.insert(0, recipe["name"])
            
            self.view.time_scale.set(recipe["time"])
            self.view.diff_var.set(recipe["difficulty"])
            self.view.combo_cat.set(recipe["category"])
            
            self.view.entry_ing.delete(0, tk.END)
            self.view.entry_ing.insert(0, ", ".join(recipe["ingredients"]))
            
            self.view.text_inst.delete("1.0", tk.END)
            self.view.text_inst.insert("1.0", recipe["instructions"])
            
            # Змінюємо текст кнопки "Додати", щоб користувач розумів, що він у режимі редагування
            self.view.btn_add.config(text="Зберегти зміни", command=lambda: self.save_update(name))

    def save_update(self, old_name):
        # Збираємо нові дані з полів
        new_data = {
            "name": self.view.entry_name.get().strip(),
            "category": self.view.combo_cat.get(),
            "ingredients": self.view.entry_ing.get().strip(),
            "instructions": self.view.text_inst.get("1.0", tk.END).strip(),
            "time": int(self.view.time_scale.get()),
            "difficulty": self.view.diff_var.get()
        }

        if self.model.update_recipe(old_name, new_data):
            messagebox.showinfo("Успіх", "Рецепт оновлено!")
            self.update_recipe_lists()
            # Повертаємо кнопку "Додати" до нормального стану
            self.view.btn_add.config(text=self.view.t["add_btn"], command=self.add_recipe)
            # Очищуємо поля
            self.view.entry_name.delete(0, tk.END)
            self.view.text_inst.delete("1.0", tk.END)
            
    def search_recipes(self):
        # Складний пошук за параметрами
        s_idx = self.view.ing_listbox.curselection()
        selected = [self.view.ing_listbox.get(i) for i in s_idx]
        e_idx = self.view.excl_listbox.curselection()
        excluded = [self.view.excl_listbox.get(i) for i in e_idx]
        
        allowed = []
        if self.view.search_diff_easy.get(): allowed.append("easy")
        if self.view.search_diff_med.get(): allowed.append("medium")
        if self.view.search_diff_hard.get(): allowed.append("hard")
        
        res = self.model.search_recipes(selected, excluded, self.view.search_time_scale.get(), allowed)
        self.view.res_listbox.delete(0, tk.END)
        for r in res: self.view.res_listbox.insert(tk.END, r["name"])

    def update_recipe_lists(self):
        self.view.recipes_listbox.delete(0, tk.END)
        for r in self.model.get_all_recipes():
            self.view.recipes_listbox.insert(tk.END, r["name"])

    def on_recipe_double_click(self, event):
        widget = event.widget
        sel = widget.curselection()
        if sel:
            name = widget.get(sel[0])
            for r in self.model.get_all_recipes():
                if r["name"] == name:
                    self.view.show_custom_details_dialog(r)