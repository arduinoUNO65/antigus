# quarantine.py
# Functions for managing quarantined files
import os
import shutil

QUARANTINE_DIR = os.path.expanduser("~/linuxguardian_quarantine")

def configure_quarantine_dir(custom_path=None):
    global QUARANTINE_DIR
    if custom_path:
        QUARANTINE_DIR = os.path.expanduser(custom_path)
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    print(f"Quarantine directory set to: {QUARANTINE_DIR}")

def quarantine_file(path):
    try:
        base = os.path.basename(path)
        dest = os.path.join(QUARANTINE_DIR, base)
        shutil.move(path, dest)
        print(f"File {path} moved to quarantine.")
    except Exception as e:
        print(f"Failed to quarantine {path}: {e}")

def restore_file(filename, restore_path):
    src = os.path.join(QUARANTINE_DIR, filename)
    try:
        shutil.move(src, restore_path)
        print(f"File {filename} restored to {restore_path}.")
    except Exception as e:
        print(f"Failed to restore {filename}: {e}")

def delete_quarantined_file(filename):
    path = os.path.join(QUARANTINE_DIR, filename)
    try:
        os.remove(path)
        print(f"File {filename} deleted from quarantine.")
    except Exception as e:
        print(f"Failed to delete {filename}: {e}")

def list_quarantine():
    files = os.listdir(QUARANTINE_DIR)
    print("Quarantined files:")
    for f in files:
        print(f"- {f}")
    return files

if __name__ == "__main__":
    print("Linux Guardian Quarantine Utility")
    print("1. List quarantined files")
    print("2. Restore a file")
    print("3. Delete a file")
    print("4. Set quarantine directory")
    choice = input("Select an option: ")
    if choice == "1":
        list_quarantine()
    elif choice == "2":
        fname = input("Enter filename to restore: ")
        rpath = input("Enter restore path: ")
        restore_file(fname, rpath)
    elif choice == "3":
        fname = input("Enter filename to delete: ")
        delete_quarantined_file(fname)
    elif choice == "4":
        newdir = input("Enter new quarantine directory: ")
        configure_quarantine_dir(newdir)
    else:
        print("Invalid option.")
