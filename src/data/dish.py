from dataclasses import dataclass

@dataclass(frozen=True)
class Dish:
    dish_id:        str
    dish_name:      str
    stall_id:       str
    stall_name:     str
    cuisine:        str
    item_type:      str
    breakfast_ok:   bool
    halal:          bool
    contains_pork:  bool
    price_sgd:      float
    energy_kcal:    int
    protein_g:      float
    fat_g:          float
    carbs_g:        float
    fibre_g:        float
    sugar_g:        int
    sodium_mg:      int
    calcium_mg:     int
    queue_min:      float
    store_rating:   float
    has_iron:       bool
    has_vit_a:      bool
    has_vit_d:      bool
    has_vit_b12:    bool
    has_vit_b6:     bool
    has_vit_c:      bool
    has_folate:     bool
    