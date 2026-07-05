from datetime import datetime, timedelta
from typing import List, Tuple
import os

def parse_date(date_str: str) -> datetime:
    """Parse a date string in DD-MM-YYYY format to a datetime object."""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}. Please use DD-MM-YYYY (e.g., 01-01-2023)")

def read_config(config_file: str = "bno_config.txt") -> dict:
    """Read default values from the configuration file."""
    config = {
        "VISA_ISSUANCE_DATE": None,
        "FIRST_ENTRY_DATE": None,
        "TRAVEL_PERIODS": []
    }
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            value = value.strip()
            
            if key == "VISA_ISSUANCE_DATE":
                config[key] = parse_date(value)
            elif key == "FIRST_ENTRY_DATE":
                config[key] = parse_date(value)
            elif key == "TRAVEL_PERIODS" and value:
                # Split space-separated travel periods
                period_pairs = value.split()
                for pair in period_pairs:
                    try:
                        leave_date_str, return_date_str = pair.split(',')
                        leave_date = parse_date(leave_date_str)
                        return_date = parse_date(return_date_str)
                        if leave_date < return_date:
                            config["TRAVEL_PERIODS"].append((leave_date, return_date))
                        else:
                            print(f"Warning: Invalid travel period in config: {leave_date_str} to {return_date_str}. Ignored.")
                    except ValueError as e:
                        print(f"Warning: Error parsing travel period '{pair}': {e}. Ignored.")
    
    return config

def calculate_ilr_absences(travel_periods: List[Tuple[datetime, datetime]], start_date: datetime, end_date: datetime) -> Tuple[int, List[Tuple[datetime, datetime, int]]]:
    """
    Calculate total days spent outside the UK in any 365-day period for ILR.
    Returns the maximum days absent and a list of periods exceeding 180 days.
    """
    max_days_absent = 0
    exceeding_periods = []

    current_date = start_date
    while current_date <= end_date - timedelta(days=365):
        period_end = current_date + timedelta(days=365)
        days_absent = 0

        for leave_date, return_date in travel_periods:
            period_leave = max(leave_date, current_date)
            period_return = min(return_date, period_end)
            if period_leave < period_return:
                days_absent += (period_return - period_leave).days

        if days_absent > max_days_absent:
            max_days_absent = days_absent
        if days_absent > 180:
            exceeding_periods.append((current_date, period_end, days_absent))

        current_date += timedelta(days=1)

    return max_days_absent, exceeding_periods

def calculate_citizenship_absences(travel_periods: List[Tuple[datetime, datetime]], citizenship_app_date: datetime) -> Tuple[int, int, bool]:
    """
    Calculate absences for citizenship requirements.
    Returns total absences in 5 years, absences in last 12 months, and presence 5 years ago.
    """
    five_year_start = citizenship_app_date - timedelta(days=5*365)
    one_year_start = citizenship_app_date - timedelta(days=365)
    
    total_absences = 0
    last_year_absences = 0
    
    for leave_date, return_date in travel_periods:
        # Total absences in 5 years
        period_leave = max(leave_date, five_year_start)
        period_return = min(return_date, citizenship_app_date)
        if period_leave < period_return:
            total_absences += (period_return - period_leave).days
        
        # Absences in last 12 months
        period_leave = max(leave_date, one_year_start)
        period_return = min(return_date, citizenship_app_date)
        if period_leave < period_return:
            last_year_absences += (period_return - period_leave).days
    
    # Check presence 5 years before application
    was_present = not any(five_year_start >= leave_date and five_year_start < return_date for leave_date, return_date in travel_periods)
    
    return total_absences, last_year_absences, was_present

def main():
    print("BNO Visa Absence Calculator")
    print("This tool checks absences for ILR (≤180 days per 365-day period) and British citizenship.")
    print("Citizenship requirements: ≤450 days total absences in 5 years, ≤90 days in last 12 months, present in UK 5 years before application.")
    print("Dates should be in DD-MM-YYYY format (e.g., 01-01-2023).")
    
    # Read configuration
    try:
        config = read_config()
        visa_issuance = config["VISA_ISSUANCE_DATE"]
        first_entry = config["FIRST_ENTRY_DATE"]
        default_travel_periods = config["TRAVEL_PERIODS"]
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    print(f"Your visa was issued on {visa_issuance.strftime('%d-%m-%Y')}.")
    print(f"You first entered the UK on {first_entry.strftime('%d-%m-%Y')}.")
    print(f"The period from {visa_issuance.strftime('%d-%m-%Y')} to {(first_entry - timedelta(days=1)).strftime('%d-%m-%Y')} will be counted as an absence.\n")

    # Default start date for ILR (visa issuance)
    default_start_date = visa_issuance
    end_date = default_start_date + timedelta(days=5*365)

    # Override ILR start date
    print(f"Default ILR residence period start date: {default_start_date.strftime('%d-%m-%Y')} (visa issuance date)")
    # override = input(f"Would you like to use a different start date (e.g., {first_entry.strftime('%d-%m-%Y')} for first entry)? (yes/no): ").lower()
    override = 'no'
    if override == 'yes':
        while True:
            try:
                start_date_str = input("Enter the start date of your 5-year ILR residence period (DD-MM-YYYY): ")
                start_date = parse_date(start_date_str)
                end_date = start_date + timedelta(days=5*365)
                break
            except ValueError as e:
                print(e)
    else:
        start_date = default_start_date

    # Get planned citizenship application date
    print("\nFor citizenship, you plan to apply 1 year after ILR (e.g., 1 year after April 2029).\nUsing default: 22-04-2030")
    while True:
        try:
            citizenship_date_str = '22-04-2030'
            # citizenship_date_str = input("Enter your planned citizenship application date (DD-MM-YYYY, e.g., 01-04-2030): ")
            citizenship_app_date = parse_date(citizenship_date_str)
            if citizenship_app_date < end_date + timedelta(days=365):
                print("Error: Citizenship application must be at least 1 year after ILR (end of 5-year period).")
                continue
            break
        except ValueError as e:
            print(e)

    # Initialize travel periods
    travel_periods = [(visa_issuance, first_entry)] if start_date <= first_entry else []
    travel_periods.extend(default_travel_periods)

    # Collect additional travel periods
    print("\nLoaded default travel periods from configuration:")
    if default_travel_periods:
        for leave_date, return_date in default_travel_periods:
            days = (return_date - leave_date).days
            print(f" - Left UK on {leave_date.strftime('%d-%m-%Y')} to {return_date.strftime('%d-%m-%Y')}: {days} days absent")
    else:
        print(" - No default travel periods found.")
    
    print("\nEnter additional travel periods (when you left and returned to the UK).")
    print("Enter 'done' when you have entered all travel periods.")
    while True:
        leave_date_str = input("Enter date you left the UK (DD-MM-YYYY) or 'done' to finish: ")
        if leave_date_str.lower() == 'done':
            break

        return_date_str = input("Enter date you returned to the UK (DD-MM-YYYY): ")

        try:
            leave_date = parse_date(leave_date_str)
            return_date = parse_date(return_date_str)

            if leave_date >= return_date:
                print("Error: Return date must be after leave date.")
                continue
            if leave_date < start_date and leave_date < visa_issuance:
                print("Error: Travel dates cannot be before visa issuance date.")
                continue

            travel_periods.append((leave_date, return_date))
        except ValueError as e:
            print(e)

    if not travel_periods:
        print("\nNo absences recorded (only the period before first entry, if applicable).")
        days_before_entry = (first_entry - visa_issuance).days if start_date <= first_entry else 0
        print(f"Days absent before first entry ({visa_issuance.strftime('%d-%m-%Y')} to {(first_entry - timedelta(days=1)).strftime('%d-%m-%Y')}): {days_before_entry}")
        if days_before_entry > 180:
            print("WARNING: You have exceeded the 180-day absence limit for ILR due to time before first entry.")
            print("You may not meet the continuous residence requirement for ILR.")
            print("Consider consulting an immigration solicitor for advice.")
        else:
            print("You are compliant with the 180-day rule for ILR.")
        print("\nNo travel periods to assess for citizenship requirements.")
        return

    # Calculate ILR absences
    max_days_absent, exceeding_periods = calculate_ilr_absences(travel_periods, start_date, end_date)

    # Calculate citizenship absences
    total_absences, last_year_absences, was_present = calculate_citizenship_absences(travel_periods, citizenship_app_date)

    # Print ILR results
    print("\nILR Results:")
    print(f"Maximum days absent in any 365-day period: {max_days_absent}")
    if max_days_absent > 180:
        print("WARNING: You have exceeded the 180-day absence limit for ILR in the following periods:")
        for start, end, days in exceeding_periods:
            print(f" - From {start.strftime('%d-%m-%Y')} to {end.strftime('%d-%m-%Y')}: {days} days absent")
        print("You may not meet the continuous residence requirement for ILR.")
        print("Consider consulting an immigration solicitor for advice.")
    else:
        print("You are compliant with the 180-day rule for ILR continuous residence.")

    # Print citizenship results
    print("\nCitizenship Results (based on planned application date):")
    print(f"Total absences in 5 years before {citizenship_app_date.strftime('%d-%m-%Y')}: {total_absences} days")
    print(f"Absences in 12 months before {citizenship_app_date.strftime('%d-%m-%Y')}: {last_year_absences} days")
    print(f"Present in UK on {(citizenship_app_date - timedelta(days=5*365)).strftime('%d-%m-%Y')}: {'Yes' if was_present else 'No'}")
    
    citizenship_compliant = True
    if total_absences > 450:
        print("WARNING: Total absences exceed 450 days in the 5 years before application.")
        citizenship_compliant = False
    if last_year_absences > 90:
        print("WARNING: Absences exceed 90 days in the 12 months before application.")
        citizenship_compliant = False
    if not was_present:
        print("WARNING: You were not present in the UK 5 years before the application date.")
        citizenship_compliant = False
    
    if citizenship_compliant:
        print("You are compliant with the residence requirements for citizenship (assuming ILR held for 12 months).")
    else:
        print("You may not meet the residence requirements for citizenship.")
        print("Consider consulting an immigration solicitor for advice.")

    # Summary of all travel periods
    print("\nSummary of all travel periods:")
    for leave_date, return_date in travel_periods:
        days = (return_date - leave_date).days
        print(f" - Left UK on {leave_date.strftime('%d-%m-%Y')} to {return_date.strftime('%d-%m-%Y')}: {days} days")
        
if __name__ == "__main__":
    main()