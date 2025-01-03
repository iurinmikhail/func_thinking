"""Пример функций с побочными эффектами.
В дальнейшем будет показан рефакторинг, как выделить чистые функции.
"""

import logging
from decimal import Decimal
from typing import Any, Mapping

from src._types import Name, Price, Product, Cart, T, K, V
from src.utils import log_message, show_free_shipping_icon, hide_free_shipping_icon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s) <%(filename)s::%(funcName)s::%(lineno)d> %(message)s",
)
logger = logging.getLogger("__name__")


SHOPPING_CART: Cart = {}
FREE_SHIPPING_THRESHOLD = Decimal(10)

MESSAGES: dict[str, str] = {
    "free_shipping": "У вас бесплатная доставка",
    "paid_shipping": "У вас платная доставка",
    "tax_amount": "Сумма налога: {tax}",
    "cart_total": "Сумма к оплате: {total}",
    "log_add_to_cart": "Добавлен товар в корзину:{product}"
}


def set_free_shipping_icon(is_show: bool) -> None:
    if is_show:
        show_free_shipping_icon(MESSAGES, logger=logger)
    else:
        hide_free_shipping_icon(MESSAGES, logger=logger)


def update_shipping_icons(cart: Cart) -> None:
    for button in cart.values():
        new_cart = add_product(cart=cart, product=button)
        has_free_shipping = is_free_shipping(new_cart)
        set_free_shipping_icon(is_show=has_free_shipping)


def set_tax_dom(price: Price) -> None:
    log_message("tax_amount", MESSAGES, logger=logger, tax=round(price, 2))


def update_tax_dom(total: Decimal) -> None:
    set_tax_dom(calc_tax(total))


def calc_tax(amount: Decimal) -> Decimal:
    return amount * Decimal(0.10)


def set_cart_total_dom(total: Decimal) -> None:
    log_message("cart_total", MESSAGES, logger=logger, total=total)


def cart_tax(cart: Cart) -> Decimal:
    """Вычисляет налог."""
    return calc_tax(calc_total(cart))


def add_element_last(array: list[T], elem: T) -> list[T]:
    # копирование при записи
    new_array = array.copy()  # создать копию
    new_array.append(elem)  # изменить копию
    return new_array  # Вернуть копию


def add_product(cart: Cart, product: Product) -> Cart:
    """Добавляет товар в корзину."""
    return object_set(obj=cart, key=product["name"], value=product)


def make_product(name: Name, price: Price) -> Product:
    """Создает единицу товара."""
    return Product(name=name, price=price)


def set_price(product: Product, price: Price) -> Product:
    product_copy = product.copy()
    product_copy["price"] = price
    return product_copy


def array_set(array: list[T], idx: int, value: Any) -> list[T]:
    array_copy = array.copy()
    array_copy[idx] = value
    return array_copy


def set_price_by_name(cart: Cart, name: Name, price: Price) -> Cart:
    if is_in_cart(cart, name):
        return object_set(obj=cart, key=name, value=set_price(cart[name], price))
    product = make_product(name=name, price=price)
    return object_set(cart, name, product)


def remove_items(array: list[T], idx: int) -> list[T]:
    """Удаление из списка по индексу с копированием при записи."""
    new_array = array.copy()
    new_array.pop(idx)
    return new_array


def calc_total(cart: Cart) -> Decimal:
    return sum(map(lambda x: x["price"], cart.values()))


def is_free_shipping(cart: Cart) -> bool:
    """Проверяет действие бесплатной доставки."""
    return calc_total(cart) >= FREE_SHIPPING_THRESHOLD


def log_add_to_cart(product: Product) -> None:
    log_message("log_add_to_cart", MESSAGES, logger=logger, product=product)


def add_product_to_cart(name: Name, price: Price, shopping_cart: Cart) -> Cart:
    """Добавляет товар в корзину."""
    product=make_product(name=name, price=price)
    new_shopping_cart = add_product(
        cart=shopping_cart, product=product,
    )

    total = calc_total(new_shopping_cart)
    set_cart_total_dom(total)
    update_shipping_icons(new_shopping_cart)
    update_tax_dom(total)
    log_add_to_cart(product)
    return new_shopping_cart


def remove_item_by_name(cart: Cart, name: Name) -> Cart:
    """Удаление товара из корзины по его наименования."""
    if is_in_cart(cart, name):
        return obj_delete(cart, name)
    return cart


def delete_handler(name: Name, shopping_cart: Cart) -> Cart:
    """Удаляет товар из корзины по его наименования."""
    new_shopping_cart = remove_item_by_name(shopping_cart, name)
    total = calc_total(new_shopping_cart)
    set_cart_total_dom(total)
    update_shipping_icons(new_shopping_cart)
    update_tax_dom(total)
    return new_shopping_cart


def is_in_cart(cart: Cart, name: Name) -> bool:
    """Проверяет наличие товара в корзине."""
    return name in cart


def free_tie_clip(cart: Cart) -> Cart:
    """Добавляет зажим для галстука,
    если в корзине есть галстук и нет зажима."""
    has_tie = is_in_cart(cart, "tie")
    has_tie_clip = is_in_cart(cart, "tie clip")
    if has_tie and not has_tie_clip:
        tie_clip = make_product("tie clip", 0)
        return add_product(cart, tie_clip)
    return cart


def object_set(obj: Mapping[K, V], key: K, value: V) -> Mapping[K, V]:
    obj_copy = obj.copy()
    obj_copy[key] = value
    return obj_copy


def obj_delete(obj: Mapping[K, V], key: K) -> Mapping[K, V]:
    obj_copy = obj.copy()
    del obj_copy[key]
    return obj_copy


def is_watch_discount(cart: Cart) -> bool:
    """Проверяет, доступна ли скидка на часы"""
    product_discount_name = Name("watch")
    total_for_discount = 100
    total = calc_total(cart)
    has_watch = is_in_cart(cart, product_discount_name)
    return total > total_for_discount and has_watch
