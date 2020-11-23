import logging
import json

import azure.functions as func

def compute_ingredients(weight):
    return {
        "Salt": {"unit": "cups", "quantity": 0.05 * weight},
        "Water": {"unit": "gallons", "quantity": 0.66 * weight},
        "Brown sugar": {"unit": "cups", "quantity": 0.13 * weight},
        "Shallots": {"unit": "cups", "quantity": 0.2 * weight},
        "Garlic": {"unit": "cloves", "quantity": 0.4 * weight},
        "Whole peppercorns": {"unit": "tablespoons", "quantity": 0.13 * weight},
        "Dried juniper berries": {"unit": "tablespoons", "quantity": 0.13 * weight},
        "Fresh rosemary": {"unit": "tablespoons", "quantity": 0.13 * weight},
        "Thyme": {"unit": "tablespoons", "quantity": 0.06 * weight}
    }

def compute_cooking_duration(weight):
    return {
        "Brine time (hours)": 2.4 * weight,
        "Roast time (minutes)": 15 * weight
    }

def compute_recipe(turkey_weight):
    return {
        "Ingredients": compute_ingredients(turkey_weight),
        "Cooking duration": compute_cooking_duration(turkey_weight)
    }

def prettify_recipe(recipe):
    for ingredient, details in recipe["Ingredients"].items():
        details["quantity"] = round(details["quantity"], 2)
    return recipe

def handler(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    weight: int = int(req.params.get('turkeyWeight'))

    if weight:
        return func.HttpResponse(
                json.dumps(prettify_recipe(compute_recipe(weight))),
                mimetype="application/json")
    else:
        return func.HttpResponse(
             "Please pass the turkey weight on the query string as 'turkeyWeight'",
             status_code=400
        )

if __name__ == "__main__":
    print(json.dumps(prettify_recipe(compute_recipe(10))))
