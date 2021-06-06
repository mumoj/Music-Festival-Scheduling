"""
    Module for generating a festival event's timetable

    Parameters
    ----------
    all_classes: All classes being performed in the festival.
    event: QuerySet
        The festival event for which the timetable is being constructed.
"""

import datetime
from pprint import pprint
from typing import Union, List

from django.db.models import QuerySet

from performances.models import (
    Class,
    Performance,
    Locality,
    Institution,
    Event)

all_classes = Class.objects.all().order_by('performance_duration')
__event__ = None


def get_event(event):
    global __event__
    if __event__ is None:
        __event__ = event


# OPTIMIZE: Possible repetition
def generate_time_table(theaters_assigned_performances_per_day: dict):
    tt: dict = {}
    for theater, days in theaters_assigned_performances_per_day.items():
        all_days_dict: dict = {}
        for day, sessions in days.items():
            all_sessions_dict: dict = {}
            for session, performances in sessions.items():
                performance_periods_dicts: list = append_performance_start_and_end_time(
                    session_start=session, performances=performances)
                all_sessions_dict.update({session: performance_periods_dicts})
            all_days_dict.update({day: all_sessions_dict})
        tt.update({theater: all_days_dict})
        pprint(tt)
    return tt


def append_performance_start_and_end_time(session_start, performances: Union[QuerySet, List[Performance]]):
    start_time = session_start
    performance_periods_dicts: list = []
    for performance in performances:
        end_time = start_time + datetime.timedelta(
            minutes=performance.performance_class.performance_duration)
        performance_dict = {performance: (start_time, end_time)}
        performance_periods_dicts.append(performance_dict)
        start_time = end_time
    return performance_periods_dicts


def schedule_performances_for_each_theater() -> dict:
    """"
    Returns
    -------
        theaters_assigned_performances: dict
             A dict with the distribution of performances among theaters and festival sessions
            For example:
                <Theater: Mandela's Hall>: {1: {datetime.datetime(1900, 1, 1, 8, 0):[
                                                       <Performance: Performance object (48512)>,
                                                       <Performance: Performance object (48511)>,
                                                       <Performance: Performance object (48510)>,
                                                       <Performance: Performance object (48509)>,
                                                       <Performance: Performance object (48518)>,
                                                       <Performance: Performance object (48517)>,
                                                       <Performance: Performance object (48516)>,
                                                       <Performance: Performance object (48515)>,
                                                       <Performance: Performance object (48514)>],
                                 datetime.datetime(1900, 1, 1, 11, 30): [],
                                 datetime.datetime(1900, 1, 1, 14, 0): []}}}

    """

    total_time_taken = total_time_taken_by_all_event_performances(event_performances=get_performances_to_be_performed())
    theaters = __event__.theater_set.all()

    theaters_assigned_performances: dict = divide_classes_among_theaters(
        total_time_taken=total_time_taken,
        classes=all_classes,
        theaters=theaters)

    for theater, value in theaters_assigned_performances.items():
        performance_classes: list = theaters_assigned_performances[theater]
        theaters_assigned_performances[theater] = {}  # Initialize a dict for sessions in an event day.

        day = 1
        left_over_performances: list = []  # To be updated at the end of each day.
        festival_sessions_in_a_day = list(sessions_in_a_day())
        day_performances: dict = {day: {}}
        theaters_assigned_performances[theater].update(day_performances)
        session_performances: dict = {session[1]: [] for session in festival_sessions_in_a_day}

        # Initialize an empty list for each session
        theaters_assigned_performances[theater][day].update(session_performances)
        for i, performance_class in enumerate(performance_classes):
            bar: dict = event_day_scheduling(
                left_over_performances=left_over_performances,
                festival_sessions=festival_sessions_in_a_day,
                performances_in_a_day_per_session={},
                class_performances=list(performance_class.performance_set.all()))

            for session_key, performances in bar[0].items():  # Add performances to each session.
                theaters_assigned_performances[theater][day][session_key] += performances

            if i < len(performance_classes)-1:  # Find the incoming class' performance duration
                next_class_duration: int = performance_classes[i + 1].performance_duration
            else:
                next_class_duration: int = performance_classes[i].performance_duration

            for session in bar[2]:  # Iterate over balance  sessions' time
                if session[0] >= next_class_duration:
                    festival_sessions_in_a_day = bar[2]  # Use whatever balance session time  remains to depletion.
                    break
            else:  # Start a new event day if the next class' performance duration does not fit into any session time.
                festival_sessions_in_a_day = list(sessions_in_a_day())
                day += 1
                day_performances: dict = {day: {}}
                theaters_assigned_performances[theater].update(day_performances)
                session_performances: dict = {session[1]: [] for session in festival_sessions_in_a_day}
                theaters_assigned_performances[theater][day].update(session_performances)

            left_over_performances = bar[1]
    return theaters_assigned_performances


def event_day_scheduling(
        left_over_performances: list,
        festival_sessions: list,
        performances_in_a_day_per_session: dict,
        class_performances: list):
    """
    Schedule performances into the set event day session,
    carrying over left over class performances into the next session,
    and sometimes day.

    Parameters
    ----------
    class_performances: list
        All the performances belonging to a particular class.
    left_over_performances: list
        Whatever class performances don't fit into a session.
    festival_sessions: list
        The defined sessions ina festival day.
    performances_in_a_day_per_session: dict
        Where performances are allocated into the various sessions in  single day.

    Returns
    -------
    performances_in_a_day_per_session: dict

    """
    festival_sessions = [list(session_tuple) for session_tuple in festival_sessions]
    for i, session in enumerate(festival_sessions):
        session_dict = {session[1]: []}  # Initialize a  dict for a session's performances.
        performances_in_a_day_per_session.update(session_dict)

        time_taken_by_left_over_performances = 0
        for performance in left_over_performances:  # Find the total time taken by left over performances.
            time_taken_by_left_over_performances += performance.performance_class.performance_duration

        if time_taken_by_left_over_performances < session[0]:
            performances_in_a_day_per_session[session[1]] = left_over_performances
            session[0] -= time_taken_by_left_over_performances

            foo: tuple = class_performances_scheduling(
                class_performances=class_performances,
                session_time=session[0],
                scheduled_performances=[],
                balance_performances=[],
                event_performances=get_performances_to_be_performed()
            )  # Schedule the passed class to the remaining session time.

            if foo[0]:  # If performances are scheduled to the session.
                scheduled_performances = foo[0]
                performances_in_a_day_per_session[session[1]] = \
                    performances_in_a_day_per_session[session[1]] + scheduled_performances
                festival_sessions[i][0] = foo[2]  # Update the session time.
                class_performances = foo[1]  # Update class_performances for next session.

        elif time_taken_by_left_over_performances > session[0]:
            # If leftover performances do not fit into session time, schedule the passed class directly .
            foo: tuple = class_performances_scheduling(
                class_performances=left_over_performances,
                session_time=session[0],
                scheduled_performances=[],
                balance_performances=left_over_performances,
                event_performances=get_performances_to_be_performed())

            scheduled_performances = foo[0]
            performances_in_a_day_per_session[session[1]] = \
                performances_in_a_day_per_session[session[1]] + scheduled_performances
            balance_performances = foo[1]
            left_over_performances = balance_performances
            festival_sessions[i][0] = 0  # Record depletion of session time.

            continue
        else:
            if time_taken_by_left_over_performances == session[0]:
                performances_in_a_day_per_session[session[1]] = left_over_performances
                festival_sessions[i][0] = 0  # Record depletion of session time.

                continue

    if class_performances:  # Set whatever performances remain to be scheduled the next day.
        left_over_performances += class_performances
    return performances_in_a_day_per_session, left_over_performances, festival_sessions


def divide_classes_among_theaters(
        total_time_taken: int,
        theaters: Union[QuerySet, List[Class]],
        classes: Union[QuerySet, List[Class]]) -> dict:
    """
    Divide the class es among available theaters.

    Parameters
    ----------
    total_time_taken: int
        Total time taken by the all performances in an event.
    theaters: QuerySet
        All the theaters available in an event.
    classes:
        All the classes allowed in an event.

    Returns
    -------
    performance_classes_per_theater: dict
        A dict containing dicts of all the theaters with their allocated theaters.
    """

    no_of_theaters: int = len(theaters)
    if no_of_theaters > 0:
        average_time_per_theater: float = total_time_taken / no_of_theaters
    else:
        raise ZeroDivisionError

    performance_classes_per_theater: dict = {}
    remaining_classes: list = list(classes)

    for theater in theaters:
        time_to_theater: int = 0  # Time allocated to theater.
        performance_classes_per_theater.update({theater: []})

        remaining_classes[:] = [c for c in remaining_classes if c is not None]
        for i, performance_class in enumerate(remaining_classes):

            no_of_performances: int = performance_class.performance_set.count()
            if no_of_performances == 0:  # Exclude classes with no registered performances.
                remaining_classes[i] = None  # Remove class
                continue

            # Consider only the current event's performances for a class.
            no_of_performances: int = 0
            for performance in get_performances_to_be_performed():
                if performance in performance_class.performance_set.all():
                    no_of_performances += 1
                else:
                    continue
            time_taken = performance_class.performance_duration * no_of_performances

            if time_to_theater < average_time_per_theater:
                time_to_theater += time_taken
                performance_classes_per_theater[theater].append(performance_class)
                remaining_classes[i] = None  # Remove a class once it is allocated to a theater.
            else:
                if time_to_theater >= average_time_per_theater:
                    break
    return performance_classes_per_theater


def total_time_taken_by_all_event_performances(event_performances: Union[QuerySet, List[Class]]) -> int:
    """
    Calculate time to be taken by all performances in all the classes in a festival event.

    Parameters
    ----------
    event_performances: All the performances in a festival event.

    Returns
    -------
    total_time: Total time allocated to all the performances.
    """

    total_time: int = 0
    for performance in event_performances:
        time_taken: int = performance.performance_class.performance_duration
        total_time += time_taken
    return total_time


def class_performances_scheduling(
        class_performances: list,
        session_time: int,
        balance_performances: list,
        scheduled_performances: list,
        event_performances: Union[QuerySet, List[Event]]):
    """

    Parameters
    ----------
    event_performances:
        All the performances in an event.
    balance_performances: list
        Performances that did not fit into a session.
    scheduled_performances: list
        Performances already scheduled for a session.
    class_performances: list
        Performances to be scheduled.
    session_time: int
        Session time available in minutes.

    Returns
    -------
    """

    for performance in class_performances:
        if performance in event_performances:  # Exclude performances not belonging to the event
            if performance.performance_class.performance_duration <= session_time:
                scheduled_performances.append(performance)
                session_time -= performance.performance_class.performance_duration
            else:
                if performance.performance_class.performance_duration > session_time:
                    balance_performances.append(performance)
        else:
            continue

    return scheduled_performances, balance_performances, session_time


def get_performances_to_be_performed():
    """
        Performances belonging to the event locality and level.
    """
    global __event__
    all_localities = Locality.objects.all().values_list('pk', __event__.event_level.lower())
    venue_locality = [locality for locality in all_localities if locality[0] == __event__.venue.locality.pk][0]

    # Filter event_locality by the venue's zone, sub-county, county or region
    event_localities_pks = [locality[0] for locality in all_localities if locality[1] == venue_locality[1]]
    event_localities = [Locality.objects.get(pk=event_locality_pk) for event_locality_pk in event_localities_pks]

    event_institutions = Institution.objects.filter(locality__in=event_localities)
    event_performances = Performance.objects.filter(institution__in=event_institutions)

    return event_performances


def sessions_in_a_day() -> tuple:
    """
    Define the sessions allowed in a festival event day.

    Returns
    -------
    tuple
        A tuple containing time taken in a session and
        the session start time object.
    """

    first_session_start: str = '0800'
    first_session_end: str = '1100'
    second_session_start: str = '1130'
    second_session_end: str = '1300'
    third_session_start: str = '1400'
    third_session_end: str = '1700'

    first_session = (
        get_session(a=first_session_start, b=first_session_end))
    second_session = (
        get_session(a=second_session_start, b=second_session_end))
    third_session = (
        get_session(a=third_session_start, b=third_session_end))

    return first_session, second_session, third_session


def get_session(a: str, b: str):
    """
    Find the time taken to complete each session.

    Parameters
    ----------
    a : str
        Start time.
    b : str
        Stop time.

    Returns
    -------
    timedelta :  object
        Diff between stop time and start time.
    start time object
    """
    timedelta = datetime.datetime.strptime(b, "%H%M") - datetime.datetime.strptime(a, "%H%M")
    timedelta = timedelta.seconds / 60  # Convert to minutes
    return timedelta, datetime.datetime.strptime(a, "%H%M")
