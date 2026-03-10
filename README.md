# moore_num

A Python library for converting numbers to Mooré (Mossi) language text and vice versa.

🚀 **Try the interactive demo:** [num2text-playground.vercel.app](https://num2text-playground.vercel.app/)

## Features

- **Number to Mooré Text**: Convert integers to their textual representation in Mooré.
- **Mooré Text to Number**: Parse Mooré number phrases back into integers.
- **Money Mode**: Special scaling factor (x5) for currency calculations common in Burkina Faso.
- **Support for Large Numbers**: Handles units, tens, hundreds, thousands, millions, and billions.

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
# Output: "Koabga la pisi la a nu"

# Money mode (5 CFA = 1 unit in common counting)
print(convert_to_text(500, is_money=True))
# Output: "Koabga"
```

### Reverse Conversion (Text to Number)

```python
from moore_num import text_to_num

# Standard reverse
print(text_to_num("Piig la a yii"))
# Output: 12

# Money mode reverse
print(text_to_num("Koabga", is_money=True))
# Output: 500
```

### Command Line Interface

```bash
# Forward
num2moore 125

# Reverse
num2moore "Piig la a yii" --reverse

# Money mode
num2moore 500 --money
```

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
