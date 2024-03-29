#!/usr/bin/python

from decimal import Decimal

def FormatTable(header, table_rows):
	# print('header', header, 'table_rows', table_rows)
	new_header = {'name': 'weight'}
	new_table = []
	for row in table_rows:
		new_table.append({
			'stock': row[0],
			'wt': round(Decimal(row[4].replace('%', '')) / Decimal(100.0), 4),
			'sector': row[1]}
		)

	return new_header, new_table

