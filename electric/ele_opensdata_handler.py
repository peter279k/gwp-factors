handler = open('./datasets/electric_94_105.csv', 'r')
contents = handler.readlines()
contents[-1] += '\n '
contents = contents[1:]
handler.close()

csv_contents = ''

for content in contents:
    gwp = content[0:-2].split(',')
    year = gwp[0][0:-1]
    co2e_val = gwp[2]
    csv_contents += year + ',' + co2e_val + '\n'

handler = open('./datasets/electric_co2e.csv', 'w')
handler.write(csv_contents)
handler.close()
