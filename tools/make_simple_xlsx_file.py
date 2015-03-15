#!/usr/bin/env python
# coding: utf-8

import os
import re
import xlsxwriter
from datetime import datetime

FILENAME = 'simple.xlsx'
DEBUG = False

DATA = [
    ('Person', 'Mary'),
    ('Age', 44),
    ('Income', 2000),
    ('Fee', -500),
    ('Birth', datetime(1970, 01, 03, 10, 0)),
    ('C2', ('insert_image', 'photo.jpg')),
]

if DEBUG:
    DATA.append(('E2', ('insert_image', 'photo_2.jpg')))

workbook = xlsxwriter.Workbook(FILENAME)
bold = workbook.add_format({'bold': 1})
date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
money_format = workbook.add_format({'num_format': '$#,##0'})


def main():
    # preparations
    row, col = (1, 0)
    worksheet = workbook.add_worksheet()
    if os.path.exists(FILENAME):
        os.unlink(FILENAME)

    # write headers
    worksheet.write('A1', 'Fields', bold)
    worksheet.write('B1', 'Values', bold)

    # write data
    for key, value in DATA:
        # write first column
        if re.match('\w\d+', key):
            pass
            # just won't write data with 'point' format: A1, A10, C120, etc
        else:
            worksheet.write(row, col, key)

        # write data with several data fmts
        if isinstance(value, datetime):
            worksheet.write(row, col + 1, value, date_format)
        elif key.lower() in ('income', 'fee'):
            worksheet.write(row, col + 1, value, money_format)
        elif re.match(r'\w\d+', key):
            # worksheet.insert_image(row, col + 1, 'photo.jpg')
            getattr(worksheet, value[0])(key, value[1])
        else:
            worksheet.write(row, col + 1, value)
        row += 1
    worksheet.write(row, 0, 'Clean income')
    worksheet.write(row, 1, '=SUM(B4:B5)', money_format)
    workbook.close()

if __name__ == '__main__':
    main()
