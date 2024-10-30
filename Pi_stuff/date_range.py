# Date range getter
# gpt made it so dont be mad
from datetime import datetime, timedelta
import re


def get_time_range(duration_str):
    # Parse the input for number and time unit (minutes, hours, days)
    match = re.match(r"(\d+)([mhd])", duration_str)
    if not match:
        raise ValueError(
            "Invalid input. Use the format 'Xm', 'Xh', or 'Xd', where X is a number."
        )

    amount = int(match.group(1))
    unit = match.group(2)

    # Determine the timedelta based on the unit
    if unit == "m":  # minutes
        delta = timedelta(minutes=amount)
    elif unit == "h":  # hours
        delta = timedelta(hours=amount)
    elif unit == "d":  # days
        delta = timedelta(days=amount)
    elif unit == "w":  # weeks
        delta = timedelta(weeks=amount)

    # Current time (end time)
    end_time = datetime.now()

    # Calculate the start time
    start_time = end_time - delta

    # Format the output as "YYYY-MM-DD H:M to YYYY-MM-DD H:M"
    return f"{start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')}"
