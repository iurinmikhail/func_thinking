"""Пример функций с побочными эффектами.
В дальнейшем будет показан рефакторинг, как выделить чистые функции.
"""

import logging
from typing import NamedTuple, TypeAlias, Any, TypeVar, Generic
from decimal import Decimal
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s) <%(filename)s::%(funcName)s::%(lineno)d> %(message)s",
)
logger = logging.getLogger("__name__")

Name: TypeAlias = str
Price: TypeAlias = Decimal

T = TypeVar("T")


class Product(NamedTuple):
    name: str
    price: Decimal

    def show_free_shipping_icon(self, messages: dict[str, str]):
        log_message("free_shipping", messages)

    def hide_free_shipping_icon(self, messages: dict[str, str]):
        log_message("paid_shipping", messages)


Cart: TypeAlias = list[Product]

SHOPPING_CART: list[Product] = []


class LoggerError(Exception): ...


class LevelLogging(str, Enum):
    INFO = "info"


MESSAGES = {
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
    for button in get_buy_buttons_dom():
        new_cart = add_item(cart, button)
        has_free_shipping = is_free_shipping(new_cart)
        set_free_shipping_icon(button=button, is_show=has_free_shipping)


def is_free_shipping(cart: Cart):
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


def add_item_to_cart(name: str, price: float) -> None:
    global SHOPPING_CART
    new_shopping_cart = add_item(SHOPPING_CART, make_product(name=name, price=price))
    SHOPPING_CART = new_shopping_cart
    total = calc_total(SHOPPING_CART)
    set_cart_total_dom(total)
    update_shipping_icons(SHOPPING_CART)
    update_tax_dom(total)


def remove_item_by_name(cart: Cart, name: Name) -> Cart:
    idx = None
    for i, _ in enumerate(cart):
        if cart[i].name == name:
            idx = i
    if idx is not None:
        return remove_items(cart, idx)
    return cart

def remove_items(array: list[T], idx: int) -> list[T]:
    new_array = array.copy()
    new_array.pop(idx)
    return new_array


def delete_handler(name: Name) -> None:
    global SHOPPING_CART
    shopping_cart = remove_item_by_name(SHOPPING_CART, name)
    total = calc_total(shopping_cart)
    set_cart_total_dom(total)
    update_shipping_icons(shopping_cart)
    update_tax_dom(total)
    SHOPPING_CART = shopping_cart



if __name__ == "__main__":
    product = Product(name="car", price=Decimal(15))
    add_item_to_cart(name="car", price=15)
    print(f"{SHOPPING_CART=}")
    assert SHOPPING_CART == [product]
    delete_handler(name=product.name)
    assert SHOPPING_CART == []