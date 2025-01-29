from utils.Scraper import Scraper
import sys


class Main:
    # CSS selector for extracting links to search results
    search_results_links_css_selector = 'div[class="Nv2PK tH5CWc THOPZb "] a[class="hfpxzc"]'

    def __init__(self,
                 headless_mode: str = '--headless',
                 output_format: str = 'csv',
                 reviews_scrape: bool = False,
                 website_scrape: bool = False,
                 url: str = "https://www.google.com/maps/",
                 ) -> None:
        """
        Initializes the Main class with scraper configurations and Google Maps URL.

        :param headless_mode: Browser mode ('--headless' for invisible mode, '--window' for visible mode).
        :param output_format: Format for saving scraped data (e.g., 'csv' or 'json').
        :param reviews_scrape: Boolean flag to enable or disable scraping reviews.
        :param website_scrape: Boolean flag to enable or disable scraping website links.
        :param url: Google Maps URL to start the scraping session.
        """
        self.Scraper = Scraper(headless_mode=headless_mode,
                               reviews_scrape=reviews_scrape,
                               output_format=output_format,
                               website_scrape=website_scrape
                               )
        self.headless_mode = headless_mode
        self.output_format = output_format
        self.reviews_scrape = reviews_scrape
        self.website_scrape = website_scrape
        self.url = url

    def run(self) -> None:
        """
        Executes the scraping workflow for Google Maps data:
        1. Accepts user input for search queries.
        2. Initializes the web driver and navigates to the provided URL.
        3. Performs a search for the user-provided query.
        4. Scrolls through the search results to load more data.
        5. Extracts links from the search results.
        6. Scrapes data from the extracted links and saves it in the specified format.
        """
        try:
            # Step 1: Take user input for the search query.
            search_input = self.Scraper.input_handler()

            # Step 2: Initialize the web driver and navigate to the starting URL.
            driver = self.Scraper.initialize_driver(url=self.url)

            # Step 3: Perform the search for the user-provided query.
            self.Scraper.perform_search(driver, search_input)

            # Step 4: Scroll through the search results to ensure all data is loaded.
            self.Scraper.scroll_to_bottom(driver, self.search_results_links_css_selector,
                                                  self.search_results_links_css_selector)

            # Step 5: Extract links to individual search results.
            links = self.Scraper.get_links_from_elements(driver, self.search_results_links_css_selector)

            # Step 6: Scrape data from the extracted links and save it in the desired format.
            self.Scraper.scrape_data_from_links(links=links,
                                                output_format=self.output_format,
                                                output_file_path=f"{search_input}.{self.output_format}".replace(' ', '_'),
                                                reviews=self.reviews_scrape,
                                                website_scrape=self.website_scrape
                                                )

        except KeyboardInterrupt:
            print("\nProcess interrupted. Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    # Instantiate the Main class with custom configurations and start the scraper.
    app = Main(headless_mode='--headless', reviews_scrape=True, output_format='csv', website_scrape=True)
    app.run()
