def resolve_suffix(text):
    text = text.replace(",", "")
    decimal_val = float(0)
    suffix = ""
    if text.isnumeric():
        decimal_val = float(text)
    else:
        decimal_val = float(text[:-1])
    if not len(text) <= 1:
            suffix = text[-1].lower()
    resolved_decimal_val = decimal_val
    if suffix == "k":
        resolved_decimal_val = decimal_val * 10 ** 3
    elif suffix == "m":
        resolved_decimal_val = decimal_val *  10 ** 6
    elif suffix == "b":
        resolved_decimal_val = decimal_val *  10 ** 9
    elif suffix == "t":
        resolved_decimal_val = decimal_val *  10 ** 12
    return round(resolved_decimal_val)