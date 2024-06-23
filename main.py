import time
from ConfigManager import ConfigManager
from FileManager import FileManager

def main_menu():
  while True:
    print('\n\n----------------------')
    print('Valheim Backup Utility')
    print('----------------------')
    config = ConfigManager.load_config()
    time.sleep(0.7)
    print('\n----------------------')
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Read current config')
    print('(4) Regenerate config')
    
    choice = input('Choose an option (1-3, 0 to exit): ')
    
    if choice == '1':
      FileManager.sync_files('upload')
    elif choice == '2':
      FileManager.sync_files('download')
    elif choice == '3':
      ConfigManager.print_config(config)
    elif choice == '4':
      ConfigManager.generate_config()
    elif choice == '0':
      print('Goodbye!')
      break
    else:
      print('Not an option. Try again.')
    time.sleep(2)

if __name__ == '__main__':
  main_menu()
    
# os.system('git pull')