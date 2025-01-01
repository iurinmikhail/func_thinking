from unittest import TestCase, mock, main

from src.send_email import (
    SendIssue,
    messages_for_subscribers,
    select_coupon_by_rank,
    REC_COUNT_FOR_BEST,
    SUBJECT_FOR_GOOD,
    SUBJECT_FOR_BEST,
    EMAIL_FROM,
)

from src._types import Message, Email, Subscriber, RecRank, Coupon, CodeCoupon, Rank, Rank


class TestSendIssue(TestCase):
    def set_up(self):
        self.coupons = [
            Coupon(code=CodeCoupon("A1"), rank=Rank.GOOD.value),
            Coupon(code=CodeCoupon("A2"), rank=Rank.BAD.value),
            Coupon(code=CodeCoupon("A3"), rank=Rank.BEST.value),
            Coupon(code=CodeCoupon("A4"), rank=Rank.BEST.value),
        ]
        self.subscriber_best = Subscriber(
            email=Email("best@test.test"),
            rec_rank=RecRank(REC_COUNT_FOR_BEST + 1)
        )
        self.subscriber_good = Subscriber(
            email=Email("good@test.test"),
            rec_rank=RecRank(REC_COUNT_FOR_BEST - 1)
        )
        self.good_coupons =[CodeCoupon("A1")]
        self.best_coupons = [CodeCoupon("A3"), CodeCoupon("A4")]

        self.message_best = Message(
                from_ = EMAIL_FROM,
                to=self.subscriber_best.email,
                subject=SUBJECT_FOR_BEST,
                body=(", ").join(self.best_coupons),
            )
        self.message_good = Message(
                from_ = EMAIL_FROM,
                to=self.subscriber_good.email,
                subject=SUBJECT_FOR_GOOD,
                body=(", ").join(self.good_coupons),
            )

    def test_send_issue(self):
        self.set_up()
        subscribers = [self.subscriber_best]
        fetch_coupons_from_db = mock.Mock(return_value=self.coupons)
        fetch_subscribers_from_db = mock.Mock(return_value=subscribers)
        send_email = mock.Mock()

        send_issue = SendIssue(
            _fetch_coupons_from_db=fetch_coupons_from_db,
            _select_coupon_by_rank=select_coupon_by_rank,
            _fetch_subscribers_from_db=fetch_subscribers_from_db,
            _messages_for_subscribers=messages_for_subscribers,
            _send_email=send_email,
        )
        send_issue()
        fetch_coupons_from_db.assert_called_once()
        fetch_subscribers_from_db.assert_called_once()
        send_email.assert_called_once()

    def test_select_coupon_by_rank__when_rank_good(self):
        self.set_up()
        result = select_coupon_by_rank(self.coupons, Rank.GOOD)
        self.assertEqual(result, self.good_coupons)

    def test_select_coupon_by_rank__when_rank_best(self):
        self.set_up()
        result = select_coupon_by_rank(self.coupons, Rank.BEST)
        self.assertEqual(result, self.best_coupons)

    def test_messages_for_subscribers(self):
        self.set_up()
        subscribers = [self.subscriber_best, self.subscriber_good]
        expected = [self.message_best, self.message_good]
        result = messages_for_subscribers(subscribers, goods=self.good_coupons, bests=self.best_coupons)
        self.assertEqual(expected, list(result))


if __name__ == "__main__":
    main()
