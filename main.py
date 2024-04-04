import customtkinter as tk
import serial
import sys
import glob
import serial_functions as sf
import threading as thread
import time

app_x: int = 700
app_y: int = 400
app = tk.CTk()
app.title("Mini Serial Monitor")
app.geometry(str(app_x)+"x"+str(app_y))
app.grid_columnconfigure(0, weight=1) #add grid
tk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
tk.set_appearance_mode("light")
read: bool = False
csv_option: bool = False
prova: str = "hey"
ser = serial.Serial(timeout=1)
ser.port = "COM1"
ser.baudrate = 9600
scan_freq: int = 200

def serial_port(choice):
    ser.port = choice
    print_screen(ser)

def serial_baud(choice):
    ser.baudrate = int(choice)
    print_screen(ser)

def set_scan_freq(f):
    global scan_freq
    scan_freq = f

def print_serial_list():
    print(sf.serial_ports())

def read_messages():
    global read
    read = not read
    ss = scan_freq_entry.get()
    if len(ss.strip())!=0:
        set_scan_freq(ss)
    else:
        set_scan_freq(200)
    if read:
        button.configure(text="Stop",fg_color="#ab0000",hover_color="#ab0000")
        setup_frame.configure(border_width=3,border_color="#00ab4d")
        connect()
    else:
        button.configure(text="Connect",fg_color="#00ab4d",hover_color="#00ab4d")
        setup_frame.configure(border_width=0)
        disconnect()
    thread.Thread(target=read_serial).start()

def connect() -> None:
    try:
        ser.open()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print_screen(ser)

def disconnect() -> None:
    try:
        ser.close()
    except BaseException as e:
        print('Failed to do something: ' + str(e))
    print_screen(ser)

def read_serial():
    global read
    global csv_option
    global scan_freq
    while read:
        textbox.delete("0.0", "end")  # delete all text
        if not csv_option:
            textbox.insert("0.0", ser.readline())
        else:
            try:
                lista = ser.readline().replace('\n','').replace('\t','').replace("'",'').split(',')
                print_screen(lista)
                for el in lista:
                    textbox.insert("0.0", str(el) + "\n")
            except BaseException as e:
                print('Failed to do something: ' + str(e))
            
        time.sleep(int(scan_freq)/1000)

def optionmenu_callback(choice):
    print_screen("optionmenu dropdown clicked:", choice)

def checkbox_event():
    global csv_option
    csv_option = bool(check_csv_var.get())
    print_screen("CSV division:" + str(check_csv_var.get()))

def print_screen(str_to_print):
    textbox_log.delete("0.0", "end")  # delete all text
    textbox_log.insert("0.0", str_to_print)

#layout

#col1
setup_frame = tk.CTkFrame(app)
setup_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

portList = tk.CTkOptionMenu(setup_frame, values=[v for v in sf.serial_ports()],command=serial_port)
portList.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

baudList = tk.CTkOptionMenu(setup_frame, values=["9600","31250","115200"],command=serial_baud)
baudList.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

check_csv_var = tk.StringVar(value="False")
check_csv = tk.CTkCheckBox(setup_frame, text="CSV format", command=checkbox_event,
                                     variable=check_csv_var, onvalue="True", offvalue="False")
check_csv.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

scan_freq_entry = tk.CTkEntry(setup_frame, placeholder_text="Scan freq (ms)")
scan_freq_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

button = tk.CTkButton(setup_frame, text="Connect", command=read_messages,fg_color="#00ab4d",hover_color="#00ab4d")
button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

#col2
read_frame = tk.CTkFrame(app)
read_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

textbox = tk.CTkTextbox(master=read_frame, width=400, corner_radius=0,font = ("Arial", 20),fg_color="transparent")
textbox.grid(row=0, column=1, sticky="nsew")
textbox.insert("0.0", "Serial stream here!\n")

#row 2
log_frame = tk.CTkFrame(app)
log_frame.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="nsw",columnspan=2)
textbox_log = tk.CTkTextbox(master=log_frame, width=700, corner_radius=0,font = ("Arial", 15),fg_color="transparent",wrap='char')
textbox_log.grid(row=0, column=1, sticky="sw")
textbox_log.insert("0.0", "Console\n")

if __name__=='__main__':
    app.mainloop()