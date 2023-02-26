import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL to canyon website and the bike I want to buy including color information
URL="https://www.canyon.com/de-de/rennrad/race-rennrad/ultimate/cf-sl/ultimate-cf-sl-8-aero/3319.html?dwvar_3319_pv_rahmenfarbe=R101_P01"
#URL="https://www.canyon.com/de-de/rennrad/endurance-rennrad/endurace/cf-sl/endurace-cf-sl-8-di2/3366.html?dwvar_3366_pv_rahmenfarbe=GY%2FBK"

# bike status
statusMessage = "bald verfügbar"

# Get the page content  and parse it with BeautifulSoup
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# Get the availability status of the bikes with sizes M and L
results = soup.find_all(attrs={"data-product-size": ["M","L"]})
#print(results)

# initalize a dictionary to store the results
bike_dict = {}

# loop over the results and get the size, availability status and availability message
for bike in results:
    
    # get the attributes of the bike
    bikeSize = bike.find("div", class_="productConfiguration__variantType js-productConfigurationVariantType").text.strip()
    bikeStatus = bike.find("div", class_="productConfiguration__availabilityMessage").text.strip()
    bikeAvail = bike.find("div", class_="productConfiguration__availabilitySubMessage")
    # check for none type for bikeAvail since it can be empty
    if bikeAvail is not None:
        bikeAvail = bikeAvail.text.strip()

    # create new dictionary with status and availability message
    bike = {'status': bikeStatus, 'availability': bikeAvail}
    bike_dict[bikeSize] = bike

# loop over the dictionary and check if the bike is available
for key, value in bike_dict.items():

    # check it the value contains the status message
    if statusMessage not in value['status'].lower():
        print("The bike is available in size " + key)

# add time stamp to the dictionary
bike_dict['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    

# print the dictionary
print(bike_dict)

