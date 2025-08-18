import customtkinter
import logging
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from services.file_service import FileService


class TextHandler(logging.Handler):
    """Logging handler that writes log records to a Tkinter Text/ScrolledText widget.

    Uses widget.after(...) to ensure UI updates happen on the main thread.
    """
    def __init__(self, text_widget: ScrolledText):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record) + '\n'
            # Schedule UI update on main thread
            self.text_widget.after(0, self._append, msg)
        except Exception:
            self.handleError(record)

    def _append(self, msg: str) -> None:
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

class App(customtkinter.CTk):
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 350
    WINDOW_TITLE = "Valheim Backup Utility"
    
    def __init__(self):
        super().__init__()
        self._configure_window()
        self.radio_var = customtkinter.IntVar(master=self, value=0)
        self.status_text = customtkinter.StringVar(value="Ready")

        # create UI widgets and layout
        self._create_widgets()
        self._layout_widgets()

        # set up GUI logging handler after widgets are created
        self._setup_gui_logging()
        
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
        # status area: use a ScrolledText widget to show live logs
        # create a standard Tk ScrolledText because customtkinter may not expose scrolling behavior
        self.log_widget = ScrolledText(self.frame_status, state='disabled', wrap='word', height=8)
        # optional small label showing a short status message
        self.label_status = customtkinter.CTkLabel(
            self.frame_status,
            textvariable=self.status_text,
            font=("Arial", 12),
        )
        self.label_config = customtkinter.CTkLabel(
            self.frame_config,
            text="Configuration",
            font=("Arial", 16, "bold")
        )

        # keep a reference to the GUI log handler so we can remove it later if needed
        self._gui_log_handler = None

    def _setup_gui_logging(self):
        """Attach a logging.Handler that writes into the log_widget and preload existing log file."""
        root_logger = logging.getLogger()
        # create handler and formatter matching app log format (no ANSI colors)
        handler = TextHandler(self.log_widget)
        fmt = '%(asctime)s - %(name)s - [%(levelname)s]: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)
        self._gui_log_handler = handler

        # preload existing log file into the widget if it exists
        try:
            with open('app.log', 'r', encoding='utf-8') as f:
                contents = f.read()
            if contents:
                # insert contents on the main thread
                self.log_widget.configure(state='normal')
                self.log_widget.insert(tk.END, contents)
                self.log_widget.see(tk.END)
                self.log_widget.configure(state='disabled')
        except FileNotFoundError:
            # no existing log file yet
            pass
        
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
        self.button_start.pack(side="bottom", padx=20, pady=15)

        # Pack status widgets (label + log area)
        self.label_status.pack(padx=10, pady=(6, 3), anchor="w")
        self.log_widget.pack(fill="both", expand=True, padx=10, pady=(0,10))
        # Configuration label
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
