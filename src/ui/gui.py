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
        self.status_text = customtkinter.StringVar(value="Ready")
        self._create_widgets()
        self._layout_widgets()
        
    def _configure_window(self):
        """Configure the main window."""
        self.title(self.WINDOW_TITLE)
        self.geometry(f"{self.WINDOW_HEIGHT}x{self.WINDOW_WIDTH}+800+400")
        # self.grid_columnconfigure((0, 1, 2), weight=1)
        # self.grid_rowconfigure((0, 1, 2, 3), weight=1)

    def _create_widgets(self):
        """Create all widgets used in the application."""
        self.frame_top = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_actions = customtkinter.CTkFrame(self, border_width=1)
        self.frame_config = customtkinter.CTkFrame(self, border_width=1)
        self.frame_status = customtkinter.CTkFrame(self, border_width=1)
        self.radio_download = customtkinter.CTkRadioButton(
            self.frame_actions,
            text="Download (Start of session)",
            variable=self.radio_var,
            value=1,
        )
        self.radio_upload = customtkinter.CTkRadioButton(
            self.frame_actions,
            text="Upload (End of session)",
            variable=self.radio_var,
            value=2,
        )
        self.button_start = customtkinter.CTkButton(
            self.frame_actions, 
            text="Start", 
            command=self.on_start_button_click
            )
        self.label_status = customtkinter.CTkLabel(
            self.frame_status, 
            textvariable=self.status_text, 
            font=("Arial", 14)
            )
        self.label_config = customtkinter.CTkLabel(
            self.frame_config,
            text="Configuration",
            font=("Arial", 16, "bold")
        )
        
    def _layout_widgets(self):
        """Arrange widgets in the application window."""
        # Pack frames
        self.frame_top.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 5))
        self.frame_actions.pack(in_=self.frame_top, side="left", fill="both", padx=(0, 5))
        self.frame_config.pack(in_=self.frame_top, side="right", fill="both", expand=True, padx=(5, 0))
        self.frame_status.pack(side="bottom", fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Pack action widgets for frame_actions
        self.radio_download.pack(padx=20, pady=(15, 5), fill="x")
        self.radio_upload.pack(padx=20, pady=(5, 15), fill="x")
        self.button_start.pack(padx=20, pady=15, anchor="s")

        # Pack labels
        self.label_status.pack(padx=10, pady=10, anchor="w") # Status label
        self.label_config.pack(padx=10, pady=10, anchor="n") # Configuration label
    
    def on_start_button_click(self):
        """Handle the Start button click event."""
        action = self.radio_var.get()
        if action == 1:
            self.status_text.set("Downloading files...")
            FileService.sync_files('download')
            self.status_text.set("Download complete!")
        elif action == 2:
            self.status_text.set("Uploading files...")
            FileService.sync_files('upload')
            self.status_text.set("Upload complete!")
        else:
            self.status_text.set("Please select an action.")
            return None
    
# Run the application
def run():
    app = App()
    app.mainloop()
