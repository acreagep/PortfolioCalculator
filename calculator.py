

def future_value(principal: float, rate: float, years: int) -> float:
    """Calculate portfolio growth with annual compounding."""
    return principal * (1 + rate) ** years


def project_growth(principal: float, rate: float, years: int) -> list[float]:
    """Return portfolio balances from year 0 through the final year."""
    return [
        future_value(principal, rate, year)
        for year in range(years + 1)
    ]
