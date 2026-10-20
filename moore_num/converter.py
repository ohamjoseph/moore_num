"""
Mooré number to text converter.
"""

UNITS_SHORT = {
    1: "ye", 2: "yi", 3: "tã", 4: "naase", 5: "nu",
    6: "yoobe", 7: "yopoe", 8: "nii", 9: "wɛ"
}

UNITS_LONG = {
    1: "yembre", 2: "yiibu", 3: "tãabo", 4: "naase", 5: "nu",
    6: "yoobe", 7: "yopoe", 8: "nii", 9: "wɛ"
}

TENS = {
    10: "piiga", 20: "pisi", 30: "pis-tã", 40: "pis-naase", 50: "pis-nu",
    60: "pis-yoobe", 70: "pis-yopoe", 80: "pis-nii", 90: "pis-wɛ"
}

def convert_to_text(n: int, is_money: bool = False) -> str:
    """Converts an integer to its Mooré text representation."""
    if n < 0:
        return "- " + convert_to_text(-n, is_money=is_money)
    if is_money:
        # Millions and billions are absolute CFA values (no ×5 scaling).
        # Amounts below 1 million use the 5-wakir system.
        big = (n // 1_000_000) * 1_000_000   # absolute million/billion part
        small = n % 1_000_000                 # rest, expressed in wakirs (÷5)
        small_wakirs, small_francs = small // 5, small % 5

        if big == 0 and small == 0:
            return _convert_internal(0)

        parts = []
        if big > 0:
            parts.append(_convert_internal(big))
        if small_wakirs > 0:
            parts.append(_convert_internal(small_wakirs))
        elif small_francs > 0 and big > 0:
            # no wakirs, only loose francs after a big amount
            pass

        base = " la ".join(parts) if parts else ""

        if small_francs > 0:
            franc_str = "tãmb a " + _convert_internal(small_francs)
            if base:
                return base + " la " + franc_str
            return franc_str
        return base if base else _convert_internal(0)

    return _convert_internal(n)

def _convert_internal(n: int, use_short: bool = False) -> str:
    if n == 0: return "zaalem"
    if n <= 10:
        if n == 10: return "piiga"
        if n == 1 and not use_short: return "ye"
        return UNITS_LONG[n] if not use_short else UNITS_SHORT[n]
    
    if n < 20:
        unit = n - 10
        return f"piig la a {UNITS_SHORT[unit]}"
    
    if n < 100:
        ten, unit = (n // 10) * 10, n % 10
        if unit == 0: return TENS[ten]
        return f"{TENS[ten]} la a {UNITS_SHORT[unit]}"
            
    if n < 1000:
        h, rem = n // 100, n % 100
        if h == 1:
            prefix = "koabg" if rem > 0 else "koabga"
        elif h == 2:
            prefix = "kobsi"
        else:
            prefix = f"kobs-{UNITS_SHORT[h]}"
        if rem == 0: return prefix
        sep = " la a " if rem < 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000:
        return _convert_scaled(n, 1000, "tus")
    if n < 1_000_000_000:
        return _convert_scaled(n, 1_000_000, "milyõ")
    if n < 1_000_000_000_000:
        return _convert_scaled(n, 1_000_000_000, "milyar")
    return str(n)

def _convert_scaled(n: int, scale: int, word: str) -> str:
    """Each digit of the multiplier gets its own scale word:
    46000 = 40000 + 6000 -> "tus pis-naase la tus a yoobe"."""
    k, rem = n // scale, n % scale
    digits = [d for d in (k // 100 * 100, k // 10 % 10 * 10, k % 10) if d]
    parts = []
    for i, d in enumerate(digits):
        followed = i < len(digits) - 1 or rem > 0
        if word == "tus":
            if d == 1:
                parts.append("tusr" if followed else "tusri")
            elif d < 10:
                parts.append(f"tus a {UNITS_SHORT[d]}")
            else:
                parts.append(f"tus {_convert_internal(d)}")
        elif d < 10:
            parts.append(f"{word} a {_convert_internal(d, use_short=followed)}")
        else:
            parts.append(f"{word} {_convert_internal(d)}")
    text = " la ".join(parts)
    if rem == 0: return text
    sep = " la a " if rem < 10 else " la "
    return f"{text}{sep}{_convert_internal(rem, use_short=True)}"

REVERSE_UNITS = {v.lower(): k for k, v in UNITS_LONG.items()}
REVERSE_UNITS_SHORT = {v.lower(): k for k, v in UNITS_SHORT.items()}
REVERSE_TENS = {v.lower(): k for k, v in TENS.items()}

def _get_val(w: str) -> int:
    w = w.lower().strip()
    if w in REVERSE_UNITS: return REVERSE_UNITS[w]
    if w in REVERSE_UNITS_SHORT: return REVERSE_UNITS_SHORT[w]
    if w in REVERSE_TENS: return REVERSE_TENS[w]
    if w in ["piig", "piiga"]: return 10
    if w in ["koabg", "koabga"]: return 100
    if w == "kobsi": return 200
    if w.startswith("kobs-") and w[5:] in REVERSE_UNITS_SHORT:
        return REVERSE_UNITS_SHORT[w[5:]] * 100
    if w in ["tusr", "tusri"]: return 1000
    if w == "zaalem": return 0
    raise ValueError(f"Unknown Mooré number word: {w!r}")

SCALES = {"tus": 1000, "milyõ": 1_000_000, "milyar": 1_000_000_000}

def text_to_num(text: str, is_money: bool = False) -> int:
    text = text.lower().strip()
    if text.startswith("-"):
        return -text_to_num(text[1:], is_money=is_money)
    if is_money:
        # Split off any loose francs first
        if "tãmb a" in text:
            if "la tãmb a" in text:
                main_part, franc_part = text.split("la tãmb a", 1)
            else:
                main_part, franc_part = text.split("tãmb a", 1)
            francs = text_to_num(franc_part.strip(), is_money=False)
        else:
            main_part = text
            francs = 0

        # Now parse the main part with hybrid scaling:
        # tokens that resolve to >= 1,000,000 are absolute; rest is ×5 (wakirs)
        main_part = main_part.strip()
        main_val = text_to_num(main_part, is_money=False) if main_part else 0
        if main_val >= 1_000_000:
            big = (main_val // 1_000_000) * 1_000_000
            small_wakirs = main_val % 1_000_000
            return big + small_wakirs * 5 + francs
        else:
            return main_val * 5 + francs

    # A number is a sum of terms; a scale word multiplies exactly one following
    # term (one digit), so "tus pis-naase la a yoobe" is 40000 + 6.
    words = [w for w in text.split() if w not in ("la", "a")]
    if not words:
        raise ValueError(f"No Mooré number found in {text!r}")
    total = 0
    i = 0
    while i < len(words):
        w = words[i]
        if w in SCALES:
            if i + 1 < len(words) and words[i + 1] not in SCALES and words[i + 1] not in ("tusr", "tusri"):
                i += 1
                total += _get_val(words[i]) * SCALES[w]
            else:
                total += SCALES[w]
        else:
            total += _get_val(w)
        i += 1
    return total
