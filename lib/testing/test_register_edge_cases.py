import pytest

from cash_register import CashRegister


@pytest.mark.parametrize('value', [-1, 101, 20.5, '20', None, True])
def test_invalid_discount_keeps_previous_value(value, capsys):
    register = CashRegister(20)
    register.discount = value
    assert register.discount == 20
    assert capsys.readouterr().out == 'Not valid discount\n'


def test_invalid_initial_discount_defaults_to_zero(capsys):
    register = CashRegister('invalid')
    assert register.discount == 0
    assert capsys.readouterr().out == 'Not valid discount\n'


@pytest.mark.parametrize('discount', [0, 100])
def test_discount_boundaries(discount, capsys):
    register = CashRegister(discount)
    register.add_item('book', 10)
    register.apply_discount()
    assert register.total == 10 * (1 - discount / 100)


def test_registers_have_separate_lists():
    first = CashRegister()
    second = CashRegister()
    first.add_item('book', 5, 2)
    assert first.previous_transactions == [
        {'item': 'book', 'price': 5, 'quantity': 2}
    ]
    assert second.items == []
    assert second.previous_transactions == []
    assert second.total == 0


def test_void_removes_only_last_batch():
    register = CashRegister()
    register.add_item('book', 5)
    register.add_item('pen', 2)
    register.add_item('book', 4, 2)
    register.void_last_transaction()
    assert register.total == 7
    assert register.items == ['book', 'pen']
    assert len(register.previous_transactions) == 2
    register.void_last_transaction()
    register.void_last_transaction()
    assert register.total == 0
    assert register.items == []
    assert register.previous_transactions == []


def test_empty_register_messages(capsys):
    register = CashRegister(20)
    register.apply_discount()
    register.void_last_transaction()
    assert capsys.readouterr().out == (
        'There is no discount to apply.\n'
        'There is no transaction to void.\n'
    )
    assert register.total == 0


def test_void_after_discount_and_new_purchase():
    register = CashRegister(20)
    register.add_item('book', 10)
    register.add_item('pen', 2, 3)
    register.apply_discount()
    assert register.total == pytest.approx(12.8)
    assert register.items == ['book', 'pen', 'pen', 'pen']
    assert len(register.previous_transactions) == 2
    register.add_item('ruler', 3)
    register.void_last_transaction()
    assert register.total == pytest.approx(12.8)
    register.void_last_transaction()
    assert register.total == pytest.approx(8)
    assert register.items == ['book']
    register.void_last_transaction()
    assert register.total == 0


def test_fractional_discount_message(capsys):
    register = CashRegister(15)
    register.add_item('book', 9.99)
    register.apply_discount()
    assert register.total == pytest.approx(8.4915)
    assert capsys.readouterr().out == (
        'After the discount, the total comes to $8.49.\n'
    )
