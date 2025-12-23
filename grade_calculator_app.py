import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

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

# ---------------- App ----------------
class AdvancedGradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Casio Grade Calculator Pro")
        self.root.geometry("420x620")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.input_value = ""

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        # Student Name
        tk.Label(self.root, text="Student Name",
                 fg="white", bg="#121212").pack(pady=5)

        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(padx=20, fill="x")

        # Display
        self.display = tk.Entry(
            self.root, font=("Digital-7", 28),
            bg="black", fg="#00ff88",
            bd=8, justify="right"
        )
        self.display.pack(padx=20, pady=15, fill="x")

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root, orient="horizontal",
            length=350, mode="determinate"
        )
        self.progress.pack(pady=10)

        # Result
        self.result_label = tk.Label(
            self.root, text="Enter Marks (0–100)",
            fg="white", bg="#121212", font=("Arial", 12)
        )
        self.result_label.pack(pady=5)

        # Buttons
        self.create_buttons()

        # History
        tk.Label(self.root, text="History",
                 fg="#00ff88", bg="#121212").pack(pady=5)

        self.history = tk.Listbox(
            self.root, height=6,
            bg="#1e1e1e", fg="white"
        )
        self.history.pack(padx=20, fill="both")

    # ---------------- Buttons ----------------
    def create_buttons(self):
        frame = tk.Frame(self.root, bg="#121212")
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
                frame, text=b, width=6, height=2,
                bg="#2b2b2b", fg="white",
                font=("Arial", 14),
                command=lambda x=b: self.press(x)
            ).grid(row=r, column=c, padx=5, pady=5)
            c += 1
            if c == 3:
                c = 0
                r += 1

        tk.Button(frame, text="AC", bg="#aa3333",
                  fg="white", width=6, height=2,
                  command=self.clear).grid(row=4, column=0)

        tk.Button(frame, text="=", bg="#00aa88",
                  fg="black", width=6, height=2,
                  command=self.calculate).grid(row=4, column=1)

        tk.Button(frame, text="SAVE", bg="#4444aa",
                  fg="white", width=6, height=2,
                  command=self.save_csv).grid(row=4, column=2)

    # ---------------- Logic ----------------
    def press(self, val):
        self.flash()
        self.input_value += val
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.input_value)

    def clear(self):
        self.flash()
        self.input_value = ""
        self.display.delete(0, tk.END)
        self.result_label.config(text="Enter Marks (0–100)", fg="white")
        self.progress["value"] = 0

    def calculate(self):
        self.flash()
        try:
            name = self.name_entry.get().strip()
            score = float(self.input_value)

            if not name:
                raise ValueError("Name missing")
            if not (0 <= score <= 100):
                raise ValueError("Invalid score")

            grade, remark = calculate_grade(score)
            self.animate_progress(score)

            color = "#00ff88" if grade != "F" else "#ff4444"
            self.result_label.config(
                text=f"{name} → Grade {grade} ({remark})",
                fg=color
            )

            self.history.insert(
                0, f"{name} | {score}% → {grade}"
            )

        except:
            messagebox.showerror("Error", "Enter valid name & score")

    def animate_progress(self, target):
        self.progress["value"] = 0
        for i in range(int(target)):
            self.root.after(i*5,
                lambda v=i: self.progress.config(value=v))

    def save_csv(self):
        if not self.history.size():
            messagebox.showwarning("No Data", "Nothing to save")
            return

        with open("grade_results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            for item in self.history.get(0, tk.END):
                writer.writerow([item])

        messagebox.showinfo("Saved", "Results saved to grade_results.csv")

    def flash(self):
        self.root.configure(bg="#1e1e1e")
        self.root.after(80, lambda: self.root.configure(bg="#121212"))

# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedGradeCalculator(root)
    root.mainloop()
