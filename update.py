#!/usr/bin/env python3
import os
import shutil

SUBMODULE_DIR = "homebrew"
TARGET_DIR = "data"
IGNORE = {"_img", "_font", ".github"}  # Folders or files to ignore
IGNORE_EXT = {".bin", ".zip"}  # Ignore files with these extensions


def should_ignore(path):
    # Check folder names
    if any(part in IGNORE for part in path.split(os.sep)):
        return True
    # Check file extensions
    if os.path.splitext(path)[1] in IGNORE_EXT:
        return True
    return False


def copy_files(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        # Relative path from src
        rel_path = os.path.relpath(root, src)
        if should_ignore(rel_path):
            continue

        # Ensure target directory exists
        target_root = os.path.join(dst, rel_path)
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            if should_ignore(file):
                continue
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)


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
    copy_files(SUBMODULE_DIR, TARGET_DIR)
    remove_deleted(SUBMODULE_DIR, TARGET_DIR)
    print(f"Submodule files synced!")
