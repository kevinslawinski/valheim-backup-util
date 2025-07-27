import sys

class App:
    @staticmethod
    def start():
        if '--cli' in sys.argv:
            from ui.console import run
        else:
            from ui.gui import run
        run()
  
if __name__ == '__main__':
    App.start()