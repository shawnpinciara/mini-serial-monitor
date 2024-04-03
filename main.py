import customtkinter as tk
import serial
import sys
import glob
import serial_functions as sf
import threading as thread
import time

app = tk.CTk()
app.title("Mini Serial Monitor")
app.geometry("600x400")
app.grid_columnconfigure(0, weight=1) #add grid
tk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
tk.set_appearance_mode("light")
read = False
prova = "hey"
ser = serial.Serial(timeout=1)

def serial_connect(choice):
    ser.port = choice
    try:
        ser.open()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print_screen(ser)

def serial_baud(choice):
    ser.baudrate = int(choice)
    try:
        ser.open()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print_screen(ser)

def print_serial_list():
    print(sf.serial_ports())

def read_messages():
    global read
    read = not read
    if read:
        button.configure(text="Stop",fg_color="#ab0000",hover_color="#ab0000")
    else:
        button.configure(text="Read",fg_color="#00ab4d",hover_color="#00ab4d")
    print(read)
    thread.Thread(target=read_serial).start()

def read_serial():
    global read
    while read:
        #print("reading")
        textbox.delete("0.0", "end")  # delete all text
        textbox.insert("0.0", ser.readline())
        time.sleep(200/1000)

def optionmenu_callback(choice):
    print_screen("optionmenu dropdown clicked:", choice)

def checkbox_event():
    print_screen("checkbox toggled, current value:", check_csv_var.get())

def print_screen(str_to_print):
    textbox_log.delete("0.0", "end")  # delete all text
    textbox_log.insert("0.0", str_to_print)

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

button = tk.CTkButton(setup_frame, text="Read", command=read_messages,fg_color="#00ab4d",hover_color="#00ab4d")
button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
#col2
read_frame = tk.CTkFrame(app)
read_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

textbox = tk.CTkTextbox(master=read_frame, width=400, corner_radius=0,font = ("Arial", 20),fg_color="transparent")
textbox.grid(row=0, column=1, sticky="nsew")
textbox.insert("0.0", "Some example text!\n")

#row 2
log_frame = tk.CTkFrame(app)
log_frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsw",columnspan=2)
textbox_log = tk.CTkTextbox(master=log_frame, width=700, corner_radius=0,font = ("Arial", 15),fg_color="transparent",wrap='char')
textbox_log.grid(row=0, column=1, sticky="sw")
textbox_log.insert("0.0", "Some example text!\n")

app.mainloop()