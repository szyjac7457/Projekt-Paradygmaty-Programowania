import sys
from src.parsing.reader import parse_csv
from src.core.result import filter_ok
from src.core.functional import pipe
from src.transform.filters import has_medal, by_country
from src.aggregate.reducers import (
    count_medals_by_country,
    count_medals_by_sex,
    count_medals_by_year,
    calculate_age_statistics,
    count_medals_by_sport,
    count_participation_by_decade,
    count_medals_by_sport_and_country
)
from src.aggregate.report import (
    generate_medal_ranking_report,
    generate_sex_distribution_report,
    generate_medals_by_year_report,
    generate_age_statistics_report,
    generate_top_sports_report,
    generate_female_participation_report,
    generate_dominance_report
)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/athlete_events.csv'
    print(f"Uruchamianie silnika analitycznego dla pliku: {path}...\n")

    # Parsowanie i czyszczenie
    wszyscy_czysci_zawodnicy = list(pipe(parse_csv, filter_ok)(path))
    
    #  Tylko medaliśc
    tylko_medalisci = list(filter(has_medal, wszyscy_czysci_zawodnicy))
    
    #ylko polscy medaliści
    polscy_medalisci = list(filter(by_country('POL'), tylko_medalisci))

    
    raport_kraje = generate_medal_ranking_report(count_medals_by_country(tylko_medalisci))
    raport_plec = generate_sex_distribution_report(count_medals_by_sex(tylko_medalisci))
    raport_wiek = generate_age_statistics_report(calculate_age_statistics(tylko_medalisci))
    raport_polska_lata = generate_medals_by_year_report(count_medals_by_year(polscy_medalisci), "POLSKIE MEDALE W LATACH")
    
    # Medale Polaków
    raport_sport_polska = generate_top_sports_report(count_medals_by_sport(polscy_medalisci), 10, "MEDALE POLAKÓW WEDŁUG DYSCYPLIN")

    raport_kobiety = generate_female_participation_report(count_participation_by_decade(wszyscy_czysci_zawodnicy))
    raport_dominacja = generate_dominance_report(count_medals_by_sport_and_country(tylko_medalisci), 10)


    print(raport_kraje)
    print()
    print(raport_plec)
    print()
    print(raport_wiek)
    print()
    print(raport_sport_polska)
    print()
    print(raport_polska_lata)
    print()
    print(raport_kobiety)
    print()
    print(raport_dominacja)

if __name__ == '__main__':
    main()