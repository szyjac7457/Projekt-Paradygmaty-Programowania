from src.aggregate.reducers import count_total_medals
from src.parsing.parser import Athlete

def test_count_total_medals():
    
    athletes = [
        Athlete(name="Kamil Stoch", sex="M", age=26, height=173.0, weight=55.0, 
                team="Poland", noc="POL", year=2014, season="Winter", 
                sport="Ski Jumping", event="Large Hill", medal="Gold"),
        Athlete(name="Robert Lewandowski", sex="M", age=32, height=185.0, weight=81.0, 
                team="Poland", noc="POL", year=2020, season="Summer", 
                sport="Football", event="Football", medal=None),
        Athlete(name="Piotr Żyła", sex="M", age=34, height=176.0, weight=59.0, 
                team="Poland", noc="POL", year=2021, season="Winter", 
                sport="Ski Jumping", event="Normal Hill", medal="Bronze")
    ]
    
    
    result = count_total_medals(athletes)
    assert result == 2

from src.aggregate.reducers import calculate_average_demographics

def test_calculate_average_demographics():
    athletes = [
        Athlete(name="Zawodnik 1", sex="M", age=20, height=180.0, weight=80.0, 
                team="Poland", noc="POL", year=2000, season="Summer", 
                sport="Judo", event="Men's", medal=None),
        Athlete(name="Zawodnik 2", sex="M", age=30, height=190.0, weight=90.0, 
                team="Poland", noc="POL", year=2000, season="Summer", 
                sport="Judo", event="Men's", medal=None),
        Athlete(name="Brak Danych", sex="M", age=None, height=190.0, weight=90.0, 
                team="Poland", noc="POL", year=2000, season="Summer", 
                sport="Judo", event="Men's", medal=None) 
    ]
    
   
    result = calculate_average_demographics(athletes)
    
    assert result["avg_age"] == 25.0
    assert result["avg_height"] == 185.0

from src.aggregate.report import generate_medal_ranking_report

def test_generate_medal_ranking_report():
   
    mock_data = {"USA": 10, "POL": 15, "GER": 5}
    
    
    report = generate_medal_ranking_report(mock_data)
    
   
    assert "1. POL - 15 medali" in report
    assert "2. USA - 10 medali" in report
    assert "3. GER - 5 medali" in report
    assert "=== KLASYFIKACJA MEDALOWA ===" in report



from src.aggregate.reducers import count_medals_by_sport, calculate_age_statistics
from src.aggregate.report import generate_top_sports_report, generate_age_statistics_report

#TESTY DLA AGREGATORÓW

def test_count_medals_by_sport():
    athletes = [
        Athlete(name="A1", sex="M", age=20, height=180.0, weight=80.0, team="POL", noc="POL", year=2000, season="Summer", sport="Judo", event="E", medal="Gold"),
        Athlete(name="A2", sex="M", age=20, height=180.0, weight=80.0, team="POL", noc="POL", year=2000, season="Summer", sport="Judo", event="E", medal="Silver"),
        Athlete(name="A3", sex="M", age=20, height=180.0, weight=80.0, team="POL", noc="POL", year=2000, season="Summer", sport="Volleyball", event="E", medal="Bronze"),
        Athlete(name="A4", sex="M", age=20, height=180.0, weight=80.0, team="POL", noc="POL", year=2000, season="Summer", sport="Football", event="E", medal=None) # Bez medalu
    ]
    
    result = count_medals_by_sport(athletes)
     
    assert result == {"Judo": 2, "Volleyball": 1}

def test_calculate_age_statistics():
    athletes = [
        Athlete(name="A1", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="T", year=2000, season="Summer", sport="S", event="E", medal="Gold"),
        Athlete(name="A2", sex="M", age=24, height=180.0, weight=80.0, team="T", noc="T", year=2000, season="Summer", sport="S", event="E", medal="Silver"),
        Athlete(name="A3", sex="M", age=26, height=180.0, weight=80.0, team="T", noc="T", year=2000, season="Summer", sport="S", event="E", medal="Bronze"),
        Athlete(name="A4", sex="M", age=None, height=180.0, weight=80.0, team="T", noc="T", year=2000, season="Summer", sport="S", event="E", medal="Gold") # Brak wieku, ignorowany
    ]
    
    result = calculate_age_statistics(athletes)
    
    
    assert result["mean"] == 23.33
    assert result["median"] == 24
    assert result["min"] == 20
    assert result["max"] == 26

#TESTY DLA GENERATORÓW RAPORTÓW

def test_generate_age_statistics_report():
    mock_stats = {"mean": 25.5, "median": 24.0, "min": 18, "max": 40}
    report = generate_age_statistics_report(mock_stats)
    
    assert "Średnia wieku:       25.5 lat" in report
    assert "Mediana wieku:       24.0 lat" in report
    assert "Najmłodszy zawodnik: 18 lat" in report
    assert "Najstarszy zawodnik: 40 lat" in report

def test_generate_top_sports_report():
    
    mock_data = {"Football": 2, "Volleyball": 5, "Ski Jumping": 15}
    
   
    report = generate_top_sports_report(mock_data, limit=2, title="TEST SPORT")
    lines = report.split('\n')
    
    assert "1. Ski Jumping - 15 medali" in lines[1]
    assert "2. Volleyball - 5 medali" in lines[2]
    assert "Football" not in report

from src.aggregate.reducers import count_participation_by_decade, count_medals_by_sport_and_country
from src.aggregate.report import generate_female_participation_report, generate_dominance_report

def test_count_participation_by_decade():
    athletes = [
        Athlete(name="A1", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="T", year=2012, season="Summer", sport="S", event="E", medal=None),
        Athlete(name="A2", sex="F", age=22, height=170.0, weight=60.0, team="T", noc="T", year=2016, season="Summer", sport="S", event="E", medal=None),
        Athlete(name="A3", sex="F", age=24, height=172.0, weight=62.0, team="T", noc="T", year=2018, season="Winter", sport="S", event="E", medal="Gold"),
        Athlete(name="A4", sex="M", age=28, height=185.0, weight=85.0, team="T", noc="T", year=1996, season="Summer", sport="S", event="E", medal=None),
    ]

    result = count_participation_by_decade(athletes)

    assert result[2010] == {"total": 3, "female": 2}
    assert result[1990] == {"total": 1, "female": 0}

def test_count_medals_by_sport_and_country():
    athletes = [
        Athlete(name="A1", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="POL", year=2000, season="Summer", sport="Judo", event="E", medal="Gold"),
        Athlete(name="A2", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="POL", year=2000, season="Summer", sport="Judo", event="E", medal="Silver"),
        Athlete(name="A3", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="GER", year=2000, season="Summer", sport="Judo", event="E", medal="Bronze"),
        Athlete(name="A4", sex="M", age=20, height=180.0, weight=80.0, team="T", noc="USA", year=2000, season="Summer", sport="Swimming", event="E", medal=None),
    ]

    result = count_medals_by_sport_and_country(athletes)

    assert result == {"Judo": {"POL": 2, "GER": 1}}

def test_generate_female_participation_report():
    mock_data = {2010: {"total": 4, "female": 1}, 2000: {"total": 2, "female": 1}}
    report = generate_female_participation_report(mock_data)
    lines = report.split('\n')

    assert "Dekada 2000: 50.0% kobiet (1/2)" in lines[1]
    assert "Dekada 2010: 25.0% kobiet (1/4)" in lines[2]

def test_generate_dominance_report():
    mock_data = {"Judo": {"POL": 2, "GER": 1}, "Swimming": {"USA": 5}}
    report = generate_dominance_report(mock_data, limit=10)

    assert "Swimming: dominuje USA (5 medali)" in report
    assert "Judo: dominuje POL (2 medali)" in report