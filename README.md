# Google Maps Scraper

This repository contains a customizable Google Maps scraper designed to extract business information based on user-defined input criteria. The scraper is ideal for collecting structured data like software house details, restaurants, or other businesses in a specific location. 

## Features

- **Customizable Inputs:** Specify search queries (e.g., "software houses in New York") to scrape relevant business details.
- **Data Extraction:** Scrapes the following details from Google Maps:
  - Business name
  - Website URL
  - Phone number
  - Address
  - Reviews
  - Website Social Media links
- **Output Formats:** Choose between `CSV` or `JSON` for storing the scraped data.
- **Review Scraping:** Option to scrape business reviews by enabling `Review_Scrape` (default: `False`).
- **Website Scraping:** Optionally visit business websites and extract social media links by enabling `Website_Scrape` (default: `False`).
- **Modular Design:** Clean and modular code structure for easy updates and maintenance.

---

## File Structure

```
├── Main.py                 # Entry point of the application
├── utils/
│   ├── Scraper.py          # Core scraping logic for Google Maps
│   ├── Pprints.py          # Utility for terminal-friendly progress printing
│   ├── DataHandler.py      # Handles data storage and format selection
│   ├── Website_Scraper.py  # Handles scraping of social media links from websites
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/google-maps-scraper.git
   cd google-maps-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Open `Main.py` and configure the desired settings:
   - **Search Query:** Define the business and location to scrape.
   - **Output Format:** Set to either `CSV` or `JSON`.
   - **Review Scrape:** Enable (`True`) or disable (`False`) review scraping.
   - **Website Scrape:** Enable (`True`) or disable (`False`) website scraping.

2. Run the scraper:
   ```bash
   python Main.py
   ```

---

## Customization

### 1. Scraping Reviews
To include reviews, set the `Review_Scrape` flag to `True` in `Main.py`. Reviews will be included in the output.

### 2. Website Scraping
To scrape social media links from websites, set the `Website_Scrape` flag to `True` in `Main.py`.

### 3. Output Formats
Select the desired output format (`CSV` or `JSON`) in `Main.py` for storing the scraped data.

---

## Example Configuration in `Main.py`

```python
from utils.Scraper import Scraper
from utils.DataHandler import DataHandler
from utils.Website_Scraper import WebsiteScraper

# Configuration
search_query = "software houses in New York"
output_format = "CSV"  # Options: "CSV", "JSON"
review_scrape = True  # Enable or disable review scraping
website_scrape = False  # Enable or disable website scraping

# Run the scraper
scraper = Scraper()
data_handler = DataHandler()
website_scraper = WebsiteScraper()

scraper.run(search_query, review_scrape, website_scrape, output_format)
```

---

## Outputs

The scraper generates structured data files based on the chosen format:

![Output](https://github.com/user-attachments/assets/41478744-4368-4e0d-9ce3-943592be7978)


1. **CSV Output**:
   ```
   Name, Website, Phone, Address, Reviews (if enabled), Social Media Links (if enabled)
   ```
2. **JSON Output**:
   ```json
   [
       {
           "name": "Example Business",
           "website": "https://example.com",
           "phone": "+1-234-567-890",
           "address": "123 Example Street, New York, NY",
           "reviews": ["Review 1", "Review 2", ...],  # Optional
           "social_media_links": ["https://twitter.com/example", ...]  # Optional
       }
   ]
   ```

---

## Dependencies

- Python 3.8+
- Required Python packages (listed in `requirements.txt`):
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `json`
  - Any other dependencies used in the project

---

## Contribution

Contributions are welcome! Feel free to create a pull request or open an issue to report bugs or request features.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
