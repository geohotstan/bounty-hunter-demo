** Github Backend **
Issues
  - github issues is used as bounty tracker
  - issues tagged as bounty is tracked and displayed on site
Repo
  - repo is automatically forked upon user joining the bounty
Actions
  - github CI is used as basic filtering for bounty submissions

** Site Frontend ** 
minimize user's interaction with github interface
Payment
  - payout of bounty is handled on site upon closing the issue
Evaluation
  - automate the evaluation of the submissions using CI (unitest)
    and other tools (maybe LLMs?) to rate the responses before
    having human review
  - make clean interface for code reviewers (automatic branching
    and open code in vscode)
