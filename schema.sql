DROP TABLE IF EXISTS global_inventory;
DROP TABLE IF EXISTS potion_catalog;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS cart_items;

CREATE TABLE global_inventory (
    id INT PRIMARY KEY,
    num_red_ml INT NOT NULL,
    num_green_ml INT NOT NULL,
    num_blue_ml INT NOT NULL,
    gold INT NOT NULL
);

CREATE TABLE potion_catalog (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    potion_type INT[] NOT NULL
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,
    sku TEXT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (sku) REFERENCES potion_catalog(sku)
);

INSERT INTO global_inventory (id, num_red_ml, num_green_ml, num_blue_ml, gold)
VALUES (1, 0, 0, 0, 100);
INSERT INTO potion_catalog (sku, name, quantity, price, potion_type)
VALUES ('RED_POTION_0', 'red potion', 0, 50, ARRAY[100, 0, 0, 0]),
       ('GREEN_POTION_0', 'green potion', 0, 50, ARRAY[0, 100, 0, 0]),
       ('BLUE_POTION_0', 'blue potion', 0, 50, ARRAY[0, 0, 100, 0]),
       ('YELLOW_POTION_0', 'yellow potion', 0, 50, ARRAY[50, 50, 0, 0]);