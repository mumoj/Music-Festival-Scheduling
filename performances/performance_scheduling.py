import datetime
import asyncio
from typing import Union, List

from django.db.models import QuerySet
from django.db.models.query import EmptyQuerySet

from performances.models import Class, Event


def schedule_performances_for_each_theatre() -> dict:
    all_classes = Class.objects.all().order_by('performance_duration')
    total_time_taken = total_time_taken_by_all_classes(classes=all_classes)
    theaters = Event.theater_set.all()

    festival_sessions: tuple = sessions_in_a_day()
    theaters_assigned_performances = divide_classes_among_theaters(
        total_time_taken=total_time_taken,
        classes=all_classes,
        theaters=theaters)

    for key, value in theaters_assigned_performances.items():
        performance_classes: list = theaters_assigned_performances[key]
        theaters_assigned_performances[key] = {}  # Initialize a dict for sessions
        theaters_assigned_performances_per_session: dict = theaters_assigned_performances

        for session in festival_sessions:
            session_dict = {session[1]: []}  # Initialize a  dict for a session performances.
            theaters_assigned_performances[key].update(session_dict)

            performances_scheduled: tuple = session_performance_scheduling(
                ordered_classes=performance_classes,
                session_time=session[0])

            if performances_scheduled[0]:
                theaters_assigned_performances[key][session[1]] = performances_scheduled[0]
            else:
                performances_scheduled = session_performance_scheduling(
                    ordered_classes=performance_classes,
                    session_time=session[0])
        return theaters_assigned_performances_per_session


def divide_classes_among_theaters(
        total_time_taken: int,
        theaters: Union[QuerySet, List[Class]],
        classes: Union[QuerySet, List[Class]]) -> dict:
    """
    Divide the classes among available theaters.
    """
    no_of_theaters: int = len(theaters)
    average_time_per_theater: float = total_time_taken / no_of_theaters
    performance_classes_per_theater: dict = {}
    remaining_classes: list = list(classes)

    for theater in theaters:
        time_to_theater = 0
        performance_classes_per_theater.update({theater: []})

        for performance_class in remaining_classes:
            time_taken = performance_class.performance_duration * \
                         performance_class.performance_set.count()

            if time_to_theater < average_time_per_theater:
                time_to_theater += time_taken
                performance_classes_per_theater[theater].append(performance_class)
                remaining_classes.pop(0)  # Remove a class once it is allocated to a theater.
            else:
                break
    return performance_classes_per_theater


def total_time_taken_by_all_classes(classes) -> int:
    """
    Calculate time to be taken by all performances in all classes.
    """
    total_time: int = 0
    for performance_class in classes:
        time_taken = performance_class.performance_duration * \
                     performance_class.performance_set.count()
        total_time += time_taken

    return total_time


def session_performance_scheduling(ordered_classes: Union[QuerySet, List[Class]], session_time: int):
    """
    Schedule class performances into the defined sessions in  a festival event day,
    giving priority to classes with the least performance_duration
    """

    unscheduled_performances = []
    session_performances = []

    if ordered_classes:
        for performance_class in ordered_classes:

            if performance_class.performance_duration < session_time:
                class_performances = performance_class.performance_set.all()
                session_performances.extend(class_performances)

                time_taken = len(class_performances) * performance_class.performance_duration
                if session_time - time_taken >= 0:
                    session_time -= time_taken
                    continue
                else:

                    session_time = balance_class_scheduling(
                        remaining_class_performances=class_performances,
                        remaining_session_time=session_time,
                        session_performances=session_performances,
                        unscheduled_performances=unscheduled_performances)

        return tuple(session_performances), unscheduled_performances, session_time
    else:
        return EmptyQuerySet


def balance_class_scheduling(
        remaining_class_performances: Union[QuerySet, List[Class]],
        remaining_session_time: int,
        session_performances: list,
        unscheduled_performances: list):
    """
    Schedule the performances of whichever class doesn't fit into a session individually,
    and placing the leftover performances of that class into the unscheduled_performances list
    to be scheduled into the next session.
    """

    for performance in remaining_class_performances:

        if performance.performance_class.performance_duration <= remaining_session_time:
            session_performances.append(performance)
            remaining_session_time -= performance.performance_class.performance_duration
        else:
            unscheduled_performances.append(performance)
    return remaining_session_time


def sessions_in_a_day() -> tuple:
    """
    Define the sessions allowed in a festival event day.
    """
    first_session_start: str = '0800'
    first_session_end: str = '1100'
    second_session_start: str = '1130'
    second_session_end: str = '1300'
    third_session_start: str = '1400'
    third_session_end: str = '1700'

    first_session = get_session_duration(a=first_session_start, b=first_session_end)
    second_session = get_session_duration(a=second_session_start, b=second_session_end)
    third_session = get_session_duration(a=third_session_start, b=third_session_end)

    return (
        (first_session.total_seconds() / 60, first_session_start),
        (second_session.total_seconds() / 60, second_session_start),
        (third_session.total_seconds() / 60, second_session_start)
    )


def get_session_duration(a: str, b: str):
    """Find the time taken to complete each session"""
    return datetime.datetime.strptime(b, "%H%M") - datetime.datetime.strptime(a, "%H%M")
