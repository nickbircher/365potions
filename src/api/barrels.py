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
    print(f"barrels delivered: {barrels_delivered} order_id: {order_id}")

    with db.engine.begin() as connection:
        for barrel in barrels_delivered:
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE global_inventory SET
                    num_red_ml = num_red_ml + :num_red_ml,
                    num_green_ml = num_green_ml + :num_green_ml,
                    num_blue_ml = num_blue_ml + :num_blue_ml,
                    gold = gold - :gold_deduct;
                    """
                ),
                {
                    "num_red_ml": barrel.potion_type[0] * barrel.quantity * barrel.ml_per_barrel,
                    "num_green_ml": barrel.potion_type[1] * barrel.quantity * barrel.ml_per_barrel,
                    "num_blue_ml": barrel.potion_type[2] * barrel.quantity * barrel.ml_per_barrel,
                    "gold_deduct": barrel.price,
                })

    return "OK"

# Gets called once a day
# Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
# and the shop returns back which barrels they'd like to purchase and how many.
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    print(wholesale_catalog)

    sql_to_execute = "SELECT num_red_ml, num_green_ml, num_blue_ml, gold FROM global_inventory;"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_to_execute)).fetchone()
        num_red_ml = result[0]
        num_green_ml = result[1]
        num_blue_ml = result[2]
        gold = result[3]

        if num_red_ml <= num_green_ml and num_red_ml <= num_blue_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [1, 0, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
                    else:
                        return []

        elif num_green_ml <= num_blue_ml and num_green_ml <= num_red_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 1, 0, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
                    else:
                        return []

        elif num_blue_ml <= num_green_ml and num_blue_ml <= num_red_ml:
            for barrel in wholesale_catalog:
                if barrel.potion_type == [0, 0, 1, 0]:
                    if gold >= barrel.price:
                        return [
                            {
                                "sku": barrel.sku,
                                "quantity": 1,
                            }
                        ]
                    else:
                        return []
        else:
            return []
