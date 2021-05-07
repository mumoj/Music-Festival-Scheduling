import datetime
import asyncio
from typing import Union, List

from django.db.models import QuerySet
from django.db.models.query import EmptyQuerySet

from performances.models import Class


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


