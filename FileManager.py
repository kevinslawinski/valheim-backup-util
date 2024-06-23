import os
import shutil

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