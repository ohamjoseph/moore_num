# moore_num

A Python library for converting numbers to Mooré (Mossi) language text and vice versa.

🚀 **Try the interactive demo:** [num2text-playground.vercel.app](https://num2text-playground.vercel.app/)

## Features

- **Number to Mooré Text**: Convert integers to their textual representation in Mooré.
- **Mooré Text to Number**: Parse Mooré number phrases back into integers.
- **Money Mode**: Counts amounts below one million in *wakirs* (1 wakir = 5 FCFA), as is common in Burkina Faso. Millions and billions stay absolute FCFA values, and leftover francs are read as "tãmb a ...".
- **Support for Large Numbers**: Handles units, tens, hundreds, thousands, millions, and billions (up to 999 999 999 999).
- **Negative Numbers**: Prefixed with "- " in both directions.
- **Strict Parsing**: Unknown words raise a `ValueError` instead of being silently ignored.

## Installation

```bash
pip install moore_num
```

## Usage

### Forward Conversion (Number to Text)

```python
from moore_num import convert_to_text

# Standard conversion
print(convert_to_text(125))
# Output: "koabg la pisi la a nu"

# Each digit of a thousands/millions/billions multiplier gets its own scale word
print(convert_to_text(46000))
# Output: "tus pis-naase la tus a yoobe"   (40 000 + 6 000)
print(convert_to_text(40006))
# Output: "tus pis-naase la a yoobe"       (40 000 + 6)

# Money mode (1 wakir = 5 FCFA)
print(convert_to_text(500, is_money=True))
# Output: "koabga"
print(convert_to_text(7, is_money=True))
# Output: "ye la tãmb a yiibu"             (1 wakir + 2 francs)
```

### Reverse Conversion (Text to Number)

```python
from moore_num import text_to_num

# Standard reverse
print(text_to_num("piig la a yi"))
# Output: 12

# Money mode reverse
print(text_to_num("koabga", is_money=True))
# Output: 500

# Unknown words raise an error
text_to_num("pisi la a bonjour")
# ValueError: Unknown Mooré number word: 'bonjour'
```

### Command Line Interface

```bash
# Forward
num2moore 125

# Reverse
num2moore "piig la a yi" --reverse

# Money mode
num2moore 500 --money
```

## Breaking changes in 0.2.2 (from 0.1.x)

- **Thousands, millions and billions**: each digit of the multiplier now gets its own scale word, so every number has a single, unambiguous text. For example, 46 000 is now `tus pis-naase la tus a yoobe` and 145 500 is `tus koabga la tus pis-naase la tus a nu la kobs-nu`. Text written in the old form (`tus koabg la pis-naase la a nu`) is now read differently.
- **`text_to_num`** raises `ValueError` on unknown words or empty input, instead of returning 0.

## License

MIT

## Citation

If you use this software in your research, please cite it using the following BibTeX format:

```bibtex
@software{moore_num,
  author = {Ouily, Hamed Joseph},
  title = {moore\_num: A Python library for converting numbers to Mooré text},
  url = {https://github.com/ohamjoseph/moore_num},
  year = {2026}
}
```
