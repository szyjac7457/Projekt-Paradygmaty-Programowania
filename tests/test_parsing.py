import pytest
from src.core.result import Ok, Err
from src.parsing.validators import (
    parse_name, parse_sex, parse_age, parse_height, parse_weight,
    parse_team, parse_noc, parse_year, parse_season, parse_sport,
    parse_event, parse_medal,
)
from src.parsing.parser import Athlete, parse_athlete


class TestParseName:
    def test_valid(self):
        assert parse_name("Michael Phelps") == Ok("Michael Phelps")

    def test_na(self):
        assert parse_name("NA").is_err()

    def test_empty(self):
        assert parse_name("").is_err()


class TestParseSex:
    def test_male(self):
        assert parse_sex("M") == Ok("M")

    def test_female(self):
        assert parse_sex("F") == Ok("F")

    def test_invalid(self):
        assert parse_sex("X").is_err()

    def test_empty(self):
        assert parse_sex("").is_err()


class TestParseAge:
    def test_valid(self):
        assert parse_age("25") == Ok(25)

    def test_na(self):
        assert parse_age("NA") == Ok(None)

    def test_invalid_string(self):
        assert parse_age("abc").is_err()

    def test_negative(self):
        assert parse_age("-1").is_err()

    def test_too_large(self):
        assert parse_age("200").is_err()


class TestParseHeight:
    def test_valid_int(self):
        assert parse_height("180") == Ok(180.0)

    def test_valid_float(self):
        assert parse_height("175.5") == Ok(175.5)

    def test_na(self):
        assert parse_height("NA") == Ok(None)

    def test_invalid(self):
        assert parse_height("tall").is_err()


class TestParseWeight:
    def test_valid(self):
        assert parse_weight("80") == Ok(80.0)

    def test_na(self):
        assert parse_weight("NA") == Ok(None)

    def test_invalid(self):
        assert parse_weight("heavy").is_err()


class TestParseTeam:
    def test_valid(self):
        assert parse_team("Poland") == Ok("Poland")

    def test_na(self):
        assert parse_team("NA") == Ok(None)

    def test_empty(self):
        assert parse_team("") == Ok(None)


class TestParseNoc:
    def test_valid(self):
        assert parse_noc("POL") == Ok("POL")

    def test_na(self):
        assert parse_noc("NA").is_err()

    def test_empty(self):
        assert parse_noc("").is_err()


class TestParseYear:
    def test_valid(self):
        assert parse_year("2000") == Ok(2000)

    def test_na(self):
        assert parse_year("NA").is_err()

    def test_invalid(self):
        assert parse_year("abc").is_err()

    def test_empty(self):
        assert parse_year("").is_err()


class TestParseSeason:
    def test_summer(self):
        assert parse_season("Summer") == Ok("Summer")

    def test_winter(self):
        assert parse_season("Winter") == Ok("Winter")

    def test_invalid(self):
        assert parse_season("Spring").is_err()

    def test_empty(self):
        assert parse_season("").is_err()


class TestParseSport:
    def test_valid(self):
        assert parse_sport("Swimming") == Ok("Swimming")

    def test_na(self):
        assert parse_sport("NA").is_err()

    def test_empty(self):
        assert parse_sport("").is_err()


class TestParseEvent:
    def test_valid(self):
        assert parse_event("Swimming Men's 100m Freestyle") == Ok("Swimming Men's 100m Freestyle")

    def test_na(self):
        assert parse_event("NA").is_err()


class TestParseMedal:
    def test_gold(self):
        assert parse_medal("Gold") == Ok("Gold")

    def test_silver(self):
        assert parse_medal("Silver") == Ok("Silver")

    def test_bronze(self):
        assert parse_medal("Bronze") == Ok("Bronze")

    def test_na(self):
        assert parse_medal("NA") == Ok(None)

    def test_empty(self):
        assert parse_medal("") == Ok(None)

    def test_invalid(self):
        assert parse_medal("Platinum").is_err()


class TestParseAthlete:
    def _valid_row(self):
        return {
            'Name': 'Michael Phelps', 'Sex': 'M', 'Age': '23',
            'Height': '193', 'Weight': '91', 'Team': 'United States',
            'NOC': 'USA', 'Year': '2004', 'Season': 'Summer',
            'Sport': 'Swimming', 'Event': "Swimming Men's 100m Butterfly",
            'Medal': 'Gold',
        }

    def test_valid_row(self):
        result = parse_athlete(self._valid_row())
        assert result.is_ok()
        a = result.unwrap()
        assert isinstance(a, Athlete)
        assert a.name == 'Michael Phelps'
        assert a.medal == 'Gold'
        assert a.age == 23

    def test_na_medal_is_ok(self):
        row = {**self._valid_row(), 'Medal': 'NA'}
        result = parse_athlete(row)
        assert result.is_ok()
        assert result.unwrap().medal is None

    def test_na_age_is_ok(self):
        row = {**self._valid_row(), 'Age': 'NA'}
        result = parse_athlete(row)
        assert result.is_ok()
        assert result.unwrap().age is None

    def test_invalid_sex_is_err(self):
        row = {**self._valid_row(), 'Sex': 'X'}
        assert parse_athlete(row).is_err()

    def test_missing_year_is_err(self):
        row = {**self._valid_row(), 'Year': 'NA'}
        assert parse_athlete(row).is_err()

    def test_invalid_season_is_err(self):
        row = {**self._valid_row(), 'Season': 'Spring'}
        assert parse_athlete(row).is_err()

    def test_fail_fast(self):
        row = {**self._valid_row(), 'Sex': 'X', 'Season': 'Spring'}
        result = parse_athlete(row)
        assert result.is_err()
        assert 'sex' in result.reason

    def test_athlete_is_immutable(self):
        result = parse_athlete(self._valid_row())
        athlete = result.unwrap()
        with pytest.raises(Exception):
            athlete.name = 'Someone Else'
