import requests, dateutil.parser

gitUrl = "https://api.github.com/users/biplabsarkar99/repos"
gitUrl_contributor = "https://api.github.com/repos/biplabsarkar99/python-learning/collaborators"

username = "VaniChugh"
password = "Kanhajii@9"
year = 2020

totalCommits = 0
totalAdd = 0
totalRemove = 0
overallAdd = 0
overallRemove = 0
commitCount = 0
commits = []

print("")
print("Stats for {year}".format(year=year))
print("")

r = requests.get("{gitURL}".format(gitURL=gitUrl),
                 auth=(username, password))

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
total_commits = requests.get(commits_details_url)
totalCommits = len(total_commits.json())
for commit in total_commits.json():
    print("########################################")
    print(commit)
    print("########################################")
    if commit['commit']['committer']['name'] == "vallabh chugh":
        commit_count += 1


print("")
print("Total commits: {count}".format(count=totalCommits))
print("Total commits made by {} are : {}".format(username, commit_count))
print("Total lines added: {count}".format(count=overallAdd))
print("Total lines removed: {count}".format(count=overallRemove))

print("#################################################")
r1 = requests.get("{gitURL}".format(gitURL=gitUrl_contributor),
                 auth=(username, password))

for entry in r1.json():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(entry)
    if entry['login'] == 'VaniChugh':
        print(entry['events_url'])

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")