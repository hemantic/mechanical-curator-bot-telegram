from datetime import datetime

import pandas as pd
import requests
from lxml import etree


class CalculationService:
    food_groups = {
        "plants": [
            "авокадо",
            "банан",
            "хурма",
            "миндаль",
            "клубника",
            "финик",
            "малина",
            "перец",
            "помидор",
            "чеснок",
            "лук",
            "маслины",
            "айсберг",
            "калина",
            "вишня",
            "кокос",
            "морковь",
            "имбирь",
            "тыква",
            "голубика",
            "яблоко",
            "огурец",
            "лимон",
            "эдамаме",
            "груша",
            "грейпфрут",
            "оливки",
            "огурцы",
            "салат овощной",
            "руккола",
            "редис",
            "мушмула",
        ],
        "seafood": [
            "кальмар",
            "креветки",
            "мидии",
        ],
        "fish": [
            "форель",
            "семга",
            "лосось",
        ],
        "milk": [],
        "liver": [
            "печень",
            "печеночные",
        ],
        "eggs": [
            "яйцо",
        ],
    }

    def __init__(self, fatsecret_instance, day=None):
        self.fs = fatsecret_instance
        self.day = day

    def __call__(self):
        if not self.day:
            selected_date = datetime.now()
        else:
            selected_date = self.day

        today_foods_df = pd.DataFrame(data=self.fs.food_entries_get(date=selected_date))

        generic_foods = []

        for _, row in today_foods_df[today_foods_df["serving_id"] != "0"].iterrows():
            weight = self.to_grams(
                row["food_id"], row["serving_id"], row["number_of_units"]
            )

            generic_foods.append(
                {
                    "food_entry_name": row["food_entry_name"],
                    "food_id": row["food_id"],
                    "weight": weight,
                    "food_source": "generic",
                    "food_group": self.decide_food_group(row["food_entry_name"]),
                }
            )

        recipe_foods = []

        for _, row in today_foods_df[today_foods_df["serving_id"] == "0"].iterrows():
            total_servings, ingredients = self.load_recipe(row["food_id"])
            eaten_servings = row["number_of_units"]

            portion = float(eaten_servings) / float(total_servings)

            for ingredient in ingredients:
                weight = (
                    self.to_grams(
                        ingredient["food_id"],
                        ingredient["serving_id"],
                        ingredient["number_of_units"],
                    )
                    * portion
                )

                recipe_foods.append(
                    {
                        "food_entry_name": ingredient["food_entry_name"],
                        "food_id": ingredient["food_id"],
                        "weight": weight,
                        "food_source": "recipe",
                        "food_group": self.decide_food_group(
                            ingredient["food_entry_name"]
                        ),
                    }
                )

        overall_foods_df = pd.DataFrame(data=generic_foods + recipe_foods)

        return self.generate_message(overall_foods_df)

    def generate_message(self, overall_foods_df):
        plants_generic_weight = overall_foods_df[
            (overall_foods_df["food_source"] == "generic")
            & (overall_foods_df["food_group"] == "plants")
        ]["weight"].sum()
        plants_recipe_weight = overall_foods_df[
            (overall_foods_df["food_source"] == "recipe")
            & (overall_foods_df["food_group"] == "plants")
        ]["weight"].sum()
        plants_all_weight = plants_generic_weight + plants_recipe_weight

        calcium = 0

        seafood_weight = overall_foods_df[overall_foods_df["food_group"] == "seafood"][
            "weight"
        ].sum()
        seafood_protein = "?"

        liver_weight = overall_foods_df[overall_foods_df["food_group"] == "liver"][
            "weight"
        ].sum()
        liver_protein = "?"

        eggs = 0

        fish_weight = overall_foods_df[overall_foods_df["food_group"] == "fish"][
            "weight"
        ].sum()

        result = ""
        result += f"Растительность: {round(plants_all_weight)}г по свежему весу\n"
        result += f"Кальций: {calcium}%\n"
        result += f"Морепродукты: {round(seafood_weight)}г ({seafood_protein}г белка)\n"
        result += f"Печень: {round(liver_weight)}г ({liver_protein}г белка)\n"
        result += f"Желтки: {round(eggs, 1)}\n"
        result += f"Рыба: {round(fish_weight)}г"

        return result

    def get_serving(self, food_id, serving_id):
        food = self.fs.food_get(food_id)

        servings = (
            food["servings"]["serving"]
            if isinstance(food["servings"]["serving"], list)
            else [food["servings"]["serving"]]
        )

        if serving_id == str(0):
            return servings[0]

        for serving in servings:
            if serving["serving_id"] == str(serving_id):
                return serving

    def to_grams(self, food_id, serving_id, number_of_units):
        serving = self.get_serving(food_id, serving_id)

        return (
            float(number_of_units)
            * float(serving["metric_serving_amount"])
            / float(serving["number_of_units"])
        )

    def load_recipe(self, recipe_id):
        ingredients = []

        response = requests.get(
            f"https://android.fatsecret.com/android/RecipeAndroidPage.aspx?rid={recipe_id}"
        )

        root = etree.fromstring(response.content)

        servings = root.xpath("//servings/text()")[0]

        for ingredient in root.xpath("//recipeingredient"):
            ingredients.append(
                {
                    "food_entry_name": ingredient.xpath("./name/text()")[0],
                    "food_id": ingredient.xpath("./associatedrecipeid/text()")[0],
                    "serving_id": ingredient.xpath("./portionid/text()")[0],
                    "number_of_units": ingredient.xpath("./portionamount/text()")[0],
                }
            )

        return servings, ingredients

    def decide_food_group(self, food_name):
        # First guess is da best!
        for food_group_name, food_group_items in self.food_groups.items():
            for food_group_item in food_group_items:
                if food_group_item.casefold() in food_name.casefold():
                    return food_group_name

        return "other"
