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
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.recipes, file, ensure_ascii=False, indent=4)

    def add_recipe(self, name, category, ingredients, instructions, time, difficulty):
        new_recipe = {
            "name": name,
            "category": category,
            "ingredients": [i.strip().lower() for i in ingredients.split(',') if i.strip()],
            "instructions": instructions.strip(),
            "time": int(time),
            "difficulty": difficulty
        }
        self.recipes.append(new_recipe)
        self.save_data()

    def delete_recipe(self, name):
        self.recipes = [r for r in self.recipes if r['name'] != name]
        self.save_data()

    def get_all_recipes(self):
        return self.recipes

    def search_recipes(self, selected_ingredients, excluded_ingredients, max_time, allowed_diffs):
        result = []
        selected_set = set([i.lower() for i in selected_ingredients])
        excluded_set = set([i.lower() for i in excluded_ingredients])
        
        for recipe in self.recipes:
            # Фільтр по складності (якщо нічого не вибрано, показуємо всі)
            recipe_diff = recipe.get('difficulty', 'easy')
            if allowed_diffs and recipe_diff not in allowed_diffs:
                continue
                
            recipe_ing_set = set(recipe['ingredients'])
            
            # Фільтр заборонених
            if excluded_set.intersection(recipe_ing_set):
                continue
            
            # Фільтр по часу
            if recipe.get('time', 0) > max_time:
                continue
                
            # Фільтр бажаних
            if selected_set:
                if selected_set.intersection(recipe_ing_set):
                    result.append(recipe)
            else:
                result.append(recipe)
                
        return result