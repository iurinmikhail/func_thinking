import unittest

from unittest.mock import patch, call, Mock
from decimal import Decimal

from src.shipping_cart import add_product_to_cart, Product, delete_handler


class TestShippingCard(unittest.TestCase):
    @patch("src.shipping_cart.SHOPPING_CART", new_callable=list)
    @patch("src.shipping_cart.logger.info")
    def test_add_item_to_cart__when_paid_shipping(
        self, mock_logger: Mock, mock_cart: list
    ) -> None:

        cart = Product(name="car", price=Decimal(5))
        mock_cart = add_product_to_cart(
            name=cart.name, price=cart.price, shopping_cart=mock_cart
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
        mock_cart = add_product_to_cart(cart.name, cart.price, mock_cart)

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
        mock_cart = delete_handler(cart.name, mock_cart)

        expected_calls = [
            call("Сумма к оплате: 0"),
            call("Сумма налога: 0.00"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_cart, [])


if __name__ == "__main__":
    unittest.main()
