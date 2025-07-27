import os
import shutil
from services.config_service import ConfigService

class FileService:
  @staticmethod
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
    
  @staticmethod
  def sync_files(action):
    config_service = ConfigService()
    config = config_service.get()
    world_file = config.get('world_file_name')
    local_path = config.get('local_path')
    repo_path = config.get('repo_path')
    files = [f'{world_file}.db', f'{world_file}.fwl']
    if action == 'upload':
      confirm = input(f'End of session upload. Confirm: (y/n) ')
      if confirm.lower() == 'y':
        FileService.copy_files(local_path, repo_path, files)
      else:
        print('Nothing uploaded.')
    elif action == 'download':
      confirm = input(f'Start of session download. Confirm: (y/n) ')
      if confirm.lower() == 'y':
        FileService.copy_files(repo_path, local_path, files)
      else:
        print('Nothing downloaded.')
    print('Navigating to main menu...')
