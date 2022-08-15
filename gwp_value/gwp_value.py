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
csv_contents_arr = csv_contents.split('\n')[9:-1]

index = 0
for csv_content in csv_contents_arr:
    csv_content_index = 0
    csv_content_arr = csv_content.split(',')
    for value in csv_content_arr:
        if value == '':
            csv_content_arr[csv_content_index] = '0'
        csv_content_index += 1
    csv_contents_arr[index] = ','.join(csv_content_arr)
    index += 1

csv_contents = '\n'.join(csv_contents_arr) + '\n'


csv_path = './datasets/globalwarmingpotentials.csv'
with open(csv_path, 'w') as file_handler:
    file_handler.write(csv_contents)

print('The globalwarmingpotentials.csv file has been saved in datasets folder.')
