from typing import final, Callable, Iterator
from dataclasses import dataclass
from src._types import Message, Subscriber, Email, Coupon, Rank, CodeCoupon


REC_COUNT_FOR_BEST = 10
SUBJECT_FOR_BEST = "123"
SUBJECT_FOR_GOOD = "123"
EMAIL_FROM = Email("from@test.test")


def sub_coupon_rank(subscriber: Subscriber) -> Rank:
    if subscriber.rec_rank >= REC_COUNT_FOR_BEST:
        return Rank.BEST
    return Rank.GOOD


def message_for_subscriber(subscriber: Subscriber, goods: list[CodeCoupon], bests: list[CodeCoupon]) -> Message:
    rank_bool = sub_coupon_rank(subscriber) == Rank.BEST
    return Message(
            from_=EMAIL_FROM,
            to=subscriber.email,
            subject=(SUBJECT_FOR_GOOD, SUBJECT_FOR_BEST)[rank_bool],
            body=(", ").join((goods, bests)[rank_bool]),
        )


def messages_for_subscribers(
        subscribers: list[Subscriber],
        goods: list[CodeCoupon],
        bests: list[CodeCoupon],
        ) -> Iterator[Message]:
    for subscriber in subscribers:
        yield message_for_subscriber(subscriber, goods=goods, bests=bests)


def select_coupon_by_rank(coupons: list[Coupon], rank: Rank) -> list[CodeCoupon]:
    return [coupon.code for coupon in coupons if coupon.rank == rank]


@final
@dataclass(slots=True, frozen=True, kw_only=True)
class SendIssue:
    _fetch_coupons_from_db: Callable[[None], list[Coupon]]
    _select_coupon_by_rank: Callable[[list[Coupon]], list[CodeCoupon]]
    _fetch_subscribers_from_db: Callable[[None], list[Subscriber]]
    _messages_for_subscribers: Callable[[None], Iterator[Message]]
    _send_email: Callable[[Message], None]
    def __call__(self) -> None:
        coupons = self._fetch_coupons_from_db()
        good_coupons: list[CodeCoupon] = self._select_coupon_by_rank(coupons, Rank.GOOD)
        best_coupons: list[CodeCoupon] = self._select_coupon_by_rank(coupons, Rank.BEST)
        subscribers = self._fetch_subscribers_from_db()
        for email in self._messages_for_subscribers(subscribers, good_coupons, best_coupons):
            self._send_email(email)
