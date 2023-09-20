from flask import Flask, render_template, request, redirect, url_for
from github import Github

app = Flask(__name__)

github_token = "YOUR_GITHUB_TOKEN"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_name = request.form["repo_name"]
        issues = get_bounty_issues(repo_name)
        return render_template("issues.html", issues=issues, repo_name=repo_name)
    return render_template("index.html")

def get_bounty_issues(repo_name):
    try:
        github = Github(github_token)
        repo = github.get_repo(repo_name)
        issues = [issue for issue in repo.get_issues(labels=["bounty"])]
        return issues
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
