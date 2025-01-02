"""Пример функций с побочными эффектами.
В дальнейшем будет показан рефакторинг, как выделить чистые функции.
"""

import logging
from typing import NamedTuple, TypeAlias, Any, TypeVar, Generic
from decimal import Decimal
from enum import Enum
from copy import deepcopy


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s) <%(filename)s::%(funcName)s::%(lineno)d> %(message)s",
)
logger = logging.getLogger("__name__")

Name: TypeAlias = str
Price: TypeAlias = Decimal

T = TypeVar("T")


class Product(NamedTuple):
    name: Name
    price: Price

    def show_free_shipping_icon(self, messages: dict[str, str]):
        log_message("free_shipping", messages)

    def hide_free_shipping_icon(self, messages: dict[str, str]):
        log_message("paid_shipping", messages)


Cart: TypeAlias = list[Product]

SHOPPING_CART: Cart = []


class LoggerError(Exception): ...


class LevelLogging(str, Enum):
    INFO = "info"


MESSAGES: dict[str, str] = {
    "free_shipping": "У вас бесплатная доставка",
    "paid_shipping": "У вас платная доставка",
    "tax_amount": "Сумма налога: {tax}",
    "cart_total": "Сумма к оплате: {total}",
}


def build_log_message(message_type: str, messages: dict[str, str], **kwargs) -> str:
    if message_type in messages:
        return messages[message_type].format(**kwargs)
    raise LoggerError(f"Неизвестный тип сообщения: {message_type}")


def log_message(
    message_type: str,
    messages: dict[str, str],
    level: str = LevelLogging.INFO.value,
    **kwargs,
) -> None:
    message = build_log_message(message_type, messages, **kwargs)
    getattr(logger, level)(message)


def get_buy_buttons_dom() -> Cart:
    return SHOPPING_CART


def set_free_shipping_icon(button: Product, is_show: bool) -> None:
    if is_show:
        button.show_free_shipping_icon(MESSAGES)
    else:
        button.hide_free_shipping_icon(MESSAGES)


def update_shipping_icons(cart: Cart) -> None:
    for button in cart:
        new_cart = add_item(cart, button)
        has_free_shipping = is_free_shipping(new_cart)
        set_free_shipping_icon(button=button, is_show=has_free_shipping)


def is_free_shipping(cart: Cart):
    """Проверяет действие бесплатной доставки."""
    return calc_total(cart) >= 20


def set_tax_dom(price: Price) -> None:
    log_message("tax_amount", MESSAGES, tax=round(price, 2))


def update_tax_dom(total: Decimal) -> None:
    set_tax_dom(calc_tax(total))


def calc_tax(amount: Decimal) -> Decimal:
    return amount * Decimal(0.10)


def set_cart_total_dom(total: Decimal) -> None:
    log_message("cart_total", MESSAGES, total=total)


def calc_total(cart: list[Product]) -> Decimal:
    return sum(map(lambda x: x.price, cart))


def cart_tax(cart: Cart) -> Decimal:
    """Вычисляет налог."""
    return calc_tax(calc_total(cart))


def add_element_last(array: list[T], elem: T) -> list[T]:
    # копирование при записи
    new_array = array.copy()  # создать копию
    new_array.append(elem)  # изменить копию
    return new_array  # Вернуть копию


def add_item(cart: Cart, product: Product) -> Cart:
    return add_element_last(cart, product)


def make_product(name: str, price: float) -> Product:
    return Product(
        name=Name(name),
        price=Price(price),
    )


def set_price(product: Product, price: Price) -> Product:
    product_copy = deepcopy(product)
    product_copy.price = price
    return product_copy


def set_price_by_name(cart: Cart, name: Name, price: Price) -> Cart:
    cart_copy = cart.copy()
    for product in cart_copy:
        if product.name == name:
            product = set_price(product, price)
    return cart_copy


def get_idx_by_name(cart: Cart, name: Name) -> int | None:
    """Получает по наименования индекс в корзине."""
    for idx, product in enumerate(cart):
        if product.name == name:
            return idx
    return None


def remove_item_by_name(cart: Cart, name: Name) -> Cart:
    idx = get_idx_by_name(cart, name)
    if idx is not None:
        return remove_items(cart, idx)
    return cart


def remove_items(array: list[T], idx: int) -> list[T]:
    """Удаление из списка по индексу с копированием при записи."""
    new_array = array.copy()
    new_array.pop(idx)
    return new_array


def add_product_to_cart(name: str, price: float, shopping_cart: Cart) -> Cart:
    """Добавляет товар в корзину."""
    new_shopping_cart = add_item(shopping_cart, make_product(name=name, price=price))

    total = calc_total(new_shopping_cart)
    set_cart_total_dom(total)
    update_shipping_icons(new_shopping_cart)
    update_tax_dom(total)
    return new_shopping_cart


def delete_handler(name: Name, shopping_cart: Cart) -> Cart:
    """Удаляет товар из корзины по его наименования."""
    new_shopping_cart = remove_item_by_name(shopping_cart, name)
    total = calc_total(new_shopping_cart)
    set_cart_total_dom(total)
    update_shipping_icons(new_shopping_cart)
    update_tax_dom(total)
    return new_shopping_cart


if __name__ == "__main__":
    product = Product(name="car", price=Decimal(15))
    SHOPPING_CART = add_product_to_cart(
        name="car", price=15, shopping_cart=SHOPPING_CART
    )
    print(f"{SHOPPING_CART=}")
    assert SHOPPING_CART == [product]
    SHOPPING_CART = delete_handler(name=product.name, shopping_cart=SHOPPING_CART)
    print(f"{SHOPPING_CART=}")
    assert SHOPPING_CART == []
