import logging


def is_valid(news, field=None):
    """Checks fields in a news object for validity. If a field does not exist,
    or its value is not defined, return False.

    # Arguments
        news: a news dictionary object
        field: field to be checked for validity

    # Returns:
        valid: returns true if field is valid
    """
    try:
        news[field]
    except:
        return False
    if news[field]:
        return True
    return False
