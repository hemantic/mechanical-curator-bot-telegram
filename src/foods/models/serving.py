from django.db import models


class Serving(models.Model):
    serving_id = None

    food_entry_id = None
    food_id = None

    food_entry_description = None
    food_entry_name = None
    meal = None

    number_of_units = models.FloatField(null=True)

    calories = models.FloatField(null=True)

    protein = models.FloatField(null=True)
    carbohydrate = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    trans_fat = models.FloatField(null=True)
    saturated_fat = models.FloatField(null=True)
    monounsaturated_fat = models.FloatField(null=True)
    polyunsaturated_fat = models.FloatField(null=True)
    cholesterol = models.FloatField(null=True)

    fiber = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    iron = models.FloatField(null=True)
    potassium = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    sugar = models.FloatField(null=True)
    vitamin_a = models.FloatField(null=True)
    vitamin_c = models.FloatField(null=True)

    date_int = None
