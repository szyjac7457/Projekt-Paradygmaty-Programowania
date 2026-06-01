from src.core.result import Ok, Err


def parse_name(s):
    if not s or s == 'NA':
        return Err("missing name")
    return Ok(s)


def parse_sex(s):
    if s not in ('M', 'F'):
        return Err(f"invalid sex: {s!r}")
    return Ok(s)


def parse_age(s):
    if s == 'NA':
        return Ok(None)
    try:
        v = int(s)
    except (ValueError, TypeError):
        return Err(f"invalid age: {s!r}")
    if v < 0 or v > 150:
        return Err(f"age out of range: {s!r}")
    return Ok(v)


def parse_height(s):
    if s == 'NA':
        return Ok(None)
    try:
        return Ok(float(s))
    except (ValueError, TypeError):
        return Err(f"invalid height: {s!r}")


def parse_weight(s):
    if s == 'NA':
        return Ok(None)
    try:
        return Ok(float(s))
    except (ValueError, TypeError):
        return Err(f"invalid weight: {s!r}")


def parse_team(s):
    if not s or s == 'NA':
        return Ok(None)
    return Ok(s)


def parse_noc(s):
    if not s or s == 'NA':
        return Err("missing NOC")
    return Ok(s)


def parse_year(s):
    if not s or s == 'NA':
        return Err("missing year")
    try:
        return Ok(int(s))
    except (ValueError, TypeError):
        return Err(f"invalid year: {s!r}")


def parse_season(s):
    if s not in ('Summer', 'Winter'):
        return Err(f"invalid season: {s!r}")
    return Ok(s)


def parse_sport(s):
    if not s or s == 'NA':
        return Err("missing sport")
    return Ok(s)


def parse_event(s):
    if not s or s == 'NA':
        return Err("missing event")
    return Ok(s)


def parse_medal(s):
    if not s or s == 'NA':
        return Ok(None)
    if s in ('Gold', 'Silver', 'Bronze'):
        return Ok(s)
    return Err(f"invalid medal: {s!r}")
