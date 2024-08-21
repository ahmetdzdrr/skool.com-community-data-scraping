import pandas as pd
import re
from time import sleep
import random
from DrissionPage import ChromiumPage, ChromiumOptions

class AgentScraper:
    """
    A scraper class for extracting community data from a website.

    Attributes:
        base_url (str): The base URL of the website to scrape.
        user_profile (str): The user profile for ChromiumPage.
        waited_time (int): Time to wait between page requests.
        parsed_info (list): List to store parsed information.
        page (ChromiumPage): ChromiumPage object for browser interaction.
    """

    def __init__(self, base_url, user_profile, waited_time=5):
        """
        Initializes the scraper with the base URL, user profile, and wait time.

        Args:
            base_url (str): The base URL of the website.
            user_profile (str): The user profile for ChromiumPage.
            waited_time (int): Time to wait between requests (default is 5).
        """
        self.base_url = base_url
        self.user_profile = user_profile
        self.waited_time = waited_time
        self.parsed_info = []
        self.page = self.select_user_return_page(user_profile)

    def select_user_return_page(self, user):
        """
        Sets up the ChromiumPage with the specified user profile.

        Args:
            user (str): The user profile name.

        Returns:
            ChromiumPage: The initialized ChromiumPage object.
        """
        print(f"Initializing ChromiumPage with user profile: {user}")
        options = ChromiumOptions()
        options.set_user(user=user)
        page = ChromiumPage(addr_or_opts=options)
        page.set.cookies.clear()
        print("ChromiumPage initialized and cookies cleared.")
        return page

    def get_last_page_number(self):
        """
        Fetches the last page number from the pagination of the website.

        Returns:
            int: The number of the last page.
        """
        print(f"Fetching last page number from {self.base_url}")
        self.page.get(self.base_url)
        sleep(random.random() * 3)  # Wait randomly to mimic human interaction
        print(f"Page loaded: {self.base_url}")

        pagination_div = self.page.ele('.styled__DesktopPaginationControls-sc-4zz1jl-1 iBxcTJ')
        if pagination_div:
            print("Pagination div found.")
            last_page_buttons = pagination_div.eles('.styled__ButtonWrapper-sc-dscagy-1 ikjxol')
            if last_page_buttons:
                last_page_button = last_page_buttons[-1]
                last_page = int(last_page_button.text.strip())
                print(f"Last page button found with page number: {last_page}")
            else:
                print("No last page button found. Defaulting to page 1.")
                last_page = 1
        else:
            print("Pagination div not found. Defaulting to page 1.")
            last_page = 1

        return last_page

    def extract_data_from_page(self, url):
        """
        Extracts data from a single page.

        Args:
            url (str): The URL of the page to scrape.

        Returns:
            list: A list of dictionaries containing the extracted data.
        """
        print(f"Extracting data from {url}")
        self.page.get(url)
        sleep(random.random() * 3)  # Wait randomly to mimic human interaction
        print(f"Page loaded: {url}")

        cards_div = self.page.ele('.styled__DiscoveryCards-sc-jt9hr-7 lnuLcQ')
        if cards_div:
            print("Cards div found.")
            links = cards_div.eles('.styled__ChildrenLink-sc-i4j3i6-1 kbNjnr styled__DiscoveryCardLink-sc-13ysp3k-0 eyLtsl')
            print(f"Found {len(links)} links.")

            data = []
            for link in links:
                href = link.attrs.get('href')
                if not href:
                    print("No href found for link. Skipping.")
                    continue

                full_url = f'https://www.skool.com{href}'
                print(f'Processing link: {full_url}')

                content_div = link.ele('.styled__DiscoveryCardContent-sc-13ysp3k-4 cggWfX')
                if content_div:
                    # Extract community name
                    community_name_div = content_div.ele('.styled__TypographyWrapper-sc-m28jfn-0 eoHmvk')
                    community_name = community_name_div.text.strip() if community_name_div else 'N/A'

                    # Extract status, members, and price
                    meta_div = content_div.ele('.styled__DiscoveryCardMeta-sc-13ysp3k-7 jjNZwk')
                    status, members, price = 'N/A', 'N/A', 'N/A'
                    if meta_div:
                        text_content = meta_div.text.strip()
                        print(f'Meta div text: {text_content}\n')
                        parts = re.split(r'•', text_content)
                        if len(parts) > 0:
                            status = parts[0].strip()
                        if len(parts) > 1:
                            members = parts[1].strip()
                            if '.' in members and 'k' in members:
                                members = float(parts[1].split('kMembers')[0]) * 1000
                            elif 'k' in members and '.' not in members:
                                members = int(parts[1].split('kMembers')[0]) * 1000
                            else:
                                members = int(parts[1].split('Members')[0])
                        if len(parts) > 2:
                            price = parts[2]
                            if '/month' in price:
                                price = price.split(' /month')[0]
                    
                    print(f'Full URL: {full_url}')
                    print(f'Community Name: {community_name}')
                    print(f'Status: {status}')
                    print(f'Members: {members}')
                    print(f'Price: {price}')
                    print("=" * 40)

                    data.append({
                        'Full URL': full_url,
                        'Community Name': community_name,
                        'Status': status,
                        'Members': members,
                        'Price': price
                    })

            return data
        else:
            print("Cards div not found.")
        return []

    def scrape_all_pages(self):
        """
        Scrapes data from all pages and saves the results to a CSV file.
        """
        print(f"Starting to scrape all pages from {self.base_url}")
        last_page = self.get_last_page_number()
        print(f"Total number of pages: {last_page}")
        all_data = []

        for page_num in range(1, last_page + 1):
            print(f"Scraping page {page_num}...")
            url = f'{self.base_url}?p={page_num}'
            page_data = self.extract_data_from_page(url)
            all_data.extend(page_data)

        df = pd.DataFrame(all_data)
        df.to_csv('main_content_data.csv', index=False, encoding='utf-8-sig')
        print(f"Data has been extracted and saved to 'main_content_data.csv'.")

    def close(self):
        """
        Closes the ChromiumPage and quits the browser.
        """
        print("Closing the page.")
        self.page.quit()

if __name__ == "__main__":
    base_url = 'https://www.skool.com/discovery'
    user_profile = 'Profile 5'
    scraper = AgentScraper(base_url=base_url, user_profile=user_profile)
    scraper.scrape_all_pages()
    scraper.close()
