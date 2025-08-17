import customtkinter

from services.file_service import FileService

class App(customtkinter.CTk):
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 350
    WINDOW_TITLE = "Valheim Backup Utility"
    
    def __init__(self):
        super().__init__()
        self._configure_window()
        self.radio_var = customtkinter.IntVar(master=self, value=0)
        self._create_widgets()
        self._layout_widgets()
        
    def _configure_window(self):
        """Configure the main window."""
        self.title(self.WINDOW_TITLE)
        self.geometry(f"{self.WINDOW_HEIGHT}x{self.WINDOW_WIDTH}+800+400")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

    def _create_widgets(self):
        """Create all widgets used in the application."""
        self.radio_download = customtkinter.CTkRadioButton(
            self,
            text="Download (Start of session)",
            variable=self.radio_var,
            value=1,
        )
        self.radio_upload = customtkinter.CTkRadioButton(
            self,
            text="Upload (End of session)",
            variable=self.radio_var,
            value=2,
        )
        self.button_start = customtkinter.CTkButton(self, text="Start", command=self.on_start_button_click)
        self.frame_config = customtkinter.CTkFrame(self)
        self.frame_status = customtkinter.CTkFrame(self)
        
    def _layout_widgets(self):
        """Arrange widgets in the application window."""
        self.radio_download.grid(row=0, column=0, padx=20, pady=(15, 5), ipady=10, sticky="we")
        self.radio_upload.grid(row=1, column=0, padx=20, pady=(5, 15), ipady=10, sticky="we")
        self.button_start.grid(row=2, column=1, padx=20, pady=15, ipady=10, sticky="w")
        self.frame_config.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nse")
        self.frame_status.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nswe")
    
    def on_start_button_click(self):
        """Handle the Start button click event."""
        action = self.radio_var.get()
        if action == 1:
            FileService.sync_files('download')
        elif action == 2:
            FileService.sync_files('upload')
        else:
            return None
    
# run the application
def run():
    app = App()
    app.mainloop()
