import json
import os

class RecipeModel:
    def __init__(self, filename="recipes.json"):
        self.filename = filename
        self.recipes = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.recipes, file, ensure_ascii=False, indent=4)

    def add_recipe(self, name, category, ingredients, instructions):
        new_recipe = {
            "name": name,
            "category": category,
            "ingredients": [i.strip().lower() for i in ingredients.split(',') if i.strip()],
            "instructions": instructions.strip()
        }
        self.recipes.append(new_recipe)
        self.save_data()

    def delete_recipe(self, name):
        self.recipes = [r for r in self.recipes if r['name'] != name]
        self.save_data()

    def get_all_recipes(self):
        return self.recipes

    def search_by_ingredients(self, selected_ingredients, excluded_ingredients=None):
        """
        Пошук рецептів. 
        Якщо є excluded_ingredients, рецепт відкидається.
        Якщо вибрано selected_ingredients, шукає хоча б один збіг.
        Якщо вибрано тільки виключення, показує всі безпечні рецепти.
        """
        if excluded_ingredients is None:
            excluded_ingredients = []
            
        result = []
        selected_set = set([i.lower() for i in selected_ingredients]) if selected_ingredients else set()
        excluded_set = set([i.lower() for i in excluded_ingredients])
        
        for recipe in self.recipes:
            recipe_ing_set = set(recipe['ingredients'])
            
            # Якщо є заборонені інгредієнти, одразу пропускаємо цей рецепт
            if excluded_set.intersection(recipe_ing_set):
                continue
                
            # Якщо є бажані інгредієнти
            if selected_set:
                if selected_set.intersection(recipe_ing_set):
                    result.append(recipe)
            else:
                # Якщо ми нічого не шукали (або шукали ТІЛЬКИ "без цибулі"),
                # додаємо цей рецепт, бо він пройшов перевірку вище
                result.append(recipe)
                
        return result