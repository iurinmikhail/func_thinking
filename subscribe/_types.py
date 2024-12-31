from typing import TypedDict, TypeAlias, final, NamedTuple
from enum import Enum


class Rank(str, Enum):
    GOOD="good"
    BEST="best"
    BAD="bad"


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
