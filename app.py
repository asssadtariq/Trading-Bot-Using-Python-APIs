'''
    importing packages needed for the app
'''

from tkinter import messagebox
import tkinter
from Bot import bot
from tkinter import *
import csv

root = Tk()
root.title("Trading with Capital.com")
root.geometry("525x625")
root.minsize(525,625)
root.maxsize(525,625)

# Creating Widgets

api_key_label = Label(root, text="Enter API Key")
api_key_e = Entry(root, width=50, borderwidth=5)

identifier_lable = Label(root, text="Enter Identifier")
identifier = Entry(root, width=50, borderwidth=5)

password_label = Label(root, text="Enter Password")
password = Entry(root, width=50, borderwidth=5)
    
direction_label = Label(root, text="Enter Direction")
direction_entry = Entry(root, width=50, borderwidth=5)
direction_entry.insert(0, "BUY")

epic_label = Label(root, text="Enter Epic")
epic_entry = Entry(root, width=50, borderwidth=5)

size_label = Label(root, text="Enter Size")
size_entry = Entry(root, width=50, borderwidth=5)

stopDistance_label = Label(root, text="Enter stopDistance")
stopDistance_entry = Entry(root, width=50, borderwidth=5)

limitDistance_label = Label(root, text="Enter limitDistance")
limitDistance_entry = Entry(root, width=50, borderwidth=5)


def trade_now():
    user_apiKey = api_key_e.get()
    user_id = identifier.get()
    user_pass = password.get()
    
    if len(user_apiKey) == 0 or len(user_id) == 0 or len(user_pass) == 0:
        messagebox.showwarning("Incomplete Credentials!", "Please Enter Complete Information")
        return
    
    direction = direction_entry.get()
    if direction != "BUY" and direction != "SELL":
        messagebox.showwarning("Wrong Value", "Direction can be BUY or SELL only")
        return         
    
    epic = epic_entry.get()
    
    size = size_entry.get()
    try:
        x = int(size)
    except:
        messagebox.showwarning("Wrong Value", "Size must be a number")
        return         
        
    stopDistance = stopDistance_entry.get()
    try:
        x = int(stopDistance)
    except:
        messagebox.showwarning("Wrong Value", "Stop Distance must be a number")
        return         
    
    limitDistance = limitDistance_entry.get()
    try:
        x = int(limitDistance)
    except:
        messagebox.showwarning("Wrong Value", "Limit Distance must be a number")
        return         
    
    if len(direction) == 0 or len(epic) == 0 or len(size) == 0 or len(stopDistance) == 0 or len(limitDistance) == 0:
        messagebox.showwarning("Incomplete Parameters!", "Please Enter Again All Values")
        return
    
    data = {
        'direction': direction,
        'epic': epic,
        'size': size,
        'stopDistance': stopDistance,
        'limitDistance': limitDistance
    }
    
    try:
        trade_bot = bot.Bot(user_id, user_pass, user_apiKey)
        connection_status_code = trade_bot.make_connection()
        if connection_status_code == 200:
            try:
                trade_status_code = trade_bot.make_trade(data_dict=data)
                if trade_status_code == 200:
                    messagebox.showinfo("Successful", "Trade has been set successfully")
                else:
                    if trade_status_code == -1:
                        messagebox.showwarning("Failure", "Size Value is too low for this Epic!")
                    else:                      
                        messagebox.showwarning("Failure", "Operation Failed Due to " + str(trade_status_code))

            except Exception:
                messagebox.showerror("Error in Trading | " + str(Exception), "Problem with Parameters! Try agin")       
        else:
            messagebox.showwarning("Failure", "Operation Failed Due to " + str(connection_status_code))

    except Exception:
        messagebox.showerror("Error in Making Connection | " + str(Exception), "API KEY, Identifier or Password is incorrect")       

def autoFill():
    filename = "userData.csv"
    file = open("Bot/"+filename)
    csv_reader = csv.reader(file)
    
    try:
        userData = csv_reader
        userData = next(userData)
        if len(userData) != 0:
            api_key_e.insert(0, userData[0])
            identifier.insert(0, userData[1])
            password.insert(0, userData[2])
        else:
            messagebox.showwarning("No data", "User data not saved")
    except:
        messagebox.showerror("No data", "User data not saved")

    
def saveInformtaion():
    user_apiKey = api_key_e.get()
    user_id = identifier.get()
    user_pass = password.get()    
    
    if len(user_apiKey) == 0 or len(user_id) == 0 or len(user_pass) == 0:
        messagebox.showwarning("Incomplete Data!", "Cannot Save User Data! Please Enter Complete Information")
        return

    filename = "userData.csv"
    with open("Bot/"+filename, "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([user_apiKey, user_id, user_pass])        
        
def reset_fields():
    api_key_e.delete(0, END)
    identifier.delete(0, END)
    password.delete(0, END)
    direction_entry.delete(0, END)
    epic_entry.delete(0, END)
    size_entry.delete(0, END)
    stopDistance_entry.delete(0, END)
    limitDistance_entry.delete(0, END)
        
def main():
    trade_btn = Button(root, text="TRADE NOW",command=trade_now, width=20, bg="black", fg="white")
    exit_btn = Button(root, text="EXIT", command=root.quit, width=20, bg="black", fg="white")
    reset_btn = Button(root, text="RESET", command=reset_fields, width=20, bg="black", fg="white")
    autofill_btn = Button(root, text="AUTO FILL", command=autoFill, width=10, bg="black", fg="white")
    saveInfo_btn = Button(root, text="SAVE DATA", command=saveInformtaion, width=10, bg="black", fg="white")
    
    # Displaying Widgets
    
    api_key_label.pack(pady=4)    
    api_key_e.pack(pady=4)

    identifier_lable.pack(pady=4)    
    identifier.pack(pady=4)

    password_label.pack(pady=4)    
    password.pack(pady=4)

    direction_label.pack(pady=4)
    direction_entry.pack(pady=4)

    epic_label.pack(pady=4)
    epic_entry.pack(pady=4)

    size_label.pack(pady=4)
    size_entry.pack(pady=4)

    stopDistance_label.pack(pady=4)
    stopDistance_entry.pack(pady=4)

    limitDistance_label.pack(pady=4)
    limitDistance_entry.pack(pady=4)

    autofill_btn.pack(pady=4, side=tkinter.LEFT)
    saveInfo_btn.pack(pady=4, side=tkinter.RIGHT)
    trade_btn.pack(pady=4)
    reset_btn.pack(pady=4)
    exit_btn.pack(pady=4)

    root.mainloop()
    
if __name__ == '__main__':
    main()