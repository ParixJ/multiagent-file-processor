from email import message_from_file

def get_type(file):
    """
    Determines the type of the provided file based on its extension
    and, if necessary, basic content inspection.

    Parameters:
    ----------
    file : file-like object
        The file to check (e.g., selected from a file dialog).

    Returns:
    -------
    str or None
        - 'json' if the file extension is .json
        - 'pdf' if the file extension is .pdf
        - 'email' if the file extension matches email types
          or if basic content inspection detects email headers
        - None if the type cannot be determined
    """

    # Extract the lowercase file extension
    file_extention_ = file.name.lower().split('.')[-1]

    # Determine type by extension
    if file_extention_ == 'json':
        return 'json'
    elif file_extention_ == 'pdf':
        return 'pdf'
    elif file_extention_ in ['eml', 'msg', 'emlx', 'mbox', 'pst', 'ost']:
        return 'email'

    # If extension check fails, inspect file content for email headers
    try:
        email_parsed = message_from_file(file)
        if email_parsed['From'] and email_parsed['To'] and email_parsed['Subject']:
            return 'email'
    except Exception as e:
        # Optional: Log the error for debugging
        print(f"Error parsing file as email: {e}")

    # If no match found
    return None
