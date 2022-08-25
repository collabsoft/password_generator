import tkinter as tk
from tkinter import messagebox
import string
import random
import json

# -------------------------- PASSWORD GENERATOR ---------------------------- #

# characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def generate_random_password():
    length = 16
    password_input.delete(0, tk.END)  # Cleaning the pass input.
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    generated_pass = "".join(password)
    password_input.insert(0, generated_pass)


# -------------------------- SAVE PASSWORD --------------------------------- #


def save():
    website = website_input.get()
    website = website.title()
    email = email_username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as f:
                # Reading old data:
                data = json.load(f)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            # Updating old data with new data:
            data.update(new_data)
            with open("data.json", "w") as f:
                # Saving updated data:
                json.dump(data, f, indent=4)
        finally:
            website_input.delete(0, tk.END)
            password_input.delete(0, tk.END)

# ---------------------------- SEARCHING PASS ------------------------------ #


def search():
    website = website_input.get()
    website = website.title()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(
            title="Error",
            message="There is no stored informations."
        )
    else:
        if website in data:
            messagebox.showinfo(
                title=f"{website} credentials:",
                message=f"Login: {data[website]['email']} \nPass: {data[website]['password']}"
                )
        else:
            messagebox.showinfo(
                title="Error",
                message=f"No credentials for {website}."
                )


# -------------------------- UI SETUP -------------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white")

# row 0
canvas = tk.Canvas(width=300, height=200, bg="white", highlightthickness=0)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# row 1
website_label = tk.Label(text="Website: ", font=("Arial", 14), bg="white")
website_label.grid(row=1, column=0)

website_input = tk.Entry(width=40)
website_input.grid(row=1, column=1)

website_search_button = tk.Button(
    text="Search", width=15, font=("Arial", 10), bg="blue", fg="white",
    command=search)
website_search_button.grid(row=1, column=2)

# row 2
email_username_label = tk.Label(
    text="Email/Username: ", font=("Arial", 14), bg="white")
email_username_label.grid(row=2, column=0)

email_username_input = tk.Entry(width=58)
email_username_input.grid(row=2, column=1, columnspan=2)

# row 3
password_label = tk.Label(text="Password: ", font=("Arial", 14), bg="white")
password_label.grid(row=3, column=0)

password_input = tk.Entry(width=40)
password_input.grid(row=3, column=1)

generate_password_button = tk.Button(
    text="Generate Password", width=15, font=("Arial", 10), bg="white",
    command=generate_random_password)
generate_password_button.grid(row=3, column=2)

# row 4
add_button = tk.Button(text="Add", width=54, bg="white", command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
