import logging
import os
import shutil
from services.config_service import ConfigService

class FileService:
    @staticmethod
    def _copy_files(src, dst, files):
        for file in files:
            src_file = os.path.join(src, file)
            dst_file = os.path.join(dst, file)
            try:
                shutil.copy2(src_file, dst_file)
                logging.info(f'Copied {file} from {src} to {dst}')
            except FileNotFoundError as e:
                logging.warning(f'File not found: {src_file}. Error: {e}')
            except Exception as e:
                logging.error(f'Error copying file {file} from {src} to {dst}: {e}')
    
    @staticmethod
    def sync_files(action):
        try:
            config = ConfigService().get()
            world_file = config.get('world_file_name')
            local_path = config.get('local_path')
            repo_path = config.get('repo_path')
            files = [f'{world_file}.db', f'{world_file}.fwl']

            if action == 'upload':
                FileService._copy_files(local_path, repo_path, files)
            elif action == 'download':
                FileService._copy_files(repo_path, local_path, files)
            else:
                logging.warning(f'Unknown action: {action}')
        except Exception:
            logging.error("An error occurred while syncing files.")
