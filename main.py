# ============================================================
#   STUDENT PROFILE MANAGEMENT SYSTEM
#   FODS Final Assessment Project
# ============================================================

import os
import matplotlib.pyplot as plt
import numpy as np


# ─────────────────────────────────────────────
# FILE SETUP — create files if they don't exist
# ─────────────────────────────────────────────

def setup_files():
    """Create the 4 data files with sample data if they don't already exist."""

    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write("admin01,Admin User,admin\n")
            f.write("s001,Siddhu Shah,student\n")
            f.write("s002,Yugant Adhikari,student\n")

    if not os.path.exists("passwords.txt"):
        with open("passwords.txt", "w") as f:
            f.write("admin01,admin123\n")
            f.write("s001,pass1234\n")
            f.write("s002,pass5678\n")

    if not os.path.exists("grades.txt"):
        with open("grades.txt", "w") as f:
            # Format: student_id, Math, CS, English, Science, Nepali
            f.write("s001,85,90,78,92,88\n")
            f.write("s002,72,65,80,70,75\n")

    if not os.path.exists("eca.txt"):
        with open("eca.txt", "w") as f:
            # Format: student_id, activity1, activity2 ...
            f.write("s001,Football,Music Club\n")
            f.write("s002,Dance,Debate Club,Art\n")


# ─────────────────────────────────────────────
# HELPER FUNCTIONS — read/write files cleanly
# ─────────────────────────────────────────────

def read_file(filename):
    """Read all lines from a file and return as a list."""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"  [!] File '{filename}' not found. Creating it now...")
        open(filename, "w").close()
        return []
    except Exception as e:
        print(f"  [!] Error reading '{filename}': {e}")
        return []


def write_file(filename, lines):
    """Write a list of lines back to a file."""
    try:
        with open(filename, "w") as f:
            for line in lines:
                f.write(line + "\n")
    except Exception as e:
        print(f"  [!] Error writing to '{filename}': {e}")


def divider():
    print("\n" + "-" * 45 + "\n")


# ─────────────────────────────────────────────
# BASE CLASS — User (blueprint for all users)
# ─────────────────────────────────────────────

class User:
    """
    Base class for all users.
    Both Admin and Student inherit from this.
    """

    def __init__(self, user_id, name, role):
        self.user_id = user_id   # e.g. "s001"
        self.name    = name      # e.g. "Siddhu Shah"
        self.role    = role      # "admin" or "student"

    def show_profile(self):
        """Print this user's basic profile."""
        print(f"\n  Name    : {self.name}")
        print(f"  ID      : {self.user_id}")
        print(f"  Role    : {self.role.capitalize()}")

    def update_profile(self):
        """Let a user change their own name."""
        try:
            print(f"\n  Current name: {self.name}")
            new_name = input("  Enter new name (or press Enter to keep): ").strip()
            if new_name:
                lines = read_file("users.txt")
                updated = []
                for line in lines:
                    parts = line.split(",")
                    if parts[0] == self.user_id:
                        parts[1] = new_name
                        self.name = new_name
                    updated.append(",".join(parts))
                write_file("users.txt", updated)
                print(f"  Name updated to '{new_name}'")
            else:
                print("  No changes made.")
        except Exception as e:
            print(f"  [!] Could not update profile: {e}")


# ─────────────────────────────────────────────
# STUDENT CLASS — inherits from User
# ─────────────────────────────────────────────

class Student(User):
    """
    A Student can:
    - View their grades
    - View their ECA activities
    - Update their own profile
    - Plot their own grade chart
    """

    def __init__(self, user_id, name):
        # Call parent __init__ with role = "student"
        super().__init__(user_id, name, "student")

    def view_grades(self):
        """Show this student's grades and their average."""
        try:
            subjects = ["Math", "CS", "English", "Science", "Nepali"]
            lines = read_file("grades.txt")

            for line in lines:
                parts = line.split(",")
                if parts[0] == self.user_id:
                    marks = list(map(int, parts[1:]))
                    print(f"\n  Grades for {self.name}:")
                    print("  " + "-" * 32)
                    for subj, mark in zip(subjects, marks):
                        bar = "#" * (mark // 10)
                        print(f"  {subj:<10}: {mark:>3}  {bar}")
                    avg = sum(marks) / len(marks)
                    print("  " + "-" * 32)
                    print(f"  Average   : {avg:.1f}")
                    grade = "A" if avg >= 80 else "B" if avg >= 65 else "C" if avg >= 50 else "F"
                    print(f"  Grade     : {grade}")
                    return
            print("  No grades found for your account.")
        except ValueError as e:
            print(f"  [!] Error reading grade data: {e}")
        except Exception as e:
            print(f"  [!] Unexpected error: {e}")

    def view_eca(self):
        """Show this student's ECA activities."""
        try:
            lines = read_file("eca.txt")
            for line in lines:
                parts = line.split(",")
                if parts[0] == self.user_id:
                    activities = parts[1:]
                    print(f"\n  ECA Activities for {self.name}:")
                    for i, act in enumerate(activities, 1):
                        print(f"    {i}. {act}")
                    return
            print("  No ECA records found for your account.")
        except Exception as e:
            print(f"  [!] Error reading ECA data: {e}")

    def plot_grades(self):
        """Draw a bar chart of this student's grades."""
        try:
            subjects = ["Math", "CS", "English", "Science", "Nepali"]
            lines = read_file("grades.txt")

            for line in lines:
                parts = line.split(",")
                if parts[0] == self.user_id:
                    marks = list(map(int, parts[1:]))
                    colors = ["#7F77DD", "#1D9E75", "#D85A30", "#378ADD", "#BA7517"]

                    plt.figure(figsize=(8, 5))
                    bars = plt.bar(subjects, marks, color=colors, edgecolor="white", linewidth=1.5)
                    plt.title(f"Grade Report — {self.name}", fontsize=14, fontweight="bold")
                    plt.ylabel("Marks (out of 100)")
                    plt.ylim(0, 115)

                    for bar, mark in zip(bars, marks):
                        plt.text(bar.get_x() + bar.get_width() / 2,
                                 bar.get_height() + 2,
                                 str(mark), ha="center", va="bottom", fontweight="bold")

                    avg = sum(marks) / len(marks)
                    plt.axhline(y=avg, color="red", linestyle="--", label=f"Average: {avg:.1f}")
                    plt.legend()
                    plt.tight_layout()
                    plt.show()
                    return
            print("  No grades found to plot.")
        except ValueError as e:
            print(f"  [!] Error reading grade data: {e}")
        except Exception as e:
            print(f"  [!] Could not plot grades: {e}")

    def student_menu(self):
        """Show the student dashboard."""
        while True:
            divider()
            print(f"  STUDENT DASHBOARD — {self.name}")
            divider()
            print("  1. View My Profile")
            print("  2. View My Grades")
            print("  3. View My ECA Activities")
            print("  4. Plot My Grades (Chart)")
            print("  5. Update My Profile")
            print("  6. Logout")
            divider()

            choice = input("  Choose an option: ").strip()

            if choice == "1":
                self.show_profile()
            elif choice == "2":
                self.view_grades()
            elif choice == "3":
                self.view_eca()
            elif choice == "4":
                self.plot_grades()
            elif choice == "5":
                self.update_profile()
            elif choice == "6":
                print(f"\n  Goodbye, {self.name}!")
                break
            else:
                print("  Invalid option. Please try again.")


# ─────────────────────────────────────────────
# ADMIN CLASS — inherits from User
# ─────────────────────────────────────────────

class Admin(User):
    """
    An Admin can:
    - Add, update, delete students
    - View all students
    - Update student ECA
    - Generate insights and analytics
    """

    def __init__(self, user_id, name):
        super().__init__(user_id, name, "admin")

    # ── ADD STUDENT ──────────────────────────

    def add_student(self):
        """Add a new student to all 4 files."""
        try:
            print("\n  ── ADD NEW STUDENT ──")

            existing_ids = [line.split(",")[0] for line in read_file("users.txt")]

            while True:
                uid = input("  Enter student ID (e.g. s003): ").strip()
                if uid in existing_ids:
                    print("  [!] That ID already exists. Try another.")
                elif not uid:
                    print("  [!] ID cannot be empty.")
                else:
                    break

            name     = input("  Enter student name: ").strip()
            password = input("  Set a password for them: ").strip()

            with open("users.txt", "a") as f:
                f.write(f"{uid},{name},student\n")

            with open("passwords.txt", "a") as f:
                f.write(f"{uid},{password}\n")

            subjects = ["Math", "CS", "English", "Science", "Nepali"]
            marks = []
            print("  Enter marks for each subject (0-100):")
            for subj in subjects:
                while True:
                    try:
                        m = int(input(f"    {subj}: "))
                        if 0 <= m <= 100:
                            marks.append(str(m))
                            break
                        else:
                            print("    [!] Must be 0-100.")
                    except ValueError:
                        print("    [!] Please enter a number.")

            with open("grades.txt", "a") as f:
                f.write(f"{uid},{','.join(marks)}\n")

            ecas = input("  Enter ECA activities (comma-separated, or press Enter to skip): ").strip()
            with open("eca.txt", "a") as f:
                if ecas:
                    f.write(f"{uid},{ecas}\n")
                else:
                    f.write(f"{uid},None\n")

            print(f"\n  Student '{name}' (ID: {uid}) added successfully!")
        except Exception as e:
            print(f"  [!] Error adding student: {e}")

    # ── VIEW ALL STUDENTS ────────────────────

    def view_all_students(self):
        """Show a table of all students."""
        try:
            lines = read_file("users.txt")
            students = [l.split(",") for l in lines if len(l.split(",")) >= 3 and l.split(",")[2] == "student"]

            if not students:
                print("\n  No students found.")
                return

            print(f"\n  {'ID':<10} {'Name':<22} {'Role'}")
            print("  " + "-" * 42)
            for s in students:
                print(f"  {s[0]:<10} {s[1]:<22} {s[2].capitalize()}")
        except Exception as e:
            print(f"  [!] Error viewing students: {e}")

    # ── DELETE STUDENT ───────────────────────

    def delete_student(self):
        """Remove a student from all 4 files."""
        try:
            print("\n  ── DELETE STUDENT ──")
            self.view_all_students()
            uid = input("\n  Enter student ID to delete: ").strip()

            users = read_file("users.txt")
            found = any(l.split(",")[0] == uid and l.split(",")[2] == "student" for l in users)
            if not found:
                print("  [!] Student ID not found.")
                return

            confirm = input(f"  Are you sure you want to delete '{uid}'? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("  Cancelled.")
                return

            for filename in ["users.txt", "passwords.txt", "grades.txt", "eca.txt"]:
                lines = read_file(filename)
                filtered = [l for l in lines if l.split(",")[0] != uid]
                write_file(filename, filtered)

            print(f"  Student '{uid}' deleted from all records.")
        except Exception as e:
            print(f"  [!] Error deleting student: {e}")

    # ── UPDATE GRADES ────────────────────────

    def update_grades(self):
        """Update a student's marks."""
        try:
            print("\n  ── UPDATE GRADES ──")
            self.view_all_students()
            uid = input("\n  Enter student ID: ").strip()

            subjects = ["Math", "CS", "English", "Science", "Nepali"]
            lines = read_file("grades.txt")
            updated = []
            found = False

            for line in lines:
                parts = line.split(",")
                if parts[0] == uid:
                    found = True
                    print(f"\n  Updating grades for {uid}:")
                    new_marks = []
                    for subj, old in zip(subjects, parts[1:]):
                        while True:
                            try:
                                m = int(input(f"    {subj} (current: {old}): "))
                                if 0 <= m <= 100:
                                    new_marks.append(str(m))
                                    break
                                else:
                                    print("    [!] Must be 0-100.")
                            except ValueError:
                                print("    [!] Enter a number.")
                    updated.append(f"{uid},{','.join(new_marks)}")
                else:
                    updated.append(line)

            if not found:
                print("  [!] No grades record for that ID.")
                return

            write_file("grades.txt", updated)
            print("  Grades updated successfully!")
        except Exception as e:
            print(f"  [!] Error updating grades: {e}")

    # ── UPDATE ECA ───────────────────────────

    def update_eca(self):
        """Update a student's ECA activities."""
        try:
            print("\n  ── UPDATE ECA ACTIVITIES ──")
            self.view_all_students()
            uid = input("\n  Enter student ID: ").strip()

            # Check student exists
            users = read_file("users.txt")
            found_user = any(l.split(",")[0] == uid and l.split(",")[2] == "student" for l in users)
            if not found_user:
                print("  [!] Student ID not found.")
                return

            # Show current ECA
            eca_lines = read_file("eca.txt")
            current = None
            for line in eca_lines:
                parts = line.split(",")
                if parts[0] == uid:
                    current = ", ".join(parts[1:])
                    break

            if current:
                print(f"  Current ECA: {current}")
            else:
                print("  No ECA record found for this student.")

            new_ecas = input("  Enter new ECA activities (comma-separated, or press Enter to skip): ").strip()

            # Update or add the record
            updated = []
            record_found = False
            for line in eca_lines:
                parts = line.split(",")
                if parts[0] == uid:
                    record_found = True
                    if new_ecas:
                        updated.append(f"{uid},{new_ecas}")
                    else:
                        updated.append(f"{uid},None")
                else:
                    updated.append(line)

            # If student had no ECA record at all, add one
            if not record_found:
                if new_ecas:
                    updated.append(f"{uid},{new_ecas}")
                else:
                    updated.append(f"{uid},None")

            write_file("eca.txt", updated)
            print("  ECA activities updated successfully!")
        except Exception as e:
            print(f"  [!] Error updating ECA: {e}")

    # ── ANALYTICS DASHBOARD ──────────────────

    def analytics_dashboard(self):
        """
        Performance Analytics Dashboard.
        Runs an inner menu with 3 features:
          A. Grade Trends
          B. ECA Impact
          C. Performance Alerts
        """
        while True:
            divider()
            print("  PERFORMANCE ANALYTICS DASHBOARD")
            divider()
            print("  A. Grade Trends      — charts for every student")
            print("  B. ECA Impact        — does ECA improve grades?")
            print("  C. Performance Alerts — who needs help?")
            print("  D. Back to Admin Menu")
            divider()

            choice = input("  Choose (A/B/C/D): ").strip().upper()

            if   choice == "A": self.analytics_grade_trends()
            elif choice == "B": self.analytics_eca_impact()
            elif choice == "C": self.analytics_performance_alerts()
            elif choice == "D": break
            else: print("  Invalid choice.")

    # ── A. GRADE TRENDS ──────────────────────

    def analytics_grade_trends(self):
        """
        Grade Trends: one line chart per student showing their marks
        across all 5 subjects, plus a class average overlay line.
        """
        try:
            subjects    = ["Math", "CS", "English", "Science", "Nepali"]
            grade_lines = read_file("grades.txt")
            user_lines  = read_file("users.txt")

            if not grade_lines:
                print("  No grade data found.")
                return

            # Build name lookup
            names = {}
            for line in user_lines:
                p = line.split(",")
                if len(p) >= 2:
                    names[p[0]] = p[1]

            # Parse all student marks
            all_marks  = []   # list of (name, [marks])
            totals     = [0] * len(subjects)

            for line in grade_lines:
                p = line.split(",")
                if len(p) >= 6:
                    marks = list(map(int, p[1:]))
                    all_marks.append((names.get(p[0], p[0]), marks))
                    for i, m in enumerate(marks):
                        totals[i] += m

            if not all_marks:
                print("  Not enough data.")
                return

            class_avg = [t / len(all_marks) for t in totals]
            colors    = ["#7F77DD", "#1D9E75", "#D85A30", "#378ADD", "#BA7517"]

            plt.figure(figsize=(9, 5))

            for i, (student, marks) in enumerate(all_marks):
                plt.plot(subjects, marks, marker="o", linewidth=2.5,
                         markersize=7, label=student, color=colors[i % len(colors)])
                for j, val in enumerate(marks):
                    plt.annotate(str(val), (subjects[j], val),
                                 textcoords="offset points", xytext=(0, 8),
                                 ha="center", fontsize=9)

            plt.plot(subjects, class_avg, marker="s", linewidth=1.5,
                     linestyle="--", color="gray", label="Class avg", alpha=0.7)

            plt.title("Grade Trends — Subject-wise Performance", fontsize=14, fontweight="bold")
            plt.ylabel("Marks")
            plt.ylim(0, 115)
            plt.axhline(y=50, color="red", linestyle=":", alpha=0.4, label="Pass (50)")
            plt.legend(fontsize=9)
            plt.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            plt.show()

            # Print summary table
            print("\n  GRADE SUMMARY TABLE:")
            print(f"  {'Student':<20} {'Math':>6} {'CS':>6} {'English':>8} {'Science':>8} {'Nepali':>7} {'Avg':>6} {'Grade':>6}")
            print("  " + "-" * 68)
            for student, marks in all_marks:
                avg   = sum(marks) / len(marks)
                grade = "A" if avg >= 80 else "B" if avg >= 65 else "C" if avg >= 50 else "F"
                print(f"  {student:<20} {marks[0]:>6} {marks[1]:>6} {marks[2]:>8} {marks[3]:>8} {marks[4]:>7} {avg:>6.1f} {grade:>6}")
            print("  " + "-" * 68)

        except ValueError as e:
            print(f"  [!] Error reading grade data: {e}")
        except Exception as e:
            print(f"  [!] Could not generate grade trends: {e}")

    # ── B. ECA IMPACT ────────────────────────

    def analytics_eca_impact(self):
        """
        ECA Impact: correlates number of ECA activities with
        average academic performance using a scatter + bar chart.
        """
        try:
            subjects    = ["Math", "CS", "English", "Science", "Nepali"]
            grade_lines = read_file("grades.txt")
            eca_lines   = read_file("eca.txt")
            user_lines  = read_file("users.txt")

            if not grade_lines:
                print("  No grade data found.")
                return

            names = {}
            for line in user_lines:
                p = line.split(",")
                if len(p) >= 2:
                    names[p[0]] = p[1]

            # Build grade average lookup
            grade_avg = {}
            for line in grade_lines:
                p = line.split(",")
                if len(p) >= 6:
                    marks = list(map(int, p[1:]))
                    grade_avg[p[0]] = round(sum(marks) / len(marks), 1)

            # Build ECA count lookup
            eca_count = {}
            for line in eca_lines:
                p = line.split(",")
                if len(p) >= 2:
                    activities = [a.strip() for a in p[1:] if a.strip() and a.strip() != "None"]
                    eca_count[p[0]] = len(activities)

            # Build data lists
            students   = []
            eca_counts = []
            avg_grades = []

            for uid, avg in grade_avg.items():
                count = eca_count.get(uid, 0)
                students.append(names.get(uid, uid))
                eca_counts.append(count)
                avg_grades.append(avg)

            if not students:
                print("  Not enough data for ECA correlation.")
                return

            # Correlation (manual, no pandas)
            n    = len(eca_counts)
            mean_e = sum(eca_counts) / n
            mean_g = sum(avg_grades) / n
            num  = sum((eca_counts[i] - mean_e) * (avg_grades[i] - mean_g) for i in range(n))
            den  = (sum((x - mean_e) ** 2 for x in eca_counts) *
                    sum((x - mean_g) ** 2 for x in avg_grades)) ** 0.5
            corr = round(num / den, 2) if den != 0 else 0

            print(f"\n  ECA vs Grade correlation coefficient: {corr}")
            if corr > 0.3:
                print("  Positive correlation — more ECA activities tend to go with higher grades.")
            elif corr < -0.3:
                print("  Negative correlation — more ECA activities tend to go with lower grades.")
            else:
                print("  Weak/no clear correlation with current data.")

            colors = ["#7F77DD", "#1D9E75", "#D85A30", "#378ADD", "#BA7517"]

            fig, axes = plt.subplots(1, 2, figsize=(13, 5))
            fig.suptitle("ECA Impact on Academic Performance", fontsize=14, fontweight="bold")

            # Left: scatter plot
            ax1 = axes[0]
            for i in range(len(students)):
                ax1.scatter(eca_counts[i], avg_grades[i],
                            s=120, color=colors[i % len(colors)], zorder=3, label=students[i])
                ax1.annotate(students[i], (eca_counts[i], avg_grades[i]),
                             textcoords="offset points", xytext=(8, 4), fontsize=9)

            if len(students) > 1:
                z = np.polyfit(eca_counts, avg_grades, 1)
                p = np.poly1d(z)
                x_range = np.linspace(min(eca_counts), max(eca_counts), 100)
                ax1.plot(x_range, p(x_range), "--", color="gray",
                         alpha=0.6, label=f"Trend (r={corr})")

            ax1.set_xlabel("Number of ECA activities")
            ax1.set_ylabel("Average grade (%)")
            ax1.set_title("ECA count vs average grade")
            ax1.set_ylim(0, 105)
            ax1.axhline(y=50, color="red", linestyle=":", alpha=0.4)
            ax1.legend(fontsize=9)
            ax1.grid(alpha=0.3)

            # Right: grouped bar — grade vs ECA count side by side
            ax2 = axes[1]
            x     = np.arange(len(students))
            width = 0.35
            bars1 = ax2.bar(x - width/2, avg_grades, width,
                            label="Avg grade (%)", color="#7F77DD", alpha=0.85)
            bars2 = ax2.bar(x + width/2, [c * 10 for c in eca_counts], width,
                            label="ECA count (×10 for scale)", color="#1D9E75", alpha=0.85)

            ax2.set_xticks(x)
            ax2.set_xticklabels(students, rotation=15, ha="right")
            ax2.set_ylabel("Value")
            ax2.set_title("Grade vs ECA involvement per student")
            ax2.set_ylim(0, 115)
            ax2.legend(fontsize=9)
            ax2.grid(axis="y", alpha=0.3)

            for bar in bars1:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                         f"{bar.get_height():.0f}", ha="center", va="bottom", fontsize=9)
            for bar, count in zip(bars2, eca_counts):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                         str(count), ha="center", va="bottom", fontsize=9)

            plt.tight_layout()
            plt.show()

            # Print table
            print("\n  ECA IMPACT TABLE:")
            print(f"  {'Student':<22} {'ECA Count':>10} {'Avg Grade':>10}")
            print("  " + "-" * 45)
            for s, e, g in zip(students, eca_counts, avg_grades):
                print(f"  {s:<22} {e:>10} {g:>10}")
            print("  " + "-" * 45)

        except ZeroDivisionError:
            print("  [!] Not enough data to calculate correlation.")
        except ValueError as e:
            print(f"  [!] Error reading data: {e}")
        except Exception as e:
            print(f"  [!] Could not generate ECA impact analysis: {e}")

    # ── C. PERFORMANCE ALERTS ────────────────

    def analytics_performance_alerts(self):
        """
        Performance Alerts: asks admin for a threshold, identifies
        all students below it, and suggests specific interventions.
        """
        try:
            subjects    = ["Math", "CS", "English", "Science", "Nepali"]
            grade_lines = read_file("grades.txt")
            eca_lines   = read_file("eca.txt")
            user_lines  = read_file("users.txt")

            if not grade_lines:
                print("  No grade data found.")
                return

            # Ask admin for the threshold
            while True:
                try:
                    threshold = float(input("\n  Enter alert threshold % (e.g. 60): ").strip())
                    if 0 <= threshold <= 100:
                        break
                    print("  Must be between 0 and 100.")
                except ValueError:
                    print("  Please enter a number.")

            names = {}
            for line in user_lines:
                p = line.split(",")
                if len(p) >= 2:
                    names[p[0]] = p[1]

            eca_lookup = {}
            for line in eca_lines:
                p = line.split(",")
                if len(p) >= 2:
                    eca_lookup[p[0]] = [a.strip() for a in p[1:] if a.strip() != "None"]

            # Parse student data into plain lists
            all_students = []   # list of dicts
            for line in grade_lines:
                p = line.split(",")
                if len(p) >= 6:
                    uid   = p[0]
                    marks = list(map(int, p[1:]))
                    avg   = round(sum(marks) / len(marks), 1)
                    all_students.append({
                        "id":      uid,
                        "name":    names.get(uid, uid),
                        "avg":     avg,
                        "marks":   marks
                    })

            at_risk = [s for s in all_students if s["avg"] < threshold]

            divider()
            print(f"  PERFORMANCE ALERTS  —  Threshold: {threshold}%")
            divider()

            if not at_risk:
                print(f"  All students are above {threshold}%. No alerts.")
            else:
                print(f"  {len(at_risk)} student(s) need attention:\n")
                for s in at_risk:
                    print(f"  Student : {s['name']} ({s['id']})")
                    print(f"  Average : {s['avg']}%  —  {threshold - s['avg']:.1f}% below threshold")

                    subj_marks = dict(zip(subjects, s["marks"]))
                    weakest    = sorted(subj_marks.items(), key=lambda x: x[1])[:2]
                    strongest  = sorted(subj_marks.items(), key=lambda x: x[1])[-1]

                    print(f"  Weakest subjects : {weakest[0][0]} ({weakest[0][1]}%), {weakest[1][0]} ({weakest[1][1]}%)")
                    print(f"  Strongest subject: {strongest[0]} ({strongest[1]}%)")

                    print("  Suggested interventions:")
                    print(f"    - Extra tutoring sessions in {weakest[0][0]} and {weakest[1][0]}")
                    ecas = eca_lookup.get(s["id"], [])
                    if len(ecas) == 0:
                        print("    - Encourage joining at least 1 ECA activity for engagement")
                    elif len(ecas) >= 3:
                        print("    - Consider reducing ECA load to focus on academics")
                    else:
                        print(f"    - Current ECA: {', '.join(ecas)} — balance maintained")
                    print(f"    - Set improvement target: reach {min(threshold + 10, 100):.0f}% average next term")
                    print()

            # Chart
            if all_students:
                names_list  = [s["name"]  for s in all_students]
                avgs_list   = [s["avg"]   for s in all_students]
                marks_list  = [s["marks"] for s in all_students]

                fig, axes = plt.subplots(1, 2, figsize=(14, 5))
                fig.suptitle(f"Performance Alerts — Threshold: {threshold}%",
                             fontsize=14, fontweight="bold")

                # Left: horizontal bar chart
                ax1 = axes[0]
                bar_colors = ["#E24B4A" if avg < threshold else "#1D9E75" for avg in avgs_list]
                bars = ax1.barh(names_list, avgs_list, color=bar_colors, edgecolor="white", linewidth=0.8)
                ax1.axvline(x=threshold, color="#BA7517", linestyle="--",
                            linewidth=1.5, label=f"Threshold ({threshold}%)")
                ax1.set_xlabel("Average grade (%)")
                ax1.set_title("Student averages vs threshold")
                ax1.set_xlim(0, 110)
                ax1.legend()
                ax1.grid(axis="x", alpha=0.3)
                for bar, val in zip(bars, avgs_list):
                    ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                             f"{val}%", va="center", fontsize=10, fontweight="bold")

                # Right: subject breakdown for at-risk (or all if none at risk)
                ax2   = axes[1]
                target = at_risk if at_risk else all_students
                x     = np.arange(len(subjects))
                width = 0.7 / max(len(target), 1)
                colors = ["#E24B4A", "#D85A30", "#BA7517", "#7F77DD", "#378ADD"]

                for i, s in enumerate(target):
                    ax2.bar(x + i * width, s["marks"], width,
                            label=s["name"], color=colors[i % len(colors)], alpha=0.85)

                ax2.set_xticks(x + width * (len(target) - 1) / 2)
                ax2.set_xticklabels(subjects)
                ax2.set_ylabel("Marks")
                ax2.set_title("Subject breakdown — students needing support"
                              if at_risk else "Subject breakdown — all students")
                ax2.set_ylim(0, 115)
                ax2.axhline(y=50, color="red", linestyle=":", alpha=0.4, label="Min pass (50)")
                ax2.legend(fontsize=9)
                ax2.grid(axis="y", alpha=0.3)

                plt.tight_layout()
                plt.show()

        except ValueError as e:
            print(f"  [!] Error reading grade data: {e}")
        except Exception as e:
            print(f"  [!] Could not generate performance alerts: {e}")

    # ── ADMIN MENU ───────────────────────────

    def admin_menu(self):
        """Show the admin dashboard."""
        while True:
            divider()
            print(f"  ADMIN DASHBOARD — {self.name}")
            divider()
            print("  1. View All Students")
            print("  2. Add New Student")
            print("  3. Update Student Grades")
            print("  4. Update Student ECA")
            print("  5. Delete Student")
            print("  6. Performance Analytics Dashboard")
            print("  7. Update My Profile")
            print("  8. Logout")
            divider()

            choice = input("  Choose an option: ").strip()

            if   choice == "1": self.view_all_students()
            elif choice == "2": self.add_student()
            elif choice == "3": self.update_grades()
            elif choice == "4": self.update_eca()
            elif choice == "5": self.delete_student()
            elif choice == "6": self.analytics_dashboard()
            elif choice == "7": self.update_profile()
            elif choice == "8":
                print(f"\n  Goodbye, {self.name}!")
                break
            else:
                print("  Invalid option. Please try again.")


# ─────────────────────────────────────────────
# LOGIN SYSTEM
# ─────────────────────────────────────────────

def login():
    """
    Validate username and password.
    Returns a Student or Admin object, or None if failed.
    """
    try:
        print("\n  Enter your credentials:")
        username = input("  Username : ").strip()
        password = input("  Password : ").strip()

        pw_lines      = read_file("passwords.txt")
        authenticated = False

        for line in pw_lines:
            parts = line.split(",")
            if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                authenticated = True
                break

        if not authenticated:
            print("\n  [!] Incorrect username or password. Please try again.")
            return None

        user_lines = read_file("users.txt")
        for line in user_lines:
            parts = line.split(",")
            if parts[0] == username:
                uid, name, role = parts[0], parts[1], parts[2]
                if role == "admin":
                    return Admin(uid, name)
                else:
                    return Student(uid, name)

        print("  [!] User record not found.")
        return None

    except Exception as e:
        print(f"  [!] Login error: {e}")
        return None


# ─────────────────────────────────────────────
# MAIN PROGRAM ENTRY POINT
# ─────────────────────────────────────────────

def main():
    setup_files()

    print("\n" + "=" * 45)
    print("   STUDENT PROFILE MANAGEMENT SYSTEM")
    print("   FODS Final Assessment  2025/2026  ")
    print("=" * 45)

    MAX_ATTEMPTS = 3

    while True:
        attempts = 0
        user     = None

        while attempts < MAX_ATTEMPTS:
            user = login()
            if user:
                break
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"  {remaining} attempt(s) remaining.")

        if not user:
            print("\n  Too many failed attempts. Exiting for security.\n")
            break

        print(f"\n  Welcome, {user.name}!")

        if isinstance(user, Admin):
            user.admin_menu()
        else:
            user.student_menu()

        again = input("\n  Login as another user? (yes/no): ").strip().lower()
        if again != "yes":
            print("\n  Thank you for using the system. Goodbye!\n")
            break


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()
