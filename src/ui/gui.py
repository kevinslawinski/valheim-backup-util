import customtkinter

from services.file_service import FileService

class App(customtkinter.CTk):
    window_width = 600
    window_height = 300
    window_title = "Valheim Backup Utility"
    
    def __init__(self):
        super().__init__()

        # Window config
        self.title(self.window_title)
        self.geometry(f"{self.window_width}x{self.window_height}+800+400")
        self.minsize(self.window_width, self.window_height)
        self.maxsize(self.window_width, self.window_height)
        self.grid_columnconfigure((0, 1), weight=1)

        # Inputs 
        self.radio_var = customtkinter.IntVar(master=self, value=0)
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
        start_button = customtkinter.CTkButton(self, text="Start", command=self.button_callback)
        
        # Layout
        radio_download.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        radio_upload.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        start_button.grid(row=3, column=0, padx=20, pady=20, sticky="e")
        
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
