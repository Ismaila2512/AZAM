import openpyxl
wb = openpyxl.load_workbook("/Users/apple/Downloads/saviynt shortlist with role.xlsx", data_only=True)
neoid = "D0T5M3E2"
found = False
for sheet in wb.worksheets:
    for row in sheet.iter_rows(values_only=True):
        for cell in row:
            if isinstance(cell, str) and neoid.lower() in cell.lower():
                found = True
print("Found:", found)
