import unittest

from unittest.mock import patch, call, Mock
from decimal import Decimal

from src.shipping_cart import (
    add_product_to_cart,
    Product,
    delete_handler,
    free_tie_clip,
    set_price_by_name,
    object_set,
    calc_total,
)
from src._types import Name, Price, Cart


class TestShippingCard(unittest.TestCase):
    @patch("src.shipping_cart.SHOPPING_CART", new_callable=dict)
    @patch("src.shipping_cart.logger.info")
    def test_add_item_to_cart__when_paid_shipping(
        self, mock_logger: Mock, mock_cart: dict
    ) -> None:

        product = Product(name=Name("car"), price=Price(5))
        mock_cart = add_product_to_cart(
            name=product["name"], price=product["price"], shopping_cart=mock_cart
        )
        expected_calls = [
            call("Сумма к оплате: 5"),
            call("У вас платная доставка"),
            call("Сумма налога: 0.50"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, {product["name"]: product})

    @patch("src.shipping_cart.SHOPPING_CART", new_callable=dict)
    @patch("src.shipping_cart.logger.info")
    def test_add_item_to_cart__when_free_shipping(
        self, mock_logger: Mock, mock_cart: dict
    ) -> None:
        product = Product(name=Name("car"), price=Price(15))
        mock_cart = add_product_to_cart(name=product["name"], price=product["price"], shopping_cart=mock_cart)

        expected_calls = [
            call("Сумма к оплате: 15"),
            call("У вас бесплатная доставка"),
            call("Сумма налога: 1.50"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart,  {product["name"]: product})

    @patch("src.shipping_cart.SHOPPING_CART", new_callable=dict)
    @patch("src.shipping_cart.logger.info")
    def test_delete_handler(self, mock_logger: Mock, mock_cart: dict) -> None:
        product = Product(name=Name("car"), price=Price(15))
        mock_cart = delete_handler(product["name"], mock_cart)

        expected_calls = [
            call("Сумма к оплате: 0"),
            call("Сумма налога: 0.00"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, {})

    def test_free_tie_clip(self):
        """Тест функции добавления бесплатного зажима к галстуку."""
        tie_clip = Product(
            name=Name("tie clip"),
            price=Price(0),
        )
        tie = Product(
            name=Name("tie"),
            price=Price(100),
        )
        cart: Cart = {tie["name"]: tie}
        assert free_tie_clip(cart) == {tie["name"]:tie, tie_clip["name"]: tie_clip}

    def test_set_price_by_name(self):
        """Тестирует функцию изменения стоимости товара."""
        name = Name("x")
        product = Product(name=name, price=Price(100))
        cart = {product["name"]: product}
        new_price = Price(400)
        assert set_price_by_name(cart, name, new_price) == {product["name"]: Product(name=name, price=new_price)}
        assert cart == {product["name"]: product}

    def test_object_set(self):
        o = {"price": 200}
        price = 37
        assert object_set(o, 'price', price) == {"price": 37}
        assert o == {"price": 200}

    def test_calc_total(self):
        o = {
            "test1": {"name": "test1", "price": 200},
            "test2": {"name": "test2", "price": 200},
            }
        assert calc_total(o) == 400

if __name__ == "__main__":
    unittest.main()
