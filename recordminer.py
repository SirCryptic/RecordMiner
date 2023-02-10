import os
import csv
import sqlite3
import json
import pandas as pd
import concurrent.futures

# Developer: SirCryptic (NullSecurityTeam)
# Info: RecordMiner 1.0
# dly4evarjw
# Fuck The System Before It Fucks You!
os.system('cls' if os.name == 'nt' else 'clear')
banner = '''
________                        ______________  _______                    
___  __ \_____________________________  /__   |/  /__(_)___________________
__  /_/ /  _ \  ___/  __ \_  ___/  __  /__  /|_/ /__  /__  __ \  _ \_  ___/
_  _, _//  __/ /__ / /_/ /  /   / /_/ / _  /  / / _  / _  / / /  __/  /    
/_/ |_| \___/\___/ \____//_/    \__,_/  /_/  /_/  /_/  /_/ /_/\___//_/     
                                                                           
'''

print(banner)

def search_file(file_path, name, dob, address):
    if not os.path.exists(file_path):
        return []

    file_ext = os.path.splitext(file_path)[1]
    results = []

    if file_ext == ".csv":
        try:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                headers = next(reader)
                for row in reader:
                    if name in row and (not dob or dob in row) and (not address or address in row):
                        results.append(dict(zip(headers, row)))
        except Exception as e:
            print(f"An error occured while reading the CSV file: {e}")
    elif file_ext == ".txt":
        try:
            with open(file_path, "r") as f:
                for line in f:
                    if name in line and (not dob or dob in line) and (not address or address in line):
                        results.append({"content": line})
        except Exception as e:
            print(f"An error occured while reading the text file: {e}")
    elif file_ext == ".sql":
        try:
            conn = sqlite3.connect(file_path)
            c = conn.cursor()
            query = f"SELECT * from records where name like '%{name}%'"
            if dob:
                query += f" and dob like '%{dob}%'"
            if address:
                query += f" and address like '%{address}%'"
            c.execute(query)
            rows = c.fetchall()
            headers = [desc[0] for desc in c.description]
            for row in rows:
                results.append(dict(zip(headers, row)))
            conn.close()
        except Exception as e:
            print(f"An error occured while reading the SQLite file: {e}")
    elif file_ext == ".json":
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                for record in data:
                    if name in record.values() and (not dob or dob in record.values()) and (not address or address in record.values()):
                        results.append(record)
        except Exception as e:
            print(f"An error occured while reading the JSON file: {e}")
    elif file_ext == ".xlsx":
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            headers = df.columns.tolist()
            for i, row in df.iterrows():
                if name in row.values and (not dob or dob in row.values) and (not address or address in row.values):
                    results.append(dict(zip(headers, row.tolist())))
        except Exception as e:
            print(f"An error occured while reading the xlsx file: {e}")
    return results

def main(folder_location):
    name = input("Enter the name to search: ")
    dob = input("Enter the date of birth (optional): ")
    address = input("Enter the address (optional): ")

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        filenames = os.listdir(folder_location)
        future_to_filename = {executor.submit(search_file, os.path.join(folder_location, filename), name, dob, address): filename for filename in filenames}
        for future in concurrent.futures.as_completed(future_to_filename):
            result = future.result()
            results.extend(result)

    if results:
        save = input("Do you want to save the results to a text file (yes/no)? ")
        if save.lower() == "yes":
            with open(f"{name}.txt", "w") as f:
                for result in results:
                    f.write(str(result))
                    f.write("\n")

        print("Results:")
        for result in results:
            print(result)
    else:
        print("No results found.")
if __name__ == "__main__":
    folder_location = input("Enter the folder location: ")
    while not os.path.isdir(folder_location):
        print(f"Error: '{folder_location}' is not a valid directory.")
        folder_location = input("Enter the folder location: ")

    try:
        main(folder_location)
    except FileNotFoundError:
        print(f"Error: The directory '{folder_location}' does not exist.")

    main(folder_location)
