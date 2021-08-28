from DataChecks import *
import pytest
import pandas as pd

@pytest.fixture
def load_data():
    df = pd.DataFrame({
        "journal": ["3 BIOTECH", "MOLECULAR BIOLOGY REPORTS", "APPLIED MATHEMATICAL MODELLING", "GENOME", "SCIENCE", "NATURE"],
        "issn": ["2190-572X", "0301-4851", "0307-904X", "0831-2796", "0036-8075", "0028-0836"],
        "access": ["1", "1", "0", "1", "0", "1"],
        "notes": ["some notes", "", "", "", "", ""]
    })
    return df

def test_check_issn() -> None:
    pass

def test_check_journal() -> None:
    pass

def test_check_access() -> None:
    pass

def test_check_notes() -> None:
    pass

def test_validate_cISSN() -> None:
    assert validate_cISSN("0046-225X") == True
    assert validate_cISSN("0091-6765") == True
    assert validate_cISSN("0091-676X") == False
    assert validate_cISSN("1313-4131") == False
    assert validate_cISSN("0000-0000") == True
    assert validate_cISSN("0000-0001") == False
    assert validate_cISSN("0000-000X") == False
    assert validate_cISSN("9999-9999") == False
    assert validate_cISSN("9999-999X") == False
    assert validate_cISSN("1234-1234") == False

    with pytest.raises(Exception):
        assert validate_cISSN(1) == Exception
        assert validate_cISSN("bjhbvj") == Exception
        assert validate_cISSN(1323-1231) == Exception
        assert validate_cISSN("00916765") == Exception
        assert validate_cISSN("0091-676Y") == Exception

def test_hasNaN(load_data) -> None:
    df = load_data
    print(df)
    assert hasNaN(df) == (False, [])
    assert hasNaN(df, includeNotes=True) == (True, ["notes"])

    df1 = df.replace("NATURE", np.nan, inplace=False)
    assert hasNaN(df1) == (True, ["journal"])
    del df1

    df2 = df.replace("SCIENCE", "", inplace=False)
    assert hasNaN(df2) == (True, ["journal"])
    del df2

    df3 = df.replace({"0307-904X": None}, inplace=False)
    assert hasNaN(df3) == (True, ["issn"])
    print(df3)
    del df3

def test_allJournalsCounted(load_data) -> None:
    df = load_data
    print(df)




