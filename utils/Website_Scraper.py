from bs4 import BeautifulSoup
from re import compile

class SocialMediaScraper:
    def __init__(self):
        """
       Initializes the SocialMediaScraper class with compiled regex patterns
       for detecting emails and social media links (Facebook, Twitter, Instagram,
       YouTube, LinkedIn) from a website.
       """
        # Regex patterns for detecting specific social media links and emails
        self._email_pattern = compile(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+')
        self._fb_pattern = compile(r'(?:https?://)?(?:www\.)?facebook\.com/\S+')
        self._twitter_pattern = compile(r'(?:https?://)?(?:www\.)?twitter\.com/\S+')
        self._insta_pattern = compile(r'(?:https?://)?(?:www\.)?instagram\.com/\S+')
        self._youtube_pattern = compile(r'(?:https?://)?(?:www\.)?youtube\.com/\S+')
        self._linkedin_pattern = compile(r'(?:https?://)?(?:www\.)?linkedin\.com/\S+')

    def scrape_site(self,driver):
        try:
            # Parse the page source using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract contact info and social media links
            site_email = list({match.group() for match in self._email_pattern.finditer(str(soup))})

            # Extract social media links from the page using the precompiled regex patterns
            facebook_links = [link['href'] for link in soup.find_all('a', href=self._fb_pattern)]
            twitter_links = [link['href'] for link in soup.find_all('a', href=self._twitter_pattern)]
            instagram_links = [link['href'] for link in soup.find_all('a', href=self._insta_pattern)]
            youtube_links = [link['href'] for link in soup.find_all('a', href=self._youtube_pattern)]
            linkedin_links = [link['href'] for link in soup.find_all('a', href=self._linkedin_pattern)]

            # Return the extracted information in a dictionary
            return{
                    "emails": site_email,
                    "facebook_links": facebook_links,
                    "twitter_links": twitter_links,
                    "instagram_links": instagram_links,
                    "youtube_links": youtube_links,
                    "linkedin_links": linkedin_links,
                 }
        except:
            # Return None in case of any exception during the scraping process
            return None
