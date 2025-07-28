import unittest
import json
import os
import tempfile
from unittest import mock
from unittest.mock import mock_open, patch

from src.services.config_service import ConfigService

class TestConfigService(unittest.TestCase):
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
        self.patcher = patch.object(ConfigService, 'USER_CONFIG', self.temp_config_file)
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
        sut = ConfigService()
        # Use a config with different values than sample_config
        new_config = {
            'world_file_name': 'NewWorld',
            'local_path': 'D:\\Games\\Valheim\\worlds_local',
            'repo_path': 'D:\\Backups\\ValheimRepo'
        }
        sut.save(new_config)
        # Check that open was called with the correct file, mode, and encoding
        mock_open.assert_called_with(sut.USER_CONFIG, 'w', encoding='utf-8')
        # Use the actual file handle from the mock
        handle = mock_open.return_value
        handle.write.assert_called()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        saved_config = json.loads(written_data)
        self.assertEqual(saved_config, new_config)
        
    def test_config_save_permission_errors(self):
        """Test saving config when file-related errors occur."""
        error_cases = [
            (PermissionError, 'PermissionError'),
            (OSError, 'OSError'),
        ]
        sut = ConfigService()
        test_config = self.sample_config.copy()
        for error, case in error_cases:
            with self.subTest(error=case):
                with patch('builtins.open', side_effect=error):
                    with self.assertRaises(error):
                        sut.save(test_config)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_config_load_valid_config_success(self, mock_file, mock_exists):
        """Test loading an existing config file."""
        # Set the mock file's read to return the sample config as JSON
        mock_file.return_value.read.return_value = json.dumps(self.sample_config)
        sut = ConfigService()
        loaded_config = sut.get()
        self.assertEqual(loaded_config, self.sample_config)
        
    def test_config_load_non_ascii_values_success(self):
        """Test loading a config file with non-ASCII/special characters."""
        config_with_unicode = self.sample_config.copy()
        config_with_unicode['world_file_name'] = '世界'
        config_with_unicode['repo_path'] = 'D:/Backups/ヴァルハイム'
        with open(self.temp_config_file, 'w', encoding='utf-8') as f:
            json.dump(config_with_unicode, f, ensure_ascii=False)
        sut = ConfigService()
        loaded = sut.get()
        self.assertEqual(loaded['world_file_name'], '世界')
        self.assertEqual(loaded['repo_path'], 'D:/Backups/ヴァルハイム')

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
                sut = ConfigService()
                with self.assertRaises(json.JSONDecodeError):
                    sut.get()

    def test_config_load_missing_fields(self):
        """Test loading a config file missing required fields."""
        required_fields = ['world_file_name', 'local_path', 'repo_path']
        for field in required_fields:
            with self.subTest(missing_field=field):
                incomplete_config = self.sample_config.copy()
                incomplete_config.pop(field)
                with open(self.temp_config_file, 'w') as f:
                    json.dump(incomplete_config, f)
                sut = ConfigService()
                with self.assertRaises(ValueError) as cm:
                    sut.get()
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
                sut = ConfigService()
                with self.assertRaises(ValueError) as cm:
                    sut.get()
                if expected_msg:
                    self.assertIn(expected_msg, str(cm.exception))
                else:
                    # For multiple corruptions, just check it's one of the expected messages
                    self.assertTrue(
                        "Config field 'world_file_name' is empty or null." in str(cm.exception) or
                        "Config field 'repo_path' is empty or null." in str(cm.exception)
                    )

    def test_config_load_when_path_is_directory(self):
        """Test loading config when the config path is a directory, not a file."""
        # Remove temp file and create a directory at the same path
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        os.mkdir(self.temp_config_file)
        try:
            sut = ConfigService()
            with self.assertRaises(ValueError) as cm:
                sut.get()
            self.assertEqual(str(cm.exception), 'Config path is a directory, not a file.')
        finally:
            # Clean up the directory
            if os.path.isdir(self.temp_config_file):
                os.rmdir(self.temp_config_file)

if __name__ == '__main__':
    unittest.main()