# this script should run every time there is a new push to the data folder
import pandas as pd

<<<<<<< HEAD
PATH_mainDB = "data//from-GDrive//mainDB.csv"
fh = open(PATH_mainDB)

df = pd.DataFrame({"col1":[1,2,3], "col2":[4,5,6]})
pd.to_csv(PATH_mainDB)
=======
PATH = "data//from-GDrive//mainDB.csv"
fh = open(PATH)
print(fh)

>>>>>>> 33bfd3a04c59f78ce47f62a023dd3553dff37ece
