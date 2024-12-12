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
        
    add_data_to_database(dataframe, "Brzina_Radnika")
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

    return pd.DataFrame(unique_values, columns=[column_name])

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
    return df_grouped.reset_index()

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
 
def worker_speed_best_all_time(df: pd.DataFrame) -> dict:
    
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

def add_data_to_database(df: pd.DataFrame, table_name):
    """Creates a table and inserts DataFrame data into an SQLite database.

    Args:
        df (pd.DataFrame): A DataFrame containing the data to be added to the database. 
            Expected columns are "Date", "Name", "Speed", and "Raw material".

    Returns:
        None
    """

    database = create_connection("baza_proizvodnja.db")
    df.to_sql(f"{table_name}", database, if_exists="replace", index=False)

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

def calculate_difference(df:pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the difference between the worker-specific average speed 
    and the process-specific average speed for each material ("Sirovina"). 

    The function computes the absolute difference and percentage difference 
    between the speeds, renames relevant columns, and returns a DataFrame 
    with the calculated metrics.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing production data, 
        including columns required to compute averages per person and process.

    Returns:
        pd.DataFrame: A DataFrame containing the following columns:
            - "Ime": Name of the worker.
            - "Sirovina": The raw material being processed.
            - "Prosječna brzina": Average speed for the process.
            - "Brzina": Speed achieved by the worker.
            - "Difference": The difference between the worker's speed and the process average.
            - "Difference %": The percentage difference relative to the worker's speed.
    """
    process_average = averages_per_process(df)
    worker_average = averages_per_person(df)
    

    merged_df = pd.merge(worker_average, process_average, on="Sirovina")
    merged_df['Difference'] = (merged_df['Brzina_x'] - merged_df['Brzina_y']).round(2)
    merged_df["Difference %"] = ((merged_df["Difference"]/merged_df["Brzina_y"])*100).round(2)
    merged_df = merged_df.rename(columns={"Brzina_x": "Brzina" ,"Brzina_y": "Prosječna brzina"})
    result_df = merged_df[['Ime', 'Sirovina', "Prosječna brzina","Brzina",'Difference', "Difference %"]]
    
    return result_df
            
def standard_deviation_per_process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the standard deviation of the "Brzina" column for each unique value in the "Sirovina" column.

    This function groups the input DataFrame by the "Sirovina" column and computes the standard deviation 
    of the "Brzina" column within each group. It is useful for analyzing variability in "Brzina" values 
    across different "Sirovina" categories.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing at least two columns:
            - "Sirovina": The column used for grouping.
            - "Brzina": The column for which the standard deviation is computed.

    Returns:
        pd.Series: A pandas Series where the index corresponds to the unique values in the "Sirovina" column,
        and the values are the standard deviations of the "Brzina" column within each group.
    """
    return df.groupby("Sirovina")["Brzina"].std()

def sort_workers(df: pd.DataFrame, ascending: bool) -> pd.DataFrame:
    df_average = averages_per_person(df)
    process_dfs = {process: group.sort_values(by="Brzina", ascending=ascending) for process, group in df_average.groupby("Sirovina")}    
    
    return process_dfs

def generate_report(checkbox1_state: int, checkbox2_state: int, checkbox3_state: int, checkbox4_state: int, checkbox5_state: int, checkbox6_state: int):
    
    data = pull_data_from_database("Brzina_Radnika")
    data_dict = {}

    if checkbox1_state == 1:
        data_dict["Prosjek po osobi"] = averages_per_person(data)
    if checkbox2_state == 1:
        data_dict["Prosjek po procesu"] = averages_per_process(data)
    if checkbox3_state == 1:
        data_dict["Odstupanje radnika od prosjeka"] = calculate_difference(data)
    if checkbox4_state == 1:
        data_dict["Standardna devijacija po procesu"] = standard_deviation_per_process(data)
    if checkbox5_state == 1:
       process_dict =  sort_workers(data, False)

       for process, process_df in process_dict.items():
           data_dict[f"{process} - najbrži"] = process_df[["Ime", "Sirovina", "Brzina"]]

    if checkbox6_state == 1:

        process_dict =  sort_workers(data, True)

        for process, process_df in process_dict.items():
           data_dict[f"{process} - najsporiji"] = process_df[["Ime", "Sirovina", "Brzina"]]

    create_document(data_dict)
    
  