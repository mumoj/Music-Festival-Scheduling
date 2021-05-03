import datetime
from model_bakery import baker
from django.test import TestCase
from performances.performance_scheduling import (
    get_session_duration,
    sessions_in_a_day,
    balance_class_scheduling,
    session_performance_scheduling)


class PerformanceSchedulingTests(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_session_duration(self):
        self.a = '0800'
        self.b = '1100'

        self.assertEqual(get_session_duration(a=self.a, b=self.b), datetime.timedelta(0, 10800))

    def test_sessions_in_a_day(self):
        self.assertEqual(sessions_in_a_day(), (180, 90, 180))

    def test_balance_class_scheduling(self):
        self.remaining_class = baker.make(
            'performances.Class',
            performance_duration=5)
        self.remaining_class_performances = baker.make(
            'performances.Performance',
            performance_class=self.remaining_class,
            _quantity=5)
        self.unscheduled_performances = []
        self.session_performances = []

        self. balance_session = balance_class_scheduling(
            remaining_class_performances=self.remaining_class_performances,
            remaining_session_time=20,
            session_performances=self.session_performances,
            unscheduled_performances=self.unscheduled_performances
        )
        self.assertEqual(len(self.unscheduled_performances), 1)
        self.assertEqual(len(self.session_performances), 4)
        self.assertEqual(self.balance_session, 0)

    def test_performance_scheduling(self):
        self.classes = baker.make_recipe('performances.tests.performance_class', 2)

        for p_class in self.classes:
            performances = baker.make(
                'performances.Performance',
                performance_class=p_class,
                _quantity=5)
            p_class.performance_set.set(performances)

        self. assertEqual(
            len(session_performance_scheduling(ordered_classes=self.classes, session_time=50)[0]),
            10
        )
        self.assertEqual(
            len(session_performance_scheduling(ordered_classes=self.classes, session_time=45)[1]),
            1
        )
        self.assertEqual(
            session_performance_scheduling(ordered_classes=self.classes, session_time=45)[2],
            0
        )




