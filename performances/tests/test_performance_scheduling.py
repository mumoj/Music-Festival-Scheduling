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
        self.all_classes = baker.make_recipe('performances.tests.performance_class', 5)
        self.event = baker.make_recipe('performances.tests.event')
        get_event(event=self.event)

        for p_class in self.all_classes:
            performances = baker.make(
                'performances.Performance',
                performance_class=p_class,
                _quantity=5)
            p_class.performance_set.set(performances)

        self.performance_class = baker.make('performances.Class', performance_duration=5)
        self.class_performances = baker.make(
            'performances.Performance',
            performance_class=self.performance_class, _quantity=5)

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
        self.assertEqual(sessions_in_a_day(),
                         ((180, datetime.datetime.strptime('0800', "%H%M")),
                          (90, datetime.datetime.strptime('1130', "%H%M")),
                          (180, datetime.datetime.strptime('1400', "%H%M"))
                          ))

    def test_get_performances_to_be_performed(self):
        self.localities = baker.make_recipe('performances.tests.locality', 4)
        self.institutions = baker.make_recipe('performances.tests.institution', 6)
        pprint(get_performances_to_be_performed())

    def test_performances_scheduled_per_session(self):
        self.assertEqual(
            len(class_performances_scheduling(
                class_performances=self.class_performances, session_time=20,
                balance_performances=[],
                scheduled_performances=[])[0]),
            4,
            msg="Scheduled performances should be 4")

    def test_class_performances_left_over_after_a_session(self):
        self.assertEqual(
            len(class_performances_scheduling(
                class_performances=self.class_performances, session_time=20,
                balance_performances=[],
                scheduled_performances=[])[1]),
            1,
            msg="Unscheduled performances should be 1")

    def test_session_time_balance_after_performances_are_scheduled(self):
        self.assertEqual(
            class_performances_scheduling(
                class_performances=self.class_performances, session_time=180,
                balance_performances=[],
                scheduled_performances=[])[2],
            155,
            msg="Session time should be 155")

    def test_total_time_taken_by_all_classes(self):
        self.assertEqual(
            total_time_taken_by_all_event_performances(classes=self.all_classes),
            125)

    def test_divide_classes_among_theaters(self):
        theaters = baker.make_recipe('performances.tests.theater', _quantity=3)
        self.total_classes = baker.make_recipe('performances.tests.performance_class', 5)

        for p_class in self.total_classes:
            performances = baker.make(
                'performances.Performance',
                performance_class=p_class,
                _quantity=5)
            p_class.performance_set.set(performances)

        self.classes_among_theaters = divide_classes_among_theaters(
            total_time_taken=125,
            theaters=theaters,
            classes=self.total_classes)

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
        self.event = baker.make_recipe('performances.tests.event')
        if self.event:
            self.theaters = baker.make_recipe(
                'performances.tests.theater', _quantity=3, venue=self.event)

        self.total_classes = baker.make_recipe('performances.tests.performance_class', 3)
        for p_class in self.total_classes:
            performances = baker.make(
                'performances.Performance',
                performance_class=p_class,
                _quantity=5)
            p_class.performance_set.set(performances)

        self.assertEqual(len(schedule_performances_for_each_theater(
            event=self.event,
            all_classes=self.total_classes)[self.event.theater_set.get(name='Chapel')]
                             [1][datetime.datetime(1900, 1, 1, 8, 0)]),
                         5)

        self.theaters = schedule_performances_for_each_theater(
            event=self.event,
            all_classes=self.total_classes)
        pprint(generate_time_table(theaters_assigned_performances_per_day=self.theaters))

    def test_append_performance_start_and_end_time(self):

        pass
