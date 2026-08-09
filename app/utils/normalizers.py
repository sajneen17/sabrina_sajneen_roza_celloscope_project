import re
import math

def normalize_value(value_str: str) -> str:
    """
    Normalizes values like 12.5, <0.5, 1.2 x 10^3, 0.8 - 1.2.
    Returns a canonical numeric string (e.g., '1200.0') or preserves verbatim if unparseable.
    """
    value_str = value_str.strip()

    # Handle scientific notation: 1.2 x 10^3 -> 1200.0
    sci_pattern = re.compile(r'([\d.]+)\s*[xX]\s*10\^?\s*([+-]?\d+)')
    match = sci_pattern.search(value_str)
    if match:
        try:
            base = float(match.group(1))
            exp = float(match.group(2))
            return f"{base * (10 ** exp):.4f}".rstrip('0').rstrip('.')
        except:
            return value_str

    # Handle ranges: 0.8 - 1.2 -> return the first value
    if ' - ' in value_str or '\u2013' in value_str:
        parts = re.split(r'\s*[\u2013-]\s*', value_str)
        if len(parts) > 1:
            try:
                return normalize_value(parts[0])
            except:
                return value_str

    # Handle < or > prefix
    if value_str.startswith('<') or value_str.startswith('>'):
        num_part = value_str[1:].strip()
        try:
            val = float(num_part)
            return value_str  # keep '<0.5' as is
        except:
            return value_str

    # Try simple float
    try:
        val = float(value_str)
        if val.is_integer():
            return str(int(val))
        else:
            return f"{val:.4f}".rstrip('0').rstrip('.')
    except ValueError:
        return value_str  # preserve verbatim

def normalize_unit(unit_str: str) -> str:
    """
    Normalizes units: mg/dL, gm/dL -> g/dL, mmol/L, 10^3/uL, etc.
    """
    unit_str = unit_str.strip()
    unit_str = unit_str.replace('gm/dL', 'g/dL')
    unit_str = unit_str.replace('gm/dl', 'g/dL')
    return unit_str

def extract_meta(lines: list) -> dict:
    """
    Dummy meta extractor. In production, use regex to find Name:, Age:, etc.
    """
    meta = {
        "patient_name": "John Doe",
        "age": "45",
        "sex": "M",
        "report_date": "2023-01-01",
        "lab_name": "City Lab",
        "reference_no": "REF123"
    }
    return meta
