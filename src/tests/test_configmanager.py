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
        # Check that open was called with the correct file, mode, and encoding
        mock_open.assert_called_with(sut.USER_CONFIG, 'w', encoding='utf-8')
        # Use the actual file handle from the mock
        handle = mock_open.return_value
        handle.write.assert_called()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        saved_config = json.loads(written_data)
        self.assertEqual(saved_config, new_config)
        
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
    def test_config_load_valid_config_success(self, mock_file, mock_exists):
        """Test loading an existing config file."""
        # Set the mock file's read to return the sample config as JSON
        mock_file.return_value.read.return_value = json.dumps(self.sample_config)
        sut = ConfigManager()
        loaded_config = sut.load_config()
        self.assertEqual(loaded_config, self.sample_config)
        
    def test_config_load_non_ascii_values_success(self):
        """Test loading a config file with non-ASCII/special characters."""
        config_with_unicode = self.sample_config.copy()
        config_with_unicode['world_file_name'] = '世界'
        config_with_unicode['repo_path'] = 'D:/Backups/ヴァルハイム'
        with open(self.temp_config_file, 'w', encoding='utf-8') as f:
            json.dump(config_with_unicode, f, ensure_ascii=False)
        sut = ConfigManager()
        loaded = sut.load_config()
        self.assertEqual(loaded['world_file_name'], '世界')
        self.assertEqual(loaded['repo_path'], 'D:/Backups/ヴァルハイム')

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_config_load_triggers_generate_on_missing_file(self, mock_open, mock_exists):
        """Test that a missing config file triggers generate_config."""
        sut = ConfigManager()
        with patch.object(ConfigManager, 'generate_config', return_value=self.sample_config.copy()) as mock_generate:
            loaded_config = sut.load_config()
            mock_generate.assert_called_once()
            self.assertEqual(loaded_config, self.sample_config)

    def test_config_load_invalid_json_and_empty_file(self):
        """Test loading a config file with invalid/corrupted JSON or empty file raises JSONDecodeError."""
        cases = [
            ('{invalid json}', 'invalid json'),
            ('', 'empty file'),
        ]
        for file_content, case in cases:
            with self.subTest(case=case):
                with open(self.temp_config_file, 'w') as f:
                    f.write(file_content)
                sut = ConfigManager()
                with self.assertRaises(json.JSONDecodeError):
                    sut.load_config()

    def test_config_load_missing_fields(self):
        """Test loading a config file missing required fields."""
        required_fields = ['world_file_name', 'local_path', 'repo_path']
        for field in required_fields:
            with self.subTest(missing_field=field):
                incomplete_config = self.sample_config.copy()
                incomplete_config.pop(field)
                with open(self.temp_config_file, 'w') as f:
                    json.dump(incomplete_config, f)
                sut = ConfigManager()
                with self.assertRaises(ValueError) as cm:
                    sut.load_config()
                self.assertIn(f"Config missing required fields: {{{field!r}}}", str(cm.exception))

    def test_config_load_corrupt_configs_fail(self):
        """Test that corrupt configs (extra fields, empty/null values) are considered invalid."""
        corrupt_cases = [
            # Extra/unexpected field
            ({**self.sample_config, 'unexpected_field': 'extra_value'}, 'extra field', "Config has unexpected fields: {'unexpected_field'}"),
            # Empty value
            ({**self.sample_config, 'world_file_name': ''}, 'empty value', "Config field 'world_file_name' is empty or null."),
            # Null value
            ({**self.sample_config, 'repo_path': None}, 'null value', "Config field 'repo_path' is empty or null."),
            # Multiple corruptions
            ({**self.sample_config, 'world_file_name': '', 'repo_path': None}, 'multiple corruptions', None),
        ]
        for config, case, expected_msg in corrupt_cases:
            with self.subTest(case=case):
                with open(self.temp_config_file, 'w') as f:
                    json.dump(config, f)
                sut = ConfigManager()
                with self.assertRaises(ValueError) as cm:
                    sut.load_config()
                if expected_msg:
                    self.assertIn(expected_msg, str(cm.exception))
                else:
                    # For multiple corruptions, just check it's one of the expected messages
                    self.assertTrue(
                        "Config field 'world_file_name' is empty or null." in str(cm.exception) or
                        "Config field 'repo_path' is empty or null." in str(cm.exception)
                    )

    def test_config_save_permission_errors(self):
        """Test saving config when file-related errors occur."""
        error_cases = [
            (PermissionError, 'PermissionError'),
            (OSError, 'OSError'),
        ]
        sut = ConfigManager()
        test_config = self.sample_config.copy()
        for error, case in error_cases:
            with self.subTest(error=case):
                with patch('builtins.open', side_effect=error):
                    with self.assertRaises(error):
                        sut.save_config(test_config)

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

    def test_config_load_when_path_is_directory(self):
        """Test loading config when the config path is a directory, not a file."""
        # Remove temp file and create a directory at the same path
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        os.mkdir(self.temp_config_file)
        try:
            sut = ConfigManager()
            with self.assertRaises(ValueError) as cm:
                sut.load_config()
            self.assertEqual(str(cm.exception), 'Config path is a directory, not a file.')
        finally:
            # Clean up the directory
            if os.path.isdir(self.temp_config_file):
                os.rmdir(self.temp_config_file)

if __name__ == '__main__':
    unittest.main()