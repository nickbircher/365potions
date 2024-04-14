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

    sql_to_execute = "UPDATE global_inventory SET num_green_ml = num_green_ml + :quantity, gold = gold - :price;"

    for barrel in barrels_delivered:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(sql_to_execute), quantity=(barrel.quantity * barrel.ml_per_barrel), price=barrel.price)

    return "OK"

# Gets called once a day
# Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
# and the shop returns back which barrels they'd like to purchase and how many.
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    sql_to_execute = "SELECT * FROM global_inventory"


    # As a very basic initial logic, purchase a new small green potion barrel only if the number of potions in inventory is less than 10.
    for barrel in wholesale_catalog:
        if barrel.potion_type == [0, 100, 0, 0]:
            with db.engine.begin() as connection:
                result = connection.execute(sqlalchemy.text(sql_to_execute))
                num_green_potions = result.fetchone()[0]
                gold = result.fetchone()[2]
            if num_green_potions < 10 and gold >= barrel.price:
                return [
                    {
                        "sku": barrel.sku,
                        "quantity": 1,
                    }
                ]
            else:
                return []
