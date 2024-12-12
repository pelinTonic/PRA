import customtkinter as ctk
from functions import excel_to_dateframe, generate_report,add_data_to_database, pull_data_from_database, unique_values
from customtkinter import filedialog
from error import error
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import pandas as pd

def save_selected_workers(checkboxes: list):
    
    dataframe = []
    
    for checkbox in checkboxes:
        
        if checkbox.get() == 1:
            text = checkbox.cget("text")
            dataframe.append(text)
        else:
            pass
    dataframe = pd.DataFrame(dataframe)
    add_data_to_database(dataframe, "Radnici")
            

def reset_selected_workers(checkboxes: list):

    for checkbox in checkboxes:
        checkbox.deselect()


def worker_selection_screen(root_workers):

    checkbox_frame = ctk.CTkScrollableFrame(master=root_workers)
    checkbox_frame.pack(padx = 5, pady = 5)

    button_frame = ctk.CTkFrame(master=root_workers)
    button_frame.pack(padx = 5, pady = 5)

    data = pull_data_from_database("Brzina_Radnika")
    worker_names = unique_values(data, "Ime")
    
    checkboxes = []

    for index, worker in worker_names.itertuples():
        checkbox = ctk.CTkCheckBox(checkbox_frame, text = worker, width=300, onvalue=1, offvalue=0)
        checkbox.grid(row = index , column = 0, padx = 5, pady = 5)
        checkboxes.append(checkbox)

    save_button = ctk.CTkButton(button_frame, text="Save selection", command=lambda: save_selected_workers(checkboxes))
    save_button.grid(row = 0, column = 0, padx = 5, pady = 5)

    reset_button = ctk.CTkButton(button_frame, text="Reset Selection", command=lambda: reset_selected_workers(checkboxes))
    reset_button.grid(row = 0, column = 1, padx = 5, pady = 5)
   

def open_worker_selection_screen():
    root_workers = ctk.CTk()
    worker_selection_screen(root_workers)
    root_workers.mainloop()

def select_file(file_path_entry: ctk.CTkEntry, root: ctk.CTk):

    file_types = [("Excel files", "*xlsx"), ("CSV files", "*csv")]
    filename = filedialog.askopenfilename(filetypes= file_types)

    if filename: 
        filepath = os.path.abspath(filename)
        
        if filepath.endswith((".xlsx", ".csv")):
            file_path_entry.insert(ctk.END, filepath)
            
            upload_data_button_frame = ctk.CTkFrame(root)
            upload_data_button_frame.pack(padx = 5, pady = 5)

            upload_data_button = ctk.CTkButton(upload_data_button_frame, text = "Upload file", command= lambda: (excel_to_dateframe(filepath), selection_screen(root)))
            upload_data_button.pack(padx = 5, pady = 5)

        else:
            error("File not supported")
            file_path_entry.delete(0, "end")
    else:
        error("File not selected")
        file_path_entry.delete(0, "end")

def selection_screen(root: ctk.CTk):
    
    checkbox_frame = ctk.CTkFrame(root)
    checkbox_frame.pack(padx = 5, pady = 5)

    checkbox1 = ctk.CTkCheckBox(checkbox_frame, text = "Prosjek po radniku", width=300, onvalue=1, offvalue=0)
    checkbox1.grid(row = 0, column = 0, padx = 5, pady = 5)

    checkbox2 = ctk.CTkCheckBox(checkbox_frame, text = "Prosjek po procesu", width=300, onvalue=1, offvalue=0)
    checkbox2.grid(row = 0, column = 1, padx = 5, pady = 5)

    checkbox3 = ctk.CTkCheckBox(checkbox_frame, text = "Odstupanje radnika od prosjeka", width=300, onvalue=1, offvalue=0)
    checkbox3.grid(row = 1, column = 0, padx = 5, pady = 5)

    checkbox4 = ctk.CTkCheckBox(checkbox_frame, text = "Standardna devijacija po procesu", width=300, onvalue=1, offvalue=0)
    checkbox4.grid(row = 1, column = 1, padx = 5, pady = 5)

    checkbox5 = ctk.CTkCheckBox(checkbox_frame, text = "Najbolji radnici po procesu", width=300, onvalue=1, offvalue=0)
    checkbox5.grid(row = 2, column = 0, padx = 5, pady = 5)

    checkbox6 = ctk.CTkCheckBox(checkbox_frame, text = "Najgori radnici po procesu", width=300, onvalue=1, offvalue=0)
    checkbox6.grid(row = 2, column = 1, padx = 5, pady = 5)

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(padx = 5, pady = 5)

    generate_report_button = ctk.CTkButton(button_frame, text = "Generate report", command= lambda: generate_report(checkbox1.get(), checkbox2.get(), checkbox3.get(), checkbox4.get(), checkbox5.get(), checkbox6.get()))
    generate_report_button.pack(padx = 5, pady = 5)

def show_main_screen(root: ctk.ctk_tk):

    main_frame = ctk.CTkFrame(root, width=720, height=800)
    main_frame.pack(padx = 5, pady = 5)

    file_path_entry = ctk.CTkEntry(main_frame)
    file_path_entry.grid(row = 1, column = 0, padx = 5, pady = 5)

    select_file_button = ctk.CTkButton(main_frame, text="Workers", command=lambda: open_worker_selection_screen())
    select_file_button.grid(row = 0, column = 1, padx = 5, pady = 5)
    
    select_file_button = ctk.CTkButton(main_frame, text="Select file", command=lambda: select_file(file_path_entry, root))
    select_file_button.grid(row = 1, column = 1, padx = 5, pady = 5)

def app():

    root = ctk.CTk()
    show_main_screen(root)
    root.mainloop()

app()