import math

# FUNCTION FOR TRUNCATING VALUES
def smart_truncate_number(n):
    if n < 1000:
        return str(n)

    # Handle Millions (M)
    if n >= 1_000_000:
        base = n / 1_000_000  # Get the number in millions
        truncated = math.floor(base * 10) / 10  # Truncate to 1 decimal
        return f"{int(truncated) if truncated.is_integer() else truncated}M"

    # Handle Thousands (k)
    elif n >= 1000:
        base = n / 1000  # Get the number in thousands
        truncated = math.floor(base * 10) / 10  # Truncate to 1 decimal
        return f"{int(truncated) if truncated.is_integer() else truncated}k"