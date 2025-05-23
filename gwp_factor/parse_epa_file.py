import os
import re
import sys
import glob
from pyexcel_ods3 import get_data


def parse_ods_file(ods_file_path):
    dataset_path = './datasets/'
    regex = re.compile('\d+.\d+.\d+')
    matched = regex.findall(ods_file_path)
    special_keyword = '(修)'
    if len(matched) != 1:
        return False
    version = matched[0]
    if special_keyword in ods_file_path:
        version = version + special_keyword

    if os.path.isdir(dataset_path + version) is False:
        os.mkdir(dataset_path + version)
    csv_dir = dataset_path + version

    ods_data = get_data(ods_file_path)
    ods_sheet_keys = list(ods_data.keys())
    parsing_str = 'Parsing the '
    is_started_str = ' is started.'
    is_done_str = ' is done.'

    print(parsing_str + ods_sheet_keys[1] + is_started_str)
    parse_co2_burn(ods_data, ods_sheet_keys[1], csv_dir)
    print(parsing_str + ods_sheet_keys[1] + is_done_str)

    print(parsing_str + ods_sheet_keys[2] + is_started_str)
    parse_ch4_n2o_burn(ods_data, ods_sheet_keys[2], csv_dir)
    print(parsing_str + ods_sheet_keys[2] + is_done_str)

    print(parsing_str + ods_sheet_keys[3] + is_started_str)
    parse_ch4_n2o_burn(ods_data, ods_sheet_keys[3], csv_dir)
    print(parsing_str + ods_sheet_keys[3] + is_done_str)

    print(parsing_str + ods_sheet_keys[4] + is_started_str)
    parse_cfcs_gwp(ods_data, ods_sheet_keys[4], csv_dir)
    print(parsing_str + ods_sheet_keys[4] + is_done_str)

    print(parsing_str + ods_sheet_keys[6] + is_started_str)
    parse_fugitive_emission(ods_data, ods_sheet_keys[6], csv_dir)
    print(parsing_str + ods_sheet_keys[6] + is_done_str)

    print(parsing_str + ods_sheet_keys[9] + is_started_str)
    parse_fcfs_factor_emission(ods_data, ods_sheet_keys[9], csv_dir)
    print(parsing_str + ods_sheet_keys[9] + is_done_str)


def parse_co2_burn(ods_data, ods_burn_sheet_key, csv_dir):
    # 排放形式,排放源類別,燃料別,建議排放係數數值,建議排放係數單位
    csv_head = 'emission_form,emission_type,burn_type,recommended_factor,factor_unit\n'
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
    # 排放形式,排放源類別,燃料別,建議排放係數數值,建議排放係數單位
    csv_head = 'emission_form,emission_type,burn_type,recommended_factor,factor_unit\n'
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
        if len(row) != 6 or row[1] == '-':
            index += 1
            continue
        row_index = 0
        for value in row:
            if value == '─':
                row[row_index] = 0
            row_index += 1

        row = row[1:comment_index+1]
        row[0] = '"' + row[0] + '"'
        csv_row = ','.join(list(map(str, row)))
        if len(csv_row.split(',')) != 5:
            index += 1
            continue

        csv_rows += csv_row + '\n'
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True


def parse_fugitive_emission(ods_data, ods_burn_sheet_key, csv_dir):
    # 設備名稱,排放因子(％),防治設備回收率(％),防治設備使用率(％),冷媒排放係數,單位,來源
    csv_head = 'equipment_name,emission_percent,recycle_percent,usage_percent,emission_factor,unit,source\n'
    csv_file_path = csv_dir + '/' + ods_burn_sheet_key + '.csv'
    index = 237
    end_index = 244
    csv_rows = csv_head
    while index <= end_index:
        mapped = list(map(str, ods_data[ods_burn_sheet_key][index][1:]))
        csv_rows += ','.join(mapped[0:1] + mapped[2:]) + '\n'
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True

def parse_fcfs_factor_emission(ods_data, ods_burn_sheet_key, csv_dir):
    # 設備名稱(中文),IPCC名稱,最小排放因子(%),最大排放因子(%),防治設備回收率(%)
    csv_head = 'equipment_name,ipcc_name,emission_min_percent,emission_max_percent,recycle_percent\n'
    csv_file_path = csv_dir + '/' + ods_burn_sheet_key + '.csv'
    index = 2
    end_index = 9
    csv_rows = csv_head
    while index <= end_index:
        mapped = list(map(str, ods_data[ods_burn_sheet_key][index]))
        mapped[1] = '"' + mapped[1] + '"'
        factor_arr = mapped[2].split('≦')
        min_factor = factor_arr[0]
        max_factor = factor_arr[2]
        mapped[2] = min_factor + ',' + max_factor
        csv_rows += ','.join(mapped) + '\n'
        index += 1

    csv_handler = open(csv_file_path, 'w')
    csv_handler.write(csv_rows)
    csv_handler.close()

    return True

is_started_str = ' is started.'
is_done_str = ' is done.'

ods_files = glob.glob('./datasets/*.ods')
keyword = '溫室氣體排放係數管理表'
for ods_file in ods_files:
    if keyword in ods_file:
        print('Parsing ' + ods_file + is_started_str)
        parse_ods_file(ods_file)
        print('Parsing ' + ods_file + is_done_str)
