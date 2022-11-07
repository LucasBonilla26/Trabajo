import pandas as pd
import openpyxl
import xlrd
filename = 'mier.xlsx'
df1 = pd.read_excel(filename,
     engine='openpyxl', index_col=None
)
print(df1)
df1.to_csv('csvfile.csv', encoding='utf-8')
xlsx = openpyxl.load_workbook(filename)
sheet = xlsx.active
data = sheet.rows
csv = open("data.csv", "w+")
for row in data:
    l = list(row)
    print(l)
    for i in range(len(l)):
        if i == len(l) - 1:
            #print(l[i].value)
            csv.write(str(l[i].value))
        else:
            #print(l[i].value)
            csv.write(str(l[i].value) + ',')
        csv.write('\n')

## close the csv file
csv.close()

loc = (filename)
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
print(sheet.cell_value(0, 0))