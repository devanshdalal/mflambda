#!/usr/bin/python


from bs4 import BeautifulSoup
import csv

# TOP_N = 40

def ExtractTable(html, attrs, extract_links=False):
    soup = BeautifulSoup(html, 'html.parser')
    # attrs={'id':'equityTopSummaryTable'}
    table = soup.findAll("table", attrs=attrs)
    if (len(table) == 0):
        return None, None
    table = table[0]

    header = []
    output_rows = []
    links = []
    # print('tr', len(table.findAll('tr')))
    for i, table_row in enumerate(table.findAll('tr')):
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
                        # print(i, a_tags)
                        links.append(a_tags[0].attrs['href'])
                    # else:
                        # links.append('')
                output_row.append(column.text.strip())
            output_rows.append(output_row)

    if (extract_links):
        assert len(output_rows) == len(links),\
                str(len(output_rows)) + '!=' + str(len(links))

    # output_rows = output_rows[:min(len(output_rows), TOP_N)]
    # links = links[:min(len(links), TOP_N)]
    # print(header)
    # print(output_rows)
    # print(links)
    return (header, output_rows, links) if extract_links else (header, output_rows)

