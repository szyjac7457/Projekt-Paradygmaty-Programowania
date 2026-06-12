from typing import Callable
from src.parsing.parser import Athlete

def by_country(country_code: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.noc == country_code

def by_sex(sex: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.sex == sex

def by_event(event_name: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.event == event_name

def by_team(team_name: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.team == team_name

def by_season(season: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.season == season

def by_sport(sport: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.sport == sport

def by_year_range(start_year: int, end_year: int) -> Callable[[Athlete], bool]:
    return lambda athlete: start_year <= athlete.year <= end_year

def has_medal(athlete: Athlete) -> bool:
    return athlete.medal is not None

def has_specific_medal(medal_type: str) -> Callable[[Athlete], bool]:
    return lambda athlete: athlete.medal == medal_type