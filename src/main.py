import sys

class App:
    @staticmethod
    def start():
        if '--cli' in sys.argv:
            import ui.console as console
            console.run()
        else:
            import ui.gui as gui
            gui.run()

if __name__ == '__main__':
    App.start()