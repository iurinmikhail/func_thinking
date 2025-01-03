from typing import TypedDict, TypeAlias, final, NamedTuple, TypeVar
from enum import Enum
from decimal import Decimal
from src.utils import log_message

Name: TypeAlias = str
Price: TypeAlias = Decimal


class Rank(str, Enum):
    GOOD = "good"
    BEST = "best"
    BAD = "bad"


Email: TypeAlias = str
RecRank: TypeAlias = int
CodeCoupon: TypeAlias = str


@final
class Subscriber(NamedTuple):
    email: Email
    rec_rank: RecRank


@final
class Coupon(NamedTuple):
    code: CodeCoupon
    rank: Rank


@final
class Message(NamedTuple):
    from_: Email
    to: Email
    subject: str
    body: str


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class Product(TypedDict):
    name: Name
    price: Price


Cart: TypeAlias = list[Product]
