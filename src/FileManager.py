import os
import shutil
from ConfigManager import ConfigManager

class FileManager:
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
    config = ConfigManager.load_config()
    world_file = config.get('world_file_name')
    local_path = config.get('local_path')
    repo_path = config.get('repo_path')
    files = [f'{world_file}.db', f'{world_file}.fwl']
    if action == 'upload':
      FileManager.copy_files(local_path, repo_path, files)
    elif action == 'download':
      FileManager.copy_files(repo_path, local_path, files)
    print('Navigating to main menu...')