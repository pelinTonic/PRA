import pandas as pd
from DB_manager import *
from report_generation import create_document

def excel_to_dateframe(path_to_excel: str, sort: str = None) -> pd.DataFrame: 
    """   This function reads an Excel file and converts into a pandas DataFrame. 
        It also sorts the DataFrame based on a specified column if provided.

    Args:
        path_to_excel (str): The path to the Excel file
        sheet (str): The name of the sheet to be converted into a DataFrame
        sort (str, optional): The column name to sort the DataFrame by. Defaults to None.

    Returns:
        pd.DataFrame: The DataFrame obtained from the specified sheet of the Excel file, sorted by the specified column if provided
    """
    dataframe = pd.read_excel(path_to_excel)
    if sort is not None:
        dataframe = dataframe.sort_values(by=sort)
        
    add_data_to_database(dataframe)
    return dataframe

def get_column_names(dataframe: pd.DataFrame) -> list:
    """This function reads dataframe and returns headers as a list

    Args:
        dataframe (pd.DataFrame): dataframe

    Returns:
        list: list of headers
    """
    
    return dataframe.columns.values.tolist()

def unique_values(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """This function extracts the unique values from a specified column in a pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame from which to extract unique values.
        column_name (str): The name of the column from which to extract unique values.

    Returns:
        pd.DataFrame: A DataFrame containing the unique values from the specified column.
    """
    unique_values = dataframe[column_name].unique()

    return unique_values

def filter_value(dataframe: pd.DataFrame, column_name: str) -> dict:
    """    This function filters a DataFrame based on unique values of a specified column. 
        It returns a dictionary where each key is a unique value from the specified column, 
        and the corresponding value is a DataFrame filtered by that unique value.

    Args:
        dataframe (pd.DataFrame): The DataFrame to be filtered
        column_name (str): The name of the column based on whose unique values the DataFrame will be filtered.

    Returns:
        dict: A dictionary where each key is a unique value from the specified column, 
        and the corresponding value is a DataFrame filtered by that unique value.
    """

    return {group: data for group, data in dataframe.groupby(column_name)}

def count_workers_in_process(dataframe: pd.DataFrame) -> dict:
    """
    Count the number of occurrences of workers' names ('Ime') for each material ('Sirovina').

    This function filters the input DataFrame by 'Sirovina' (raw material), then counts how many times each worker's name 
    ('Ime') appears for each material. The result is a dictionary where the keys are materials and the values are 
    pandas Series containing the worker counts.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing at least two columns - 'Sirovina' (raw material) 
                                  and 'Ime' (worker name).

    Returns:
        dict: A dictionary where each key is a raw material, and the corresponding value is a pandas Series representing 
              the count of occurrences of each worker's name ('Ime') for that material.
    """
    raw_material = filter_value(dataframe, "Sirovina")
    return {material: df["Ime"].value_counts() for material, df in raw_material.items()}

def averages_per_process(df: pd.DataFrame) -> dict:
    """Calculate the average speed for each process based on the provided DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing the data.

    Returns:
        dict: A dictionary where keys are the process names ('Sirovina' values) and values are the corresponding average speeds.
        
    """
    return df.groupby("Sirovina")["Brzina"].mean().round(2)

def averages_per_person(df: pd.DataFrame) -> dict:
    """
    Calculate the average 'Brzina' for each 'Ime' and 'Sirovina' combination in the given DataFrame.

    This function groups the DataFrame by 'Ime' and 'Sirovina', calculates the mean of 'Brzina' for each group,
    rounds the mean values to 2 decimal places, and returns a nested dictionary where the outer dictionary's keys
    are the 'Ime' values and the inner dictionaries' keys are the 'Sirovina' values.

    Parameters:
    df (pandas.DataFrame): The input DataFrame. It should have columns 'Ime', 'Sirovina', and 'Brzina'.

    Returns:
    dict: A nested dictionary where the outer dictionary's keys are the 'Ime' values and the inner dictionaries'
    keys are the 'Sirovina' values. The values of the inner dictionaries are the average 'Brzina' for the corresponding
    'Ime' and 'Sirovina'.
    """
    df_grouped = df.groupby(['Ime', 'Sirovina'])['Brzina'].mean().round(2)
    return df_grouped

def filter_material(df: pd.DataFrame, material: str) -> pd.DataFrame:

    """
    Filters the DataFrame for the specified material and calculates the average speed (Brzina)
    per person (Ime) for each process involving that material.

    Args:
        df (pd.DataFrame): The DataFrame containing the data with columns "Sirovina", "Ime", and "Brzina".
        material (str): The material to filter by (column "Sirovina").

    Returns:
        pd.DataFrame: A DataFrame filtered by the given material with an additional column 
                      for the average speed (Average_Brzina) per person.
    """
    average_speeds_per_person_process = df.groupby(["Sirovina", "Ime"])["Brzina"].mean().reset_index()

  
    average_speeds_per_person_process.columns = ["Sirovina", "Ime", "Average_Brzina"]
    searched_material = df[df["Sirovina"] == material]

    return searched_material

def worker_speed_best_average(df: pd.DataFrame) ->pd.DataFrame:
    """
    Calculates and returns a DataFrame containing the average performance metrics 
    for workers based on the specific material they process. The function processes 
    the input DataFrame by filtering for unique materials, computing per-person 
    averages for each material, and combining the results.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing data about workers and 
        their performance metrics. The DataFrame is expected to have a column 
        named "Sirovina" that indicates the type of material processed.

    Returns:
        pd.DataFrame: A DataFrame containing the average performance metrics 
        for workers, grouped by material type. The output is a concatenation of 
        individual material-wise results.
    """
   
    materials = unique_values(df, "Sirovina")
    results = [] 

    for material in materials:

        searched_material = filter_material(df, material)
        result = averages_per_person(searched_material)
        results.append(result)
    
    final_result = pd.concat(results)
    return final_result
    
def worker_speed_best_all_time(df: pd.DataFrame) -> dict:
    #Trebala bi vratit samo najboljeg radnika po prosjeku u jednom procesu
    """  Finds the best worker speeds for each material.

    This function takes a DataFrame containing worker speed data and returns a dictionary 
    where the keys are unique materials (from the "Sirovina" column), and the values are 
    DataFrames sorted by the highest worker speed (from the "Brzina" column) in descending order.

    Args:
        df (pd.DataFrame): A DataFrame containing at least the following columns:
            - 'Sirovina': The material for which the worker speed is recorded.
            - 'Brzina': The speed of the worker for that material.

    Returns:
        dict: A dictionary where each key is a unique material (from the 'Sirovina' column), 
              and the corresponding value is a DataFrame of rows related to that material,
              sorted by the 'Brzina' column in descending order (best speed first).
    """
    materials = unique_values(df, "Sirovina")
    result = {}

    for material in materials:
        df_group = df[df["Sirovina"] == material]
        df_group = df_group.sort_values(by = "Brzina", ascending=False)
        result[material] = df_group

    return result

def add_data_to_database(df: pd.DataFrame):
    """Creates a table and inserts DataFrame data into an SQLite database.

    Args:
        df (pd.DataFrame): A DataFrame containing the data to be added to the database. 
            Expected columns are "Date", "Name", "Speed", and "Raw material".

    Returns:
        None
    """

    database = create_connection("baza_proizvodnja.db")
    # create_table_query = """CREATE TABLE Brzina_Radnika (
    #     Date TEXT,
    #     Name TEXT,
    #     Speed REAL,
    #     Raw material TEXT
    # )"""

    #create_table(database, create_table_query)
    df.to_sql("Brzina_Radnika", database, if_exists="replace", index=False)


def pull_data_from_database(table_name: str):

    """Fetches all data from a specified database table and converts it to a DataFrame.

    Args:
        table_name (str): The name of the database table to retrieve data from.

    Returns:
        pd.DataFrame: A DataFrame containing all rows from the specified table, 
        with columns: "Date", "Name", "Speed", and "Raw material".
    """
    database = create_connection("baza_proizvodnja.db")
    pull_query = f"SELECT * FROM {table_name}"
    data = get_all_data(database, pull_query)
    columns = get_sql_column_names(database, table_name)

    dataframe = pd.DataFrame(data, columns=columns)
    
    return dataframe



def generate_report(checkbox1_state, checkbox2_state, checkbox3_state, checkbox4_state, checkbox5_state, checkbox6_state):
    
    data = pull_data_from_database("Brzina_Radnika")
    data_dict = {}

    if checkbox1_state == 1:
        data_dict["Prosjek po osobi"] = averages_per_person(data)
    if checkbox2_state == 1:
        data_dict["Prosjek po procesu"] = averages_per_process(data)
    if checkbox3_state == 1:
        print("3")
    if checkbox4_state == 1:
        print("4")
    if checkbox5_state == 1:
        data_dict["Prosječna brzina svakog radnika"] = worker_speed_best_average(data)
    if checkbox6_state == 1:
        print("6")
    
    create_document(data_dict)
  