from Agents import FileTypeAgent,IntentAgent,ExtractAgent,UrgencyAgent
import numpy as np
from utils.decorators import decorator_main
from tkinter.filedialog import FileDialog

@decorator_main
# Main routing function for routing file to the desired Agent
async def route(file: FileDialog):

    # Returns the filetype
    ftype = FileTypeAgent.get_type(file)

    # initialise the Extract agent
    extractor_agent = ExtractAgent.ExtractAgent(file)
    
    # If the filetype is None or unsupported return None
    if ftype is None:

        return None
    
    else:

        # Returns file data like metadata, name,etc
        file_info = extractor_agent.get_content(ftype)

        # If the file_info dictionary contains the key error return the dictionary itself
        if 'error' in file_info:

            return file_info
        
        else:
            # Extracts and store email data into variables
            # This condition processes data for only filetype email
            # so the variables store the email-like data like sender, subject, etc
            if ftype == 'email':
                email_sender = file_info['content']['FROM']
                email_subject = file_info['content']['SUBJECT']
                content = file_info['content']['BODY']
                file_metadata = file_info['metadata']

            # Stores data for filetypes like PDF and JSON
            else: 
                content = file_info['content']
                file_metadata = file_info['metadata']

    # Initialise file intention classifying Agent
    intentAgent = IntentAgent.IntentAgent()
    # Initialise file urgency classifying Agent
    urgencyAgent = UrgencyAgent.UrgencyAgent()

    # Retrieve file intention and urgency from the api asyncronously
    fintent_ = await intentAgent.get_data(content)
    urgency_ = await urgencyAgent.get_data(content)
    
    # If the intent and urgency dictionary are valid 
    # they contain keys like labels and scores
    if ('labels' and 'scores' in fintent_) and ('labels' and 'scores' in urgency_):
        text_intention = fintent_['labels'][np.argmax(fintent_['scores'])]
        text_urgency = urgency_['labels'][np.argmax(urgency_['scores'])]
        
    # else if they contain key error then an API error has occured
    elif 'error' in fintent_ and urgency_:
        return {'error':f'API error. Returned {fintent_["error"],urgency_["error"]}. Please enter a valid file or try again.'}

    # Returns dictionary containing file data
    return {'file_type': ftype,
            # If the filetype was email then include the data sender and subject
            # else return empty string
            'sender': email_sender if ftype == 'email' else '-',
            'subject': email_subject if ftype == 'email' else '-',
            'file_intent':text_intention,
            'file_urgency':text_urgency,
            'file_metadata':file_metadata}