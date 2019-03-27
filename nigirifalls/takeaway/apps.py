from django.apps import AppConfig
from watson import search as watson


class TakeawayConfig(AppConfig):
    name = 'takeaway'

    def ready(self):
        dish_model = self.get_model("Dish")
        watson.register(dish_model, fields=("name", "description", "dish_type"))
