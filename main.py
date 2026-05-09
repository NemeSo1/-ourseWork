import tkinter as tk
from model import RecipeModel
from view import RecipeView
from controller import RecipeController

def main():
    model = RecipeModel("recipes.json")
    view = RecipeView()
    controller = RecipeController(model, view)
    view.mainloop()

if __name__ == "__main__":
    main()