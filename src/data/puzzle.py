import json
from dataclasses import dataclass, field
from pathlib import Path
from src.data.menu import Menu

@dataclass(frozen=True)
class Puzzle:
    id:                             str
    difficulty:                     str
    menu:                           Menu
    days:                           int
    meals_per_day:                  int
    max_times_per_dish_per_week:    int
    description:                    str
    min_store_rating:               float | None = None
    weekly:                         dict = field(default_factory=dict)
    daily:                          dict = field(default_factory=dict)
    daily_presence:                 dict = field(default_factory=dict)
    weekly_presence:                dict = field(default_factory=dict)
    objective:                      dict = field(default_factory=dict)

    @classmethod
    def create_puzzle(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            puzzle = json.load(f)
        root = Path(__file__).resolve()
        menu_path = root.parents[2] / puzzle['menu']
        puzzle['menu'] = Menu.create_menu(menu_path)
        return cls(**puzzle)
