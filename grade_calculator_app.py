import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

# ---------------- Grade Logic ----------------
def calculate_grade(score):
    if score >= 90:
        return "A+", "Excellent"
    elif score >= 80:
        return "A", "Very Good"
    elif score >= 70:
        return "B", "Good"
    elif score >= 60:
        return "C", "Average"
    elif score >= 50:
        return "D", "Pass"
    else:
        return "F", "Fail"

# ---------------- Main App ----------------
class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Calculator")
        self.root.geometry("420x580")
        self.root.resizable(False, False)

        self.input_value = ""

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        tk.Label(
            self.root,
            text="Student Grade Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(self.root, text="Student Name").pack()
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(padx=20, fill="x")

        self.display = tk.Entry(
            self.root,
            font=("Arial", 24),
            justify="right"
        )
        self.display.pack(padx=20, pady=10, fill="x")

        self.progress = ttk.Progressbar(
            self.root,
            length=320,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.result_label = tk.Label(
            self.root,
            text="Enter marks (0–100)",
            font=("Arial", 12)
        )
        self.result_label.pack(pady=5)

        self.create_buttons()

        tk.Label(self.root, text="History").pack(pady=5)
        self.history = tk.Listbox(
            self.root,
            height=7
        )
        self.history.pack(padx=20, fill="both")

    # ---------------- Buttons ----------------
    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        buttons = [
            "7","8","9",
            "4","5","6",
            "1","2","3",
            "0","."
        ]

        r = c = 0
        for b in buttons:
            tk.Button(
                frame,
                text=b,
                width=6,
                height=2,
                font=("Arial", 12),
                command=lambda x=b: self.press(x)
            ).grid(row=r, column=c, padx=5, pady=5)
            c += 1
            if c == 3:
                c = 0
                r += 1

        tk.Button(
            frame,
            text="AC",
            width=6,
            height=2,
            bg="#ff5555",
            command=self.clear
        ).grid(row=4, column=0, padx=5, pady=5)

        tk.Button(
            frame,
            text="=",
            width=6,
            height=2,
            bg="#55ff99",
            command=self.calculate
        ).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Save",
            width=6,
            height=2,
            bg="#5599ff",
            command=self.save
        ).grid(row=4, column=2, padx=5, pady=5)

    # ---------------- Input Handling ----------------
    def press(self, val):
        # Prevent multiple dots
        if val == "." and "." in self.input_value:
            return

        self.input_value += val
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.input_value)

    def clear(self):
        self.input_value = ""
        self.display.delete(0, tk.END)
        self.progress["value"] = 0
        self.result_label.config(
            text="Enter marks (0–100)",
            fg="black"
        )

    # ---------------- Calculation ----------------
    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            score = float(self.input_value)

            if not name or not (0 <= score <= 100):
                raise ValueError

            grade, remark = calculate_grade(score)

            self.animate_progress(score)

            color = "green" if grade != "F" else "red"
            self.result_label.config(
                text=f"{name}: Grade {grade} ({remark})",
                fg=color
            )

            self.history.insert(
                0,
                f"{name} | {score}% → {grade}"
            )

            # Auto clear display
            self.input_value = ""
            self.display.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid name and marks (0–100)"
            )

    # ---------------- Progress Animation ----------------
    def animate_progress(self, target):
        self.progress["value"] = 0
        step = max(1, int(target / 20))

        for i in range(0, int(target) + 1, step):
            self.root.after(
                i * 5,
                lambda v=i: self.progress.config(value=v)
            )

    # ---------------- Save to CSV ----------------
    def save(self):
        if self.history.size() == 0:
            messagebox.showwarning(
                "No Data",
                "No results to save"
            )
            return

        file_exists = os.path.exists("grade_results.csv")

        with open("grade_results.csv", "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(
                    ["Timestamp", "Student Result"]
                )

            writer.writerow(
                [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            )

            for item in self.history.get(0, tk.END):
                writer.writerow([item])

        messagebox.showinfo(
            "Saved",
            "Results saved to grade_results.csv"
        )

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
