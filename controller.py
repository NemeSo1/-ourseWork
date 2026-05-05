import tkinter as tk
from tkinter import messagebox

class RecipeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
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
        self.view.btn_search.config(command=self.search_recipes)
        self.view.recipes_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)
        self.view.res_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)

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

        self.model.add_recipe(name, cat, ings, inst, time, diff)
        self.update_recipe_lists()
        # Очищення
        self.view.entry_name.delete(0, tk.END)
        self.view.text_inst.delete("1.0", tk.END)
        
    def delete_recipe(self):
        sel = self.view.recipes_listbox.curselection()
        if not sel:
            messagebox.showwarning("Увага", "Виберіть рецепт для видалення!")
            return
            
        # Отримуємо назву вибраного рецепту
        recipe_name = self.view.recipes_listbox.get(sel[0])
        
        # Видаляємо з моделі
        self.model.delete_recipe(recipe_name)
        
        # Оновлюємо список на екрані
        self.update_recipe_lists()
        messagebox.showinfo("Успіх", f"Рецепт '{recipe_name}' видалено!")

    def search_recipes(self):
        # Отримуємо вибрані бажані інгредієнти
        sel_idx = self.view.ing_listbox.curselection()
        selected = [self.view.ing_listbox.get(i) for i in sel_idx]
        
        # Отримуємо вибрані заборонені інгредієнти
        excl_idx = self.view.excl_listbox.curselection()
        excluded = [self.view.excl_listbox.get(i) for i in excl_idx]
        
        # Отримуємо максимальний час приготування з повзунка
        max_time = self.view.search_time_scale.get()
        
        # Отримуємо вибрані рівні складності з прапорців
        allowed_diffs = []
        if self.view.search_diff_easy.get(): 
            allowed_diffs.append("easy")
        if self.view.search_diff_med.get(): 
            allowed_diffs.append("medium")
        if self.view.search_diff_hard.get(): 
            allowed_diffs.append("hard")
        
        # Викликаємо функцію пошуку з моделі, передаючи всі 4 параметри
        results = self.model.search_recipes(selected, excluded, max_time, allowed_diffs)
        
        # Очищаємо список результатів на екрані та заповнюємо новими
        self.view.res_listbox.delete(0, tk.END)
        for r in results:
            self.view.res_listbox.insert(tk.END, r["name"])

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