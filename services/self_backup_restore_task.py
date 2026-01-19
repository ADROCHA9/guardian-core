import shutil
import os
from datetime import datetime


class SelfBackupRestoreTask:
    """
    Realiza backup completo y permite restauración.
    """

    def __init__(self, root_path, backup_dir=".guardian_backups"):
        self.root = root_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def backup(self):
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(self.backup_dir, f"backup_{ts}")
        shutil.copytree(self.root, dest, dirs_exist_ok=True)
        return dest

    def restore(self, backup_path):
        shutil.copytree(backup_path, self.root, dirs_exist_ok=True)