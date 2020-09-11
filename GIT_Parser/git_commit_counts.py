import requests, dateutil.parser
import getpass
from datetime import date





class git_repo_analysis:

    def __init__(self, username, password):
        self.totalCommits = 0
        self.totalAdd = 0
        self.totalRemove = 0
        self.overallAdd = 0
        self.overallRemove = 0
        self.commitCount = 0
        self.commits = []
        self.username = username
        self.password = password
        self.year = date.today().year
        self.gitUrl_base = "https://api.github.com/users/biplabsarkar99/repos"
        self.gitUrl_collaborators = "https://api.github.com/repos/biplabsarkar99/python-learning/collaborators"

    def check_repo(self):
        print("")
        print("Stats for {year}".format(year=self.year))
        print("")

        r = requests.get("{gitURL}".format(gitURL=self.gitUrl_base),
                         auth=(self.username, self.password))

        repos = r.json()
        my_repo = ""
        print(repos)

        for repo in repos:
            print(repo)
            for item in repo:
                print("\t {} : {}".format(item,repo[item]))
            if repo['name'] == "python-learning":
                print("We have python-learning access")
                my_repo = repo
                break
        else:
            raise ValueError("Repo Not found.")

        commit_count = 0
        print(my_repo)
        commits_details_url = "/".join(repo['commits_url'].split("{")[:-1])
        self.total_commits = requests.get(commits_details_url)
        self.totalCommits = len(self.total_commits.json())
        for commit in self.total_commits.json():
            print("########################################")
            print(commit)
            print("########################################")
            if commit['commit']['committer']['name'] == "vallabh chugh":
                commit_count += 1

        print("Total commits: {count}".format(count=self.totalCommits))
        print("Total commits made by {} are : {}".format(self.username, commit_count))
        print("Total lines added: {count}".format(count=self.overallAdd))
        print("Total lines removed: {count}".format(count=self.overallRemove))

        print("#################################################")
        r1 = requests.get("{gitURL}".format(gitURL=self.gitUrl_collaborators),
                         auth=(self.username, self.password))

        for entry in r1.json():
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(entry)
            if entry['login'] == self.username:
                print(entry['events_url'])

            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


if __name__=="__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    gitHandle = git_repo_analysis(username, password)
    print(gitHandle)
    print("Handle created succesfully.")
    gitHandle.check_repo()