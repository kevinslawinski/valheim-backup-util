import unittest
import json
import os
import tempfile
from unittest import mock
from unittest.mock import mock_open, patch

from src.ConfigManager import ConfigManager

class TestConfigManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Shared sample config for all tests
        cls.sample_config = {
            'world_file_name': 'TestWorld',
            'local_path': 'C:\\Users\\TestUser\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local',
            'repo_path': 'C:\\Users\\TestUser\\ValheimRepo'
        }

    def setUp(self):
        # Create a unique temp file for each test
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.temp_config_file = self.tempfile.name
        self.tempfile.close()
        # Patch USER_CONFIG to use the temp file
        self.patcher = patch('src.ConfigManager.ConfigManager.USER_CONFIG', self.temp_config_file)
        self.patcher.start()
        # Write the shared sample config to the temp file
        with open(self.temp_config_file, 'w') as f:
            json.dump(self.sample_config, f)

    def tearDown(self):
        # Remove the temporary config file after each test
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        self.patcher.stop()

    @patch('builtins.open', new_callable=mock_open)
    def test_config_save_success(self, mock_open):
        """Test saving a config and verifying file contents."""
        sut = ConfigManager()
        # Use a config with different values than sample_config
        new_config = {
            'world_file_name': 'NewWorld',
            'local_path': 'D:\\Games\\Valheim\\worlds_local',
            'repo_path': 'D:\\Backups\\ValheimRepo'
        }
        sut.save_config(new_config)

        # Check that open was called with the correct file and mode
        mock_open.assert_called_with(sut.USER_CONFIG, 'w')
        # Use the actual file handle from the mock
        handle = mock_open.return_value
        handle.write.assert_called()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        saved_config = json.loads(written_data)
        self.assertEqual(saved_config, new_config)
        
    def test_config_save_permission_error(self):
        """Test saving config when a permission error occurs."""
        sut = ConfigManager()
        test_config = self.sample_config.copy()
        with patch('builtins.open', side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                sut.save_config(test_config)

    @patch('os.getenv', return_value='C:\\Users\\TestUser')
    def test_config_generate_success(self, mock_os_getenv):
        """Test generating a config via user input and environment."""
        with patch('builtins.input', side_effect=[
            self.sample_config['world_file_name'],
            self.sample_config['repo_path']
        ]):
            sut = ConfigManager()
            generated_config = sut.generate_config()

            # Check if the generated config matches the expected format
            self.assertEqual(generated_config['world_file_name'], self.sample_config['world_file_name'])
            self.assertEqual(generated_config['repo_path'], self.sample_config['repo_path'])

            # Verify that the config is saved correctly to the file
            saved_config = sut.load_config()
            self.assertEqual(saved_config['world_file_name'], self.sample_config['world_file_name'])
            self.assertEqual(saved_config['repo_path'], self.sample_config['repo_path'])

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_config_load_existing_config(self, mock_file, mock_exists):
        """Test loading an existing config file."""
        # Set the mock file's read to return the sample config as JSON
        mock_file.return_value.read.return_value = json.dumps(self.sample_config)
        sut = ConfigManager()
        loaded_config = sut.load_config()
        self.assertEqual(loaded_config, self.sample_config)

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_config_load_missing_config(self, mock_open, mock_exists):
        """Test loading config when file is missing, triggering generate_config."""
        mock_open.return_value.read.return_value = json.dumps(self.sample_config)
        sut = ConfigManager()
        with patch.object(ConfigManager, 'generate_config', return_value=self.sample_config.copy()):
            loaded_config = sut.load_config()
        self.assertEqual(loaded_config, self.sample_config)

    def test_config_load_invalid_json(self):
        """Test loading a config file with invalid/corrupted JSON."""
        with open(self.temp_config_file, 'w') as f:
            f.write('{invalid json}')
        sut = ConfigManager()
        with self.assertRaises(json.JSONDecodeError):
            sut.load_config()

    def test_config_load_missing_fields(self):
        """Test loading a config file missing required fields."""
        # Use a copy of sample_config and remove 'repo_path'
        incomplete_config = self.sample_config.copy()
        incomplete_config.pop('repo_path')
        with open(self.temp_config_file, 'w') as f:
            json.dump(incomplete_config, f)
        sut = ConfigManager()
        loaded = sut.load_config()
        self.assertNotIn('repo_path', loaded)

    def test_config_load_empty_file(self):
        """Test loading a config file that exists but is empty."""
        # Write an empty file
        with open(self.temp_config_file, 'w') as f:
            f.write('')
        sut = ConfigManager()
        with self.assertRaises(json.JSONDecodeError):
            sut.load_config()
                
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_config_print_success(self, mock_open, mock_exists):
        """Test printing the current configuration to stdout."""
        # Set the mock file's read_data to the sample config as JSON
        mock_open.return_value.read.return_value = json.dumps(self.sample_config)
        with patch('builtins.input', side_effect=[
            self.sample_config['world_file_name'],
            self.sample_config['repo_path']
        ]):
            sut = ConfigManager()
            with patch('builtins.print') as mocked_print:
                sut.print_config()
                # Check if print function was called with the correct output
                expected_output = [
                    f'  World Name: {self.sample_config["world_file_name"]}',
                    f'  Valheim Save Location: {self.sample_config["local_path"]}',
                    f'  Repo Path: {self.sample_config["repo_path"]}'
                ]
                mocked_print.assert_any_call('\nCurrent configuration:\n')
                for expected_line in expected_output:
                    mocked_print.assert_any_call(expected_line)

if __name__ == '__main__':
    unittest.main()