
def future_value(principal: float, rate: float, years: int) -> float:
    """Calculate portfolio growth with annual compounding."""
    return principal * (1 + rate) ** years
