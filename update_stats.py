import requests
from huggingface_hub import HfApi

USERNAME = "AI4Protein"
README_PATH = "profile/README.md"

def get_github_stats(username):
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(repos_url)
    repos = response.json()

    if isinstance(repos, dict) and "message" in repos:
        raise Exception(f"GitHub API error: {repos['message']}")

    total_stars = sum(repo["stargazers_count"] for repo in repos)
    total_forks = sum(repo["forks_count"] for repo in repos)
    return total_stars, total_forks

def update_readme(stars, forks):
    with open(README_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "<!-- 🔄 stars -->" in line:
            lines[i] = f"![Total Stars](https://img.shields.io/badge/Stars-{stars}-blue?logo=github&style=flat-square) <!-- 🔄 stars -->\n"
        if "<!-- 🔄 forks -->" in line:
            lines[i] = f"![Total Forks](https://img.shields.io/badge/Forks-{forks}-blue?logo=github&style=flat-square) <!-- 🔄 forks -->\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    try:
        stars, forks = get_github_stats(USERNAME)
        update_readme(stars, forks)
        print(f"✅ Updated profile/README.md — Stars: {stars}, Forks: {forks}")
    except Exception as e:
        print(f"❌ Error: {e}")
