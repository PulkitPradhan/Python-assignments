# Project Title: Daily Calorie Tracker CLI
# Author: Pulkit [2501730036]

import datetime # Required for Task 6 to get the timestamp

def cal_tracker():
    print("---------------------------------------------------")
    print("|                 Welcome to                      |")
    print("|          Daily Calorie Tracker CLI              |")
    print("---------------------------------------------------")
    
    ml_names = [] 
    cal_amnt = [] 
    
    # Get the daily calorie limit
    while True:
        try:
           limit = float(input("\nEnter your daily calorie limit (e.g., 2000): ")) #
           if limit > 0:
                break
           else:
                print("Please select a positive number.")
        except ValueError:
            print(" pls Enter a number ")

    # Ask the user how many meals to enter
    while True:
        try:
            num_meals = int(input(f"How many meals will you log today (1 or more)? "))
            if num_meals >= 1:
                break
            else:
                print("You must enter at least 1 meal.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Collect meal data
    for i in range(num_meals):
        print(f"\n--- Entering Meal {i + 1} of {num_meals} ---")
        ml_name = input("Enter meal name (e.g., Breakfast, Lunch): ")
        ml_names.append(ml_name)

        # Calorie Amount Input and Conversion
        while True:
            try:
                # Use input() and convert to float for calorie amount
                calorie_input = input("Enter calorie amount for this meal: ")
                calorie_amnt = float(calorie_input)
                cal_amnt.append(calorie_amnt)
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for calories.")
    
    
    total_calories = sum(cal_amnt)
    average_calories = total_calories / len(cal_amnt) if cal_amnt else 0.0

    # Determine limit status
    limit_status = ""
    
    if total_calories > limit:
        limit_status = " WARNING!! : You have EXCEEDED your daily calorie limit!"
    else:
        limit_status = " Success: You are WITHIN your daily calorie limit."
    
   

    # Build the report string for printing and saving
    report_lines = []
    report_lines.append("\n----------------------------------------")
    report_lines.append("              DAILY CALORIE REPORT                ")
    report_lines.append(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") # For Task 6
    report_lines.append(f"Daily Limit: {limit} Calories")
    report_lines.append("\n----------------------------------------")
    
    # Header of the summary table
    report_lines.append(f"{'Meal Name':<20}\t{'Calories':>10}")
    report_lines.append("\n----------------------------------------")

    for meal, calories in zip(ml_names, cal_amnt):
        report_lines.append(f"{meal:<20}\t{calories:>10.2f}") 
        report_lines.append("\n----------------------------------------")


    # Summary calculations
    report_lines.append(f"{'Total:':<20}\t{total_calories:>10.2f}")
    report_lines.append(f"{'Average:':<20}\t{average_calories:>10.2f}")
    report_lines.append("\n----------------------------------------")
    report_lines.append(f"Limit Status: {limit_status}")
    report_lines.append("\n----------------------------------------")

    # Print the report to the CLI
    for line in report_lines:
        print(line)

    # Task 6 (Bonus): Save Session Log to File 
    
    save_log = input("\nDo you want to save this session log to a file? (yes/no): ").lower()
    
    if save_log == 'yes':
        filename = "cal_track.txt"
        try:
            with open(filename, "a") as file:
                file.write("\n" + "\n".join(report_lines))
                file.write("\n\n")
            print(f"\nReport successfully saved to {filename}")
        except Exception as e:
            print(f"\nError saving file: {e}")

if __name__ == "__main__":
    cal_tracker()
