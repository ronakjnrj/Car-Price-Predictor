import csv, requests
from bs4 import BeautifulSoup


def scrape(request):

    html_content = requests.get('https://www.cars24.com/buy-used-cars-jaipur/?listingSource=ViewAllCars&storeCityId=2130')

    soup = BeautifulSoup(html_content, 'html.parser')
    car_cards = soup.find_all('a', class_='styles_carCardWrapper__sXLIp')

    car_data_list = []

    for card in car_cards:
        try:
            name = card.find('span', class_='bAcffq').text.strip()
            variant = card.find('span', class_='bKVBht').text.strip()
            price = card.find('p', class_='hvRpEM').text.strip()
            year = name.split()[0]
            
            specs = [spec.text.strip() for spec in card.find_all('p', class_='kNDBvu')]
            location = card.find('div', class_='styles_hubAddress__URioy').text.strip()

            car_info = {
                "year": year,
                "car": name,
                "model": variant,
                "kilometers": specs[0] if len(specs) > 0 else None,
                "fuel": specs[1] if len(specs) > 1 else None,
                "transmission": specs[2] if len(specs) > 2 else None,
                "city_code": location,
                "price": price,
            }
            
            car_data_list.append(car_info)

        except AttributeError:
            continue
 
    # Save to CSV
    if car_data_list:
        with open('cars_data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=car_data_list[0].keys())
            writer.writeheader()
            writer.writerows(car_data_list)
        print(f"Data successfully saved to CSV File")

