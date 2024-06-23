import os
import shutil
import time

def copy_files(src, dst, files):
  for file in files:
    src_file = os.path.join(src, file)
    dst_file = os.path.join(dst, file)
    try:
      shutil.copy2(src_file, dst_file)
      print(f'Copied file: {file}')
    except FileNotFoundError:
      print(f'File not found: {src_file}')
    except Exception as e:
      print(f'Error copying file {src_file}: {e}')

def sync_files(action):
  config = load_config()
  world_file = config.get('world_file_name')
  local_path = config.get('local_path')
  repo_path = config.get('repo_path')
  files = [f'{world_file}.db', f'{world_file}.fwl']
  if action == 'upload':
    copy_files(local_path, repo_path, files)
  elif action == 'download':
    copy_files(repo_path, local_path, files)
  print('Navigating to main menu...')

def upload_files():
  sync_files('upload')

def download_files():
  sync_files('download')

def main_menu():
  while True:
    print('\n\n----------------------')
    print('Valheim Backup Utility')
    print('----------------------')
    config = load_config()
    time.sleep(0.7)
    print('\n----------------------')
    print('(1) Upload world files to git repository')
    print('(2) Download world files from git repository')
    print('(3) Read current config')
    print('(4) Regenerate config')
    
    choice = input('Choose an option (1-3, 0 to exit): ')
    
    if choice == '1':
      upload_files()
    elif choice == '2':
      download_files()
    elif choice == '3':
      print_config(config)
    elif choice == '4':
      generate_config()
    elif choice == '0':
      print('Goodbye!')
      break
    else:
      print('Not an option. Try again.')
    time.sleep(2)

if __name__ == '__main__':
  main_menu()
    
# os.system('git pull')