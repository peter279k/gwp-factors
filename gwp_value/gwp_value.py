import os
import sys
import codecs
import requests


def remove_utf8_bom(path):
    buffer_size = 4096
    bom_length = len(codecs.BOM_UTF8)
 
    with open(path, "r+b") as fp:
        chunk = fp.read(buffer_size)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[bom_length:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(bom_length, os.SEEK_CUR)
                chunk = fp.read(buffer_size)
            fp.seek(-bom_length, os.SEEK_CUR)
            fp.truncate()


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


remove_utf8_bom(csv_path)
print('The globalwarmingpotentials.csv file has been saved in datasets folder.')
