from functools import reduce
from typing import Iterable
from itertools import chain, repeat
from src.parsing.parser import Athlete
from src.transform.mappers import map_to_decade, extract_dominance_info

#Zliczanie wszystkich medali
def _medal_counter_accumulator(current_total: int, athlete: Athlete) -> int:
    if athlete.medal is not None:
        return current_total + 1
    return current_total

def count_total_medals(athletes: Iterable[Athlete]) -> int:
    return reduce(_medal_counter_accumulator, athletes, 0)

#Klasyfikacja medalowa krajów
def _medals_by_country_accumulator(current_state: dict[str, int], athlete: Athlete) -> dict[str, int]:
    if athlete.medal is not None:
        obecna_liczba = current_state.get(athlete.noc, 0)
        return {**current_state, athlete.noc: obecna_liczba + 1}
    return current_state

def count_medals_by_country(athletes: Iterable[Athlete]) -> dict[str, int]:
    return reduce(_medals_by_country_accumulator, athletes, {})

#Statystyki demograficzne
def _demographics_accumulator(state: dict[str, float], athlete: Athlete) -> dict[str, float]:
    if athlete.age is not None and athlete.height is not None:
        return {
            "count": state["count"] + 1,
            "age_sum": state["age_sum"] + athlete.age,
            "height_sum": state["height_sum"] + athlete.height
        }
    return state

def calculate_average_demographics(athletes: Iterable[Athlete]) -> dict[str, float]:
    initial_state = {"count": 0, "age_sum": 0.0, "height_sum": 0.0}
    final_state = reduce(_demographics_accumulator, athletes, initial_state)
    
    count = final_state["count"]
    if count == 0:
        return {"avg_age": 0.0, "avg_height": 0.0}
        
    return {
        "avg_age": round(final_state["age_sum"] / count, 1),
        "avg_height": round(final_state["height_sum"] / count, 1)
    }

#Medale według płci
def _medals_by_sex_accumulator(state: dict[str, int], athlete: Athlete) -> dict[str, int]:
    if athlete.medal is not None and athlete.sex:
        obecna_liczba = state.get(athlete.sex, 0)
        return {**state, athlete.sex: obecna_liczba + 1}
    return state

def count_medals_by_sex(athletes: Iterable[Athlete]) -> dict[str, int]:
    return reduce(_medals_by_sex_accumulator, athletes, {})

#Medale według lat
def _medals_by_year_accumulator(state: dict[int, int], athlete: Athlete) -> dict[int, int]:
    if athlete.medal is not None and athlete.year:
        obecna_liczba = state.get(athlete.year, 0)
        return {**state, athlete.year: obecna_liczba + 1}
    return state

def count_medals_by_year(athletes: Iterable[Athlete]) -> dict[int, int]:
    return reduce(_medals_by_year_accumulator, athletes, {})

#Analiza wieku
def _age_stats_accumulator(state: dict, athlete: Athlete) -> dict:
    if athlete.age is not None:
        freq = state["freq"]
        new_freq = {**freq, athlete.age: freq.get(athlete.age, 0) + 1}
        
        new_min = athlete.age if state["min"] is None else min(state["min"], athlete.age)
        new_max = athlete.age if state["max"] is None else max(state["max"], athlete.age)
        
        return {
            "freq": new_freq,
            "sum": state["sum"] + athlete.age,
            "count": state["count"] + 1,
            "min": new_min,
            "max": new_max
        }
    return state

def calculate_age_statistics(athletes: Iterable[Athlete]) -> dict:
    initial_state = {"freq": {}, "sum": 0, "count": 0, "min": None, "max": None}
    final_state = reduce(_age_stats_accumulator, athletes, initial_state)
    
    count = final_state["count"]
    if count == 0:
        return {"mean": 0.0, "median": 0.0, "min": 0, "max": 0}
        
    mean = round(final_state["sum"] / count, 2)
    
    
    sorted_freq = sorted(final_state["freq"].items(), key=lambda x: x[0])
    expanded_ages = list(chain.from_iterable(map(lambda item: repeat(item[0], item[1]), sorted_freq)))
    
    mid = count // 2
    median = expanded_ages[mid] if count % 2 != 0 else (expanded_ages[mid - 1] + expanded_ages[mid]) / 2.0
    
    return {
        "mean": mean,
        "median": median,
        "min": final_state["min"],
        "max": final_state["max"]
    }


#Medale
def _medals_by_sport_accumulator(state: dict[str, int], athlete: Athlete) -> dict[str, int]:
    if athlete.medal is not None and athlete.sport:
        current_count = state.get(athlete.sport, 0)
        return {**state, athlete.sport: current_count + 1}
    return state

def count_medals_by_sport(athletes: Iterable[Athlete]) -> dict[str, int]:
    return reduce(_medals_by_sport_accumulator, athletes, {})

#Udział kobiet w dekadach
def _participation_by_decade_accumulator(state: dict[int, dict[str, int]], athlete: Athlete) -> dict[int, dict[str, int]]:
    info = map_to_decade(athlete)
    decade = info["decade"]
    current = state.get(decade, {"total": 0, "female": 0})
    updated = {
        "total": current["total"] + 1,
        "female": current["female"] + (1 if info["sex"] == "F" else 0),
    }
    return {**state, decade: updated}

def count_participation_by_decade(athletes: Iterable[Athlete]) -> dict[int, dict[str, int]]:
    return reduce(_participation_by_decade_accumulator, athletes, {})

#Dominacja krajów w dyscyplinach
def _dominance_accumulator(state: dict[str, dict[str, int]], athlete: Athlete) -> dict[str, dict[str, int]]:
    noc, sport, year, medal = extract_dominance_info(athlete)
    if medal is None:
        return state
    sport_counts = state.get(sport, {})
    updated = {**sport_counts, noc: sport_counts.get(noc, 0) + 1}
    return {**state, sport: updated}

def count_medals_by_sport_and_country(athletes: Iterable[Athlete]) -> dict[str, dict[str, int]]:
    return reduce(_dominance_accumulator, athletes, {})