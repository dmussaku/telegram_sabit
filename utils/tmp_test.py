'''
step 3
Add a full traceback to exception to make sure the variable in the scope is printed in an exception.
'''

def get_message_text(message_struct: dict):
    message_text = message_struct['text']
    if type(message_text) in (str, bytes):
        pass
    elif type(message_text) == list:
        message_text = message_text[0]
    else:
        message_text = ""
    if type(message_text) != str:
        raise AttributeError(f'{message_text} is not a string. Cant use lower method on it')

    return message_text.lower().strip()