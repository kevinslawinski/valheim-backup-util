import logging
import sys

class App:
    @staticmethod
    def start():
        # Set up logging to both console and file
        log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)
        # Add file handler
        file_handler = logging.FileHandler('app.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        logging.getLogger().addHandler(file_handler)
        
        # Default GUI, but offer CLI option with --cli
        if '--cli' in sys.argv:
            import ui.console as console
            console.run()
        else:
            import ui.gui as gui
            gui.run()

if __name__ == '__main__':
    App.start()