import os
import sys
import codecs
import requests


url = 'https://github.com/openclimatedata/globalwarmingpotentials/raw/main/globalwarmingpotentials.csv'
response = requests.get(url)

counter = 0
retry_counter = 3

while response.status_code != 200:
    if counter == retry_counter:
        print('The Retry counter is up to the limited.')
        sys.exit(1)
    response = requests.get(url)
    counter += 1

csv_contents = response.text
csv_contents = '\n'.join(csv_contents.split('\n')[9:])

csv_path = './datasets/globalwarmingpotentials.csv'
with open(csv_path, 'w') as file_handler:
    file_handler.write(csv_contents)


print('The globalwarmingpotentials.csv file has been saved in datasets folder.')
