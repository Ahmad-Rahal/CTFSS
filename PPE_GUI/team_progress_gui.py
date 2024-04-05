import customtkinter as ctk
from tkinter import messagebox

class Team_Progress_GUI:
    def __init__(self, configuration_gui):
        self.frames = None
        self.root = None
        self.configuration_gui = configuration_gui

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

    def create_GUI(self):
        self.frames = {}

        self.root = ctk.CTkToplevel()
        self.root.configure()
        self.root.title("Progress show")
        self.root.geometry("700x400")
        self.root.minsize(700, 400)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.protocol("WM_DELETE_WINDOW", self.closeShow)

 
        self.messageBoxFlug = False 
         
        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=2)

        lbl_team_title = ctk.CTkLabel(self.root, text="Team", font=ctk.CTkFont(size=25))
        lbl_team_title.grid(row=0, column=0, sticky="nswe", pady=(5,0))
        lbl_etape_title = ctk.CTkLabel(self.root, text="Level", font=ctk.CTkFont(size=25), width=290)
        lbl_etape_title.grid(row=0, column=1, sticky="nswe", pady=(5,0))
        lbl_progress_title = ctk.CTkLabel(self.root, text="Progress", font=ctk.CTkFont(size=25))
        lbl_progress_title.grid(row=0, column=2, sticky="nsew", pady=(5,0))
          
        self.update_gui()
        self.root.focus()

    def add_team(self, difference):
        for index in range(difference):
            self.oldNumberOfTeam = len(self.frames)
            team_label = ctk.CTkLabel(self.root, text=f"", font=("tuple", 17), height=10)
            team_label.grid(row=self.oldNumberOfTeam+1, column=0, sticky="")
    
            level_label = ctk.CTkLabel(self.root, text="", font=("tuple", 17))
            level_label.grid(row=self.oldNumberOfTeam+1, column=1, sticky="nswe")
    
            progress_bar = ctk.CTkProgressBar(self.root, mode="determinate", height=10, width=5)
            progress_bar.grid(row=self.oldNumberOfTeam+1, column=2, sticky="nswe", pady=10, padx=(20, 20))
    
            self.frames[self.oldNumberOfTeam] = {"level_label": level_label,
                                              "progress_bar": progress_bar, 'team_label':team_label}

    def remove_team(self):
        self.frames_last_index = len(self.frames)-1
        self.frames[self.frames_last_index]['level_label'].grid_forget()
        self.frames[self.frames_last_index]['progress_bar'].grid_forget()
        self.frames[self.frames_last_index]['team_label'].grid_forget()
        del self.frames[self.frames_last_index]

        
    def update_gui(self):
        if self.configuration_gui.udp_server:
            if self.configuration_gui.udp_server.socket_run_flag:
                self.difference = len(self.configuration_gui.udp_server.clients) - len(self.frames)
                if self.difference:
                    self.add_team(self.difference)
                for index, (ip_address, data) in enumerate(self.configuration_gui.udp_server.clients.items()):
                    self.frames[index]['team_label'].configure(text=f'{data["team_num"]}')
                    self.frames[index]['level_label'].configure(
                        text=f'{self.configuration_gui.etape_descriptions[int(data["etape"])]}')
                    self.frames[index]['progress_bar'].set(int(data['etape']) / 8)
                    
        self.root.after(1000, self.update_gui)
        
        
    def closeShow(self):
        if not self.messageBoxFlug:
            self.messageBoxFlug =True
            if messagebox.askyesno("Confirmation", "Do you want to close the show ?"):
                self.root.destroy()
                self.frames.clear()
            else:
                self.messageBoxFlug = False