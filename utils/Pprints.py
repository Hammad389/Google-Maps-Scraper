from platform import system as system_platform
from os import system
from os.path import isfile
from psutil import Process

class Pprints:

    # Define color codes for terminal printing
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    MAGENTA = '\033[35m'
    LIGHTGREY = '\033[37m'

    def __init__(self) -> None:
        """
        Initialize the Pprints class with default parameters and process information.
        """
        self.process = Process()     # Get process information for memory usage
        self.log_file = 'logs.txt'  # Default log file name
        self.search_string= None    # Placeholder for search query
        self.headless_mode = '--headless'    # Default mode for headless browser operation
        self.website_scrape = False     # Flag for scraping website data
        self.output_format = 'csv'       # Default output format
        self.reviews_scrape = False     # Flag for scraping reviews

    @staticmethod
    def clean_terminal() -> str:
        """
        Clears the terminal screen based on the platform (Windows or Unix-based).

        Returns:
            str: The platform name.
        """
        if system_platform() == 'Windows':
            system('cls')   # Clear terminal for Windows
        else:
            system('clear')      # Clear terminal for Unix-like OS
        return system_platform()    # Return the platform name

    # Function to set up the extra parameters for pretty_prints function
    def set_search_string(self, search_string: str, headless_mode: str, reviews_scrape: bool, output_format: str, website_scrape: bool) -> None:
        """
        Set various scraping parameters for the class instance.

        Args:
            search_string (str): The search query to scrape.
            headless_mode (bool): Flag to enable headless mode for scraping.
            reviews_scrape (bool): Flag to enable scraping of reviews.
            output_format (str): The desired output format (e.g., 'csv').
            website_scrape (bool): Flag to enable scraping of website data.
        """
        self.search_string = search_string
        self.headless_mode = headless_mode
        self.reviews_scrape = reviews_scrape
        self.output_format = output_format
        self.website_scrape = website_scrape


    def pretty_prints(self, status: str, log: bool = False) -> None:
        """
        Prints a formatted status message to the terminal, including platform info,
        parameters, and current memory usage. Optionally logs the message to a file.

        Args:
            status (str): The status message to print.
            log (bool): Flag to indicate if the status should be logged to a file.
        """
        memory_info = self.process.memory_info()    # Get memory usage of the current process
        current_memory_usage = memory_info.rss / 1024 / 1024    # Convert memory to MB

        # Non-log message to be printed to the terminal
        non_log_msg = f"Status: {status}\n"

        # Log message with detailed information about the environment and settings
        log_msg = f"{self.GREEN}Platform: {self.clean_terminal()}\n" \
                  f"{self.CYAN}Developer: HAMMAD\n" \
                  f"{self.GREEN}GMAP Scraper Version: 0.2\n" \
                  f"{self.WARNING}GitHub: github.com/Hammad389\n" \
                  f"{self.LIGHTGREY}GMAP SCRAPER PARAMETERS SETTING:\n" \
                  f"{self.LIGHTGREY}MODE: {self.headless_mode}\n"\
                  f"{self.LIGHTGREY}WEBSITE SCRAPE: {self.website_scrape}\n"\
                  f"{self.LIGHTGREY}REVIEWS SCRAPE: {self.reviews_scrape}\n"\
                  f"{self.LIGHTGREY}OUTPUT FORMAT: {self.output_format}\n"\
                  f"{self.MAGENTA}SEARCHED QUERY: {self.search_string}\n" \
                  f"{self.CYAN}Status: {status}\n" \
                  f"{self.WARNING}MemoryUsageByScript: {current_memory_usage: .2f}MB\n" \
                  f"{self.RED}Warning: Don't open the output file while script is running\n{self.RESET}"

        # Print the log message
        print(log_msg)

        # Log message to the log file if the log flag is set
        if log:
            if isfile(self.log_file):
                file_obj = open(self.log_file, 'a')
                file_obj.write(non_log_msg)
                file_obj.close()
            else:
                file_obj = open(self.log_file, 'w')
                file_obj.write(non_log_msg)
                file_obj.close()

