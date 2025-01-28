import csv
import json
from pathlib import Path

class DataHandler:
    def __init__(self, save_mode:str ='csv'):
        """
        Initializes the DataHandler class with a specified save mode.

        Args:
            save_mode (str): The mode to save data in ('csv' or 'json'). Default is 'csv'.
        """
        self.save_mode = save_mode


    def save_method(self, save_mode: str, data: list, output_file_path: str) -> None:
        """
        Saves the given data using the specified save mode ('csv' or 'json').

        Args:
            save_mode (str): The mode to save data in ('csv' or 'json').
            data (list): The data to be saved (list of dictionaries).
            output_file_path (str): The path to the output file where data is saved.
        """
        if save_mode == 'csv':
            self.save_in_csv(data, output_file_path)
        elif save_mode == 'json':
            self.save_in_json(data, output_file_path)
        else:
            raise ValueError("Invalid data input")  # Use a standard exception or define a custom one


    @staticmethod
    def save_in_csv(data, output_file_path):
        """
        Saves data to a CSV file.

        Args:
            data (list): The data to be saved (list of dictionaries).
            output_file_path (str): The path to the output file where data is saved.
        """
        if not data:
            print("No data to save.")
            return

        field_names = data[0].keys()    # Extract the field names (keys of the first dictionary)
        file_exists = Path(output_file_path).is_file()  # Check if the file already exists

        with open(output_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)

            # Write header only if the file does not exist
            if not file_exists:
                writer.writeheader()

            writer.writerows(data)  # Write all rows in one go
        print(f"Data saved to {output_file_path}")


    @staticmethod
    def save_in_json(data, output_file_path):
        """
        Saves data to a JSON file.

        Args:
            data (list): The data to be saved (list of dictionaries).
            output_file_path (str): The path to the output file where data is saved.
        """
        if not data:
            print("No data to save.")
            return

        file_exists = Path(output_file_path).is_file()  # Check if the file already exists

        if file_exists:
            try:
                # Open the file in read-write mode
                with open(output_file_path, mode='r+', encoding='utf-8') as file:
                    try:
                        existing_data = json.load(file)     # Load existing data from the file
                    except json.JSONDecodeError:
                        print(f"File {output_file_path} is empty or corrupted. Starting fresh.")
                        existing_data = []
                    existing_data.extend(data)  # Add new data to the existing data
                    file.seek(0)    # Move the file pointer back to the beginning
                    json.dump(existing_data, file, indent=4)    # Write the updated data
            except Exception as e:
                print(f"Error updating JSON file: {e}")
        else:
            # If the file doesn't exist, create a new file and save the data
            with open(output_file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        print(f"Data saved to {output_file_path}")


