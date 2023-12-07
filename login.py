import tkinter, json
from tkinter import messagebox

logged_in, current_user, current_user_num, high_score, x, y = False, "", 0, "", 0, 0

def write_json(data):
    with open("settings.json", "w") as json_file:
        json.dump(data, json_file)

def read_json():
    with open("settings.json", "r") as json_file:
        return json.load(json_file)

def open_login_form():
    data = read_json()

    root = tkinter.Tk()
    root.title("Numtrix login")
    root.geometry("600x400")
    root.configure(bg="#808080")

    def login():
        global logged_in, current_user, current_user_num, high_score, x, y
        credentials = [(user["name"], user["password"]) for user in data]
        for i, credential in enumerate(credentials):
            if credential[0] == username_entry.get() and credential[1] == password_entry.get():
                messagebox.showinfo(title=f"Successfully logged in as {username_entry.get()}", message=f"Welcome to the game, {username_entry.get()}")
                current_user = username_entry.get()
                current_user_num = i
                high_score = data[i]["high_score"]
                x, y = [int(i.strip()) for i in dimension_entry.get().split(",")]
                root.destroy()
                logged_in = True
                return
        messagebox.showerror(title="Error", message="Invalid username or password!!")

    frame = tkinter.Frame(bg="#808080")
    login_text = tkinter.Label(frame, text="Welcome, Enter your credential please", bg="#808080", fg="#FFF", font=("Arial", 18))
    username_text = tkinter.Label(frame, text="Username", bg="#333333", fg="#FFFFFF", font=("Arial", 16))
    password_text = tkinter.Label(frame, text="Password", bg="#333333", fg="#FFFFFF", font=("Arial", 16))
    dimension_text = tkinter.Label(frame, text="Diffculty \n (Dimension of the board) \n [x, y]", bg="#333333", fg="#FFFFFF", font=("Arial", 16))
    username_entry = tkinter.Entry(frame, font=("Arial", 16))
    password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
    login_button = tkinter.Button(frame, text="Login", bg="#808080", fg="#FFFFFF", font=("Arial", 16), command=login)

    dimension_entry = tkinter.Entry(frame, font=("Arial", 16))

    login_text.grid(row=0, column=0, columnspan=3, sticky="news", pady=40)
    username_text.grid(row=1, column=0)
    password_text.grid(row=2, column=0)
    dimension_text.grid(row=3, column=0)
    dimension_entry.grid(row=3, column=1)
    username_entry.grid(row=1, column=1, pady=10)
    password_entry.grid(row=2, column=1, pady=10)
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    frame.pack()
    root.mainloop()
    return logged_in, current_user, current_user_num, high_score, x, y
