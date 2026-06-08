def shorten_uuid(uuid_obj, length=8):
    """
    Generate a human-readable identifier from a UUID.

    By default, returns the first 8 characters.
    """
    if not uuid_obj:
        return ""
    return str(uuid_obj).split("-")[0][:length].upper()
