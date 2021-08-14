import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List

def authenticateGDrive(jsonFilename:str) -> gspread.Client:
    """
    Authorises API client information from jsonFilename with Google Cloud Platform
    returns: authorised client as gspread.Client object
    """
    assert type(jsonFilename) == str, "jsonFilename must be a str"
    assert jsonFilename.endswith(".json"), f"{jsonFilename} is not a .json file"

    scope = ["https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonFilename, scope)
    client = gspread.authorize(creds)

    return client

def getData(client:gspread.Client, file:str, by="name", sheetNum=0) -> List[dict]:
    """
    gets data from sheetNum of file using an authenticated Google Cloud Platform client object
    - client = gspread.Client class 
    returns: list of each row in the spreadsheet as a dict with each col as key
    - example: [{"Serial No": 0, "Name": "Abby"}, {"Serial No": 1, "Name": "Jason"}]
    """
    assert type(file) == str, "file must be a str"
    assert type(sheetNum) == int and sheetNum >= 0, "sheetNum must be an int and at least 0"
    assert by in ["name", "id", "url"], "by must be one of name, id or url"

    if by == "name":
        sheets = client.open(file)
    elif by == "id":
        sheets = client.open_by_key(file)
    elif by == "url":
        sheets = client.open_by_url(file)

    data = sheets.get_worksheet(sheetNum)
    data = data.get_all_records()

    return data
