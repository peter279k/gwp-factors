import os
import re
import sys
import glob
from pyexcel_ods3 import get_data


def parse_ods_file(ods_file_path):
    dataset_path = './datasets/'
    regex = re.compile('\d+.\d+.\d+')
    matched = regex.findall(ods_file_path)
    if len(matched) != 1:
        return False
    version = matched[0]
    if os.path.isdir(dataset_path + version) is False:
        os.mkdir(dataset_path + version)
    csv_dir = dataset_path + version

    ods_data = get_data(ods_file_path)
    ods_sheet_keys = list(ods_data.keys())
    parse_co2_burn(ods_data, ods_sheet_keys[1], csv_dir)
    parse_ch4_n2o_burn(ods_data, ods_sheet_keys[2], csv_dir)
    parse_ch4_n2o_burn(ods_data, ods_sheet_keys[3], csv_dir)
    parse_cfcs_gwp(ods_data, ods_sheet_keys[4], csv_dir)


def parse_co2_burn(ods_data, ods_burn_sheet_key, csv_dir):
    csv_head = '排放形式,排放源類別,燃料別,建議排放係數數值,建議排放係數單位\n'
    csv_file_path = csv_dir + '/' + ods_burn_sheet_key + '.csv'
    index = 6
    emit_type = ''
    emit_category = ''
    csv_rows = csv_head
    while len(ods_data[ods_burn_sheet_key][index]) > 1:
        row = ods_data[ods_burn_sheet_key][index]
        if row[1] != '':
            emit_type = row[1]
        if row[2] != '':
            emit_category = row[2]
        csv_rows += '%s,%s,%s,%s,%s\n' % (
            emit_type,
            emit_category,
            row[3],
            row[17],
             row[18]
        )
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True


def parse_ch4_n2o_burn(ods_data, ods_burn_sheet_key, csv_dir):
    csv_head = '排放形式,排放源類別,燃料別,建議排放係數數值,建議排放係數單位\n'
    csv_file_path = csv_dir + '/' + ods_burn_sheet_key + '.csv'
    index = 6
    emit_type = ''
    emit_category = ''
    csv_rows = csv_head
    while len(ods_data[ods_burn_sheet_key][index]) > 1:
        row = ods_data[ods_burn_sheet_key][index]
        if row[1] != '':
            emit_type = row[1]
        if row[2] != '':
            emit_category = row[2]
        csv_rows += '%s,%s,%s,%s,%s\n' % (
            emit_type,
            emit_category,
            row[3],
            row[14],
             row[15]
        )
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True


def parse_cfcs_gwp(ods_data, ods_burn_sheet_key, csv_dir):
    ods_heads = ods_data[ods_burn_sheet_key][1]
    comment_index = ods_heads.index('備註')
    csv_head = ','.join(ods_heads[1:comment_index]) + '\n'
    csv_file_path = csv_dir + '/' + ods_burn_sheet_key + '.csv'
    index = 2
    csv_rows = csv_head
    while index < len(ods_data[ods_burn_sheet_key]):
        row = ods_data[ods_burn_sheet_key][index]
        if len(row) <= 2:
            index += 1
            continue

        csv_rows += ','.join(list(map(str, row[1:comment_index+1]))) + '\n'
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True



ods_files = glob.glob('./datasets/*.ods')
keyword = '溫室氣體排放係數管理表'
for ods_file in ods_files:
    if keyword in ods_file:
        print('Parsing ' + ods_file + ' is started.')
        parse_ods_file(ods_file)
        print('Parsing ' + ods_file + ' is done.')