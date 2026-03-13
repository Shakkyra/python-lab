import pytest
from abc import ABC, abstractmethod

# Phase 1 — Classes
# Run: pytest src/python_lab/phases/phase_1/exercises/test_04_classes.py -v

class BankAccount:
    """Bank account with overdraft protection and transaction history.

    - deposit(amount): raises ValueError if amount <= 0
    - withdraw(amount): raises ValueError if amount <= 0 or insufficient funds
    - balance: read-only property
    - transactions: list of {"type": "deposit"|"withdraw", "amount": float}
    - __str__: "BankAccount(owner=Ada, balance=1000.00)"
    """
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self._balance = balance
        self._transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
        self._transactions.append({"type": "deposit", "amount": amount})

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._transactions.append({"type": "withdraw", "amount": amount})

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def transactions(self) -> list:
        return list(self._transactions)

    def __str__(self) -> str:
        return f"BankAccount(owner={self.owner}, balance={self._balance:.2f})"


class BoundedList:
    """List with a maximum capacity.
    Raises OverflowError when appending beyond capacity.
    Supports: len(), indexing, iteration, `in` operator, str().

    __str__: "BoundedList(capacity=3, items=[1, 2])"
    """
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._items = []

    def append(self, item) -> None:
        if len(self._items) >= self._capacity:
            raise OverflowError(f"BoundedList is full (capacity={self._capacity})")
        self._items.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item) -> bool:
        return item in self._items

    def __str__(self) -> str:
        return f"BoundedList(capacity={self._capacity}, items={self._items})"


class Shape(ABC):
    """Abstract base: all shapes must implement area(), perimeter(), describe()."""

    @abstractmethod
    def area(self) -> float: pass

    @abstractmethod
    def perimeter(self) -> float: pass

    @abstractmethod
    def describe(self) -> str: pass


class Circle(Shape):
    """Circle(5).area() -> ~78.54   |   describe() -> "Circle(radius=5)" """
    PI = 3.14159

    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return self.PI * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * self.PI * self.radius

    def describe(self) -> str: 
        return f"Circle(radius={self.radius})"

class Rectangle(Shape):
    """Rectangle(4, 6).area() -> 24   |   describe() -> "Rectangle(width=4, height=6)" """
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def describe(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

def total_area(shapes: list) -> float:
    """Sum of areas of all shapes.
    Works for ANY Shape — doesn't know or care about the concrete type.
    This is polymorphism. This is why design patterns work.

    total_area([Circle(1), Rectangle(2, 3)]) -> ~9.14
    total_area([])                           -> 0
    """
    if not shapes:
        return 0
    
    return sum(shape.area() for shape in shapes)
    
# ── tests ─────────────────────────────────────────────────────────

class TestBankAccount:
    @pytest.fixture
    def account(self):
        return BankAccount(owner="Ada", balance=1000)

    def test_initial_balance(self, account):
        assert account.balance == 1000

    def test_deposit(self, account):
        account.deposit(500)
        assert account.balance == 1500

    def test_withdraw(self, account):
        account.withdraw(200)
        assert account.balance == 800

    def test_insufficient_funds(self, account):
        with pytest.raises(ValueError, match="insufficient funds"):
            account.withdraw(9999)

    def test_invalid_deposit(self, account):
        with pytest.raises(ValueError):
            account.deposit(-100)
        with pytest.raises(ValueError):
            account.deposit(0)

    def test_transaction_history(self, account):
        account.deposit(100)
        account.withdraw(50)
        assert len(account.transactions) == 2
        assert account.transactions[0] == {"type": "deposit", "amount": 100}
        assert account.transactions[1] == {"type": "withdraw", "amount": 50}

    def test_balance_read_only(self, account):
        with pytest.raises(AttributeError):
            account.balance = 9999

    def test_str(self, account):
        assert str(account) == "BankAccount(owner=Ada, balance=1000.00)"


class TestBoundedList:
    @pytest.fixture
    def bl(self):
        b = BoundedList(capacity=3)
        b.append(10)
        b.append(20)
        return b

    def test_len(self, bl):
        assert len(bl) == 2

    def test_getitem(self, bl):
        assert bl[0] == 10

    def test_iter(self, bl):
        assert list(bl) == [10, 20]

    def test_contains(self, bl):
        assert 10 in bl
        assert 99 not in bl

    def test_overflow(self, bl):
        bl.append(30)
        with pytest.raises(OverflowError):
            bl.append(40)

    def test_str(self):
        bl = BoundedList(capacity=3)
        bl.append(1); bl.append(2)
        assert str(bl) == "BoundedList(capacity=3, items=[1, 2])"


class TestShapes:
    def test_circle_area(self):
        assert Circle(5).area() == pytest.approx(78.53, rel=1e-2)

    def test_circle_perimeter(self):
        assert Circle(5).perimeter() == pytest.approx(31.41, rel=1e-2)

    def test_circle_describe(self):
        assert Circle(5).describe() == "Circle(radius=5)"

    def test_rectangle_area(self):
        assert Rectangle(4, 6).area() == 24

    def test_rectangle_perimeter(self):
        assert Rectangle(4, 6).perimeter() == 20

    def test_rectangle_describe(self):
        assert Rectangle(4, 6).describe() == "Rectangle(width=4, height=6)"

    def test_shape_is_abstract(self):
        with pytest.raises(TypeError):
            Shape()

    def test_total_area_mixed(self):
        shapes = [Circle(1), Rectangle(2, 3)]
        assert total_area(shapes) == pytest.approx(3.14159 + 6, rel=1e-2)

    def test_total_area_empty(self):
        assert total_area([]) == 0

    def test_polymorphism(self):
        shapes = [Circle(2), Rectangle(3, 4), Circle(1)]
        assert total_area(shapes) > 0
