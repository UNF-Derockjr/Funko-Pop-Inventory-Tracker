import requests
import time
import xml.etree.ElementTree as ET

# Your eBay App ID for the production environment
APP_ID = 'DerrickK-FunkoPop-PRD-24d86fa63-b70f4016'  # Replace with your actual Production App ID

def get_sold_items(search_term, category_id, condition_id, entries_per_page, max_retries=5):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    params = {
        'OPERATION-NAME': 'findCompletedItems',
        'SERVICE-VERSION': '1.7.0',
        'SECURITY-APPNAME': APP_ID,
        'RESPONSE-DATA-FORMAT': 'XML',
        'REST-PAYLOAD': '',
        'keywords': search_term,
        'categoryId': category_id,
        'itemFilter(0).name': 'Condition',
        'itemFilter(0).value': condition_id,
        'itemFilter(1).name': 'FreeShippingOnly',
        'itemFilter(1).value': 'true',
        'itemFilter(2).name': 'SoldItemsOnly',
        'itemFilter(2).value': 'true',
        'sortOrder': 'PricePlusShippingLowest',
        'paginationInput.entriesPerPage': entries_per_page,
        'paginationInput.pageNumber': 1
    }

    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//{http://www.ebay.com/marketplace/search/v1/services}item'):
                title = item.find('{http://www.ebay.com/marketplace/search/v1/services}title').text
                current_price = item.find('.//{http://www.ebay.com/marketplace/search/v1/services}currentPrice').text
                print(f"Item: {title}, Sold Price: ${current_price}")
            return
        elif response.status_code == 500:
            error_tree = ET.fromstring(response.content)
            error_id = error_tree.find('.//{http://www.ebay.com/marketplace/search/v1/services}errorId')
            if error_id is not None and error_id.text == '10001':
                retry_after = response.headers.get('Retry-After')
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return

if __name__ == '__main__':
    search_term = 'batman'
    category_id = '88988'
    condition_id = '1000'
    entries_per_page = 2
    get_sold_items(search_term, category_id, condition_id, entries_per_page)