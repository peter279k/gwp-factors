import os
import sys
import glob


matched_csv_files = glob.glob('./datasets/*/4_*.csv')
for matched_csv_file in matched_csv_files:
    file_handler = open(matched_csv_file, 'r')
    contents = file_handler.readlines()
    content_index = 0
    for content in contents:
        arr = content[0:-1].split(',')
        index = 0
        for value in arr:
            if value == '':
                arr[index] = '0'
            index += 1
        contents[content_index] = ','.join(arr) + '\n'
        content_index += 1
    file_handler.close()

    file_handler = open(matched_csv_file, 'w')
    file_handler.write(''.join(contents))
    file_handler.close()

    print('Empty columns are in the %s file is filled as the zero.' % matched_csv_file)
