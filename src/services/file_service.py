import logging
import os
import shutil
from .config_service import ConfigService

class FileService:
    """
    Provides file operations for syncing Valheim world files between local and remote paths.
    """
    @staticmethod
    def _copy_files(src, dst, files):
        """
        Copy specified files from source to destination directory.
        Args:
            src (str): Source directory path.
            dst (str): Destination directory path.
            files (list): List of filenames to copy.
        Logs:
            Info when a file is copied successfully.
            Warning if a file is not found.
            Error for other exceptions during copy.
        """
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
        """
        Sync Valheim world files between local and remote paths based on the action.
        Args:
            action (str): 'upload' to copy from local to remote, 'download' to copy from remote to local.
        Logs:
            Warning for unknown actions.
            Error for unhandled exceptions during sync.
        """
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
