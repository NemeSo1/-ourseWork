import json

class RecipeModel:
    def __init__(self, filename="recipes.json"):
        self.filename = filename
        self.recipes = self.load_recipes()

    def load_recipes(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_recipes(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=4)

    def add_recipe(self, name, category, ingredients, instructions, time, difficulty):
        # Перетворюємо рядок інгредієнтів у список
        ing_list = [i.strip().lower() for i in ingredients.split(",") if i.strip()]
        new_recipe = {
            "name": name,
            "category": category,
            "ingredients": ing_list,
            "instructions": instructions,
            "time": int(time),
            "difficulty": difficulty
        }
        self.recipes.append(new_recipe)
        self.save_recipes()

    def delete_recipe(self, name):
        self.recipes = [r for r in self.recipes if r["name"] != name]
        self.save_recipes()
        
    def update_recipe(self, old_name, updated_data):
        for i, r in enumerate(self.recipes):
            if r["name"] == old_name:
                # Оновлюємо інгредієнти з рядка у список, як при додаванні
                if isinstance(updated_data["ingredients"], str):
                    updated_data["ingredients"] = [i.strip().lower() for i in updated_data["ingredients"].split(",") if i.strip()]
                
                self.recipes[i] = updated_data
                self.save_recipes()
                return True
        return False

    def get_all_recipes(self, search_query="", category="Всі"):
        # Фільтрація для вкладки "Мої рецепти"
        filtered = self.recipes
        if category != "Всі" and category != "All":
            filtered = [r for r in filtered if r["category"] == category]
        if search_query:
            filtered = [r for r in filtered if search_query.lower() in r["name"].lower()]
        return filtered

    def search_recipes(self, selected_ings, excluded_ings, max_time, allowed_diffs):
        # Складний пошук для вкладки "Пошук страв"
        results = []
        sel_set = set([i.lower() for i in selected_ings])
        excl_set = set([i.lower() for i in excluded_ings])
        
        for r in self.recipes:
            r_ings = set(r["ingredients"])
            # Фільтр часу та складності
            if r["time"] > max_time: continue
            if allowed_diffs and r["difficulty"] not in allowed_diffs: continue
            # Фільтр заборонених інгредієнтів
            if excl_set.intersection(r_ings): continue
            
            if sel_set:
                if sel_set.issubset(r_ings): results.append(r)
            else:
                results.append(r)
        return results