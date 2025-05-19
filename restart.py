import os
import subprocess
import sys


def update_and_restart():
  old_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
  subprocess.run(['git', 'pull'], check=True)
  new_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

  if old_hash != new_hash:
    print('[INFO] New version detected. Restarting...')
    python = sys.executable
    os.execv(python, [python] + sys.argv)
  else:
    print('[INFO] Already up to date. No restart needed.')


if __name__ == '__main__':
  print('Starting script...')
  print(sys.executable)
  print(sys.argv)
  update_and_restart()

  # Your actual sensor logic continues below...
  print('Running latest version of the script...')
