import os
import subprocess

def clone_repo(repo_url: str, base_dir: str = "repos") -> str:
    """
    Clones a GitHub repository into a local directory.

    Args:
        repo_url (str): GitHub repo URL
        base_dir (str): Folder to store repos

    Returns:
        str: Path to cloned repository
    """

    # Create base directory if not exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Extract repo name
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(base_dir, repo_name)

    # If already exists → skip cloning
    if os.path.exists(repo_path):
        print(f"Repo already exists at {repo_path}")
        return repo_path

    try:
        print(f"Cloning {repo_url}...")

        result = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True,
            capture_output=True,
            text=True
        )

        print("Clone successful!")
        return repo_path

    except subprocess.CalledProcessError as e:
        print("Error cloning repo:")
        print(e.stderr)
        raise e
    

if __name__ == "__main__":
    repo_url = "https://github.com/Hariom-Nagar211/Whatsapp-Chat-Analyzer"
    path = clone_repo(repo_url)
    print("Cloned to:", path)    