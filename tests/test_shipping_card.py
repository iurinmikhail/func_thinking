import unittest

from unittest.mock import patch, call, Mock
from decimal import Decimal

from src.shipping_cart import add_item_to_cart, Product, SHOPPING_CART

class TestShippingCard(unittest.TestCase):
    @patch("shipping_cart.logger.info")
    def test_add_item_to_cart__when_paid_shipping(self, mock_logger: Mock) -> None:
        # global SHOPPING_CART
        SHOPPING_CART.clear()

        cart = Product(name='car', price=Decimal(5))
        add_item_to_cart(name=cart.name, price=cart.price)

        expected_calls = [
            call("Сумма к оплате: 5"),
            call("У вас платная доставка"),
            call("Сумма налога: 0.50"),
        ]
        mock_logger.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(SHOPPING_CART, [cart])

    # @patch("shipping_cart.logger.info")
    # def test_add_item_to_cart__when_free_shipping(self, mock_logger: Mock) -> None:
    #     global SHOPPING_CART
    #     SHOPPING_CART.clear()
    #     cart = Product(name='car', price=Decimal(15))
    #     add_item_to_cart(cart.name, cart.price)

    #     expected_calls = [
    #         call("Сумма к оплате: 15"),
    #         call("У вас бесплатная доставка"),
    #         call("Сумма налога: 1.50"),
    #     ]
    #     mock_logger.assert_has_calls(expected_calls, any_order=False)
    #     self.assertEqual(SHOPPING_CART, [cart])

if __name__ == "__main__":
    unittest.main()
