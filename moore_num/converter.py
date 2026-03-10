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

def _get_token_value(w: str) -> int:
    w = w.lower()
    if w in REVERSE_UNITS: return REVERSE_UNITS[w]
    if w in REVERSE_UNITS_SHORT: return REVERSE_UNITS_SHORT[w]
    if w in REVERSE_TENS: return REVERSE_TENS[w]
    if w == "piig": return 10
    if w in ["koabg", "koabga"]: return 100
    if w == "kobsi": return 200
    if w.startswith("kobs-"):
        unit = w.split("-", 1)[1]
        val = REVERSE_UNITS_SHORT.get(unit, REVERSE_UNITS.get(unit, 1))
        return val * 100
    return 0

def _extract_numbers(s: str) -> list[int]:
    words = [w for w in s.split() if w not in ["la", "a"]]
    vals = []
    for w in words:
        v = _get_token_value(w)
        if v > 0: vals.append(v)
    if not vals: return []
    numbers = []
    current_num = vals[0]
    last_val = vals[0]
    for v in vals[1:]:
        if v < last_val: current_num += v
        else:
            numbers.append(current_num)
            current_num = v
        last_val = v
    numbers.append(current_num)
    return numbers

def text_to_num(text: str, is_money: bool = False) -> int:
    def _strip_conj(s):
        s = s.strip()
        if s.startswith("la a "): return s[5:].strip()
        if s.startswith("la "): return s[3:].strip()
        return s

    def _parse(s):
        s = s.strip().lower()
        if not s or s == "zaalem": return 0
        
        if "milyar" in s:
            if "milyar ye" in s:
                p = s.split("milyar ye", 1)
                return 1_000_000_000 + _parse(_strip_conj(p[1]))
            p = s.split("milyar", 1)
            rem_str = p[1].strip()
            if not rem_str: return 1_000_000_000
            if rem_str.startswith("la "): return 1_000_000_000 + _parse(_strip_conj(rem_str))
            
            idx1 = rem_str.find("milyõ")
            idx2 = rem_str.find("tus")
            if idx1 == -1: idx1 = len(rem_str)
            if idx2 == -1: idx2 = len(rem_str)
            split_idx = min(idx1, idx2)
            
            m_part = rem_str[:split_idx]
            rest_str = rem_str[split_idx:]
            
            nums = _extract_numbers(m_part)
            mult = nums[0] if nums else 1
            rem_val = sum(nums[1:]) if len(nums)>1 else 0
            return mult * 1_000_000_000 + rem_val + _parse(_strip_conj(rest_str))
            
        if "milyõ" in s:
            if "milyõ a ye" in s:
                p = s.split("milyõ a ye", 1)
                return 1_000_000 + _parse(_strip_conj(p[1]))
            p = s.split("milyõ", 1)
            count = _parse(p[0]) if p[0].strip() else 1
            return count * 1_000_000 + _parse(_strip_conj(p[1]))

        if "tus" in s:
            if "tusri" in s:
                p = s.split("tusri", 1)
                return 1000 + _parse(_strip_conj(p[1]))
            if "tus a" in s:
                p = s.split("tus a", 1)
                nums = _extract_numbers(_strip_conj(p[1]))
                mult = nums[0] if nums else 1
                return mult * 1000 + sum(nums[1:])
            p = s.split("tus", 1)
            rem_str = p[1].strip()
            if not rem_str: return 1000
            if rem_str.startswith("la "):
                nums = _extract_numbers(_strip_conj(rem_str))
                return 1000 + sum(nums)
            else:
                nums = _extract_numbers(rem_str)
                mult = nums[0] if nums else 1
                return mult * 1000 + sum(nums[1:])

        if "kobsi" in s:
            p = s.split("kobsi", 1)
            nums = _extract_numbers(_strip_conj(p[1]))
            return 200 + sum(nums)
            
        if "kobs" in s:
            p = s.replace("kobs-", "kobs ").split("kobs", 1)
            nums = _extract_numbers(_strip_conj(p[1]))
            mult = nums[0] if nums else 1
            return mult * 100 + sum(nums[1:])
            
        if "koabg" in s:
            p = s.replace("koabga", "koabg").split("koabg", 1)
            nums = _extract_numbers(_strip_conj(p[1]))
            return 100 + sum(nums)

        nums = _extract_numbers(s)
        return sum(nums)

    val = _parse(text)
    return val * 5 if is_money else val
