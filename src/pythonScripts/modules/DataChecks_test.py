from DataChecks import *
import pytest

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

