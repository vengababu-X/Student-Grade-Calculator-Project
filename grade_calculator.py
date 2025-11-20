# Save this file as: grade_calculator.py

# --- Data Structure: List to store results ---
all_student_results = []
# --- Control Flow: Flag for the While loop ---
running = True

def calculate_grade(score):
    """
    Uses conditional statements (if, elif, else) and comparison operators 
    (>=) to determine the grade and corresponding comment.
    """
    # Grade Determination using IF/ELIF/ELSE
    if score >= 90:
        return "A+", "Excellent performance! Keep up the great work."
    elif score >= 80:
        return "A", "Very strong performance. Well done."
    elif score >= 70:
        return "B", "Solid effort. Good understanding of the material."
    elif score >= 60:
        return "C", "Acceptable performance. Could use more practice."
    elif score >= 50:
        return "D", "Minimum passing grade. Review challenging topics."
    else:
        # Catch-all condition for scores below 50
        return "F", "Failing grade. Requires immediate attention and study."

def run_calculator():
    """Main function to handle user input, calculation, and data storage."""
    global running

    print("\n--- Student Grade Calculator ---")

    # Get student name
    student_name = input("Enter student's name (or type 'quit' to finish): ").strip()
    if student_name.lower() == 'quit':
        running = False
        return

    # --- Error Handling: Use try-except for robust input ---
    try:
        # Get student score
        score_input = input(f"Enter {student_name}'s percentage score (0-100): ")
        score = float(score_input)
    except ValueError:
        print("❌ Invalid input. Please enter a numerical score (e.g., 85).")
        return # Skip to the next iteration of the while loop

    # Check for valid score range
    if not (0 <= score <= 100):
        print("⚠️ Score must be between 0 and 100.")
        return # Skip to the next iteration of the while loop

    # Calculate grade and comment
    grade, comment = calculate_grade(score)

    # Display the result
    print(f"\n✅ Result for {student_name}:")
    print(f"   Score: {score:.1f}%")
    print(f"   Grade: **{grade}**")
    print(f"   Comment: {comment}")

    # --- List Modification: Store the result in the list ---
    result_entry = {
        "name": student_name,
        "score": score,
        "grade": grade,
        "comment": comment
    }
    all_student_results.append(result_entry)
    print("--- Result saved. ---")


# --- Control Flow: WHILE loop to calculate grades for multiple students ---
while running:
    run_calculator()

# --- Program End ---
print("\n=== Grading Session Complete ===")

# --- List Access: Display the final list of stored results ---
if all_student_results:
    print("\n📚 Summary of All Results:")
    for result in all_student_results:
        # For loop iterates through the list
        print(f"* **{result['name']}**: {result['score']}% -> Grade {result['grade']}")
else:
    print("No student results were recorded.")
