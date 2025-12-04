# Name: [Your Name Here]
# Date: 25th Nov, 2025
# Assignment: GradeBook Analyzer

import csv
import os

def print_header():
    print("="*40)
    print("   GradeBook Analyzer 1.0")
    print("="*40)

# --- Task 3: Statistical Analysis Functions  ---

def calculate_average(marks_dict):
    """Calculates arithmetic mean of scores."""
    if not marks_dict: return 0
    scores = list(marks_dict.values())
    return sum(scores) / len(scores)

def calculate_median(marks_dict):
    """Calculates median score manually."""
    if not marks_dict: return 0
    scores = sorted(marks_dict.values())
    n = len(scores)
    mid = n // 2
    
    if n % 2 == 1:
        return scores[mid]
    else:
        return (scores[mid - 1] + scores[mid]) / 2

def find_max_score(marks_dict):
    """Returns the maximum score."""
    if not marks_dict: return 0
    return max(marks_dict.values())

def find_min_score(marks_dict):
    """Returns the minimum score."""
    if not marks_dict: return 0
    return min(marks_dict.values())

# --- Task 2: Data Entry Functions [cite: 28] ---

def get_manual_input():
    """Getting student data via manual typing."""
    marks = {}
    print("\n--- Manual Entry Mode ---")
    print("Type 'done' as name to finish entry.")
    
    while True:
        name = input("Enter Student Name: ").strip()
        if name.lower() == 'done':
            break
        try:
            score = float(input(f"Enter marks for {name}: "))
            marks[name] = score
        except ValueError:
            print("Invalid input! Please enter a number for marks.")
    return marks

def get_csv_input():
    """Loading student data from a CSV file."""
    marks = {}
    filename = input("Enter CSV filename (e.g., data.csv): ").strip()
    
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming CSV format: Name, Score
                if len(row) >= 2:
                    try:
                        name = row[0].strip()
                        score = float(row[1].strip())
                        marks[name] = score
                    except ValueError:
                        continue # Skip header or bad data
        print(f"Successfully loaded {len(marks)} records.")
    except FileNotFoundError:
        print("Error: File not found.")
    return marks

# --- Task 4 & 5: Grading Logic and Filtering ---

def analyze_grades(marks_dict):
    """Assigns grades and filters pass/fail."""
    grades = {}
    # Task 4: Grade Assignment [cite: 42, 43]
    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
            
    return grades

def print_summary(marks_dict, grades_dict):
    """Task 6: Results Table and User Loop [cite: 53]"""
    
    if not marks_dict:
        print("No data to analyze.")
        return

    # 1. Statistical Summary [cite: 39]
    avg = calculate_average(marks_dict)
    median = calculate_median(marks_dict)
    max_score = find_max_score(marks_dict)
    min_score = find_min_score(marks_dict)

    print("\n--- Class Statistics ---")
    print(f"Average Score : {avg:.2f}")
    print(f"Median Score  : {median:.2f}")
    print(f"Highest Score : {max_score}")
    print(f"Lowest Score  : {min_score}")

    # 2. Pass/Fail Filter using List Comprehension [cite: 47-50]
    # Note: Assignment defines Pass as >= 40, even though Grade F is < 60.
    passed_students = [name for name, score in marks_dict.items() if score >= 40]
    failed_students = [name for name, score in marks_dict.items() if score < 40]

    print(f"\nTotal Passed: {len(passed_students)}")
    print(f"Total Failed: {len(failed_students)}")

    # 3. Grade Distribution Count [cite: 45]
    print("\n--- Grade Distribution ---")
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for g in grades_dict.values():
        if g in grade_counts:
            grade_counts[g] += 1
    
    for g, count in grade_counts.items():
        print(f"Grade {g}: {count} students")

    # 4. Formatted Table [cite: 54]
    print("\n" + "="*35)
    print(f"{'Name':<15} {'Marks':<10} {'Grade':<5}")
    print("-" * 35)
    for name, score in marks_dict.items():
        print(f"{name:<15} {score:<10} {grades_dict[name]:<5}")
    print("="*35 + "\n")

# --- Main Execution Loop ---

def main():
    print_header()
    
    while True: # Task 6: Menu Loop 
        print("1. Manual Entry")
        print("2. Load from CSV")
        print("3. Exit")
        
        choice = input("\nChoose an option (1-3): ")
        
        marks_data = {}
        
        if choice == '1':
            marks_data = get_manual_input()
        elif choice == '2':
            marks_data = get_csv_input()
        elif choice == '3':
            print("Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice.")
            continue
        
        if marks_data:
            # Perform Analysis
            student_grades = analyze_grades(marks_data)
            print_summary(marks_data, student_grades)

if __name__ == "__main__":
    main()
