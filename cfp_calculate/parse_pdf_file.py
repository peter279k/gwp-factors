import os
import sys
import pdftotext


factor_pdf_file = './datasets/cfp_factors.pdf'
print('Parsing the %s is started!' % factor_pdf_file)

if os.path.isfile(factor_pdf_file) is False:
    print('The %s PDF file is not found.' % factor_pdf_file)
    sys.exit(1)

with open(factor_pdf_file, 'rb') as f:
    pdf_contents = pdftotext.PDF(f)


keywords = ['揭露項目', '內容']

csv_tw_head = '中文名稱,英文名稱,碳足跡數值,碳足跡數值單位,數量,宣告單位,生命週期範疇(系統邊界),生產區域名稱,盤查起迄日,公告年份'
csv_head = 'ch_name,en_name,co2e_value,co2e_unit,amount,declared_unit,lifecycle_boundary,produce_area_name,checked_date_range,published_year'

head_arr = csv_tw_head.split(',')
csv_contents = csv_head + '\n'
csv_file_path = './datasets/cfp_factors.csv'

pdf_contents_index = 0
while pdf_contents_index < len(pdf_contents):
    pdf_content = pdf_contents[pdf_contents_index]
    page_arr = pdf_content.split('\n')
    if len(page_arr) < 1:
        pdf_contents_index += 1
        continue

    check_item_row = page_arr[0]

    if check_item_row.count(keywords[0]) != 1 and check_item_row.count(keywords[1]) != 1:
        pdf_contents_index += 1
        continue

    item_ch_name = page_arr[1].replace(' ', '').replace(head_arr[0], '')
    item_en_name = page_arr[2].replace(' ', '').replace(head_arr[1], '')

    index = 4
    while head_arr[2] not in page_arr[index]:
        index += 1

    co2e_val_info = page_arr[index].replace(head_arr[2], '').split(' ')
    co2e_value = co2e_val_info[-2]
    co2e_unit = co2e_val_info[-1]

    index = 5
    while head_arr[4] not in page_arr[index]:
        index += 1

    amount = page_arr[index].replace(' ', '').replace(head_arr[4], '')

    while head_arr[5] not in page_arr[index]:
        index += 1

    declared_unit = page_arr[index].replace(head_arr[5], '').replace(' ', '')

    index = 5
    life_cycle_keyword = '生命週期範疇'
    while life_cycle_keyword not in page_arr[index]:
        index += 1

    life_cycle_boundary = page_arr[index].replace(' ', '').replace(life_cycle_keyword, '')

    index = 5
    while head_arr[7] not in page_arr[index]:
        index += 1

    produce_area_name = page_arr[index].replace(' ', '').replace(head_arr[7], '')

    index = 8
    while head_arr[8] not in page_arr[index]:
        index += 1

    checked_date = page_arr[index].replace(' ', '').replace(head_arr[8], '')

    find_published_year = False
    index = 8
    while index < len(page_arr) and head_arr[9] not in page_arr[index]:
        index += 1

    if index < len(page_arr):
        published_year = page_arr[index].replace(' ', '').replace(head_arr[9], '')
        find_published_year = True

    if find_published_year is False:
        pdf_contents_index += 1
        next_pdf_content = pdf_contents[pdf_contents_index]
        next_page_arr = next_pdf_content.split('\n')
        index = 0
        while head_arr[9] not in next_page_arr[index]:
            index += 1

        published_year = next_page_arr[index].replace(' ', '').replace(head_arr[9], '')

    csv_row = '"%s","%s",%s,%s,%s,%s,%s,%s,%s,%s\n' % (
        item_ch_name,
        item_en_name,
        co2e_value,
        co2e_unit,
        amount,
        declared_unit,
        produce_area_name,
        life_cycle_boundary[0:5],
        checked_date,
        published_year,
    )

    csv_contents += csv_row

    pdf_contents_index += 1

with open(csv_file_path, 'w') as f:
    f.write(csv_contents)

print('Parsing the %s PDF file is done.\nThe %s CSV file is saved in dataserts folder.' % (
    factor_pdf_file,
    csv_file_path,
))
