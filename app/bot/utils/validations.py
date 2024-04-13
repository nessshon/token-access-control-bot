def is_decimal(s: str) -> bool:
    if s.startswith("-"):
        s = s[1:]
    return s.isdigit()


def is_float(s: str) -> bool:
    try:
        s = s.replace(",", ".")
        float(s)
    except ValueError:
        return False
    return True
