import tkinter as tk

class RecipeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.setup_bindings()
        self.update_recipe_lists()

    def setup_bindings(self):
        self.view.lang_menu.add_command(label="Українська", command=lambda: self.change_language("uk"))
        self.view.lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.view.btn_add.config(command=self.add_recipe)
        self.view.btn_delete.config(command=self.delete_recipe)
        self.view.btn_search.config(command=self.search_recipes)
        self.view.recipes_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)
        self.view.res_listbox.bind("<Double-Button-1>", self.on_recipe_double_click)

    def change_language(self, lang):
        self.view.current_lang = lang
        self.view.update_ui_text()

    def add_recipe(self):
        name = self.view.entry_name.get().strip()
        category = self.view.combo_cat.get()
        ingredients = self.view.entry_ing.get().strip()
        instructions = self.view.text_inst.get("1.0", tk.END).strip()

        if not name or not ingredients or not instructions:
            self.view.show_error("Будь ласка, заповніть всі поля!")
            return

        self.model.add_recipe(name, category, ingredients, instructions)
        
        self.view.entry_name.delete(0, tk.END)
        self.view.entry_ing.delete(0, tk.END)
        self.view.text_inst.delete("1.0", tk.END)
        
        self.update_recipe_lists()

    def delete_recipe(self):
        selected = self.view.recipes_listbox.curselection()
        if selected:
            name = self.view.recipes_listbox.get(selected[0])
            self.model.delete_recipe(name)
            self.update_recipe_lists()

    def search_recipes(self):
        # Зчитуємо бажані інгредієнти
        sel_ind = self.view.ing_listbox.curselection()
        selected_ings = [self.view.ing_listbox.get(i) for i in sel_ind]
        
        # Зчитуємо заборонені інгредієнти
        excl_ind = self.view.excl_listbox.curselection()
        excl_ings = [self.view.excl_listbox.get(i) for i in excl_ind]
        
        # Передаємо обидва списки в модель
        results = self.model.search_by_ingredients(selected_ings, excl_ings)
        
        self.view.res_listbox.delete(0, tk.END)
        if not results:
            self.view.res_listbox.insert(tk.END, "Нічого не знайдено :(")
        else:
            for r in results:
                self.view.res_listbox.insert(tk.END, r["name"])

    def update_recipe_lists(self):
        self.view.recipes_listbox.delete(0, tk.END)
        for r in self.model.get_all_recipes():
            self.view.recipes_listbox.insert(tk.END, r["name"])
            
    def on_recipe_double_click(self, event):
        widget = event.widget
        selected = widget.curselection()
        if selected:
            recipe_name = widget.get(selected[0])
            for r in self.model.get_all_recipes():
                if r["name"] == recipe_name:
                    self.view.show_custom_details_dialog(r)
                    break