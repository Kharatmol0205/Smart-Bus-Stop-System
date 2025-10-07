# tk_login.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_db_password",
    "database": "smartbus"
}


def verify_credentials(email, password):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, email, hashed_password FROM users WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return False, "User not found"
        if pwd_context.verify(password, row["hashed_password"]):
            return True, row["id"]
        else:
            return False, "Incorrect password"
    except Exception as e:
        return False, f"DB error: {e}"


def on_login():
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    ok, info = verify_credentials(email, password)
    if ok:
        messagebox.showinfo("Success", f"Logged in! user id: {info}")
        # continue to app
    else:
        messagebox.showerror("Error", str(info))


root = tk.Tk()
root.title("Login")

tk.Label(root, text="Email:").grid(row=0, column=0, padx=6, pady=6)
entry_email = tk.Entry(root)
entry_email.grid(row=0, column=1, padx=6, pady=6)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=6, pady=6)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=6, pady=6)

tk.Button(root, text="Login", command=on_login).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
