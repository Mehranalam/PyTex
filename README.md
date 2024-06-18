### PyTex

Implementing a typesetting system for mathematical formulas using TeX algorithms and fonts inside Python without relying on an external TeX installation is a complex task

<img src="/app/formula.png" alt="output PyTex">

- [ ] Compiler design part is completed, which you can see from the `/compiler` folder.

```python
token_specification = [
        ('NUMBER',    r'\d+(\.\d*)?'),    # Integer or decimal number
        ('IDENT',     r'[A-Za-z]'),       # Identifiers (variables)
        ('OP',        r'[+\-*/^]'),       # Arithmetic operators
        ('FRAC',      r'\\frac'),         # Fraction
        ('LBRACE',    r'\{'),             # Left brace
        ('RBRACE',    r'\}'),             # Right brace
        ('WS',        r'\s+'),            # Whitespace
        ('MISMATCH',  r'.'),              # Any other character
    ]
```