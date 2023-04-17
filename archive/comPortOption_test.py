import tkinter as tk
import serial.tools.list_ports as port_list

class SerialGUI:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Serial Port Selector")
        self.master.geometry("300x200")
        
        self.port_label = tk.Label(self.master, text="Select Serial Port:")
        self.port_label.pack(pady=10)
        
        self.port_variable = tk.StringVar()
        self.port_variable.set("PORT")
        
        try:
            self.port_option_menu = tk.OptionMenu(self.master, self.port_variable, self.get_serial_ports)
            self.port_option_menu.pack()
        except:
            pass
        
        self.apply_button = tk.Button(self.master, text="Apply", command=self.apply_port)
        self.apply_button.pack(pady=20)
        
    @property
    def get_serial_ports(self):
        ports = []
        for port in port_list.comports():
            ports.append(port.device)
            print(port)
        return ports
    
    def apply_port(self):
        selected_port = self.port_variable.get()
        print("Selected port: " + selected_port)
        # Insert code here to update your Arduino communication code with the selected port
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()
