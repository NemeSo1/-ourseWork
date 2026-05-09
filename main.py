import tkinter as tk
from model import RecipeModel
from view import RecipeView
from controller import RecipeController

def main():
    # Ініціалізація компонентів MVC
    model = RecipeModel("recipes.json")
    
    # Створюємо view без передачі root (бо RecipeView сам створює вікно)
    view = RecipeView() 
    
    controller = RecipeController(model, view)
    
    # Запускаємо цикл обробки подій через об'єкт view
    view.mainloop()

if __name__ == "__main__":
    main()