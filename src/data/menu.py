import json
from src.data.dish import Dish

class Menu:
    def __init__(self, dishes):
        self.dishes = dishes
    
    @classmethod
    def create_menu(cls, path):
        with open(path, "r", encoding='utf-8') as f:
            dishes = json.load(f)
        converted_dishes = {dish_id: Dish(**params) for dish_id, params in dishes.items()}
        return cls(converted_dishes)
    
    def get_dish(self, dish_id):
        return self.dishes[dish_id]
    
    def get_all_dishes(self):
        return self.dishes.values()