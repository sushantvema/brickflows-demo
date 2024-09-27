from datetime import datetime
from pytz import timezone

def dummy():
    # Get current datetime in UTC
    utc_datetime = datetime.now(timezone('UTC'))

    # Convert UTC datetime to PST
    pst_datetime = utc_datetime.astimezone(timezone('US/Pacific'))

    # Format PST datetime as 'YYYYMMDDTHHMMSS'
    formatted_datetime = pst_datetime.strftime("%Y%m%dT%H%M%S")

    logger.info(f"Current run timestamp: {formatted_datetime}")
