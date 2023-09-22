#! /usr/bin/env python3
import os
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for
from github import Github, Issue, Auth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
g = Github()
gt = os.getenv("GT", None)
loggedin = False
cache: Dict[str, Issue.Issue] = {}

def site_router():
    try: 
        g.get_user().login
    except: 
        return redirect(url_for("index"))
    if not cache: 
        return redirect(url_for("welcome"))
    else: 
        return None
            

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            github_token = request.form.get("input_data")
            auth = Auth.Token(gt) if github_token == "test" else Auth.Token(github_token)
            g.__init__(auth=auth)
            g.get_user().login
            return redirect(url_for("welcome"))
        except Exception as e:
            return render_template("home.html", error_message=str(e))
    return render_template("home.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    try: g.get_user().login
    except: return redirect(url_for("index"))
    if request.method == "POST":
        repo_name = request.form["repo_name"]
        repo_name = "geohotstan/SolidGoldMagikarp" if repo_name == "test" else repo_name
        return redirect(url_for("get_bounty_issues", repo_name=repo_name.replace("/", "_")))
    return render_template("index.html")

@app.route("/issues/<repo_name>")
def get_bounty_issues(repo_name: str):
    try: g.get_user().login
    except: return redirect(url_for("index"))
    repo = g.get_repo(repo_name.replace("_", "/"))
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
    # fork the repo under a fork name bounty/<name>
    return None

if __name__ == "__main__":
    app.run(debug=True)
