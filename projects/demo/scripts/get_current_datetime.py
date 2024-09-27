def main():
    from datetime import datetime
    from pytz import timezone

    # Get current datetime in UTC
    utc_datetime = datetime.now(timezone('UTC'))

    # Convert UTC datetime to PST
    pst_datetime = utc_datetime.astimezone(timezone('US/Pacific'))

    # Format PST datetime as 'YYYYMMDDTHHMMSS'
    formatted_datetime = pst_datetime.strftime("%Y%m%dT%H%M%S")

    return formatted_datetime

if __name__ == "__main__":
   main() 
