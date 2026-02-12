import os, datetime, shutil
from utils.logger import log_action

def delete_expired_files(base_folder="data_storage", retention_days=30):
    now = datetime.datetime.utcnow()
    for root, dirs, files in os.walk(base_folder):
        for name in files:
            filepath = os.path.join(root, name)
            mtime = datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath))
            if (now - mtime).days > retention_days:
                os.remove(filepath)
                user_id = extract_user_id(root)
                log_action(user_id, "file_deleted", f"{filepath} expired")
        for name in dirs:
            dirpath = os.path.join(root, name)
            mtime = datetime.datetime.utcfromtimestamp(os.path.getmtime(dirpath))
            if (now - mtime).days > retention_days:
                shutil.rmtree(dirpath, ignore_errors=True)
                user_id = extract_user_id(dirpath)
                log_action(user_id, "folder_deleted", f"{dirpath} expired")

def extract_user_id(path):
    for p in path.split(os.sep):
        if p.startswith("user_"):
            try: return int(p.replace("user_",""))
            except: return None
    return None