
import tkinter as tk
from tkinter import ttk
import re
import random
import string
import secrets

# Create main window
root = tk.Tk()
root.title("Password Complexity Checker")
root.geometry("500x450")
root.resizable(False, False)

# Main frame for padding and layout
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --------------------------
# Password Input Section
# --------------------------
password_label = tk.Label(main_frame, text="Enter Password:", font=("Arial", 12))
password_label.grid(row=0, column=0, sticky="w")

# The password entry widget uses the "show" option to mask input
password_entry = tk.Entry(main_frame, show="*", width=40, font=("Arial", 12))
password_entry.grid(row=0, column=1, pady=5, sticky="w")

# Show Password Toggle
show_password_var = tk.BooleanVar(value=False)
def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")  # Show the actual text
    else:
        password_entry.config(show="*")  # Mask the text

show_password_cb = tk.Checkbutton(main_frame, text="Show Password",
                                  variable=show_password_var, command=toggle_password)
show_password_cb.grid(row=1, column=1, sticky="w", pady=5)

# --------------------------
# Password Strength Indicator
# --------------------------
strength_text_label = tk.Label(main_frame, text="Password Strength:", font=("Arial", 12))
strength_text_label.grid(row=2, column=0, sticky="w", pady=5)

# This label will display the text (e.g., "Very Weak", "Moderate", "Strong")
strength_var = tk.StringVar()
strength_display = tk.Label(main_frame, textvariable=strength_var, font=("Arial", 12, "bold"))
strength_display.grid(row=2, column=1, sticky="w", pady=5)

# A progress bar shows the strength score graphically.
progress = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress.grid(row=3, column=0, columnspan=2, pady=10)

# --------------------------
# Criteria Checklist Labels
# --------------------------
# Each criterion is shown as a label that turns green when met.
criteria_labels = {}
criteria_texts = {
    "length": "Minimum 8 characters (12+ recommended)",
    "uppercase": "At least one uppercase letter (A-Z)",
    "lowercase": "At least one lowercase letter (a-z)",
    "digit": "At least one number (0-9)",
    "special": "At least one special character (@, #, $, %, etc.)"
}

# Start listing criteria from row 4 downward.
row_index = 4
for key, text in criteria_texts.items():
    lbl = tk.Label(main_frame, text=text, font=("Arial", 10), fg="red")
    lbl.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=2)
    criteria_labels[key] = lbl
    row_index += 1

# --------------------------
# Password Evaluation Function
# --------------------------
def evaluate_password(event=None):
    """
    Evaluates the entered password based on:
      • Length (minimum 8; bonus for 12+)
      • Presence of uppercase letters
      • Presence of lowercase letters
      • Presence of digits
      • Presence of special characters
    Updates the progress bar, strength text, and checklist labels accordingly.
    """
    password = password_entry.get()
    score = 0
    max_score = 6  # 2 points for length (>=8 and bonus for >=12) + 1 each for 4 criteria

    # --- Check Length ---
    if len(password) >= 8:
        score += 1
        criteria_labels["length"].config(fg="green")
        if len(password) >= 12:
            score += 1  # Bonus point for recommended length
    else:
        criteria_labels["length"].config(fg="red")

    # --- Check for Uppercase Letters ---
    if re.search(r"[A-Z]", password):
        score += 1
        criteria_labels["uppercase"].config(fg="green")
    else:
        criteria_labels["uppercase"].config(fg="red")

    # --- Check for Lowercase Letters ---
    if re.search(r"[a-z]", password):
        score += 1
        criteria_labels["lowercase"].config(fg="green")
    else:
        criteria_labels["lowercase"].config(fg="red")

    # --- Check for Digits ---
    if re.search(r"\d", password):
        score += 1
        criteria_labels["digit"].config(fg="green")
    else:
        criteria_labels["digit"].config(fg="red")

    # --- Check for Special Characters ---
    # Here we define a set of special characters
    if re.search(r"[@#$%^&*(),.?!]", password):
        score += 1
        criteria_labels["special"].config(fg="green")
    else:
        criteria_labels["special"].config(fg="red")

    # Update the progress bar (max score is 6)
    progress['maximum'] = max_score
    progress['value'] = score

    # Set the strength message and its color based on the score
    if len(password) == 0:
        strength_var.set("")
        strength_display.config(fg="black")
    elif score <= 2:
        strength_var.set("Very Weak")
        strength_display.config(fg="red")
    elif score <= 4:
        strength_var.set("Moderate")
        strength_display.config(fg="orange")
    else:
        strength_var.set("Strong")
        strength_display.config(fg="green")

# Bind the key release event to evaluate the password in real time
password_entry.bind("<KeyRelease>", evaluate_password)

# --------------------------
# Button Functions
# --------------------------
def generate_password():
    """
    Generates a secure random password that meets all criteria.
    The password will be 12 characters long and include at least one uppercase,
    one lowercase, one digit, and one special character.
    """
    length = 12  # Default secure length
    password_chars = []
    # Ensure each criterion is met
    password_chars.append(secrets.choice(string.ascii_uppercase))
    password_chars.append(secrets.choice(string.ascii_lowercase))
    password_chars.append(secrets.choice(string.digits))
    password_chars.append(secrets.choice("@#$%^&*(),.?!"))
    # Fill the remaining characters randomly from the combined pool
    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + "@#$%^&*(),.?!"
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining_length))
    # Shuffle to mix the characters
    random.shuffle(password_chars)
    password_generated = ''.join(password_chars)
    # Insert generated password into entry widget and update evaluation
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password_generated)
    evaluate_password()

def copy_password():
    """Copies the current password to the clipboard."""
    password = password_entry.get()
    root.clipboard_clear()
    root.clipboard_append(password)

# --------------------------
# Buttons for Generate and Copy
# --------------------------
button_frame = tk.Frame(main_frame)
button_frame.grid(row=row_index, column=0, columnspan=2, pady=10)

generate_btn = tk.Button(button_frame, text="Generate Secure Password",
                         command=generate_password, font=("Arial", 10))
generate_btn.grid(row=0, column=0, padx=10)

copy_btn = tk.Button(button_frame, text="Copy Password",
                     command=copy_password, font=("Arial", 10))
copy_btn.grid(row=0, column=1, padx=10)

# --------------------------
# Run the Application
# --------------------------
root.mainloop()
