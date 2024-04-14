from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    
    sql_to_execute = "SELECT * FROM global_inventory"
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_to_execute))
        num_green_potions = result.fetchone()[0]


    if num_green_potions is not None:
        return [
            {
                "sku": "GREEN_POTION_0",
                "name": "green potion",
                "quantity": num_green_potions, 
                "price": 50,
                "potion_type": [0, 100, 0, 0],
            }
        ]
    else:
        return []
