import pytest

from calculator import add, divide, multiply, read_number, subtract


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_subtract_numbers():
    assert subtract(10, 4) == 6


def test_multiply_numbers():
    assert multiply(6, 7) == 42


def test_divide_numbers():
    assert divide(12, 3) == 4


def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(1, 0)


def test_decimal_calculations():
    assert add(1.25, 2.5) == pytest.approx(3.75)
    assert subtract(5.5, 2.25) == pytest.approx(3.25)
    assert multiply(1.5, 2.5) == pytest.approx(3.75)
    assert divide(7.5, 2.5) == pytest.approx(3.0)


def test_read_number_retries_after_invalid_input(monkeypatch, capsys):
    inputs = iter(("not-a-number", "3.5"))
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))

    assert read_number("Enter a number: ") == 3.5
    assert "Invalid number." in capsys.readouterr().out
