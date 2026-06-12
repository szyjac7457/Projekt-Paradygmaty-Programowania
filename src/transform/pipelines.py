from src.core.functional import pipe
from src.transform.filters import by_country, by_season, has_medal, by_sport

def polish_summer_medalists():
    return pipe(
        lambda athletes: filter(by_country('POL'), athletes),
        lambda athletes: filter(by_season('Summer'), athletes),
        lambda athletes: filter(has_medal, athletes)
    )

def sport_participants(sport_name: str, season: str):
    return pipe(
        lambda athletes: filter(by_sport(sport_name), athletes),
        lambda athletes: filter(by_season(season), athletes)
    )