import GoogleDriveSheets as gds
import DataChecks as dc
import pandas as pd
import numpy as np

def getAllFileIDs(handler):
    """
    Gets all file IDs from the Google Drive folders (raw, clean, byHand)
    returns: cleaned{"byHand":[ids],"fromInst":[ids]}, raw[ids]
    """
    FOLDER_RAW_ID = "17JUv2o-fKmFsgg2m65HNO-TMDUdn5Q2U"
    FOLDER_CLEANED_ID = "191OoRTm1ip05Zuk7My-eMa-t9B2IeJbD"
    FOLDER_BYHAND_ID = "1hbsLRm_1x6adC1OZgULKw16O-li9hRBq"

    CLEANED_SHEETS_IDs = {"byHand":[], "fromInst":[]}
    FILES_IN_RAW_IDs = []

    filesInCleaned = handler.getFileListInFolder(FOLDER_CLEANED_ID, handler.getDriveService())
    for file in filesInCleaned:
        CLEANED_SHEETS_IDs["fromInst"].append(file["id"])

    filesInByHand = handler.getFileListInFolder(FOLDER_BYHAND_ID, handler.getDriveService())
    for file in filesInByHand:
        CLEANED_SHEETS_IDs["byHand"].append(file["id"])

    filesInRaw = handler.getFileListInFolder(FOLDER_RAW_ID, handler.getDriveService())
    for file in filesInRaw:
        FILES_IN_RAW_IDs.append([file["id"]])
        # print(file)
        # fileMimeType = file["mimeType"]
        # while fileMimeType == "application/vnd.google-apps.folder":
        #     childFilesinFile = handler.getFileListInFolder(file["id"], handler.getDriveService())
        #     FILES_IN_RAW_ID[file["id"]].add

    return CLEANED_SHEETS_IDs, FILES_IN_RAW_IDs


def commitFile(file):
    pass

def getAllJournals(handler) -> pd.DataFrame:
    journals = handler.getSheetsData(handler.getSheetsDriveClient(), "1W-A354T_93Nra8rKL_MY5tmwMDlfaLAdLKTwNUJv2EA")
    j_df = pd.DataFrame(journals)[["journal", "issn"]]
    return j_df

def main():

    handler = gds.Handler("creds.json", "client_secrets_GDrive-oauth2.json")
    ALL_JOURNAL_ISSN = getAllJournals(handler)   # pd.DataFrame
    CLEANED_SHEETS_IDs, FILES_IN_RAW_IDs = getAllFileIDs(handler)

    # for sheetID in CLEANED_SHEETS_IDs:

    #     # getting data from sheet as df
    #     sheet = handler.getSheetsData(handler.getSheetsDriveClient(), sheetID)
    #     df = pd.DataFrame(sheet).astype("string")

    #     # data checks
    #     correctShape, correctCols, noDuplicates = dc.basicChecks(df)
    #     if not correctShape: raise dc.DataChecksException("DataFrame shape is not (1372, 4).", sheetID, "correctShape", "")
    #     if not correctCols: raise dc.DataChecksException("DataFrame columns are not ['journal', 'issn', 'access', 'notes'].", sheetID, "correctCols", "")
    #     if not noDuplicates: raise dc.DataChecksException("DataFrame contains duplicates.", sheetID, "correctCols", "")

    #     hasNaN, detail = dc.hasNaN(df)
    #     if hasNaN:
    #         detail = "NaN values found in columns: " + str(detail)
    #         raise dc.DataChecksException(f"DataFrame contains NaN values", sheetID, "hasNaN", detail)

    #     allJournalsCounted, detail = dc.allJournalsCounted(df, ALL_JOURNAL_ISSN)
    #     if allJournalsCounted == False:
    #         detail = "uncounted journals: " + str(detail)
    #         raise dc.DataChecksException(f"Not all journals are present in DataFrame",  sheetID, "allJournalsCounted", detail)

    #      observed_df_journals_ISSN = df.drop(["access", "notes"], axis=1, inplace=False)
    #      journalsMatchISSN, detail = dc.journalsMatchISSN(ALL_JOURNAL_ISSN, observed_df_journals_ISSN)
    #      if journalsMatchISSN == False:
    #          detail = "mismatched journals: " + str(detail)
    #          raise dc.DataChecksException(f"Journal and ISSN mismatch found in DataFrame", sheetID, "journalsMatchISSN", detail)

    #     # upload sheet to GitHub repo
    #     # merge sheet to mainDB.csv

    #     pass


    sheetID = CLEANED_SHEETS_IDs["fromInst"][0]
    sheet = handler.getSheetsData(handler.getSheetsDriveClient(), sheetID)
    df = pd.DataFrame(sheet).astype("string")

    # data checks
    correctShape, correctCols, noDuplicates = dc.basicChecks(df)
    if not correctShape: raise dc.DataChecksException("DataFrame shape is not (1372, 4).", sheetID, "correctShape", "")
    if not correctCols: raise dc.DataChecksException("DataFrame columns are not ['journal', 'issn', 'access', 'notes'].", sheetID, "correctCols", "")
    if not noDuplicates: raise dc.DataChecksException("DataFrame contains duplicates.", sheetID, "correctCols", "")

    # hasNaN, detail = dc.hasNaN(df)
    # if hasNaN:
    #     detail = "NaN values found in columns: " + str(detail)
    #     raise dc.DataChecksException(f"DataFrame contains NaN values", sheetID, "hasNaN", detail)

    allJournalsCounted, detail = dc.allJournalsCounted(df, ALL_JOURNAL_ISSN)
    if allJournalsCounted == False:
        detail = "uncounted journals: " + str(detail)
        raise dc.DataChecksException(f"Not all journals are present in DataFrame",  sheetID, "allJournalsCounted", detail)

    observed_df_journals_ISSN = df.drop(["access", "notes"], axis=1, inplace=False)
    journalsMatchISSN, detail = dc.journalsMatchISSN(ALL_JOURNAL_ISSN, observed_df_journals_ISSN)
    if journalsMatchISSN == False:
        detail = "mismatched journals: " + str(detail)
        raise dc.DataChecksException(f"Journal and ISSN mismatch found in DataFrame", sheetID, "journalsMatchISSN", detail)



main()
