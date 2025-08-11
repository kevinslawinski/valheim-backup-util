import customtkinter

from services.file_service import FileService

class App(customtkinter.CTk):
    window_width = 700
    window_height = 350
    window_title = "Valheim Backup Utility"
    
    def __init__(self):
        super().__init__()

        # Window config
        self.title(self.window_title)
        self.geometry(f"{self.window_width}x{self.window_height}+800+400")
        # self.minsize(self.window_width, self.window_height)
        # self.maxsize(self.window_width, self.window_height)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Variables 
        self.radio_var = customtkinter.IntVar(master=self, value=0)
        
        # Assets
        radio_download = customtkinter.CTkRadioButton(
            self,
            text="Download (Start of session)",
            variable=self.radio_var,
            value=1,
        )
        radio_upload = customtkinter.CTkRadioButton(
            self,
            text="Upload (End of session)",
            variable=self.radio_var,
            value=2,
        )
        button_start = customtkinter.CTkButton(self, text="Start", command=self.button_callback)
        frame_config = customtkinter.CTkFrame(self)
        frame_status = customtkinter.CTkFrame(self)
        
        # Layout
        radio_download.grid(row=0, column=0, padx=20, pady=(15, 5), ipady=10, sticky="we")
        radio_upload.grid(row=1, column=0, padx=20, pady=(5, 15), ipady=10, sticky="we")
        button_start.grid(row=2, column=1, padx=20, pady=15, ipady=10, sticky="w")
        
        frame_config.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nse")
        
        frame_status.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nswe")
        
    # functions
    def button_callback(self):
        action = self.get_action()
        if action == 1:
            FileService.sync_files('download')
        elif action == 2:
            FileService.sync_files('upload')
        else:
            return None
    
    def get_action(self):
        return self.radio_var.get()

# run the application
def run():
    app = App()
    app.mainloop()
