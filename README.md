# BN(O) Visa Absence Calculator

A command-line Python utility designed for Hong Kong British National (Overseas) visa holders to track their travel history, calculate UK absences, and confidently plan their timelines for **Indefinite Leave to Remain (ILR)** and **British Citizenship (Naturalisation)**.

## 🚀 Why This Tool Exists

The UK Home Office enforces strict, but completely different, residence requirements for ILR and British Citizenship. This script prevents you from making expensive application mistakes by checking your travel history against both sets of immigration laws:

1. **ILR Rule (Continuous Residence):** You must not be absent from the UK for more than **180 days in any rolling 365-day period**. The countdown can legally start from your visa issuance date.
2. **Citizenship Rule (5-Year Rule):** You must not exceed **450 days total** of absences over 5 years, and no more than **90 days** in the final 12 months.
3. **The Citizenship "Physical Presence" Catch:** You **must** have been physically standing on UK soil on the *exact calendar date 5 years prior* to the day the Home Office receives your citizenship application. 

This script catches gaps between your visa approval and arrival date, and automatically flags if a holiday 5 years ago will cause an automatic citizenship rejection.

---

## 🛠️ Features

* Automatically processes the initial landing gap (time between visa issuance and first UK entry) as a standard absence.
* Evaluates a rolling 365-day window to ensure compliance with the 180-day ILR limit.
* Validates your planned British Citizenship application date to ensure you were physically in the UK exactly 5 years prior.
* Supports loading travel histories via a plain-text configuration file (`bno_config.txt`) so you don't have to manually type trips every time.

---

## 📁 Configuration Setup

To save time, create a configuration file named `bno_config.txt` in the same directory as the script. Use the format below to structure your data:

```text
VISA_ISSUANCE_DATE=22-04-2024 
FIRST_ENTRY_DATE=30-07-2024
TRAVEL_PERIODS= 17-12-2024,10-01-2025 30-03-2025,24-04-2025 24-09-2025,20-10-2025 02-05-2026,19-05-2026 07-11-2026,15-11-2026
```

## 💻 How to Run
1. Clone or download this repository.
2. Ensure you have Python 3 installed.
3. Open your terminal in the project directory and run:
```python
python bno_visa_calculator.py
```

## 📊 Sample Output
Below is an example of the CLI execution. Notice how the tool catches a critical timeline issue where a vacation exactly 5 years prior to the target application date would trigger an automatic citizenship rejection:

```text
BNO Visa Absence Calculator
This tool checks absences for ILR (≤180 days per 365-day period) and British citizenship.
Citizenship requirements: ≤450 days total absences in 5 years, ≤90 days in last 12 months, present in UK 5 years before application.
Dates should be in DD-MM-YYYY format (e.g., 01-01-2023).
Your visa was issued on 22-04-2024.
You first entered the UK on 30-07-2024.
The period from 22-04-2024 to 29-07-2024 will be counted as an absence.

Default ILR residence period start date: 22-04-2024 (visa issuance date)

For citizenship, you plan to apply 1 year after ILR (e.g., 1 year after April 2029).
Using default: 22-04-2030

Loaded default travel periods from configuration:
 - Left UK on 17-12-2024 to 10-01-2025: 24 days absent
 - Left UK on 30-03-2025 to 24-04-2025: 25 days absent
 - Left UK on 24-09-2025 to 20-10-2025: 26 days absent
 - Left UK on 02-05-2026 to 19-05-2026: 17 days absent
 - Left UK on 07-11-2026 to 15-11-2026: 8 days absent

Enter additional travel periods (when you left and returned to the UK).
Enter 'done' when you have entered all travel periods.
Enter date you left the UK (DD-MM-YYYY) or 'done' to finish: done

ILR Results:
Maximum days absent in any 365-day period: 146
You are compliant with the 180-day rule for ILR continuous residence.

Citizenship Results (based on planned application date):
Total absences in 5 years before 22-04-2030: 52 days
Absences in 12 months before 22-04-2030: 0 days
Present in UK on 23-04-2025: No
WARNING: You were not present in the UK 5 years before the application date.
You may not meet the residence requirements for citizenship.
Consider consulting an immigration solicitor for advice.

Summary of all travel periods:
 - Left UK on 22-04-2024 to 30-07-2024: 99 days
 - Left UK on 17-12-2024 to 10-01-2025: 24 days
 - Left UK on 30-03-2025 to 24-04-2025: 25 days
 - Left UK on 24-09-2025 to 20-10-2025: 26 days
 - Left UK on 02-05-2026 to 19-05-2026: 17 days
 - Left UK on 07-11-2026 to 15-11-2026: 8 days
```

