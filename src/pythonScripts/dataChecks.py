def validate_cISSN(issn:str) -> bool:
    """
    Validates the last character (c) of the ISSN number, based on the first 7 digits
    returns: boolean: True if c is valid False otherwise
    """
    assert type(issn) == str, "issn must be a string"

    issn_num = issn[:4] + issn[5:-1]
    issn_c = issn[-1]

    # check c validity
    issn_num_sum = 0
    inv_index = 8
    for num in issn_num:
        num = int(num)
        issn_num_sum += num*inv_index
        inv_index -= 1
        
    mod = issn_num_sum%11
    if mod == 0: c = 0
    else:
        c = 11-mod
        if c == 10: c = 'X'

    return str(c) == issn_c