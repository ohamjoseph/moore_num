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
    if is_money:
        n = n // 5
    if n < 0:
        return "Nindre " + _convert_internal(abs(n))
    return _convert_internal(n)

def _convert_internal(n: int, use_short: bool = False) -> str:
    if n == 0: return "Zaalem"
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
        t, rem = n // 1000, n % 1000
        if t == 1:
            prefix = "tusr" if rem > 0 else "tusri"
        elif t < 10:
            prefix = f"tus a {UNITS_SHORT[t]}"
        else:
            prefix = f"tus {_convert_internal(t)}"
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000_000:
        m, rem = n // 1_000_000, n % 1_000_000
        if m == 1:
            prefix = "milyõ a ye"
        else:
            prefix = f"milyõ {_convert_internal(m)}"
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000_000_000:
        b, rem = n // 1_000_000_000, n % 1_000_000_000
        if b == 1:
            prefix = "milyar ye"
        else:
            prefix = f"milyar {_convert_internal(b)}"
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"
    return str(n)

REVERSE_UNITS = {v.lower(): k for k, v in UNITS_LONG.items()}
REVERSE_UNITS_SHORT = {v.lower(): k for k, v in UNITS_SHORT.items()}
REVERSE_TENS = {v.lower(): k for k, v in TENS.items()}

def _get_val(w: str) -> int:
    w = w.lower().strip()
    if not w: return 0
    if w in REVERSE_UNITS: return REVERSE_UNITS[w]
    if w in REVERSE_UNITS_SHORT: return REVERSE_UNITS_SHORT[w]
    if w in REVERSE_TENS: return REVERSE_TENS[w]
    if w in ["piig", "piiga"]: return 10
    if w in ["koabg", "koabga"]: return 100
    if w == "kobsi": return 200
    if w.startswith("kobs-"):
        unit = w.split("-", 1)[1]
        return REVERSE_UNITS_SHORT.get(unit, 1) * 100
    if w.startswith("pis-"):
        unit = w.split("-", 1)[1]
        return REVERSE_UNITS_SHORT.get(unit, 1) * 10
    if w == "tus": return 1000
    if w in ["tusr", "tusri"]: return 1000
    if w == "milyõ": return 1000000
    if w == "milyar": return 1000000000
    if w == "zaalem": return 0
    return 0

def text_to_num(text: str, is_money: bool = False) -> int:
    raw_words = text.lower().strip().split()
    tokens = []
    i = 0
    while i < len(raw_words):
        w = raw_words[i]
        if w == "la": tokens.append("PLUS")
        elif w == "a": i += 1; continue
        elif w == "ye": tokens.append(1)
        elif w == "milyõ" and i+2 < len(raw_words) and raw_words[i+1] == "a" and raw_words[i+2] == "ye":
            tokens.append(1000000); i += 3; continue
        elif w == "milyar" and i + 1 < len(raw_words) and raw_words[i+1] == "ye":
            tokens.append(1000000000); i += 2; continue
        else:
            v = _get_val(w)
            if v > 0:
                if w in ["tusri", "tusr", "koabga", "kobsi"]:
                    tokens.append(v); tokens.append("PLUS")
                else: tokens.append(v)
            elif w == "zaalem": tokens.append(0)
        i += 1
    
    def solve(ts):
        if not ts: return 0
        max_s = -1; max_idx = -1
        for i, v in enumerate(ts):
            if isinstance(v, int) and v >= 100 and v > max_s:
                max_s = v; max_idx = i
        
        if max_idx == -1:
            total = 0; curr = 0
            for v in ts:
                if v == "PLUS": continue
                if v < curr or curr == 0: curr += v
                else: total += curr; curr = v
            return total + curr
        
        left = ts[:max_idx]
        right = ts[max_idx+1:]
        
        if left:
            while left and left[-1] == "PLUS": left.pop()
            mult = solve(left)
            return (mult if mult > 0 else 1) * max_s + solve(right)
        else:
            if not right: return max_s
            if right[0] == "PLUS": return max_s + solve(right[1:])
            
            mult_ts = []; rem_ts = []; last_v = 99999999999
            for j, v in enumerate(right):
                if v == "PLUS":
                    if j+1 < len(right) and isinstance(right[j+1], int):
                        nv = right[j+1]
                        if nv >= last_v: rem_ts = right[j+1:]; break
                        if nv < 10 and last_v < 10: rem_ts = right[j+1:]; break
                    mult_ts.append(v)
                elif isinstance(v, int):
                    if v < max_s: mult_ts.append(v); last_v = v
                    else: rem_ts = right[j:]; break
            mult = solve(mult_ts)
            return (mult if mult > 0 else 1) * max_s + solve(rem_ts)

    res = solve(tokens)
    return res * 5 if is_money else res
