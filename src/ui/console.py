import os
import time

from services.config_service import ConfigService
from services.file_service import FileService

def menu_header():
    print('\n----------------------')
    print('Valheim Backup Utility')
    print('----------------------')
    
def menu_options():
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Read current config')
    print('(4) Regenerate config')

def prompt_for_choice():
    choice = input('Choose an option (1-4, 0 to exit): ')
    return choice

def run():
    while True:
        menu_header()
        config_service = ConfigService()
        config_service.load_config()
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_header()
        menu_options()

        choice = prompt_for_choice()
        
        if choice == '1':
            FileService.sync_files('upload')
        elif choice == '2':
            FileService.sync_files('download')
        elif choice == '3':
            config_service.print_config()
        elif choice == '4':
            config_service.generate_config()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Not an option. Try again.')
        time.sleep(2)