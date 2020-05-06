#!/usr/bin/python


from bs4 import BeautifulSoup
import csv


def ExtractTable(html, attrs, extract_links=False):
    soup = BeautifulSoup(html, 'html.parser')
    # attrs={'id':'equityTopSummaryTable'}
    table = soup.findAll("table", attrs=attrs)
    assert len(table) != 0
    table = table[0]

    header = []
    output_rows = []
    links = []
    for table_row in table.findAll('tr'):
        if header == [] and table_row.findAll('th') != []:
            for column in table_row.findAll('th'):
                header.append(column.text.strip())
        else:
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                if extract_links:
                    a_tags = column.findAll('a')
                    if a_tags != []:
                        links.append(a_tags[0].attrs['href'])
                output_row.append(column.text.strip())
            output_rows.append(output_row)

    # print(header)
    # print(output_rows)
    # print(links)
    return (header, output_rows, links) if extract_links else (header, output_rows)
