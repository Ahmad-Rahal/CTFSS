import customtkinter as ctk
from tkinter import messagebox
from udp_server import UDP_Server
from team_progress_gui import Team_Progress_GUI


class GUI:
    def __init__(self):
        self.udp_server = None
        self.teamFrames = {}
        self.runningFlag = False
        self.team_progress_gui = None
        self.etape_descriptions = {
            0: "Initial stage",
            1: "Scan of the machine",
            2: "Access to the backend site web",
            3: "Access to the backend user account",
            4: "Become admin in backend site web",
            5: "Attack through FTP",
            6: "Connection through SSH",
            7: "Become root",
            8: "Access to the DB"
        }
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        # Configure window
        self.root.geometry("1100x600")
        self.root.minsize(1100, 600)
        self.root.title("Capture The Flag GUI")
        self.root.protocol("WM_DELETE_WINDOW", self.closeProgram)

        self.runningFlag = True
        self.remove_message_flag = False

        self.server_state = ctk.BooleanVar()
        self.server_state.set(False)
        
        self.socket_state_flag = ctk.BooleanVar()
        self.socket_state_flag.set(False)

        self.chk_Ethernet_var = ctk.IntVar()
        self.chk_AutoIP_var = ctk.IntVar()
        self.new_team = ctk.BooleanVar()
        self.new_team.set(False)

        # Configure grid layout (1x2) (rowsxcolumns)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=10)
        self.root.rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(master=self.root)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.columnconfigure(0, weight=1)
        # self.sidebar_frame.rowconfigure((0, 1, 2, 3, 4, 5, 7, 8, 9), weight=1)
        # self.sidebar_frame.rowconfigure((7), weight=10)

        self.menu = ctk.CTkLabel(master=self.sidebar_frame, text="Configuration Menu",
                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.menu.grid(row=0, column=0, sticky="news", pady=10)


        # Create another frame to display server variables
        self.server_frame = ctk.CTkFrame(master=self.sidebar_frame, fg_color="#212121")
        self.server_frame.grid(row=1, column=0, sticky="ns")
        self.server_frame.columnconfigure(0, weight=1)
        self.server_frame.columnconfigure(1, weight=1)
        
        self.lbl_ServerStatus = ctk.CTkLabel(master=self.server_frame, text="Server Status:  OFF", anchor="w", width=70)
        self.lbl_ServerStatus.grid(row=0, column=0, sticky="snw",columnspan=2, pady=(15,0))

        self.lbl_ServerIP = ctk.CTkLabel(master=self.server_frame, text="IP Address: ", anchor="w")
        
        self.entry_ServerIP = ctk.CTkEntry(master=self.server_frame, width=120, placeholder_text="192.168.31.65")

        self.lbl_ServerPort = ctk.CTkLabel(master=self.server_frame, text="Port: ", anchor="w", width=70)
        self.lbl_ServerPort.grid(row=2, column=0, sticky="nsw", pady=(15,0))

        self.entry_ServerPort = ctk.CTkEntry(master=self.server_frame, width=120, placeholder_text="9999")
        self.entry_ServerPort.grid(row=2, column=1, sticky="w",pady=(15,0) )
        
        self.Ip_combobox = ctk.CTkComboBox(master=self.server_frame, values=["Detect IPv4","Ethernet", "Custom"], command=self.combobox_callback)
        self.Ip_combobox.grid(row=3, column=0, sticky="we", pady=(40,0), columnspan=2)
        
        self.btn_start_server = ctk.CTkButton(master=self.server_frame, text="Start Server", font=ctk.CTkFont(size=16),
                                              command=self.start_server)
        self.btn_start_server.grid(row=4, column=0, sticky="ew", pady=(15,0), columnspan=2)
        
        self.btn_reset_settings = ctk.CTkButton(master=self.server_frame, text="Reset Settings",
                                                command=self.reset_program, font=ctk.CTkFont(size=16))
        
        self.interface_switch = ctk.CTkSwitch(master=self.server_frame, text="Team Interface")
        
        self.btn_interface = ctk.CTkButton(master=self.server_frame, text="Team Interface",
                                           command=self.show_team_progress_gui, font=ctk.CTkFont(size=16))
        self.btn_interface.grid(row=5, column=0, sticky="ew", pady=(250, 10), columnspan=2)

        # create scrollable frame to display team info
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self.root, label_text="Teams State")
        self.scrollable_frame.grid(row=0, column=1, padx=(15, 15), pady=(15, 15), sticky="nsew")
        self.scrollable_frame.columnconfigure(0, weight=2)
        

        self.update_gui()

        self.root.mainloop()


    def combobox_callback(self,value):
        self.chk_Ethernet_var.set(False)
        self.chk_AutoIP_var.set(False)
        self.lbl_ServerIP.grid_forget()
        self.entry_ServerIP.grid_forget()  
        if value == "Detect IPv4":
            self.chk_AutoIP_var.set(True)
        elif value == "Ethernet":
            self.chk_AutoIP_var.set(True)
            self.chk_Ethernet_var.set(True)
        elif value == "Custom":
            self.lbl_ServerIP.configure(text="IP Address: ")
            self.lbl_ServerIP.grid(row=1, column=0, sticky="nws", pady=(15,0))
            self.entry_ServerIP.grid(row=1, column=1, sticky="w", pady=(15,0))
    
    def start_server(self):
        if self.entry_ServerPort.get().strip():
            if self.Ip_combobox.get() == "Custom":    
                if self.entry_ServerIP.get().strip():
                    self.udp_server = UDP_Server(server_port=int(self.entry_ServerPort.get()),
                                                 server_ip=self.entry_ServerIP.get(),
                                                 net_mode=net_mode)
                else:
                    messagebox.askokcancel("Attention", "Please enter an IP address")
            elif self.Ip_combobox.get() == "Ethernet":
                net_mode = "ETH"
                self.udp_server = UDP_Server(server_port=int(self.entry_ServerPort.get()), server_ip="AUTO",
                                             net_mode=net_mode)
            elif self.Ip_combobox.get() == "Detect IPv4":
                net_mode = "INET"
                self.udp_server = UDP_Server(server_port=int(self.entry_ServerPort.get()), server_ip="AUTO",
                                             net_mode=net_mode)
        else:
            messagebox.askokcancel("Attention", "Please enter a port")
            
        if self.udp_server:
            if self.udp_server.socket_run_flag: 
                self.update_sidebar_frame()

            
        
    def update_sidebar_frame(self):
        if self.udp_server.socket_run_flag:
            self.lbl_ServerStatus.configure(text="Server Status:  ON", text_color="green")
            self.lbl_ServerIP.grid(row=1, column=0, sticky="nws", pady=(8,0))
            self.lbl_ServerPort.grid(row=2, column=0, sticky="nsw", pady=(8,0))
            self.lbl_ServerIP.configure(text=f"IP Address:  {self.udp_server.server_ip}")
            self.lbl_ServerPort.configure(text=f"Port:  {self.udp_server.server_port}")
            self.btn_reset_settings.grid(row=3, column=0, sticky="we", pady=(40,0))
            self.entry_ServerIP.grid_forget()
            self.entry_ServerPort.grid_forget()
            self.btn_start_server.grid_forget()
            self.Ip_combobox.grid_forget()
        else:
            self.lbl_ServerStatus.configure(text="Server Status:  OFF", text_color="white")
            self.lbl_ServerPort.configure(text=f"Port: ")
            self.entry_ServerPort.grid(row=2, column=1, sticky="w",pady=(15,0) )
            self.btn_start_server.grid(row=4, column=0, sticky="ew", pady=(20,0), columnspan=2)
            self.Ip_combobox.grid(row=3, column=0, sticky="we", pady=(40,0), columnspan=2)
            self.btn_reset_settings.grid_forget()
            self.combobox_callback(self.Ip_combobox.get())
            
            
    def reset_program(self): 
        for ipAddress in self.udp_server.clients:
            self.teamFrames[ipAddress]['team_frame'].grid_forget()
        self.udp_server.clients.clear()
        self.teamFrames.clear()
        self.udp_server.socket.close()
        self.udp_server.socket_run_flag = False
        self.update_sidebar_frame()
        
        


    def update_gui(self):
        if self.udp_server:
            if self.udp_server.new_client:
                self.new_team.set(True)
                self.udp_server.new_client = False

        if self.new_team.get():
            # Add new team frame
            self.add_Team_Frame()
            self.new_team.set(False)
        
        if self.udp_server:
            for ip_address, team_frame in self.teamFrames.items():
                team_frame['etape_label'].configure(text=f"Etape: {str(self.udp_server.clients[ip_address]['etape'])} - "
                                                         f"{self.etape_descriptions[int(self.udp_server.clients[ip_address]['etape'])]}")
                team_frame['time_label'].configure(text=f"Time elapsed: {self.udp_server.clients[ip_address]['time']}")

        self.root.after(1000, self.update_gui)

    def add_Team_Frame(self):
        # Get the new team based on the max team number
        new_team = list(self.udp_server.clients.items())[-1]
        frame = {}

        team_frame = ctk.CTkFrame(master=self.scrollable_frame, fg_color="#363636", corner_radius=7)
        team_frame.grid(column=0, padx=20, pady=10, sticky="nswe")
        team_frame.columnconfigure((0, 1), weight=2)
        team_frame.columnconfigure((2, 3), weight=1)

        team_label = ctk.CTkLabel(master=team_frame, font=(tuple, 14), anchor="w",
                                  text=f"Team: {new_team[1]['team_num']}")
        team_label.grid(row=0, column=0, padx=(25, 0), sticky="nswe")

        ip_label = ctk.CTkLabel(master=team_frame, font=(tuple, 14), anchor="w", text=f"IP: {new_team[0]}")
        ip_label.grid(row=1, column=0, padx=(25, 0), sticky="nswe")

        etape_label = ctk.CTkLabel(master=team_frame, font=(tuple, 14), anchor="w", width=290)
        etape_label.grid(row=0, column=1, padx=(5, 0), sticky="nswe")

        time_label = ctk.CTkLabel(master=team_frame, font=(tuple, 14), anchor="w")
        time_label.grid(row=1, column=1, padx=(5, 0), sticky="nswe")

        remove_button = ctk.CTkButton(master=team_frame, text="Remove", command=lambda: self.remove_team(new_team[0]))
        remove_button.grid(row=0, column=2, pady=(5, 2), padx=0, sticky="nse")

        dbreset_button = ctk.CTkButton(master=team_frame, text="Reset DB", command=lambda: self.reset_db(new_team[0]))
        dbreset_button.grid(row=1, column=2, pady=(2, 5), padx=0, sticky="nse")

        self.teamFrames[new_team[0]] = {'team_frame': team_frame, 'etape_label': etape_label,
                                        'time_label': time_label}

    def remove_team(self, ip_address):
        if messagebox.askyesno("Confirmation", "Do you really want to remove the team?"):
                print(f"Removing IP: {ip_address}")
                self.teamFrames[ip_address]['team_frame'].grid_forget()
                if self.team_progress_gui:
                    self.team_progress_gui.remove_team()
                del self.teamFrames[ip_address]
                del self.udp_server.clients[ip_address]

    def reset_db(self, ip_address):
        print(f"Resetting DB asociated to {ip_address}")
        self.udp_server.send_message("reset_db", ip_address)

    def show_team_progress_gui(self):   
        self.team_progress_gui = Team_Progress_GUI(self)
        self.team_progress_gui.create_GUI()
     
    def closeProgram(self):
        if messagebox.askyesno("Confirmation", "Do you want to close program?"):
            self.runningFlug = False
            self.root.destroy()
     