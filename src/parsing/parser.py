from dataclasses import dataclass
from src.core.result import sequence
from src.parsing.validators import (
    parse_name, parse_sex, parse_age, parse_height, parse_weight,
    parse_team, parse_noc, parse_year, parse_season, parse_sport,
    parse_event, parse_medal,
)


@dataclass(frozen=True)
class Athlete:
    name: str
    sex: str
    age: int | None
    height: float | None
    weight: float | None
    team: str | None
    noc: str
    year: int
    season: str
    sport: str
    event: str
    medal: str | None


def parse_athlete(row):
    result = sequence([
        parse_name(row.get('Name', '')),
        parse_sex(row.get('Sex', '')),
        parse_age(row.get('Age', 'NA')),
        parse_height(row.get('Height', 'NA')),
        parse_weight(row.get('Weight', 'NA')),
        parse_team(row.get('Team', 'NA')),
        parse_noc(row.get('NOC', '')),
        parse_year(row.get('Year', '')),
        parse_season(row.get('Season', '')),
        parse_sport(row.get('Sport', '')),
        parse_event(row.get('Event', '')),
        parse_medal(row.get('Medal', 'NA')),
    ])
    return result.map(lambda vals: Athlete(*vals))
