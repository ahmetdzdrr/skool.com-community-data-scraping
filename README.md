# skool.com-community-data-scraping

This repository contains scripts and tools for scraping community data from Skool.com, focusing on profile information and other relevant details. The collected data is processed and stored for further analysis.

## Features

- **Scraping Profiles**: Extracts community profiles including names, roles, and other key details.
- **Data Preprocessing**: Cleans and structures the scraped data for easy analysis.
- **Profile Details Extraction**: Captures detailed information from individual profiles.

## Setup

### Prerequisites

- Python 3.x
- Required libraries (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahmetdzdrr/skool.com-community-data-scraping.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Scrape Profiles**:
   Run `scrape.py` to start scraping profile data from Skool.com.
   ```bash
   python scrape.py
   ```
   
2. **Extract Profile Details**:
   Use `scrape_profile_details.py` to gather detailed information from specific profiles.
   ```bash
   python scrape_profile_details.py
   ```

3. **Data Preprocessing**:
   Clean and structure the raw data using `preprocessing.py`.
   ```bash
   python preprocessing.py
   ```

## File Structure

- `scrape.py`: Main script for scraping profiles.
- `scrape_profile.py`: Script for extracting additional profile information.
- `scrape_profile_details.py`: Extracts detailed profile data.
- `preprocessing.py`: Cleans and preprocesses scraped data.
- `requirements.txt`: Lists all dependencies.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, feel free to reach out.
- [LinkedIn](https://www.linkedin.com/in/ahmet-dizdar)