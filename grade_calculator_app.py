import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

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

class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.input_value = ""

        tk.Label(root, text="Student Grade Calculator",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(root, text="Student Name").pack()
        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.pack(padx=20, fill="x")

        self.display = tk.Entry(root, font=("Arial", 24),
                                justify="right")
        self.display.pack(padx=20, pady=10, fill="x")

        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack(pady=10)

        self.result_label = tk.Label(root, text="Enter marks (0–100)",
                                     font=("Arial", 12))
        self.result_label.pack(pady=5)

        self.create_buttons()

        tk.Label(root, text="History").pack(pady=5)
        self.history = tk.Listbox(root, height=6)
        self.history.pack(padx=20, fill="both")

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        buttons = ["7","8","9","4","5","6","1","2","3","0","."]

        r = c = 0
        for b in buttons:
            tk.Button(frame, text=b, width=6, height=2,
                      command=lambda x=b: self.press(x)).grid(row=r, column=c)
            c += 1
            if c == 3:
                c = 0
                r += 1

        tk.Button(frame, text="AC", width=6, height=2,
                  command=self.clear).grid(row=4, column=0)
        tk.Button(frame, text="=", width=6, height=2,
                  command=self.calculate).grid(row=4, column=1)
        tk.Button(frame, text="Save", width=6, height=2,
                  command=self.save).grid(row=4, column=2)

    def press(self, val):
        self.input_value += val
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.input_value)

    def clear(self):
        self.input_value = ""
        self.display.delete(0, tk.END)
        self.result_label.config(text="Enter marks (0–100)")
        self.progress["value"] = 0

    def calculate(self):
        try:
            name = self.name_entry.get().strip()
            score = float(self.input_value)
            if not name or not (0 <= score <= 100):
                raise ValueError

            grade, remark = calculate_grade(score)
            self.progress["value"] = score

            self.result_label.config(
                text=f"{name}: Grade {grade} ({remark})"
            )
            self.history.insert(0, f"{name} | {score}% → {grade}")

        except:
            messagebox.showerror("Error", "Enter valid name and score")

    def save(self):
        if self.history.size() == 0:
            messagebox.showwarning("No Data", "Nothing to save")
            return

        with open("grade_results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now()])
            for item in self.history.get(0, tk.END):
                writer.writerow([item])

        messagebox.showinfo("Saved", "Results saved to CSV")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
