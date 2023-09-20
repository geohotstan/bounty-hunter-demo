#! /usr/bin/env python3
from typing import Dict
from flask import Flask, render_template, request, redirect, url_for
from github import Github, Issue

app = Flask(__name__)
g = Github()
cache: Dict[str, Issue.Issue] = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_name = request.form["repo_name"]
        repo_name = "geohotstan/SolidGoldMagikarp" if repo_name == "test" else repo_name
        return redirect(url_for("get_bounty_issues", repo_name=repo_name.replace("/", "_")))
    return render_template("index.html")

@app.route("/issues/<repo_name>")
def get_bounty_issues(repo_name: str):
    repo = g.get_repo(repo_name.replace("_", "/"))
    issues = [issue for issue in repo.get_issues(labels=["bounty"])]
    for i in issues: cache[str(i.number)] = i
    return render_template("issues.html", repo_name=repo_name, issues=issues)

@app.route("/issue/<repo_name>/<issue_number>")
def view_issue(repo_name: str, issue_number: int):
    issue = cache[issue_number] 
    return render_template("issue.html", issue=issue)

@app.route("/issue/<repo_name>/<issue_number>/start")
def start_function(repo_name, issue_number):
    return None

if __name__ == "__main__":
    app.run(debug=True)
