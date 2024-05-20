# Google Maps Data Scraper

This project involves creating a sophisticated Google Maps scraper designed to extract detailed information from a list of addresses provided in an `input.txt` file. The scraper efficiently collects data such as names, contact details, and other relevant information. It operates recursively, gathering data from the given addresses and any related addresses found during the process. The collected data is then organized and stored in an `Gmap_data.xlsx` file, providing a comprehensive and easily accessible dataset for further analysis or use.

## Features
- Extracts names and contact details from Google Maps.
- Recursively gathers data from relevant addresses.
- Outputs data in an organized Excel file.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/google-maps-scraper.git
    cd google-maps-scraper
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare the input file:**
    - Create an `input.txt` file in the root directory of the project.
    - Add the addresses you want to scrape, each on a new line.

2. **Run the scraper:**
    ```bash
    python scraper.py
    ```

3. **Output:**
    - The scraped data will be saved in a file named `Gmap_data.xlsx` in the root directory.

## Example

### input.txt

### Running the scraper
```bash
python scraper.py
```

### Expected output
- A file named `Gmap_data.xlsx` containing the names and contact details for the provided addresses and related addresses found during the scraping process.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or enhancements.

## Contact
For any questions or inquiries, please contact [hammadhussain389@.com].
