from CTkMessagebox import CTkMessagebox

def error(text: str):

    CTkMessagebox(title= "Error", message= text)

def info(text: str):

    CTkMessagebox(title= "Info", message= text)