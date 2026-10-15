import pytest
from unittest.mock import Mock

from praktikum.burger import Burger

def create_bun(name="Булочка", price=100):
    bun = Mock()
    bun.get_name.return_value = name
    bun.get_price.return_value = price
    return bun

def create_ingredient(ingredient_type="SAUCE", name="Соус", price=50):
    ingredient = Mock()
    ingredient.get_type.return_value = ingredient_type
    ingredient.get_name.return_value = name
    ingredient.get_price.return_value = price
    return ingredient

def test_burger_init():
    burger = Burger()
    assert burger.bun is None
    assert burger.ingredients == []

def test_set_buns():
    burger = Burger()
    bun = create_bun()
    burger.set_buns(bun)
    assert burger.bun is bun

def test_add_ingredient():
    burger = Burger()
    ingredient = create_ingredient()
    burger.add_ingredient(ingredient)
    assert burger.ingredients == [ingredient]

def test_remove_ingredient():
    burger = Burger()
    first = create_ingredient(name="Первый")
    second = create_ingredient(name="Второй")
    burger.add_ingredient(first)
    burger.add_ingredient(second)
    burger.remove_ingredient(0)
    assert burger.ingredients == [second]

@pytest.mark.parametrize(
    "index, new_index, expected",
    [
        (0, 1, ["B", "A", "C"]),
        (2, 0, ["C", "A", "B"]),
        (1, 1, ["A", "B", "C"]),
    ],
)

def test_move_ingredient(index, new_index, expected):
    burger = Burger()
    for name in ["A", "B", "C"]:
        burger.add_ingredient(create_ingredient(name=name))
    burger.move_ingredient(index, new_index)
    actual = [
        item.get_name.return_value for item in burger.ingredients
    ]
    assert actual == expected

@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_price",
    [
        (100, [], 200),
        (100, [50], 250),
        (100, [50, 30, 20], 300),
        (0, [10, 15], 25),
    ],
)

def test_get_price(bun_price, ingredient_prices, expected_price):
    burger = Burger()
    burger.set_buns(create_bun(price=bun_price))
    for price in ingredient_prices:
        burger.add_ingredient(create_ingredient(price=price))
    assert burger.get_price() == expected_price

def test_get_receipt():
    burger = Burger()
    burger.set_buns(
        create_bun(name="Флюоресцентная булочка", price=100)
    )
    burger.add_ingredient(
        create_ingredient("SAUCE", "Сырный", 50)
    )
    burger.add_ingredient(
        create_ingredient("FILLING", "Котлета", 100)
    )
    expected_receipt = (
        "(==== Флюоресцентная булочка ====)\n"
        "= sauce Сырный =\n"
        "= filling Котлета =\n"
        "(==== Флюоресцентная булочка ====)\n"
        "\n"
        "Price: 350"
    )
    assert burger.get_receipt() == expected_receipt