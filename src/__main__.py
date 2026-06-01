import sys
from src.parsing.reader import parse_csv
from src.core.result import partition_results


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/athlete_events.csv'
    oks, errs = partition_results(parse_csv(path))
    print(f"Parsed OK:    {len(oks)}")
    print(f"Parse errors: {len(errs)}")
    if errs:
        print("\nSample errors:")
        for e in errs[:5]:
            print(f"  - {e}")


if __name__ == '__main__':
    main()
