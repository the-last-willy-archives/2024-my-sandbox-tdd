def _is_div(n, div):
    return n % div == 0


def is_leapyear(year) -> bool:
    if year != round(year):
        raise ValueError(f"{year} is not an integer.")
    return _is_div(year, 4) and (not _is_div(year, 100) or _is_div(year, 400))
