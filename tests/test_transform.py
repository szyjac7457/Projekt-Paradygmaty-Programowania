import pytest
from src.parsing.parser import Athlete
from src.transform.filters import (
    by_country, by_season, by_sport, by_year_range, 
    has_medal, has_specific_medal, by_sex
)
from src.transform.mappers import (
    get_demographics, calculate_bmi, extract_medal_info,
    get_decade, map_to_decade, extract_career_info, 
    extract_dominance_info, extract_event_info,
    extract_demographics_evolution, extract_trend_info
)
from src.transform.pipelines import polish_summer_medalists, sport_participants

@pytest.fixture
def athlete_lewandowski():
    return Athlete(
        name="Robert Lewandowski", sex="M", age=32,
        height=185.0, weight=81.0, team="Poland",
        noc="POL", year=2020, season="Summer",
        sport="Football", event="Men's Football",
        medal=None
    )

@pytest.fixture
def athlete_stoch():
    return Athlete(
        name="Kamil Stoch", sex="M", age=26,
        height=173.0, weight=55.0, team="Poland",
        noc="POL", year=2014, season="Winter",
        sport="Ski Jumping", event="Men's Large Hill, Individual",
        medal="Gold"
    )

@pytest.fixture
def athlete_phelps():
    return Athlete(
        name="Michael Phelps", sex="M", age=23,
        height=193.0, weight=91.0, team="United States",
        noc="USA", year=2008, season="Summer",
        sport="Swimming", event="Men's 200m Butterfly",
        medal="Gold"
    )

@pytest.fixture
def athlete_kowalczyk():
    return Athlete(
        name="Justyna Kowalczyk", sex="F", age=27,
        height=173.0, weight=59.0, team="Poland",
        noc="POL", year=2010, season="Winter",
        sport="Cross Country Skiing", event="Women's 30 kilometres Classical",
        medal="Gold"
    )

@pytest.fixture
def athletes_list(athlete_lewandowski, athlete_stoch, athlete_phelps, athlete_kowalczyk):
    return [athlete_lewandowski, athlete_stoch, athlete_phelps, athlete_kowalczyk]

class TestFilters:
    def test_by_country(self, athletes_list):
        is_pol = by_country("POL")
        polish_athletes = list(filter(is_pol, athletes_list))
        assert len(polish_athletes) == 3
        assert "Michael Phelps" not in [a.name for a in polish_athletes]

    def test_by_season(self, athletes_list):
        is_winter = by_season("Winter")
        winter_athletes = list(filter(is_winter, athletes_list))
        assert len(winter_athletes) == 2 

    def test_has_medal(self, athletes_list):
        medalists = list(filter(has_medal, athletes_list))
        assert len(medalists) == 3 
        assert "Robert Lewandowski" not in [a.name for a in medalists]

    def test_by_year_range(self, athletes_list):
        in_range = by_year_range(2010, 2020)
        filtered = list(filter(in_range, athletes_list))
        assert len(filtered) == 3 
        
    def test_by_sex(self, athletes_list):
        is_female = by_sex("F")
        female_athletes = list(filter(is_female, athletes_list))
        assert len(female_athletes) == 1
        assert female_athletes[0].name == "Justyna Kowalczyk"

class TestMappers:
    def test_calculate_bmi_valid(self, athlete_stoch):
        bmi = calculate_bmi(athlete_stoch)
        assert bmi == 18.38

    def test_calculate_bmi_missing_data(self):
        athlete_no_weight = Athlete(
            name="Unknown", sex="M", age=20, height=180.0, weight=None,
            team="Test", noc="TST", year=2000, season="Summer",
            sport="Tennis", event="Men's Singles", medal=None
        )
        assert calculate_bmi(athlete_no_weight) is None

    def test_extract_medal_info(self, athlete_phelps):
        info = extract_medal_info(athlete_phelps)
        assert info == ("USA", "Gold")

    def test_get_decade(self):
        assert get_decade(1996) == 1990

    def test_map_to_decade(self, athlete_stoch):
        mapped = map_to_decade(athlete_stoch)
        assert mapped == {'sex': 'M', 'decade': 2010}

    def test_extract_career_info(self, athlete_kowalczyk):
        info = extract_career_info(athlete_kowalczyk)
        assert info == ("Justyna Kowalczyk", 2010, "Gold")

    def test_extract_event_info(self, athlete_lewandowski):
        info = extract_event_info(athlete_lewandowski)
        assert info == (2020, "Summer", "Men's Football", "Robert Lewandowski")

    def test_extract_demographics_evolution(self, athlete_stoch):
        info = extract_demographics_evolution(athlete_stoch)
        assert info == ("Ski Jumping", 2014, 26, 173.0, 55.0)

    def test_extract_trend_info(self, athlete_phelps):
        info = extract_trend_info(athlete_phelps)
        assert info == (2008, "Summer", "USA", "Swimming", "Michael Phelps", "M")

    def test_extract_dominance_info(self, athlete_phelps):
        info = extract_dominance_info(athlete_phelps)
        assert info == ("USA", "Swimming", 2008, "Gold")

class TestPipelines:
    def test_polish_summer_medalists_pipeline(self, athletes_list):
        pipeline_func = polish_summer_medalists()
        result = list(pipeline_func(athletes_list))
        assert len(result) == 0

        korzeniowski = Athlete(
            name="Robert Korzeniowski", sex="M", age=32,
            height=168.0, weight=60.0, team="Poland",
            noc="POL", year=2000, season="Summer",
            sport="Athletics", event="Men's 50km Walk",
            medal="Gold"
        )
        
        result_with_korzeniowski = list(pipeline_func([*athletes_list, korzeniowski]))
        assert len(result_with_korzeniowski) == 1
        assert result_with_korzeniowski[0].name == "Robert Korzeniowski"

    def test_sport_participants_pipeline(self, athletes_list):
        pipeline_func = sport_participants("Swimming", "Summer")
        result = list(pipeline_func(athletes_list))
        assert len(result) == 1
        assert result[0].name == "Michael Phelps"