#! /usr/bin/env python3
import os
from typing import Dict, Union

from flask import Flask, render_template, request, redirect, url_for
from github import Github, Issue, Auth, Repository, AuthenticatedUser
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
g = Github()
gt = os.getenv("GT", None)
cache: Dict[str, Union[Issue.Issue, Repository.Repository, AuthenticatedUser.AuthenticatedUser]] = {}

def site_router():
    if "user" not in cache: return redirect(url_for("index"))
    elif len(cache) == 1: return redirect(url_for("welcome"))
    else: return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            github_token = request.form.get("input_data")
            auth = Auth.Token(gt) if github_token == "test" else Auth.Token(github_token)
            g.__init__(auth=auth)
            user = g.get_user()
            cache["user"] = user
            user.login # TODO check if actually needed
            return redirect(url_for("welcome"))
        except Exception as e:
            return render_template("home.html", error_message=str(e))
    return render_template("home.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if "user" not in cache: return redirect(url_for("index"))
    if request.method == "POST":
        repo_name = request.form["repo_name"]
        if repo_name == "test": repo_name = "magikarpusespash/SolidGoldMagikarp"  
        try: 
            repo = g.get_repo(repo_name)
            cache['repo'] = repo
        except Exception as e:
            return render_template("index.html", error_message=str(e) + "\n" + "invalid repository")
        return redirect(url_for("get_bounty_issues", repo_name=repo_name.replace("/", "-")))
    return render_template("index.html")

@app.route("/issues/<repo_name>")
def get_bounty_issues(repo_name: str):
    if (c := site_router()) is not None: return c
    repo = cache['repo']
    issues = [issue for issue in repo.get_issues(labels=["bounty"])]
    for i in issues: cache[str(i.number)] = i
    return render_template("issues.html", repo_name=repo_name, issues=issues)

@app.route("/issue/<repo_name>/<issue_number>")
def view_issue(repo_name: str, issue_number: int):
    if (c := site_router()) is not None: return c
    issue = cache[issue_number]
    return render_template("issue.html", issue=issue)

@app.route("/issue<repo_name>/<issue_number>/start")
def start_function(repo_name, issue_number):
    if (c := site_router()) is not None: return c
    # automatically fork the repo using repo_name
    user, repo = cache['user'], cache['repo']
    g.get_user()
    # repo.create_fork()

    # git clone https://github.com/your-username/repo_name.git

    # git checkout -b bounty/<branch-name>

    # git push origin bounty/<branch-name>

    return None

if __name__ == "__main__":
    app.run(debug=True)
