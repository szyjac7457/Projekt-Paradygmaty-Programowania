import pytest
from src.parsing.parser import Athlete


@pytest.fixture
def sample_athlete():
    return Athlete(
        name="Michael Phelps", sex="M", age=23,
        height=193.0, weight=91.0, team="United States",
        noc="USA", year=2004, season="Summer",
        sport="Swimming", event="Swimming Men's 100m Butterfly",
        medal="Gold",
    )


@pytest.fixture
def sample_row():
    return {
        'Name': 'Michael Phelps', 'Sex': 'M', 'Age': '23',
        'Height': '193', 'Weight': '91', 'Team': 'United States',
        'NOC': 'USA', 'Year': '2004', 'Season': 'Summer',
        'Sport': 'Swimming', 'Event': "Swimming Men's 100m Butterfly",
        'Medal': 'Gold',
    }
