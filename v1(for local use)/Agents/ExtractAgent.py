from email import policy
from email.parser import BytesParser
from io import BytesIO
import json
from email import errors as ermail
from PyPDF2 import PdfReader
from PyPDF2 import errors as erpdf
import os

class ExtractAgent:
    """
    ExtractAgent handles extracting content from different file types:
    - JSON files
    - PDF files
    - Email files (.eml)

    Attributes:
    ----------
    file : file-like object
        The file to be processed.

    Methods:
    -------
    get_content(ftype):
        Extracts and returns the content of the file based on the specified file type.
    """

    def __init__(self, file):
        """
        Initialize the ExtractAgent with a file object.

        Parameters:
        ----------
        file : file-like object
            The file to process (selected via file dialog or other input).
        """
        self.file = file

    def get_content(self, ftype):
        """
        Extracts content from the file based on its type.

        Parameters:
        ----------
        ftype : str
            The type of the file: 'json', 'pdf', or 'email'.

        Returns:
        -------
        dict
            A dictionary containing:
            - 'content': The extracted content (text or structured data).
            - 'metadata': Metadata about the file (name, size).
            - or 'error': An error message if extraction fails.
        """

        self.ftype = ftype

        # For filetype JSON
        if self.ftype == 'json':
            try:
                with open(f'{self.file.name}', 'r') as f:
                    content = json.load(f)
            except FileNotFoundError as e:
                return {'error': f'File not found! {e}'}
            except json.JSONDecodeError as e:
                return {'error': f'Decode Error! {e}'}
            return {
                'content': content,
                'metadata': {
                    'file_name': os.path.basename(self.file.name),
                    # 'file_path': self.file.name,
                    'file_size': os.path.getsize(self.file.name) / 1024**2  # Size in MB
                }
            }

        # For filetype PDF
        elif self.ftype == 'pdf':
            try:
                content = PdfReader(self.file.name)
            except erpdf.EmptyFileError as e:
                return {'error': f'The given file is empty! {e}'}
            except erpdf.ParseError as e:
                return {'error': f'Parse error! {e}'}
            except erpdf.PdfReadError as e:
                return {'error': f'Error reading pdf {e}'}

            pages_text = ''
            for page in content.pages:
                pages_text += page.extract_text() or ''
            return {
                'content': pages_text,
                'metadata': {
                    'file_name': os.path.basename(self.file.name),
                    # 'file_path': self.file.name,
                    'file_size': os.path.getsize(self.file.name) / 1024**2 
                }
            }

        # For filetype Email (.eml)
        elif self.ftype == 'email':
            try:
                with open(f'{self.file.name}', 'rb') as f:
                    content = f.read()
                    email_parsed = BytesParser(policy=policy.default).parse(BytesIO(content))
                    if email_parsed.is_multipart():
                        # Currently not handling multipart emails
                        for part in email_parsed.walk():
                            return {'error': 'multipart/alternative not supported. Please provide another email file'}
            except FileNotFoundError as e:
                return {'error': f'File not found! {e}'}
            except ermail.MessageParseError as e:
                return {'error': f'Parse error!{e}'}

            return {
                'content': {
                    'SUBJECT': email_parsed['SUBJECT'],
                    'FROM': email_parsed['FROM'],
                    'BODY': email_parsed.get_content().strip()
                },
                'metadata': {
                    'file_name': os.path.basename(self.file.name),
                    # 'file_path': self.file.name,
                    'file_size': os.path.getsize(self.file.name) / 1024**2
                }
            }
