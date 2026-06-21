def generate_medal_ranking_report(medal_counts: dict[str, int]) -> str:
    if not medal_counts:
        return "Brak danych do wygenerowania raportu."

    sorted_ranking = sorted(medal_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Bezstanowy zip oraz range zastępujący  enumerate
    ranking_numbers = range(1, len(sorted_ranking) + 1)
    zipped_ranking = zip(ranking_numbers, sorted_ranking)
    
    lines = list(map(lambda item: f"{item[0]}. {item[1][0]} - {item[1][1]} medali", zipped_ranking))
    
    return "\n".join(["=== KLASYFIKACJA MEDALOWA ==="] + lines + ["============================="])


def generate_sex_distribution_report(sex_counts: dict[str, int]) -> str:
    if not sex_counts:
        return "Brak danych o płci."
        
    get_label = lambda sex: "Mężczyźni" if sex == "M" else "Kobiety" if sex == "F" else "Inne"
    lines = list(map(lambda item: f"{get_label(item[0])}: {item[1]} medali", sex_counts.items()))
    
    return "\n".join(["=== MEDALE WEDŁUG PŁCI ==="] + lines + ["=========================="])


def generate_medals_by_year_report(year_counts: dict[int, int], title: str = "MEDALE WEDŁUG LAT") -> str:
    if not year_counts:
        return "Brak danych."
    
    sorted_years = sorted(year_counts.items(), key=lambda item: item[0])
    lines = list(map(lambda item: f"Rok {item[0]}: {item[1]} medali", sorted_years))
    
    return "\n".join([f"=== {title} ==="] + lines + ["========================="])


def generate_age_statistics_report(stats: dict) -> str:
    if not stats or stats.get("mean") == 0.0:
        return "Brak danych o wieku."
        
    lines = [
        f"Średnia wieku:       {stats['mean']} lat",
        f"Mediana wieku:       {stats['median']} lat",
        f"Najmłodszy zawodnik: {stats['min']} lat",
        f"Najstarszy zawodnik: {stats['max']} lat"
    ]
    
    return "\n".join(["=== STATYSTYKI WIEKOWE ==="] + lines + ["=========================="])


def generate_top_sports_report(sport_counts: dict[str, int], limit: int = 10, title: str = "TOP DYSCYPLINY") -> str:
    if not sport_counts:
        return "Brak danych o dyscyplinach."

    sorted_sports = sorted(sport_counts.items(), key=lambda item: item[1], reverse=True)[:limit]
    
    # range i zip zamiast stanowego enumerate
    ranking_numbers = range(1, len(sorted_sports) + 1)
    zipped_sports = zip(ranking_numbers, sorted_sports)
    
    lines = list(map(lambda item: f"{item[0]}. {item[1][0]} - {item[1][1]} medali", zipped_sports))

    return "\n".join([f"=== {title} ==="] + lines + ["======================"])


def generate_female_participation_report(decade_stats: dict[int, dict[str, int]]) -> str:
    if not decade_stats:
        return "Brak danych o uczestnictwie."

    sorted_decades = sorted(decade_stats.items(), key=lambda item: item[0])

    def format_line(item):
        decade, stats = item
        pct = round(100 * stats["female"] / stats["total"], 1) if stats["total"] else 0.0
        return f"Dekada {decade}: {pct}% kobiet ({stats['female']}/{stats['total']})"

    lines = list(map(format_line, sorted_decades))

    return "\n".join(["=== UDZIAŁ KOBIET W DEKADACH ==="] + lines + ["================================"])


def generate_dominance_report(sport_country_counts: dict[str, dict[str, int]], limit: int = 10) -> str:
    if not sport_country_counts:
        return "Brak danych o dominacji."

    def dominant_country(item):
        sport, counts = item
        top_noc, top_count = max(counts.items(), key=lambda kv: kv[1])
        return (sport, top_noc, top_count)

    rows = sorted(map(dominant_country, sport_country_counts.items()), key=lambda r: r[2], reverse=True)[:limit]

    lines = list(map(lambda r: f"{r[0]}: dominuje {r[1]} ({r[2]} medali)", rows))

    return "\n".join(["=== DOMINACJA W DYSCYPLINACH ==="] + lines + ["==============================="])