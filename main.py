import tkinter as tk
from model import RecipeModel
from view import RecipeView
from controller import RecipeController

def main():
    root = tk.Tk()
    
    # Ініціалізація компонентів MVC
    model = RecipeModel("recipes.json")
    view = RecipeView(root)
    controller = RecipeController(model, view)
    
    # Запуск головного циклу обробки подій
    root.mainloop()

if __name__ == "__main__":
    main()