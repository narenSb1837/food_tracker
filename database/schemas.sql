CREATE TABLE Food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    protein FLOAT NOT NULL,
    carbs FLOAT NOT NULL,
    fats FLOAT NOT NULL
);
CREATE TABLE food_date(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id int,
    date DATE,
    FOREIGN KEY (food_id) REFERENCEs Food(id)
)