# this script should run every time there is a new push to the data folder
import pandas as pd 
from github import Github

GITHUB_TOKEN = "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"

PATH_mainDB = "data//from-GDrive//mainDB.csv"
# fh = open(PATH_mainDB)

# df = pd.DataFrame({"col1":[1,2,3], "col2":[4,5,6]})
# df.to_csv(PATH_mainDB)

g = GitHub(GITHUB_TOKEN)
repo = g.get_repo("colebrookson/research-access")
mainDB = repo.get_contents(PATH_mainDB, ref="testDel")
repo.delete_file(mainDB.path, "remove test", contents.sha, branch="master")

# >>> repo = g.get_repo("PyGithub/PyGithub")
# >>> contents = repo.get_contents("test.txt", ref="test")
# >>> repo.delete_file(contents.path, "remove test", contents.sha, branch="test")
# {'commit': Commit(sha="0f40b0b4f31f62454f1758d7e6b384795e48fd96"), 'content': NotSet}
