import requests
from bs4 import BeautifulSoup
from extract_resume_info import extract_info_from_resume


def get_company_address(company_name, location):
    search_query = f"{company_name} {location}"
    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        address_div = soup.find('div', {'data-attrid': 'kc:/location/location:address'})
        if address_div:
            return address_div.get_text(separator=' ', strip=True)
    return "Address not found"
