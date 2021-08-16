# this script should run every time there is a new push to the data folder
import pandas as pd 

PATH_mainDB = "data//from-GDrive//mainDB.csv"
fh = open(PATH_mainDB)

df = pd.DataFrame({"col1":[1,2,3], "col2":[4,5,6]})
df.to_csv(PATH_mainDB)
