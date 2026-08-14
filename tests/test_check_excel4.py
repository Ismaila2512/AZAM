import openpyxl
wb = openpyxl.load_workbook("/Users/apple/Downloads/saviynt shortlist with role.xlsx", data_only=True)
for sheet in wb.worksheets:
    for row in sheet.iter_rows(values_only=True):
        if row[1] and "E2" in str(row[1]):
            print(row[1])
