import pytest
from app.utils.normalizers import normalize_value

def test_normalize_simple():
    assert normalize_value("12.5") == "12.5"

def test_normalize_less_than():
    assert normalize_value("<0.5") == "<0.5"

def test_normalize_scientific():
    assert normalize_value("1.2 x 10^3") == "1200.0"

def test_normalize_range():
    assert normalize_value("0.8 - 1.2") == "0.8"
