from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/audit")
def get_inventory():
    """ """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT num_green_potions, num_green_ml, num_blue_potions, num_blue_ml, num_red_potions, num_red_ml, gold FROM global_inventory LIMIT 1;"
            )
        )
        num_green_potions = result.fetchone()[0]
        num_green_ml = result.fetchone()[1]
        num_blue_potions = result.fetchone()[2]
        num_blue_ml = result.fetchone()[3]
        num_red_potions = result.fetchone()[4]
        num_red_ml = result.fetchone()[5]
        gold = result.fetchone()[6]

    return {
        "number_of_potions": num_green_potions + num_blue_potions + num_red_potions,
        "ml_in_barrels": num_green_ml + num_blue_ml + num_red_ml,
        "gold": gold,
    }


# Gets called once a day
@router.post("/plan")
def get_capacity_plan():
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """

    return {
        "potion_capacity": 0,
        "ml_capacity": 0
        }

class CapacityPurchase(BaseModel):
    potion_capacity: int
    ml_capacity: int

# Gets called once a day
@router.post("/deliver/{order_id}")
def deliver_capacity_plan(capacity_purchase : CapacityPurchase, order_id: int):
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """

    return "OK"
