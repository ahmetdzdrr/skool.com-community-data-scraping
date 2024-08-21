from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import time

class Scraper:
    """
    A class to scrape detailed profile information from a list of creator profile URLs using DrissionPage.
    
    Attributes:
        user_profile (str): The user profile to be used for the ChromiumPage.
        waited_time (float): The time to wait between requests (default is 1.5 seconds).
        page (ChromiumPage): An instance of the ChromiumPage class.
    """
    
    def __init__(self, user_profile, waited_time=1.5):
        """
        Initializes the Scraper with user profile and wait time.
        
        Args:
            user_profile (str): The user profile to be used for the ChromiumPage.
            waited_time (float): The time to wait between requests (default is 1.5 seconds).
        """
        self.user_profile = user_profile
        self.waited_time = waited_time
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

    def fetch_profile_details(self, index, profile_url):
        """
        Fetches detailed profile information from the provided profile URL.
        
        Args:
            index (int): The index of the current URL being processed (for logging).
            profile_url (str): The URL of the creator's profile page.
        
        Returns:
            tuple: A tuple containing followers count, contributions count, and social media URLs (Instagram, Twitter, YouTube, Facebook, LinkedIn, Website).
        """
        try:
            print(f"{index}. Fetching details for: {profile_url}")
            self.page.get(profile_url)
            # Uncomment the following line if the delay is needed:
            # time.sleep(self.waited_time)

            # Fetching followers and contributions count
            followers_div = self.page.eles('.styled__TypographyWrapper-sc-m28jfn-0 eoHmvk')
            social_media_div = self.page.ele('.styled__UserSocialLinksWrapper-sc-vbxyw2-0 kILtEf')
            
            if followers_div:
                contributions_count = followers_div[0].text
                followers_count = followers_div[1].text
                print(f"Contributions Count: {contributions_count}")
                print(f"Followers Count: {followers_count}")
            else:
                print("Followers div not found.")
                followers_count, contributions_count = None, None

            # Initialize social media URLs
            instagram_url = twitter_url = youtube_url = facebook_url = linkedin_url = website_url = None
            
            if social_media_div:
                a_tags = social_media_div.eles('.styled__ChildrenLink-sc-i4j3i6-1 kbNjnr')
                for a_tag in a_tags:
                    href = a_tag.attrs.get('href', '')
                    if 'instagram.com' in href:
                        instagram_url = href
                    elif 'twitter.com' in href or 'x.com' in href:
                        twitter_url = href
                    elif 'youtube.com' in href:
                        youtube_url = href
                    elif 'facebook.com' in href:
                        facebook_url = href
                    elif 'linkedin.com' in href:
                        linkedin_url = href
                    else:
                        website_url = href
                
                print(f"Instagram: {instagram_url}\nTwitter: {twitter_url}\nYouTube: {youtube_url}\nFacebook: {facebook_url}\nLinkedIn: {linkedin_url}\nWebsite: {website_url}\n")

            return followers_count, contributions_count, instagram_url, twitter_url, youtube_url, facebook_url, linkedin_url, website_url

        except Exception as e:
            print(f"Request failed: {e}")
            return None, None, None, None, None, None, None, None

    def process_dataframe(self, df):
        """
        Processes the DataFrame to fetch detailed profile information and saves the updated DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame containing the data with 'Creator Profile URL' column.
        """
        # Initialize lists to store fetched details
        followers_counts = []
        contributions_counts = []
        instagram_urls = []
        twitter_urls = []
        youtube_urls = []
        facebook_urls = []
        linkedin_urls = []
        website_urls = []

        for index, row in df.iterrows():
            index += 1
            profile_url = row['Creator Profile URL']
            followers_count, contributions_count, instagram_url, twitter_url, youtube_url, facebook_url, linkedin_url, website_url = self.fetch_profile_details(index, profile_url)
            followers_counts.append(followers_count)
            contributions_counts.append(contributions_count)
            instagram_urls.append(instagram_url)
            twitter_urls.append(twitter_url)
            youtube_urls.append(youtube_url)
            facebook_urls.append(facebook_url)
            linkedin_urls.append(linkedin_url)
            website_urls.append(website_url)
            time.sleep(self.waited_time)
        
        # Add the fetched details to the DataFrame
        df['Followers'] = followers_counts
        df['Contributions'] = contributions_counts
        df['Instagram'] = instagram_urls
        df['Twitter'] = twitter_urls
        df['YouTube'] = youtube_urls
        df['Facebook'] = facebook_urls
        df['LinkedIn'] = linkedin_urls
        df['Website'] = website_urls

        # Save the updated DataFrame to a CSV file
        df.to_csv('full_data.csv', index=False, encoding='utf-8-sig')
        print(f"Profile details have been saved to 'full_data.csv'.")

    def close(self):
        """
        Closes the ChromiumPage instance to free up resources.
        """
        self.page.quit()

if __name__ == "__main__":
    user_profile = 'Profile 1'
    scraper = Scraper(user_profile=user_profile)
    df = pd.read_csv("data_with_creator_profiles.csv")
    scraper.process_dataframe(df)
    scraper.close()
