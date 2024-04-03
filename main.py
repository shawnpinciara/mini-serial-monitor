import customtkinter as tk
import serial
import sys
import glob
import serial_functions as sf

app = tk.CTk()
app.title("Mini Serial Monitor")
app.geometry("600x400")
app.grid_columnconfigure(0, weight=1) #add grid
tk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
tk.set_appearance_mode("light")
read = False
prova = "hey"
ser = serial.Serial()

def serial_connect(choice):
    ser.port = choice
    try:
        ser.open()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print(ser)

def serial_baud(choice):
    ser.baudrate = int(choice)
    try:
        ser.open()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print(ser)

def print_serial_list():
    print(sf.serial_ports())

def read_messages():
    #read = not read
    if read:
        read = False
    else:
        read = True
    print(read)



def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

def checkbox_event():
    print("checkbox toggled, current value:", check_csv_var.get())

#layout

#col1
setup_frame = tk.CTkFrame(app)
setup_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

portList = tk.CTkOptionMenu(setup_frame, values=[v for v in sf.serial_ports()],command=serial_connect)
portList.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

baudList = tk.CTkOptionMenu(setup_frame, values=["9600","31250","115200"],command=serial_baud)
baudList.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

check_csv_var = tk.StringVar(value="off")
check_csv = tk.CTkCheckBox(setup_frame, text="CSV format", command=checkbox_event,
                                     variable=check_csv_var, onvalue="on", offvalue="off")
check_csv.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

button = tk.CTkButton(setup_frame, text="Read", command=read_messages)
button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
#col2
read_frame = tk.CTkFrame(app)
read_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

textbox = tk.CTkTextbox(master=read_frame, width=400, corner_radius=0,font = ("Arial", 20))
textbox.grid(row=0, column=1, sticky="nsew")
textbox.insert("0.0", "Some example text!\n")
app.mainloop()