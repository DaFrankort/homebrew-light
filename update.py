#!/usr/bin/env python3
import os
import shutil

SUBMODULE_DIR = "homebrew"
TARGET_DIR = "data"
IGNORE = {'package.json', 'package-lock.json'}  # Folders or files to ignore
IGNORE_EXT = {".bin", ".zip", '.md', '.js'}  # Ignore files with these extensions


def should_ignore(path):
    name = os.path.basename(path)
    if name.startswith("_") or name.startswith("."):
        return True
    if any(part in IGNORE for part in path.split(os.sep)):
        return True
    if os.path.splitext(name)[1] in IGNORE_EXT:
        return True
    return False


def copy_files(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        # Filter out ignored directories in-place
        dirs[:] = [d for d in dirs if not should_ignore(d)]

        # Now process files
        for file in files:
            if should_ignore(file):
                continue
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(root, src)
            target_root = os.path.join(dst, rel_path)
            os.makedirs(target_root, exist_ok=True)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)


def clear_target_dir(target_dir):
    """Safely remove all files/folders inside target_dir"""
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if item == ".git":
                continue  # Never delete a .git folder
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.makedirs(target_dir)


def remove_deleted(src, dst):
    # Remove files in dst that no longer exist in src
    for root, dirs, files in os.walk(dst):
        rel_path = os.path.relpath(root, dst)
        src_root = os.path.join(src, rel_path)

        for file in files:
            dst_file = os.path.join(root, file)
            src_file = os.path.join(src_root, file)
            if not os.path.exists(src_file):
                os.remove(dst_file)

        for dir in dirs:
            dst_dir = os.path.join(root, dir)
            src_dir = os.path.join(src_root, dir)
            if not os.path.exists(src_dir):
                shutil.rmtree(dst_dir)


if __name__ == "__main__":
    os.makedirs(TARGET_DIR, exist_ok=True)
    clear_target_dir(TARGET_DIR)
    print(f'{TARGET_DIR} cleared!')
    copy_files(SUBMODULE_DIR, TARGET_DIR)
    print(f"Files copied from {SUBMODULE_DIR} to {TARGET_DIR}")
    remove_deleted(SUBMODULE_DIR, TARGET_DIR)
    print(f"Submodule files synced!")
