import os
import time

from services.config_service import ConfigService
from services.file_service import FileService

def run():
    while True:
        # Load config
        menu_header()
        try:
            print('Loading config file...')
            ConfigService().get()
        except PermissionError:
            print('You\'re on your own with this one...')
            return
        except Exception:
            print('Generating new config file...')
            prompt_new_config()
        time.sleep(1)
        
        # Display main menu
        clear_screen()
        menu_header()
        menu_options()

        choice = prompt_menu_choice()
        
        if choice == '1':
            FileService.sync_files('upload')
        elif choice == '2':
            FileService.sync_files('download')
        elif choice == '3':
            print_config()
        elif choice == '4':
            prompt_new_config()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Not an option. Try again.')
        
        input('\nPress Enter to continue...')
        clear_screen()
        time.sleep(0.5)

def menu_header():
    title = 'Valheim Backup Utility'
    border = '-' * len(title)
    print(f"{border}\n{title}\n{border}")
    
def menu_options():
    print('  (1) Upload world files to git repository')
    print('  (2) Download world files from git repository')
    print('  (3) Read current config')
    print('  (4) Regenerate config')

def print_config():
    config = ConfigService().get()
    print('\nCurrent configuration:\n')
    print(f'  World Name: {config.get("world_file_name")}')
    print(f'  Valheim Save Location: {config.get("local_path")}')
    print(f'  Repo Path: {config.get("repo_path")}')
    
def prompt_new_config():
    print('\nNew configuration:\n')
    world_file_name = input('  Name of the Valheim world: ')
    local_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'IronGate', 'Valheim', 'worlds_local')
    repo_path = input('  Path to Valheim remote repository: ')
    config = {
      'world_file_name': world_file_name,
      'local_path': local_path,
      'repo_path': repo_path
    }
    ConfigService().save(config)
    print('\nConfiguration saved successfully!')
    return config

def prompt_menu_choice():
    choice = input('Choose an option (1-4, 0 to exit): ')
    return choice

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
