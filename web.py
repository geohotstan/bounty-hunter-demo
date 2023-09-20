#! /usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from github import Github

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_name = request.form["repo_name"]
        repo_name = "geohotstan/SolidGoldMagikarp" if repo_name == "test" else repo_name
        return redirect(url_for("get_bounty_issues", repo_name=repo_name.replace("/", "_")))
    return render_template("index.html")

@app.route("/issues/<repo_name>")
def get_bounty_issues(repo_name: str):
    g = Github()
    repo = g.get_repo(repo_name.replace("_", "/"))
    issues = [issue for issue in repo.get_issues(labels=["bounty"])]
    return str(issues)

if __name__ == "__main__":
    app.run(debug=True)
