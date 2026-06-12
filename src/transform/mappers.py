from src.parsing.parser import Athlete

def get_demographics(athlete: Athlete) -> dict:
    return {
        'age': athlete.age,
        'height': athlete.height,
        'weight': athlete.weight
    }

def calculate_bmi(athlete: Athlete) -> float | None:
    if athlete.weight is not None and athlete.height is not None:
        height_m = athlete.height / 100
        return round(athlete.weight / (height_m ** 2), 2)
    return None

def extract_medal_info(athlete: Athlete) -> tuple:
    return (athlete.noc, athlete.medal)

def get_decade(year: int) -> int:
    return (year // 10) * 10

def map_to_decade(athlete: Athlete) -> dict:
    return {
        'sex': athlete.sex,
        'decade': get_decade(athlete.year)
    }

def extract_career_info(athlete: Athlete) -> tuple:
    return (athlete.name, athlete.year, athlete.medal)

def extract_event_info(athlete: Athlete) -> tuple:
    return (athlete.year, athlete.season, athlete.event, athlete.name)

def extract_demographics_evolution(athlete: Athlete) -> tuple:
    return (athlete.sport, athlete.year, athlete.age, athlete.height, athlete.weight)

def extract_trend_info(athlete: Athlete) -> tuple:
    return (athlete.year, athlete.season, athlete.noc, athlete.sport, athlete.name, athlete.sex)

def extract_dominance_info(athlete: Athlete) -> tuple:
    return (athlete.noc, athlete.sport, athlete.year, athlete.medal)