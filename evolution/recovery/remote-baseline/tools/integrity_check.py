
import os
import hashlib

def calculate_git_blob_hash(filepath):
    # This is a simplified representation. Actual Git blob hashing is more complex.
    # It involves prepending 'blob <size>\0' to the content.
    with open(filepath, 'rb') as f:
        content = f.read()
    size = len(content)
    header = f'blob {size}\0'.encode('utf-8')
    sha1 = hashlib.sha1(header + content).hexdigest()
    return sha1

def generate_manifest(repo_path, output_path):
    manifest_content = "# Repository Manifest\n\n"
    manifest_content += "| File Path | Git Blob SHA1 Hash |\n"
    manifest_content += "|-----------|--------------------|\n"

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file == 'manifest.md' or file.endswith('.pyc') or '.git' in root:
                continue
            filepath = os.path.join(root, file)
            relative_filepath = os.path.relpath(filepath, repo_path)
            try:
                sha1_hash = calculate_git_blob_hash(filepath)
                manifest_content += f"| {relative_filepath} | {sha1_hash} |\n"
            except Exception as e:
                manifest_content += f"| {relative_filepath} | ERROR: {e} |\n"
    
    with open(output_path, 'w') as f:
        f.write(manifest_content)

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    manifest_file = os.path.join(repo_root, 'evolution', 'manifest.md')
    print(f"Generating manifest for {repo_root} to {manifest_file}")
    generate_manifest(repo_root, manifest_file)
    print("Manifest generation complete.")

