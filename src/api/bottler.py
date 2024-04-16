from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    print(f"potions delivered: {potions_delivered} order_id: {order_id}")

    with db.engine.begin() as connection:
        for potion in potions_delivered:
            if potion.potion_type == [100, 0, 0, 0]:
                connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_red_potions = num_red_potions + :potion_quantity, num_red_ml = num_red_ml - :ml_quantity;"),
                    {"quantity": potion.quantity})
                
            elif potion.potion_type == [0, 100, 0, 0]:
                connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_green_potions = num_green_potions + :potion_quantity, num_green_ml = num_green_ml - :ml_quantity;"),
                    {"quantity": potion.quantity})
                
            elif potion.potion_type == [0, 0, 100, 0]:
                connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_blue_potions = num_blue_potions + :potion_quantity, num_blue_ml = num_blue_ml - :ml_quantity;"),
                    {"quantity": potion.quantity})
                
            else:
                continue

    return "OK"

@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT num_green_ml, num_blue_ml, num_red_ml FROM global_inventory;"))
        num_green_ml = result.fetchone()[0]
        num_blue_ml = result.fetchone()[1]
        num_red_ml = result.fetchone()[2]
        response = []

        if num_red_ml >= 100:
            response.append(
                {
                    "potion_type": [100, 0, 0, 0],
                    "quantity": num_red_ml // 100,
                }
            )
        if num_green_ml >= 100:
            response.append(
                {
                    "potion_type": [0, 100, 0, 0],
                    "quantity": num_green_ml // 100,
                }
            )
        if num_blue_ml >= 100:
            response.append(
                {
                    "potion_type": [0, 0, 100, 0],
                    "quantity": num_blue_ml // 100,
                }
            )

        return response
    

if __name__ == "__main__":
    print(get_bottle_plan())