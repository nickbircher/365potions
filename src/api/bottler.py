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
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE global_inventory SET
                    num_red_ml = num_red_ml - :red_ml_update,
                    num_green_ml = num_green_ml - :green_ml_update,
                    num_blue_ml = num_blue_ml - :blue_ml_update;
                    UPDATE potions SET quantity = quantity + :potion_quantity
                    WHERE potion_type = ARRAY[:potion_type_array]::int[];
                    """
                ),
                {
                    "red_ml_update": potion.potion_type[0] * potion.quantity,
                    "green_ml_update": potion.potion_type[1] * potion.quantity,
                    "blue_ml_update": potion.potion_type[2] * potion.quantity,
                    "potion_quantity": potion.quantity,
                    "potion_type_array": potion.potion_type,
                })

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
        result = connection.execute(sqlalchemy.text("SELECT num_green_ml, num_blue_ml, num_red_ml FROM global_inventory;")).fetchone()
        num_green_ml = result[0]
        num_blue_ml = result[1]
        num_red_ml = result[2]
        response = []

        if num_red_ml >= 100:
            response.append(
                {
                    "potion_type": [100, 0, 0, 0],
                    "quantity": 1,
                }
            )
        if num_green_ml >= 100:
            response.append(
                {
                    "potion_type": [0, 100, 0, 0],
                    "quantity": 1,
                }
            )
        if num_blue_ml >= 100:
            response.append(
                {
                    "potion_type": [0, 0, 100, 0],
                    "quantity": 1,
                }
            )
        if num_red_ml >= 50 and num_green_ml >= 50:
            response.append(
                {
                    "potion_type": [50, 50, 0, 0],
                    "quantity": 1,
                }
            )

        return response
    

if __name__ == "__main__":
    print(get_bottle_plan())
