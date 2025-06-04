# retrieve_file_versions.py
"""
Script to retrieve all versions of a given file from all git commits and save them in a folder.
Each version is saved as: <filename>-<commit_hash>
"""
import os
import subprocess
import sys

RETRIEVE_DIR = "retrieve"

def get_all_commits(file_path):
    result = subprocess.run([
        "git", "log", "--pretty=format:%H", "--", file_path
    ], capture_output=True, text=True, check=True)
    return result.stdout.strip().split("\n")

def save_file_version(file_path, commit_hash, out_dir):
    # Get the file content at the given commit
    result = subprocess.run([
        "git", "show", f"{commit_hash}:{file_path}"
    ], capture_output=True, text=True, check=True)
    # Prepare output filename
    base = os.path.basename(file_path)
    out_name = f"{base}-{commit_hash}"
    out_path = os.path.join(out_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    print(f"Saved {out_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python retrieve_file_versions.py <relative-path-to-file>")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(RETRIEVE_DIR):
        os.makedirs(RETRIEVE_DIR)
    commits = get_all_commits(file_path)
    for commit in commits:
        try:
            save_file_version(file_path, commit, RETRIEVE_DIR)
        except Exception as e:
            print(f"Failed for commit {commit}: {e}")

if __name__ == "__main__":
    main()
