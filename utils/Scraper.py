from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import random
import validators
from time import sleep
import requests
from utils.DataHandler import DataHandler
from utils.Pprints import Pprints
from utils.Website_Scraper import SocialMediaScraper


class Scraper:
    # CSS-SELECTOR
    search_results_links_css_selector = 'div[class="Nv2PK tH5CWc THOPZb "] a[class="hfpxzc"]'   # Selector for links of search results (Google Maps business listings)
    page_end_css_selector = "div[class='lXJj5c Hk4XGb ']"   # Selector for the element indicating the end of a page (used for pagination or scrolling detection)
    entity_name_css_selector = 'h1[class="DUwDvf lfPIob"]'  # Selector for the entity name (e.g., business or location name on the details page)
    entity_rating_css_selector = 'div[class="F7nice "] span'    # Selector for the entity's rating (average customer rating)
    entity_address_css_selector = 'div[class="rogA2c "] div'    # Selector for the entity's address (full address displayed on the details page)
    entity_website_css_selector = 'a[class="CsEnBe"][data-tooltip="Open website"]'  # Selector for the entity's website link (if available)
    entity_phone_number_css_selector = 'button[data-tooltip="Copy phone number"]'   # Selector for the entity's phone number (presented as a button with a tooltip)
    entity_reviews_btn_css_selector = 'button[class="hh2c6 "][aria-label^="Reviews"]'   # Selector for the button to access reviews of the entity
    write_reviewbtn_css_selector = 'button[class="g88MCb S9kvJb "]'  # This button is the very last element in the reviews tab we will scroll to this inorder to get reviews visible
    # REVIEWS TAB
    entities_all_reviews_css_selector = 'div[class="jftiEf fontBodyMedium "]'   # Selector for all visible reviews on the reviews tab
    review_name_css_selector = 'div[class="d4r55 "]'    # Selector for the name of the reviewer
    single_reviewer_given_stars_css_selector = 'span[class="kvMYJc"]'   # Selector for the star rating given by a single reviewer
    reviewers_comment_css_selector = 'div[class="MyEned"]'  # Selector for the reviewer's written comments (if provided)


    # CLASS INITIALIZATION
    def __init__(self,
                 headless_mode: str = '--headless',    # Default mode for the browser (headless by default)
                 reviews_scrape: bool = False,          # Whether to scrape reviews for each entity
                 output_format: str = 'csv',           # Default output format for saving data (e.g., CSV or JSON)
                 website_scrape: bool = False         # Whether to scrape additional website details for each entity
                 ):

        self.DataHandler = DataHandler(save_mode=output_format)     # DataHandler class manages all file operations for saving scraped data
        self.Social_Media_Scraper = SocialMediaScraper()     # SocialMediaScraper might handle scraping of social media links (if applicable)
        self.Pprints = Pprints()    # Pprints handles formatted printing/logging for better debugging and console output
        self.website_scrape = website_scrape    # Attribute to control whether website scraping is enabled
        self.headless_mode = headless_mode   # Mode for browser operation, e.g., --headless or --window
        self.reviews_scrape = reviews_scrape   # Flag to determine whether to enable review scraping functionality
        self.output_format = output_format    # The format in which scraped data will be saved (CSV, JSON, etc.)
        self.default_wait = 15    # Default implicit wait time for web elements to load properly (in seconds)



    def initialize_driver(self, url):
        """
        Initializes the WebDriver, navigates to the given URL, and sets up a global WebDriverWait instance.

        Args:
            url (str): The Google Maps URL to visit.

        Returns:
            driver (WebDriver): The initialized Selenium WebDriver instance.
        """
        # Log the setup process for debugging and user feedback
        self.pretty_prints_override(status=f"Setting up the driver for initial search")

        # Configure Chrome browser options
        chrome_options = Options()      # Initialize ChromeOptions for customizing browser behavior
        chrome_options.add_argument(self.headless_mode)  # Add headless mode argument (default or specified)
        chrome_options.add_argument("--force-device-scale-factor=0.8")  # Adjust zoom level to 80% for better visuals
        chrome_options.add_argument("--window-size=1920,1080")  # Set the default window size to Full HD resolution

        # Create a service object for the ChromeDriver executable
        svc = Service(executable_path=binary_path)

        # Initialize the Chrome WebDriver with the specified options and service configuration
        driver = webdriver.Chrome(service=svc, options=chrome_options)

        # Navigate the WebDriver to the target URL
        driver.get(url)    # Open the Google Maps URL provided as an argument

        # Set up an implicit wait for elements to load, improving script stability
        WebDriverWait(driver, self.default_wait)

        print(f"Driver initialized and navigated to {url}")
        return driver


    def pretty_prints_override(self, status: str, log: bool = False) -> None:
        """
        A wrapper for the pretty_prints method to handle status updates.

        Args:
            status (str): The status message to display.
            log (bool): Whether to log the status message. Defaults to False.
        """
        self.Pprints.pretty_prints(status=status, log=log)


    def input_handler(self) -> str:
        """
        Handles user input and sets up parameters for the search.

        Returns:
            str: The search query entered by the user.
        """
        # Prompt the user for a search query
        search_string = input("Enter the search query (e.g. Software houses in Karachi) : " )

        # Update the Pprints object with search-related parameters
        self.Pprints.set_search_string(
                                       search_string=search_string,
                                       headless_mode=self.headless_mode,
                                       reviews_scrape=self.reviews_scrape,
                                       output_format=self.output_format,
                                       website_scrape=self.website_scrape
                                      )

        return search_string

    def perform_search(self, driver: WebDriver, search_string: str):
        """
        Locates the search bar on Google Maps and performs a search using the provided search string.

        Args:
            driver (WebDriver): The initialized Selenium WebDriver instance.
            search_string (str): The search term to input in the search bar.
        """
        self.pretty_prints_override(status=f"Searching for the search string {search_string}")

        try:
            # Wait for the search bar to be visible
            WebDriverWait(driver, self.default_wait).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id="searchbox"] input')))

            # Locate and interact with the search bar
            search_bar = driver.find_element(By.CSS_SELECTOR, 'div[id="searchbox"] input')
            search_bar.clear()
            sleep(2)  # Simulate a natural pause before typing

            # Type the search string with a randomized delay between each character
            for ch in search_string:
                search_bar.send_keys(ch)
                sleep(random.uniform(0.3, 0.8))    # Mimic human typing speed

            # Press Enter to perform the search
            search_bar.send_keys(Keys.RETURN)

        except Exception as e:
            # Handle any errors during the search process
            print(f"An error occurred while performing the search: {e}")
            driver.quit()
            raise



    @staticmethod
    # Function to fetch multiple web elements
    def find_elements(driver: WebDriver, element_selector: str) -> list[WebElement]:
        """
        Finds all elements matching the given CSS selector on the current page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            element_selector (str): The CSS selector string to locate the elements.

        Returns:
            list: A list of WebElement objects matching the CSS selector.
        """
        elements = driver.find_elements(By.CSS_SELECTOR, element_selector)
        return elements



    @staticmethod
    # Function to scroll to a specific element
    def scroll_to_element(driver: WebDriver, element_selector: str):
        try:
            # Locate elements based on the provided CSS selector
            elements = driver.find_elements(By.CSS_SELECTOR, element_selector)

            # Ensure there is at least one element found, and select the last one if multiple are found
            if len(elements) == 1:
                element = elements[0]
            else:
                element = elements[-1]

            # Define the scroll origin based on the located element
            scroll_origin = ScrollOrigin.from_element(element)

            # Perform the scroll action from the element's position
            ActionChains(driver) \
                .scroll_from_origin(scroll_origin, 0, 500) \
                .perform()

        except IndexError:
            # Handle case where no elements are found
            pass


    # Function to scroll to the very bottom of the page do get all the dynamically loaded content
    def scroll_to_bottom(self, driver: WebDriver, last_element: str, target_element_css: str) -> None:
        """
        Scrolls recursively to the bottom of the page, loading more entities
        until all results are visible.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            last_element (str): The CSS selector for the last element to ensure the page is fully loaded.
            target_element_css (str): The CSS selector for the target elements in the search results.
        """
        self.pretty_prints_override(status=f"Scrolling recursively to reach the end!")

        # Wait until the target element is visible on the page
        WebDriverWait(driver, self.default_wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, target_element_css)))

        # Get the list of entities from the search results
        entities_tag = self.find_elements(driver, target_element_css)

        # Store the initial count of entities found
        old_entities_length = 0
        new_entities_length = len(entities_tag)

        # Loop to load more entities until the list stops growing
        while old_entities_length < new_entities_length:
            old_entities_length = new_entities_length
            try:
                # Wait for the last element to become visible before scrolling
                WebDriverWait(driver, self.default_wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, last_element)))
            except TimeoutException:
                pass

            # Scroll to the target element to trigger loading of more entities
            self.scroll_to_element(driver, target_element_css)

            # Sleep briefly to allow content to load
            sleep(2)

            # Scroll the page to the first entity in the list
            driver.execute_script("arguments[0].scrollIntoView();", entities_tag[0])

            # Sleep longer to ensure elements are loaded before checking the length
            sleep(8)

            # Update the list of entities and check if more have loaded
            entities_tag = self.find_elements(driver, target_element_css)
            new_entities_length = len(entities_tag)


    @staticmethod
    # Helper function to extract text from an element
    def extract_text(driver: WebDriver, css_selector: str, default=None):
        """
        Extracts the text content from the element located by the given CSS selector.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            css_selector (str): The CSS selector to locate the element.
            default: The value to return if the element is not found (default is None).

        Returns:
            str: The text content of the element, or the default value if the element is not found.
        """
        try:
            # Attempt to find the element and return its text content
            return driver.find_element(By.CSS_SELECTOR, css_selector).text
        except NoSuchElementException:
            # Return the default value if the element is not found
            return default


    @staticmethod
    # Helper function to extract an attribute from an element
    def extract_attribute(driver: WebDriver, css_selector: str, attribute: str, default=None) -> str:
        """
        Extracts the value of a specified attribute from the element located by the given CSS selector.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            css_selector (str): The CSS selector to locate the element.
            attribute (str): The name of the attribute to extract.
            default: The value to return if the element or attribute is not found (default is None).

        Returns:
            str: The value of the attribute, or the default value if the element or attribute is not found.
        """

        try:
            # Attempt to find the element and return the specified attribute value
            return driver.find_element(By.CSS_SELECTOR, css_selector).get_attribute(attribute)
        except NoSuchElementException:
            # Return the default value if the element or attribute is not found
            return default


    # Helper function to scrape reviews
    def scrape_reviews(self, driver) -> list:
        self.pretty_prints_override(status=f"Scraping reviews!")
        reviews = []

        # Wait for reviews section and scroll to load all reviews
        entity_reviews_btn = driver.find_element(By.CSS_SELECTOR, self.entity_reviews_btn_css_selector)
        entity_reviews_btn.click()  # Click the reviews button to open review tab of the entity

        try:
            # Wait for the reviews section to be visible
            WebDriverWait(driver, self.default_wait).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.entities_all_reviews_css_selector)))
        except TimeoutException:
            # Return an empty list if reviews section is not found or takes too long to load
            return []

        # Scroll to the bottom to load all reviews
        self.scroll_to_bottom(driver, self.entities_all_reviews_css_selector, self.entities_all_reviews_css_selector)

        # Extract reviews from the page
        all_reviews = driver.find_elements(By.CSS_SELECTOR, self.entities_all_reviews_css_selector)
        for review in all_reviews:
            # Extract each reviewer's details and review text
            reviewer_name = self.extract_text(review, self.review_name_css_selector)  # Replace '.' with reviewer name CSS selector
            stars_by_reviewer = self.extract_attribute(review, self.single_reviewer_given_stars_css_selector, 'aria-label')
            review_text = self.extract_text(review, self.reviewers_comment_css_selector)

            # Append the extracted data to the reviews list
            reviews.append({
                "reviewer_name": reviewer_name,
                "rating": stars_by_reviewer,
                "review_text": review_text
            })
        return reviews


    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validates if the provided URL is in a correct format.

        Args:
            url (str): The URL string to validate.

        Returns:
            bool: True if the URL is valid, otherwise False.
        """
        return validators.url(url)


    @staticmethod
    def is_accessible_url(url: str) -> bool:
        """
        Checks if the provided URL is accessible by making a lightweight HTTP HEAD request.

        Args:
            url (str): The URL string to check for accessibility.

        Returns:
            bool: True if the URL is accessible (status code 200), otherwise False.
        """
        try:
            # Send a HEAD request to check the URL's accessibility
            response = requests.head(url, timeout=5)  # Use HEAD for a lightweight check
            return response.status_code == 200  # Return True if status code is 200 (OK)
        except requests.RequestException:
            # Return False if there is any error during the request (timeout, invalid URL, etc.)
            return False


    # Function to recursively scrap data from given
    def scrape_data_recursively(self, driver: WebDriver, reviews_flag: bool = False, website_scrape: bool = False) -> dict:
        """
       Scrapes data from a given entity's page, including name, rating, address, phone number, website, and reviews.

       Args:
           driver (WebDriver): The initialized Selenium WebDriver instance.
           reviews_flag (bool): Flag to indicate if reviews should be scraped.
           website_scrape (bool): Flag to indicate if social media links should be scraped from the website.

       Returns:
           dict: A dictionary containing the scraped entity data including name, rating, address, website, phone number, and reviews.
        """
        self.pretty_prints_override(status=f"Scraping Data!")

        # Wait for the entity name to be visible before scraping data
        WebDriverWait(driver, self.default_wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.entity_name_css_selector)))

        # Extract entity details
        entity_name = self.extract_text(driver, self.entity_name_css_selector)
        try:
            entity_rating = float(self.extract_text(driver, self.entity_rating_css_selector))
        except TypeError:
            entity_rating = None    # Handle case where rating is not found

        # Entity's address mentioned on Google map profile
        entity_address = self.extract_text(driver, self.entity_address_css_selector)

        # Extract website and phone number with validation
        entity_website_raw = self.extract_attribute(driver, self.entity_website_css_selector, attribute='href')
        entity_website = entity_website_raw if (isinstance(entity_website_raw, str) and
                                                ('www' in entity_website_raw or 'http' in entity_website_raw or 'https' in entity_website_raw or 'com' in entity_website_raw)) else None
        entity_phone_number_raw = str(self.extract_attribute(driver, self.entity_phone_number_css_selector, attribute='aria-label'))
        entity_phone_number = entity_phone_number_raw.strip('Phone:') if entity_phone_number_raw.startswith('Phone:') else None

        # Scrape reviews if the flag is set to True
        if reviews_flag:
            reviews = self.scrape_reviews(driver)
        else:
            reviews = None

        # Scrape social media links if website_scrape is True
        social_media_links = None
        if website_scrape and entity_website is not None:
            self.pretty_prints_override(status=f"Scraping social media links from website : {entity_website}")
            if self.is_valid_url(entity_website) and self.is_accessible_url(entity_website):
                website_driver = self.initialize_driver(entity_website)
                social_media_links = self.Social_Media_Scraper.scrape_site(website_driver)
                website_driver.close()

        # Return the scraped data as a dictionary
        return {
                'Entity Name': entity_name,
                'Entity Rating': entity_rating,
                'Entity Address': entity_address,
                'Entity Website': entity_website,
                'Entity Phone_number': entity_phone_number,
                'Entity Website Details' : social_media_links,
                'Reviews': reviews
                }


    # Function to scrap links from search results
    def get_links_from_elements(self, driver: WebDriver, a_tag_element_selector: str) -> list:
        """
            Extracts and returns all the links from the search result page.

            Args:
                driver (WebDriver): The initialized Selenium WebDriver instance.
                a_tag_element_selector (str): The CSS selector for the anchor (`<a>`) tags containing the links.

            Returns:
                list: A list of URLs found in the search results.
            """
        self.pretty_prints_override(status=f"Fetching links of all entity ")
        links = []
        elements = driver.find_elements(By.CSS_SELECTOR, a_tag_element_selector)

        # Collect all the href attributes (links) from the elements
        for i in elements:
            href = i.get_attribute('href')
            links.append(href)
        print(f"Total Links:{len(links)}")
        return links

    # Function to scrape data from multiple links
    def scrape_data_from_links(self, links, output_format, output_file_path, reviews=False, website_scrape=False):
        """
       Scrapes data from multiple entity pages using the provided links.

       Args:
           links (list): List of entity page URLs to scrape.
           output_format (str): The desired output format for saving the data (e.g., JSON, CSV).
           output_file_path (str): The path where the scraped data should be saved.
           reviews (bool): Flag to indicate if reviews should be scraped.
           website_scrape (bool): Flag to indicate if social media links should be scraped from the website.

       Returns:
           None
       """
        data_list = []  # List to store the scraped data
        data_save_count = 0  # Counter to track when to save data

        # Iterate through each link and scrape data
        for link in links:
            driver = self.initialize_driver(link)   # Initialize the WebDriver for the link
            data = self.scrape_data_recursively(driver, reviews_flag=reviews, website_scrape=website_scrape)
            data_list.append(data)  # Add the scraped data to the list
            sleep(2)  # Remove for faster scraping
            driver.close()  # Close the driver after scraping

            data_save_count += 1
            if data_save_count % 3 == 0:  # Save every 3 items
                self.pretty_prints_override(status=f"Saving data to {output_file_path}")
                if data_list:  # Save only if there's data
                    self.DataHandler.save_method(save_mode=output_format,
                                                 data=data_list,
                                                 output_file_path=output_file_path)
                    data_list.clear()    #Clear the list after saving

        # Save any remaining data after the loop
        if data_list:
            self.DataHandler.save_method(save_mode=output_format, data=data_list, output_file_path=output_file_path)

