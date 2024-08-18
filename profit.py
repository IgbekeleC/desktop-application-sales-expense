import tkinter as tk
from tkinter import messagebox
from sales import sales_records, vat_rate
from expenses import expense_records
from datetime import datetime, timedelta

def create_profit_section(parent):
    profit_frame = tk.LabelFrame(parent, text="Calculate Profit/Loss")
    profit_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    # Time frame selection
    tk.Label(profit_frame, text="Select Time Frame").grid(row=0, column=0)
    time_frame_var = tk.StringVar(value="Week")
    time_frame_dropdown = tk.OptionMenu(profit_frame, time_frame_var, "Week", "Month", "Year", command=lambda _: update_dropdowns(time_frame_var, year_dropdown, month_dropdown, week_dropdown))
    time_frame_dropdown.grid(row=0, column=1)

    # Dropdowns for Year, Month, and Week
    tk.Label(profit_frame, text="Year").grid(row=1, column=0)
    year_dropdown = tk.Spinbox(profit_frame, from_=2000, to=datetime.today().year)
    year_dropdown.grid(row=1, column=1)

    tk.Label(profit_frame, text="Month").grid(row=2, column=0)
    month_dropdown = tk.Spinbox(profit_frame, from_=1, to=12)
    month_dropdown.grid(row=2, column=1)

    tk.Label(profit_frame, text="Week").grid(row=3, column=0)
    week_dropdown = tk.Spinbox(profit_frame, from_=1, to=4)
    week_dropdown.grid(row=3, column=1)

    # Initially hide the week and month dropdowns
    month_dropdown.grid_remove()
    week_dropdown.grid_remove()

    # Button to calculate profit
    tk.Button(profit_frame, text="Calculate Profit", 
              command=lambda: calculate_profit(time_frame_var, year_dropdown, month_dropdown, week_dropdown)).grid(row=4, column=0, columnspan=2)

def update_dropdowns(time_frame_var, year_dropdown, month_dropdown, week_dropdown):
    time_frame = time_frame_var.get()

    # Adjust visibility of dropdowns based on the selected time frame
    if time_frame == "Week":
        year_dropdown.grid()
        month_dropdown.grid()
        week_dropdown.grid()
    elif time_frame == "Month":
        year_dropdown.grid()
        month_dropdown.grid()
        week_dropdown.grid_remove()
    elif time_frame == "Year":
        year_dropdown.grid()
        month_dropdown.grid_remove()
        week_dropdown.grid_remove()
def calculate_profit(time_frame_var, year_dropdown, month_dropdown, week_dropdown):
    # Get the selected date and time frame
    year = int(year_dropdown.get())
    time_frame = time_frame_var.get()

    today = datetime.today()
    end_date = today

    # Determine the date range based on the selected time frame
    if time_frame == "Week":
        month = int(month_dropdown.get())
        week = int(week_dropdown.get())
        start_date = datetime(year, month, 1) + timedelta(weeks=week-1)
        end_date = min(start_date + timedelta(days=6), today)  # End date is either the end of the week or today
    elif time_frame == "Month":
        month = int(month_dropdown.get())
        start_date = datetime(year, month, 1)
        next_month = start_date.replace(day=28) + timedelta(days=4)  # Ensure the next month is reached
        end_date = min(next_month.replace(day=1) - timedelta(days=1), today)  # End date is either the end of the month or today
    elif time_frame == "Year":
        start_date = datetime(year, 1, 1)
        end_date = min(datetime(year, 12, 31), today)  # End date is either the end of the year or today

    # Filter sales records and calculate total revenue and VAT based on the date range
    total_revenue = 0.0
    total_vat = 0.0

    for record in sales_records:
        record_date = datetime.strptime(record[0], '%Y-%m-%d')
        if start_date <= record_date <= end_date:
            total_price = float(record[5])  # Total price including VAT
            vat_amount = total_price * vat_rate / (1 + vat_rate)  # Extract VAT from the total price
            total_vat += vat_amount
            total_revenue += (total_price - vat_amount)  # Revenue excluding VAT

    # Filter expense records based on the date range and ensure valid conversion to float
    total_expense = 0.0
    for record in expense_records:
        record_date = datetime.strptime(record[0], '%Y-%m-%d')
        if start_date <= record_date <= end_date:
            try:
                expense_amount = float(record[2])
                total_expense += expense_amount
            except ValueError:
                print(f"Skipping invalid expense record: {record}")  # Log the invalid record

    # Calculate profit or loss
    profit_loss = total_revenue - total_expense

    # Determine if it's a profit or loss
    if profit_loss > 0:
        result_message = (f"Time Frame: {time_frame}\nStart Date: {start_date.strftime('%Y-%m-%d')}\nEnd Date: {end_date.strftime('%Y-%m-%d')}\n"
                          f"Revenue (excl. VAT): ${total_revenue:.2f}\nExpenses: ${total_expense:.2f}\nTotal VAT: ${total_vat:.2f}\n"
                          f"Profit: ${profit_loss:.2f}")
    else:
        result_message = (f"Time Frame: {time_frame}\nStart Date: {start_date.strftime('%Y-%m-%d')}\nEnd Date: {end_date.strftime('%Y-%m-%d')}\n"
                          f"Revenue (excl. VAT): ${total_revenue:.2f}\nExpenses: ${total_expense:.2f}\nTotal VAT: ${total_vat:.2f}\n"
                          f"Loss: ${profit_loss:.2f}")

    messagebox.showinfo("Profit/Loss", result_message)




