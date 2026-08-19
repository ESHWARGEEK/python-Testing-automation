import re

def is_valid_email(email: str) -> bool:
    """Validates email format using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def calculate_discount(price: float, percent: float) -> float:
    """Returns discounted price. Raises ValueError if percent is not between 0 and 100."""
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    return price - (price * (percent / 100.0))

def validate_age(age: int) -> bool:
    """Returns True if age is between 0 and 120 inclusive."""
    return 0 <= age <= 120
