import sys

import logger as logging

class App:
    @staticmethod
    def start():
        logging.initialize_logger()
        
        # Default GUI, but offer CLI option with --cli
        if '--gui' in sys.argv:
            import ui.gui as gui
            gui.run()
        else:
            import ui.console as console
            console.run()

if __name__ == '__main__':
    App.start()