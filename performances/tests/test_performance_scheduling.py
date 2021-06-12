import datetime
from pprint import pprint

from model_bakery import baker
from django.test import TestCase
from performances.performance_scheduling import (
    get_event,
    get_session,
    sessions_in_a_day,
    get_performances_to_be_performed,
    class_performances_scheduling,
    total_time_taken_by_all_event_performances,
    divide_classes_among_theaters,
    event_day_scheduling,
    schedule_performances_for_each_theater,
    generate_time_table)


class PerformanceSchedulingTests(TestCase):
    def setUp(self) -> None:
        self.localities = baker.make_recipe('performances.tests.locality', 4)
        self.institutions = baker.make_recipe('performances.tests.institution', 5)
        self.all_classes = baker.make_recipe('performances.tests.p_class', 5)
        self.event = baker.make_recipe('performances.tests.event')
        get_event(event=self.event)

        for p_class in self.all_classes:
            a = baker.make_recipe('performances.tests.performance')
            b = baker.make_recipe('performances.tests.performance')
            c = baker.make_recipe('performances.tests.performance')
            d = baker.make_recipe('performances.tests.performance')
            e = baker.make_recipe('performances.tests.performance')

            p_class.performance_set.set([a, b, c, d, e])

        self.performance_class = baker.make('performances.Class', performance_duration=5)
        self.institution = baker.make_recipe('performances.tests.institution')
        self.class_performances = baker.make(
            'performances.Performance',
            performance_class=self.performance_class,
            institution=self.institution,
            _quantity=5
        )

        self.unscheduled_performances = []
        self.session_performances = []

    def test_get_session(self):
        self.a = '0800'
        self.b = '1100'

        self.assertEqual(get_session(a=self.a, b=self.b)[0], 180)
        self.assertEqual(
            get_session(a=self.a, b=self.b)[1],
            datetime.datetime.strptime('0800', "%H%M")
        )

    def test_sessions_in_a_day(self):
        self.assertEqual(
            sessions_in_a_day(),
            ((180, datetime.datetime.strptime('0800', "%H%M")),
             (90, datetime.datetime.strptime('1130', "%H%M")),
             (180, datetime.datetime.strptime('1400', "%H%M")))
        )

    def test_get_performances_to_be_performed(self):
        self.assertEqual(len(list(get_performances_to_be_performed())), 25)

    def test_performances_scheduled_per_session(self):
        self.event_performances = get_performances_to_be_performed()
        self.assertEqual(
            len(class_performances_scheduling(
                class_performances=self.class_performances, session_time=20,
                balance_performances=[],
                scheduled_performances=[],
                event_performances=self.event_performances)[0]),
            4,
            msg="Scheduled performances should be 4"
        )

    def test_class_performances_left_over_after_a_session(self):
        self.event_performances = get_performances_to_be_performed()
        self.assertEqual(
            len(class_performances_scheduling(
                class_performances=self.class_performances, session_time=20,
                balance_performances=[],
                scheduled_performances=[],
                event_performances=self.event_performances)[1]),
            1,
            msg="Unscheduled performances should be 1"
        )

    def test_session_time_balance_after_performances_are_scheduled(self):
        self.event_performances = get_performances_to_be_performed()
        self.assertEqual(
            class_performances_scheduling(
                class_performances=self.class_performances, session_time=180,
                balance_performances=[],
                scheduled_performances=[],
                event_performances=self.event_performances)[2],
            155,
            msg="Session time should be 155"
        )

    def test_non_event_performances_are_discounted(self):
        self.event_performances = get_performances_to_be_performed()
        self.ins = baker.make('performances.Institution')
        self.class_performances = self.class_performances = baker.make(
            'performances.Performance',
            performance_class=self.performance_class,
            institution=self.ins,
            _quantity=5
        )

        self.assertEqual(
            class_performances_scheduling(
                class_performances=self.class_performances, session_time=180,
                balance_performances=[],
                scheduled_performances=[],
                event_performances=self.event_performances)[2],
            180,
            msg="Session time should be 180, unused"
        )

    def test_total_time_taken_by_all_classes(self):
        self.event_performances = get_performances_to_be_performed()
        self.assertEqual(
            total_time_taken_by_all_event_performances(event_performances=self.event_performances),
            150
        )

    def test_divide_classes_among_theaters(self):
        theaters = baker.make_recipe('performances.tests.theater', _quantity=3)

        self.classes_among_theaters = divide_classes_among_theaters(
            total_time_taken=125,
            theaters=theaters,
            classes=self.all_classes)

        self.average_time_to_theater = 25
        for key, value in self.classes_among_theaters.items():
            self.assertLessEqual(len(value), 2, msg='Classes allocated to theater must not be more than 2')

    def test_event_day_scheduling_with_no_left_over_performances(self):
        self.assertEqual(event_day_scheduling(
            left_over_performances=[],
            festival_sessions=list(sessions_in_a_day()),
            class_performances=self.class_performances,
            performances_in_a_day_per_session={})[2],

                         [[155.0, datetime.datetime(1900, 1, 1, 8, 0)],
                          [90.0, datetime.datetime(1900, 1, 1, 11, 30)],
                          [180.0, datetime.datetime(1900, 1, 1, 14, 0)]]
                         )

    def test_event_day_scheduling_with_left_over_performances(self):
        self.performance_class = baker.make('performances.Class', performance_duration=40)
        self.class_performances = baker.make(
            'performances.Performance',
            performance_class=self.performance_class, _quantity=5)
        self.assertEqual(event_day_scheduling(
            left_over_performances=[],
            festival_sessions=list(sessions_in_a_day()),
            class_performances=self.class_performances,
            performances_in_a_day_per_session={})[2],

                         [[20.0, datetime.datetime(1900, 1, 1, 8, 0)],
                          [50.0, datetime.datetime(1900, 1, 1, 11, 30)],
                          [180.0, datetime.datetime(1900, 1, 1, 14, 0)]]
                         )

    def test_schedule_performances_for_each_theater(self):
        pass

    def test_append_performance_start_and_end_time(self):

        pass
