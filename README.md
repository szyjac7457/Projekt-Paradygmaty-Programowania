# Funkcyjny silnik analizy danych Igrzysk Olimpijskich

**Projekt zaliczeniowy — Paradygmaty Programowania, Część II (Programowanie funkcyjne)**

Autorzy: Szymon Jachimowicz, Mikołaj Szyra, Paweł Zubalski
Kierunek: Sztuczna Inteligencja, 1° stopień, 2. semestr

---

## 1. Streszczenie projektu

Projekt realizuje silnik analityczny przetwarzający duży zbiór danych historycznych Igrzysk Olimpijskich (ponad 120 lat wyników, ok. 270 tys. rekordów zawodników) w paradygmacie funkcyjnym. Architektura systemu w całości odchodzi od podejścia imperatywnego — zamiast mutowalnego stanu, pętli i modyfikacji danych w miejscu, buduje **potok (pipeline) złożony z czystych funkcji**, przez który dane przepływają i są sukcesywnie przekształcane.

Rdzeniem systemu jest jednokierunkowy przepływ informacji:

```
surowe dane CSV
    → parsowanie i walidacja (monada Result)
    → transformacje (filtrowanie, mapowanie, wzbogacanie)
    → agregacje i statystyki (reduce/fold)
    → raport (klasyfikacje medalowe, statystyki, trendy)
```

Każdy etap potoku to czysta funkcja — przekształca dane wejściowe w nowe dane wyjściowe, nie modyfikując wejścia i nie powodując efektów ubocznych.

---

## 2. Cel projektu

Celem projektu jest zaprojektowanie i implementacja realnego, użytecznego systemu analitycznego, którego architektura **eksponuje paradygmat funkcyjny w jego naturalnej postaci**. Wybór dziedziny (analiza danych historycznych) nie jest przypadkowy — przetwarzanie zbiorów danych w postaci pipeline'u przekształceń jest jednym z kanonicznych zastosowań paradygmatu funkcyjnego i pozwala w sposób organiczny wykorzystać wszystkie cztery główne mechanizmy przedstawione w Części II wykładu:

- czyste funkcje i kompozycja,
- funkcje wyższego rzędu i wyrażenia lambda,
- leniwa ewaluacja (generatory),
- monada (`Result` / `Maybe`).

Mechanizmy te nie są w projekcie doklejone w sposób sztuczny — każdy z nich rozwiązuje konkretny problem domenowy, który pojawia się przy przetwarzaniu rzeczywistych, niedoskonałych danych.

---

## 3. Problem domenowy i wyzwania architektoniczne

Rzeczywiste dane historyczne charakteryzują się **niejednorodnością i niekompletnością** (brakujące wartości wieku, wzrostu, wagi zawodników, puste pola medali dla nieklasyfikowanych) oraz koniecznością składania wielu niezależnych przekształceń i agregacji. Architektura projektu odpowiada na cztery główne wyzwania:

### 3.1. Zarządzanie błędami bez efektów ubocznych

Błędne lub niekompletne wiersze (brakujące pola, niepoprawny format liczbowy) nie mogą przerywać działania całego potoku ani wymuszać rozproszonej obsługi wyjątków poprzez `try/except`. W paradygmacie funkcyjnym błąd jest traktowany jako **wartość**, która przepływa przez potok obok danych poprawnych — pozwala to na końcu rozdzielić rekordy poprawne od odrzuconych bez przerywania przepływu.

### 3.2. Komponowalność i rozszerzalność

Dodanie nowej analizy — nowego rankingu, nowej statystyki, nowego filtra po dyscyplinie — nie może wymagać modyfikacji istniejącego kodu. Ma polegać wyłącznie na **dołączeniu kolejnej czystej funkcji** do potoku. Jest to funkcyjny odpowiednik zasady otwarte-zamknięte (OCP) z programowania obiektowego.

### 3.3. Wydajność pamięciowa

System musi przetwarzać zbiór o dużej liczbie rekordów (~270 tys.) **bez wczytywania całości do pamięci operacyjnej na raz**. Realizowane jest to przez leniwą ewaluację — dane płyną przez potok strumieniowo, wiersz po wierszu, a obliczenia wykonywane są dopiero w momencie, gdy wynik jest potrzebny.

### 3.4. Brak współdzielonego stanu mutowalnego

Eliminacja mutacji danych zapewnia **przewidywalność, testowalność i brak skutków ubocznych**. Każde wywołanie funkcji z tymi samymi argumentami daje ten sam wynik (właściwość transparentności referencyjnej), co radykalnie upraszcza testowanie i rozumowanie o kodzie.

---

## 4. Zastosowane mechanizmy funkcyjne

Rozwiązanie powyższych problemów opiera się na synergicznym połączeniu czterech mechanizmów paradygmatu funkcyjnego.

### 4.1. Czyste funkcje i kompozycja

Każdy etap potoku jest czystą funkcją w sensie matematycznym — przekształca dane wejściowe w nowe dane wyjściowe, **bez modyfikacji wejścia i bez efektów ubocznych**. Cały przepływ budowany jest poprzez kompozycję (`compose` / `pipe`) tych funkcji w jeden potok.

Przykładowo, zamiast pisać:

```python
# Podejście imperatywne (NIE używamy tego)
result = []
for row in data:
    parsed = parse(row)
    if parsed['year'] > 2000:
        parsed['country_upper'] = parsed['country'].upper()
        result.append(parsed)
```

stosujemy:

```python
# Podejście funkcyjne
pipeline = compose(
    map_fn(add_country_upper),
    filter_fn(lambda r: r['year'] > 2000),
    map_fn(parse_row),
)
result = pipeline(data)
```

### 4.2. Funkcje wyższego rzędu i wyrażenia lambda

Operacje filtrowania i mapowania są **sparametryzowane funkcjami przekazywanymi jako argumenty** (predykaty, mappery). Pozwala to składać dowolne łańcuchy przetwarzania z małych, wielokrotnie używalnych klocków.

Przykłady wykorzystania w projekcie:

```python
filter_by_country = lambda c: lambda r: r['country'] == c
filter_by_season  = lambda s: lambda r: r['season'] == s
filter_by_year_range = lambda a, b: lambda r: a <= r['year'] <= b

medals_pl_summer = pipe(
    filter_fn(filter_by_country('POL')),
    filter_fn(filter_by_season('Summer')),
    filter_fn(lambda r: r['medal'] is not None),
)
```

### 4.3. Leniwa ewaluacja (generatory)

Dane przepływają przez potok **leniwie**, wiersz po wierszu, ewaluowane na żądanie. Umożliwia to przetwarzanie całego dużego zbioru bez nadmiernego zużycia pamięci oraz eliminuje zbędne obliczenia (np. przy wyciąganiu pierwszych 10 wyników nie liczymy reszty).

W Pythonie realizowane przez generatory:

```python
def read_csv_lazy(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row  # leniwe — wiersz wraca dopiero gdy potrzebny
```

### 4.4. Monada Result / Maybe

Obsługa błędów bez wyjątków i bez przerywania potoku. Niepoprawne lub niekompletne rekordy opakowywane są w wartość reprezentującą sukces (`Ok`) lub porażkę (`Err`), która propaguje się przez kolejne kroki potoku. Funkcje operujące na wartościach `Result` automatycznie "przepuszczają" błędy dalej (operacja `bind` / `flat_map`), aż na końcu można rozdzielić poprawne wyniki od odrzuconych rekordów.

Schematycznie:

```python
Ok(value).map(f)       # → Ok(f(value))
Err(reason).map(f)     # → Err(reason)   # błąd przepływa nietknięty

Ok(value).bind(f)      # → f(value)      # f zwraca Result
Err(reason).bind(f)    # → Err(reason)
```

Dzięki temu cały kod parsowania pozostaje liniowy i czytelny, bez zagnieżdżonych `try/except`.

### 4.5. Hybrydowość: Elementy obiektowe w służbie paradygmatu funkcyjnego

Choć rdzeniem systemu są mechanizmy funkcyjne, projekt zaimplementowano w języku Python. Pozwoliło to na stworzenie architektury hybrydowej (funkcyjno-obiektowej), w której elementy programowania obiektowego bezpośrednio wspierają i ułatwiają realizację celów funkcyjnych:

* **Niemutowalne Obiekty Danych (Value Objects):** Reprezentacja zawodnika — klasa `Athlete` — została zdefiniowana za pomocą `@dataclass(frozen=True)`. Gwarantuje to absolutną niemutowalność stanu obiektów po ich utworzeniu (brak efektów ubocznych), co jest fundamentem podejścia funkcyjnego.
* **Obiektowy interfejs monad:** Monady `Ok` oraz `Err` zaimplementowano jako klasy posiadające metody `.map()` oraz `.bind()`. Ułatwia to czytelne łańcuchowanie operacji (Fluent API / Method Chaining) bez konieczności tworzenia głęboko zagnieżdżonych wywołań funkcyjnych.
* **Hermetyzacja struktur danych:** Wykorzystanie klas do definiowania typów pozwala na statyczne otypowanie kodu (Type Hints) i bezpieczniejsze zarządzanie złożonymi strukturami bez rezygnacji z czystości funkcyjnej.

---

## 5. Architektura systemu

System dzieli się na trzy warstwy potoku, odpowiadające naturalnemu podziałowi prac w zespole 3-osobowym.

### 5.1. Warstwa I — Parsowanie i walidacja

**Odpowiedzialność:** zamiana surowych wierszy CSV w otypowane rekordy zawodników; obsługa niekompletnych i błędnych danych.

**Wykorzystane mechanizmy:** czyste funkcje, monada `Result`, leniwa ewaluacja (czytanie pliku przez generator).

**Wejście:** strumień surowych wierszy z pliku CSV.
**Wyjście:** strumień wartości `Result[Athlete]` — `Ok(rekord)` dla poprawnych, `Err(powód)` dla odrzuconych.

### 5.2. Warstwa II — Transformacje

**Odpowiedzialność:** filtrowanie (po kraju, sezonie, dyscyplinie, roku), mapowanie, wzbogacanie rekordów o pola wyliczane.

**Wykorzystane mechanizmy:** funkcje wyższego rzędu, lambdy, kompozycja, leniwa ewaluacja.

**Wejście:** strumień poprawnych rekordów zawodników.
**Wyjście:** strumień rekordów po przefiltrowaniu i transformacjach.

### 5.3. Warstwa III — Agregacje i raportowanie

**Odpowiedzialność:** obliczanie klasyfikacji medalowych, statystyk zawodników, trendów historycznych; generowanie raportu końcowego.

**Wykorzystane mechanizmy:** `reduce` / `fold`, funkcje wyższego rzędu, leniwa ewaluacja.

**Wejście:** strumień przefiltrowanych rekordów.
**Wyjście:** sformatowane raporty tekstowe wypisywane na konsolę (struktury słownikowe gotowe do dalszej wizualizacji).

---

## 6. Analizy i raporty

System generuje następujące analizy (zaimplementowane):

- **Klasyfikacja medalowa krajów** — ranking krajów według liczby zdobytych medali.
- **Rozkład medali według płci** — zestawienie medali zdobytych przez kobiety i mężczyzn.
- **Statystyki wiekowe** — średnia, mediana oraz wartości skrajne wieku medalistów (liczone bez pętli imperatywnych).
- **Dorobek medalowy Polski** — medale reprezentacji Polski według lat oraz według dyscyplin.
- **Udział kobiet w kolejnych dekadach** — procentowy udział kobiet wśród uczestników w podziale na dekady.
- **Dominacja w dyscyplinach** — kraj z największą liczbą medali w każdej dyscyplinie.

Kierunki dalszego rozwoju (planowane, jeszcze niezaimplementowane): ranking najbardziej utytułowanych zawodników i długość karier olimpijskich, trendy liczby uczestniczących krajów i zawodników w czasie oraz statystyki organizacyjne poszczególnych edycji igrzysk.

---

## 7. Struktura projektu

```
olympic-functional-analyzer/
├── README.md
├── pyproject.toml              # konfiguracja projektu i zależności
├── .gitignore
├── data/
│   ├── .gitkeep                # CSV pobierany lokalnie, nie wersjonowany
│   └── README.md               # instrukcja pobrania zbioru danych
├── src/
│   ├── __init__.py
│   ├── __main__.py             # punkt wejścia (python -m src)
│   ├── core/                   # narzędzia wspólne dla wszystkich warstw
│   │   ├── __init__.py
│   │   ├── result.py           # monada Result / Maybe
│   │   └── functional.py       # compose, pipe, curry, itp.
│   ├── parsing/                # Warstwa I
│   │   ├── __init__.py
│   │   ├── reader.py           # leniwe czytanie CSV (generator)
│   │   ├── parser.py           # parsowanie wierszy → Result[Athlete]
│   │   └── validators.py       # walidatory pól
│   ├── transform/              # Warstwa II
│   │   ├── __init__.py
│   │   ├── filters.py          # predykaty (HOF zwracające funkcje)
│   │   ├── mappers.py          # mappery wzbogacające rekordy
│   │   └── pipelines.py        # gotowe kompozycje
│   └── aggregate/              # Warstwa III
│       ├── __init__.py
│       ├── reducers.py         # operacje reduce/fold + statystyki
│       └── report.py           # generowanie raportów
└── tests/
    ├── __init__.py
    ├── conftest.py             # współdzielone fixture'y pytest
    ├── test_result.py
    ├── test_parsing.py
    ├── test_transform.py
    └── test_aggregate.py
```

**Uwagi do struktury:**

- **`core/`** zawiera klocki współdzielone przez wszystkie trzy warstwy potoku (monada `Result`, narzędzia kompozycji `pipe`/`compose`). Do leniwej ewaluacji wykorzystywane są wbudowane mechanizmy Pythona — generatory i moduł `itertools` — bez osobnego pliku narzędziowego.
- **`data/`** nie zawiera samego pliku CSV — zbiór danych (~40 MB) pobierany jest lokalnie zgodnie z instrukcją w `data/README.md` i ignorowany przez `.gitignore`.
- **`__main__.py`** zamiast `main.py` umożliwia uruchamianie pakietu przez `python -m src`, co jest idiomatyczne dla Pythona.
- Każdy podkatalog `src/` posiada plik `__init__.py`, dzięki czemu jest poprawnym pakietem Pythona.

---

## 8. Instalacja i uruchomienie

### 8.1. Wymagania

- Python 3.10 lub nowszy
- Brak zależności runtime — projekt korzysta wyłącznie z biblioteki standardowej. Do testów używany jest `pytest` (zależność deweloperska zdefiniowana w `pyproject.toml`).

### 8.2. Instalacja

```bash
git clone git@github.com:szyjac7457/Projekt-Paradygmaty-Programowania.git
cd Projekt-Paradygmaty-Programowania
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows
pip install -e ".[dev]"           # instalacja pakietu w trybie edytowalnym wraz z zależnościami deweloperskimi
```

### 8.3. Pobranie danych

Zbiór danych: **"120 years of Olympic history: athletes and results"**
Źródło: [Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

Plik `athlete_events.csv` należy umieścić w katalogu `data/`. Plik nie jest wersjonowany w repozytorium ze względu na rozmiar — szczegółowa instrukcja pobrania znajduje się w `data/README.md`.

### 8.4. Uruchomienie

```bash
python -m src                            # użyje domyślnej ścieżki data/athlete_events.csv
python -m src data/athlete_events.csv    # albo wskaż plik jawnie
```

Program wczytuje plik, czyści dane i wypisuje na konsolę komplet raportów: klasyfikację medalową krajów, rozkład medali wg płci, statystyki wiekowe, dorobek Polski (wg dyscyplin i lat), udział kobiet w dekadach oraz dominację krajów w dyscyplinach.

### 8.5. Testy

```bash
pytest tests/
```

---

## 9. Przykład użycia (programistycznie)

```python
from src.parsing.reader import parse_csv
from src.core.result import filter_ok
from src.transform.filters import by_country, by_season, has_medal
from src.aggregate.reducers import count_medals_by_country
from src.core.functional import pipe

# Budujemy potok jako kompozycję czystych funkcji
analyze_polish_summer_medals = pipe(
    parse_csv,                                  # leniwe czytanie + parsowanie → Result[Athlete]
    filter_ok,                                  # odrzuć błędne rekordy i wydobądź wartości
    lambda rs: filter(by_country('POL'), rs),
    lambda rs: filter(by_season('Summer'), rs),
    lambda rs: filter(has_medal, rs),
    count_medals_by_country,
)

result = analyze_polish_summer_medals('data/athlete_events.csv')
print(result)
```

---

## 10. Podział prac w zespole

| Członek zespołu | Warstwa | Główna odpowiedzialność |
|---|---|---|
| Szymon Jachimowicz | I — Parsowanie i walidacja | Implementacja monady `Result`, leniwego czytnika CSV, walidatorów |
| Paweł Zubalski | II — Transformacje | Funkcje wyższego rzędu, kompozycja, biblioteka filtrów i mapperów |
| Mikołaj Szyra | III — Agregacje i raporty | Operacje `reduce`/`fold`, statystyki, generowanie raportów |

Każda warstwa eksponuje wszystkie cztery mechanizmy funkcyjne w swoim zakresie odpowiedzialności — paradygmat jest widoczny u każdego członka zespołu.

---

## 11. Licencja

Projekt akademicki — wykorzystanie na zasadach edukacyjnych.