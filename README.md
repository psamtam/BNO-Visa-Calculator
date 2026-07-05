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
# Your visa details (DD-MM-YYYY)
VISA_ISSUANCE_DATE=22-04-2024
FIRST_ENTRY_DATE=30-07-2024

# Space-separated travel periods: LEAVE_DATE,RETURN_DATE
TRAVEL_PERIODS=17-12-2024,10-01-2025 30-03-2025,24-04-2025 24-09-2025,20-10-2025 02-05-2026,19-05-2026 07-11-2026,15-11-2026
