import unittest

from unittest.mock import patch, call, Mock
from decimal import Decimal

from src.shipping_cart import (
    add_product_to_cart,
    Product,
    delete_handler,
    free_tie_clip,
    set_price_by_name,
)
from src._types import Name, Price, Cart


class TestShippingCard(unittest.TestCase):
    @patch("src.shipping_cart.SHOPPING_CART", new_callable=list)
    @patch("src.shipping_cart.logger.info")
    def test_add_item_to_cart__when_paid_shipping(
        self, mock_logger: Mock, mock_cart: list
    ) -> None:

        cart = Product(name="car", price=Decimal(5))
        mock_cart = add_product_to_cart(
            name=cart["name"], price=cart["price"], shopping_cart=mock_cart
        )
        expected_calls = [
            call("Сумма к оплате: 5"),
            call("У вас платная доставка"),
            call("Сумма налога: 0.50"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, [cart])

    @patch("src.shipping_cart.SHOPPING_CART", new_callable=list)
    @patch("src.shipping_cart.logger.info")
    def test_add_item_to_cart__when_free_shipping(
        self, mock_logger: Mock, mock_cart: list
    ) -> None:
        cart = Product(name="car", price=Decimal(15))
        mock_cart = add_product_to_cart(name=cart["name"], price=cart["price"], shopping_cart=mock_cart)

        expected_calls = [
            call("Сумма к оплате: 15"),
            call("У вас бесплатная доставка"),
            call("Сумма налога: 1.50"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, [cart])

    @patch("src.shipping_cart.SHOPPING_CART", new_callable=list)
    @patch("src.shipping_cart.logger.info")
    def test_delete_handler(self, mock_logger: Mock, mock_cart: list) -> None:
        cart = Product(name="car", price=Decimal(15))
        mock_cart = delete_handler(cart["name"], mock_cart)

        expected_calls = [
            call("Сумма к оплате: 0"),
            call("Сумма налога: 0.00"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, [])

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
        cart: Cart = [tie]
        assert free_tie_clip(cart) == [tie, tie_clip]

    def test_set_price_by_name(self):
        """Тестирует функцию изменения стоимости товара."""
        name = "x"
        product = Product(name=name, price=100)
        cart = [product]
        new_price = Price(400)
        assert set_price_by_name(cart, name, new_price) == [Product(name=name, price=new_price)]
        assert cart == [product]


if __name__ == "__main__":
    unittest.main()
