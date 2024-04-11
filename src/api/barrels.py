from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    print(f"barrels delivered: {barrels_delivered} order_id: {order_id}")

    return "OK"

# Gets called once a day
# Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
# and the shop returns back which barrels they'd like to purchase and how many.
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    sql_to_execute = "SELECT num_green_potions FROM global_inventory"


    # As a very basic initial logic, purchase a new small green potion barrel only if the number of potions in inventory is less than 10.
    for barrel in wholesale_catalog:
        if barrel.sku == "SMALL_GREEN_BARREL":
            with db.engine.begin() as connection:
                result = connection.execute(sqlalchemy.text(sql_to_execute))
                num_green_potions = result.scalar()
            if num_green_potions < 10:
                return [
                    {
                        "sku": "SMALL_GREEN_BARREL",
                        "quantity": 1,
                    }
                ]
            else:
                return []
