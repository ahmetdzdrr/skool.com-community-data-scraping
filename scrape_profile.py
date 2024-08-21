from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import time

class Scraper:
    """
    A class to scrape creator profile URLs from a given base URL using DrissionPage.
    
    Attributes:
        base_url (str): The base URL to prepend to profile links.
        user_profile (str): The user profile to be used for the ChromiumPage.
        waited_time (float): The time to wait between requests.
        parsed_info (list): A list to store parsed information (initially empty).
        page (ChromiumPage): An instance of the ChromiumPage class.
    """
    
    def __init__(self, base_url, user_profile, waited_time=1.5):
        """
        Initializes the Scraper with base URL, user profile, and wait time.
        
        Args:
            base_url (str): The base URL to prepend to profile links.
            user_profile (str): The user profile to be used for the ChromiumPage.
            waited_time (float): The time to wait between requests (default is 1.5 seconds).
        """
        self.base_url = base_url
        self.user_profile = user_profile
        self.waited_time = waited_time
        self.parsed_info = []
        self.page = self.select_user_return_page(user_profile)

    def select_user_return_page(self, user):
        """
        Sets up the Chromium page with the specified user profile.
        
        Args:
            user (str): The user profile to be used for the ChromiumPage.
        
        Returns:
            ChromiumPage: An instance of the ChromiumPage class.
        """
        print(f"Setting up the Chromium page with user profile: {user}")
        options = ChromiumOptions()
        # Uncomment the following lines if needed for debugging or headless mode:
        # options.set_argument('--remote-debugging-port=9222')
        # options.set_argument('--no-sandbox')
        # options.set_argument('--headless=new') 
        options.set_user(user=user)
        page = ChromiumPage(addr_or_opts=options)
        page.set.cookies.clear()
        print("ChromiumPage initialized and cookies cleared.\n")
        return page

    def fetch_creator_profile_url(self, index, full_url):
        """
        Fetches the creator's profile URL from the provided full URL.
        
        Args:
            index (int): The index of the current URL being processed (for logging).
            full_url (str): The full URL of the creator's page.
        
        Returns:
            str: The complete URL to the creator's profile, or None if not found.
        """
        about_url = f"{full_url}/about"
        print(f"{index}. Fetching URL: {about_url}")

        try:
            self.page.get(about_url)
            time.sleep(self.waited_time)

            div = self.page.ele('.styled__GroupInfo-sc-ahd4cu-3 gdabfl') or self.page.ele('.styled__GroupInfo-sc-ahd4cu-3 hJcEW')
            div_parent = div.eles('.styled__InfoItem-sc-ahd4cu-5 bSfAkV')[-1]
            a_tag = div_parent.ele('.styled__ChildrenLink-sc-i4j3i6-1 kbNjnr')
            if a_tag:
                href = a_tag.attrs.get('href')
                print(f"Profile HREF: {href}")
                creator_profile_url = f"{self.base_url}{href}"
                return creator_profile_url
            else:
                print("Href attribute not found.")
                return None

        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def process_dataframe(self, df):
        """
        Processes the DataFrame to fetch creator profile URLs and saves the updated DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame containing the data with 'Full URL' column.
        """
        creator_profile_urls = []

        for index, row in df.iterrows():
            index += 1
            full_url = row['Full URL']
            creator_profile_url = self.fetch_creator_profile_url(index, full_url)
            print(f"Scraped Profile URL: {creator_profile_url}\n")
            if creator_profile_url:
                creator_profile_urls.append(creator_profile_url)
            else:
                creator_profile_urls.append(None)
            time.sleep(self.waited_time)
        
        df['Creator Profile URL'] = creator_profile_urls
        df.to_csv('data_with_creator_profiles.csv', index=False, encoding='utf-8-sig')
        print(f"Creator profile URLs have been saved to 'data_with_creator_profiles.csv'.")

    def close(self):
        """
        Closes the ChromiumPage instance to free up resources.
        """
        self.page.quit()

if __name__ == "__main__":
    base_url = 'https://www.skool.com'
    user_profile = 'Profile 1'
    scraper = Scraper(base_url=base_url, user_profile=user_profile)
    df = pd.read_csv("main_content_data.csv")
    scraper.process_dataframe(df)
    scraper.close()
