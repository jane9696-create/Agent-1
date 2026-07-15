import xlrd
import json
import sys

xls_path = r"C:\D\MRS client-2014\MRS\AI training\Claude-QSD\1. QSD standard checklist.xls"
wb = xlrd.open_workbook(xls_path, encoding_override='cp950')
ws = wb.sheet_by_name('QSD standard')

rows = []
for i in range(ws.nrows):
    row = [str(ws.cell_value(i, j)) for j in range(ws.ncols)]
    rows.append(row)

print(json.dumps(rows, ensure_ascii=False))
