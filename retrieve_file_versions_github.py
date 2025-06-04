# retrieve_file_versions_github.py
"""
Script to retrieve all versions of all files containing a given word from all commits in a GitHub repo and save them in a folder.
Each version is saved as: <filename>-<commit_hash>

Usage:
    python retrieve_file_versions_github.py <github_repo> <search_word> [directory]
Example:
    python retrieve_file_versions_github.py owner/repo parse_netflix_url
"""
import os
import sys
import requests
import base64

RETRIEVE_DIR = "retrieved"
GITHUB_API = "https://api.github.com"

# --- GitHub Auth ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
HEADERS = {
    "Authorization": "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",  # Replace with your PAT
    "Accept": "application/vnd.github.v3+json"
}
# --- Hardcoded arguments for testing ---
REPO = "Olioli4/ChromeExtension"  # Replace with your repo, e.g. "Olioli4/ChromeExtension"
SEARCH_WORD = "netflix"  # Replace with your search word
DIRECTORY = ""  # Or e.g. "src" to limit to a directory


def get_all_files(repo, directory=None):
    url = f"{GITHUB_API}/repos/{repo}/git/trees/master?recursive=1"
    print(f"DEBUG: GET {url} HEADERS={HEADERS}")
    resp = requests.get(url, headers=HEADERS)
    print(f"DEBUG: Response status={resp.status_code}")
    try:
        data = resp.json()
        print(f"DEBUG: Response json={data}")
    except Exception as e:
        print(f"DEBUG: Could not decode JSON: {e}")
        resp.raise_for_status()
        return []
    resp.raise_for_status()
    # Return list of (path, sha) tuples for blobs
    if directory:
        directory = directory.rstrip("/") + "/"
        return [(item['path'], item['sha']) for item in data.get('tree', []) if item['type'] == 'blob' and item['path'].startswith(directory)]
    else:
        return [(item['path'], item['sha']) for item in data.get('tree', []) if item['type'] == 'blob']


def file_contains_word(repo, file_path, sha, word):
    url = f"{GITHUB_API}/repos/{repo}/git/blobs/{sha}"
    print(f"DEBUG: GET {url} HEADERS={HEADERS}")
    resp = requests.get(url, headers=HEADERS)
    print(f"DEBUG: Response status={resp.status_code}")
    try:
        data = resp.json()
        print(f"DEBUG: Response json={data}")
    except Exception as e:
        print(f"DEBUG: Could not decode JSON: {e}")
        return False
    if resp.status_code != 200:
        return False
    content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    return word in content


def get_all_commits(repo, file_path):
    url = f"{GITHUB_API}/repos/{repo}/commits"
    params = {"path": file_path, "per_page": 100}
    print(f"DEBUG: GET {url} PARAMS={params} HEADERS={HEADERS}")
    commits = []
    page = 1
    while True:
        params["page"] = page
        resp = requests.get(url, params=params, headers=HEADERS)
        print(f"DEBUG: Response status={resp.status_code}")
        try:
            print(f"DEBUG: Response json={resp.json()}")
        except Exception as e:
            print(f"DEBUG: Could not decode JSON: {e}")
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        commits.extend([c["sha"] for c in data])
        page += 1
    return commits


def save_file_version(repo, file_path, commit_hash, out_dir):
    url = f"{GITHUB_API}/repos/{repo}/contents/{file_path}"
    params = {"ref": commit_hash}
    resp = requests.get(url, params=params, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Could not fetch {file_path} at {commit_hash}")
        return
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    base, ext = os.path.splitext(os.path.basename(file_path))
    # Save under out_dir with subfolders matching file_path, and filename as <originalname>-<commit_hash><ext>
    rel_dir = os.path.dirname(file_path)
    target_dir = os.path.join(out_dir, rel_dir)
    os.makedirs(target_dir, exist_ok=True)
    out_name = f"{base}-{commit_hash}{ext}"
    out_path = os.path.join(target_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {out_path}")


def main():
    repo = REPO
    search_word = SEARCH_WORD
    directory = DIRECTORY
    if not os.path.exists(RETRIEVE_DIR):
        os.makedirs(RETRIEVE_DIR)
    print(f"Searching for files with '{search_word}' in their FILENAME..." + (f" in directory '{directory}'" if directory else ""))
    files = get_all_files(repo, directory)
    print(f"DEBUG: get_all_files returned {len(files)} files: {files}")
    matching_files = [f for f, sha in files if search_word in os.path.basename(f)]
    print(f"Found {len(matching_files)} files with '{search_word}' in filename.")
    for file_path in matching_files:
        print(f"Processing {file_path}...")
        commits = get_all_commits(repo, file_path)
        print(f"DEBUG: get_all_commits for {file_path} returned {len(commits)} commits: {commits}")
        for commit in commits:
            try:
                save_file_version(repo, file_path, commit, RETRIEVE_DIR)
            except Exception as e:
                print(f"Failed for {file_path} at commit {commit}: {e}")

if __name__ == "__main__":
    main()
