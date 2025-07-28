import unittest
import os
import tempfile
import shutil
from unittest import mock
from unittest.mock import patch

from src.services.file_service import FileService
from src.services.config_service import ConfigService

class TestFileService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_config = {
            'world_file_name': 'TestWorld',
            'local_path': None,  # Will be set per test
            'repo_path': None   # Will be set per test
        }

    def setUp(self):
        # Create temp dirs for local and repo
        self.local_dir = tempfile.mkdtemp()
        self.repo_dir = tempfile.mkdtemp()
        self.sample_config['local_path'] = self.local_dir
        self.sample_config['repo_path'] = self.repo_dir
        # Patch ConfigService.get to return our sample config
        self.patcher = patch.object(ConfigService, 'get', return_value=self.sample_config)
        self.patcher.start()
        # Create dummy world files in local_dir
        self.world_file = self.sample_config['world_file_name']
        self.db_file = f'{self.world_file}.db'
        self.fwl_file = f'{self.world_file}.fwl'
        for fname in [self.db_file, self.fwl_file]:
            with open(os.path.join(self.local_dir, fname), 'w') as f:
                f.write('testdata')

    def tearDown(self):
        shutil.rmtree(self.local_dir)
        shutil.rmtree(self.repo_dir)
        self.patcher.stop()

    def test_upload_copies_files(self):
        FileService.sync_files('upload')
        for fname in [self.db_file, self.fwl_file]:
            self.assertTrue(os.path.exists(os.path.join(self.repo_dir, fname)))

    def test_download_copies_files(self):
        # First upload files to repo_dir
        FileService.sync_files('upload')
        # Remove files from local_dir
        for fname in [self.db_file, self.fwl_file]:
            os.remove(os.path.join(self.local_dir, fname))
        # Download back to local_dir
        FileService.sync_files('download')
        for fname in [self.db_file, self.fwl_file]:
            self.assertTrue(os.path.exists(os.path.join(self.local_dir, fname)))

    def test_unknown_action_logs_warning(self):
        with self.assertLogs('root', level='WARNING') as cm:
            FileService.sync_files('invalid_action')
        self.assertTrue(any('Unknown action' in msg for msg in cm.output))

    def test_sync_files_handles_exception(self):
        # Patch ConfigService.get to raise exception
        with patch.object(ConfigService, 'get', side_effect=Exception('fail')):
            with self.assertLogs('root', level='ERROR') as cm:
                FileService.sync_files('upload')
            self.assertTrue(any('An error occurred while syncing files.' in msg for msg in cm.output))
