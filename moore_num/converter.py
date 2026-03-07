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
        #if unit in [2, 3]: return f"piig la {UNITS_SHORT[unit]}"
        return f"piig la a {UNITS_SHORT[unit]}"
    
    if n < 100:
        ten, unit = (n // 10) * 10, n % 10
        if unit == 0: return TENS[ten]
        return f"{TENS[ten]} la a {UNITS_SHORT[unit]}"
            
    if n < 1000:
        h, rem = n // 100, n % 100
        if h == 1:
            prefix = "koabg" if 0 < rem < 30 else "koabga"
        elif h == 2:
            prefix = "kobsi"
        else:
            prefix = f"kobs-{UNITS_SHORT[h]}"
        if rem == 0: return prefix
        # Rule: use 'la a' for units/10, 'la' otherwise
        sep = " la a " if rem < 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000:
        t, rem = n // 1000, n % 1000
        if t == 1:
            prefix = "tusri" #if rem == 0 else "tus"
        elif t < 10:
            prefix = f"tus a {UNITS_SHORT[t]}"
        else:
            # 10000 -> tus piiga
            if t == 10 and rem > 0: prefix = "tus piig"
            else: prefix = f"tus {_convert_internal(t)}" 
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000_000:
        m, rem = n // 1_000_000, n % 1_000_000
        # milyõ a ye or [n] milyõ
        prefix = "milyõ a ye" if m == 1 else f"{_convert_internal(m)} milyõ"
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"

    if n < 1_000_000_000_000:
        b, rem = n // 1_000_000_000, n % 1_000_000_000
        prefix = "milyar ye" if b == 1 else f"milyar {_convert_internal(b).lower()}"
        if rem == 0: return prefix
        sep = " la a " if rem <= 10 else " la "
        return f"{prefix}{sep}{_convert_internal(rem, use_short=True)}"
    return str(n)

REVERSE_UNITS = {v.lower(): k for k, v in UNITS_LONG.items()}
REVERSE_UNITS_SHORT = {v.lower(): k for k, v in UNITS_SHORT.items()}
REVERSE_TENS = {v.lower(): k for k, v in TENS.items()}

def text_to_num(text: str, is_money: bool = False) -> int:
    def _strip_conj(s):
        s = s.strip()
        if s.startswith("la a "): return s[5:].strip()
        if s.startswith("la "): return s[3:].strip()
        return s

    def _parse(s):
        s = s.strip().lower()
        if not s or s == "zaalem": return 0
        if s in REVERSE_UNITS: return REVERSE_UNITS[s]
        if s in REVERSE_UNITS_SHORT: return REVERSE_UNITS_SHORT[s]
        if s == "piig": return 10
        if s == "piiga": return 10
        
        # Priority: Major units
        if "milyar" in s:
            p = s.split("milyar", 1)
            count = _parse(p[0]) if p[0].strip() else 1
            return count * 1_000_000_000 + _parse(_strip_conj(p[1]))
            
        if "milyõ" in s:
            if "milyõ a ye" in s:
                return 1_000_000 + _parse(_strip_conj(s.replace("milyõ a ye", "", 1)))
            p = s.split("milyõ", 1)
            count = _parse(p[0]) if p[0].strip() else 1
            return count * 1_000_000 + _parse(_strip_conj(p[1]))

        if "tus" in s:
            if "tusri" in s:
                return 1000 + _parse(_strip_conj(s.replace("tusri", "", 1)))
            if "tus a" in s:
                p = s.split("tus a", 1)
                rem_w = p[1].strip().split()
                if not rem_w: return 1000 # Should not happen
                unit = rem_w[0]
                val = REVERSE_UNITS_SHORT.get(unit, REVERSE_UNITS.get(unit, 0))
                return val * 1000 + _parse(_strip_conj(" ".join(rem_w[1:])))
            p = s.split("tus", 1)
            rem_w = p[1].strip().split()
            if not rem_w: return 1000
            if rem_w[0] in ["la", "a"]:
                return 1000 + _parse(_strip_conj(p[1]))
            else:
                count = _parse(rem_w[0])
                return count * 1000 + _parse(_strip_conj(" ".join(rem_w[1:])))

        if "kobs" in s:
            # handle kobs-yi or kobs yi
            p = s.replace("kobs-", "kobs ").split("kobs", 1)
            rem_w = p[1].strip().split()
            unit = rem_w[0]
            val = REVERSE_UNITS_SHORT.get(unit, REVERSE_UNITS.get(unit, 0))
            return val * 100 + _parse(_strip_conj(" ".join(rem_w[1:])))
        
        if "koabg" in s:
            return 100 + _parse(_strip_conj(s.replace("koabga", "").replace("koabg", "").strip()))

        # Tens and small units
        if "la a" in s:
            p = s.split("la a", 1)
            return _parse(p[0]) + _parse(p[1])
        if "la" in s:
            p = s.split("la", 1)
            return _parse(p[0]) + _parse(p[1])
            
        if s in REVERSE_TENS: return REVERSE_TENS[s]
        return 0

    val = _parse(text)
    return val * 5 if is_money else val

def _parse_small(t: str) -> int:
    t = t.strip()
    if not t: return 0
    if t in REVERSE_TENS: return REVERSE_TENS[t]
    if t in REVERSE_UNITS: return REVERSE_UNITS[t]
    if t in REVERSE_UNITS_SHORT: return REVERSE_UNITS_SHORT[t]
    if t == "piig": return 10
    return 0
