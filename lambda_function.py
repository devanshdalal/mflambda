#!/usr/bin/python

import boto3
from bs4 import BeautifulSoup
import csv
import json
import configparser
from datetime import date

from caching_urllib import FetchPage
from table_extractor import ExtractTable
from table_formatter import FormatTable

def LambdaHandler(event, context):
    print('event:', event, 'context:', context)
    config = configparser.ConfigParser()
    print('Reading the config.ini')
    config.read('config.ini')

    print('Fetching the sources')
    mf_info, mf_links = [], []
    for source in config['DEFAULT']['sources'].split(','):
        html = FetchPage(source)
        
        _, info, links = ExtractTable(html, attrs={'id':'dataTableId'}, extract_links=True)
        mf_info.extend(info)
        mf_links.extend(links)

    # print(mf_info[0])
    # print(mf_links[0])

    print('Tranforming the links to portfolio-holdings')
    for i, x in enumerate(mf_links):
        s = x.split('/')
        mf_links[i] = '/'.join(s[:-1] + ['portfolio-holdings', s[-1]])

    kvpairs = {}

    print('Fetching the sources\' portfolio-holdings')
    for i, l in zip(mf_info, mf_links):
        # print(i)
        # print(l)
        if (i[1] == 'Regular'):
            continue
        print('Fetching the portfolio-holding:', l, i)
        html = FetchPage(l)
        header, info = ExtractTable(html, attrs={'id':'equityCompleteHoldingTable'})
        # print('headeri', i)
        # print('header', header)
        # print('info', info)
        _, info = FormatTable(header, info)
        kvpairs[i[0]] = info #json.dumps(info)
        # break;
    # return

    print('Creating the dynamodb resource')
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

    print('Getting the funds table')
    funds_table = dynamodb.Table('funds')

    for k,v in kvpairs.items():
        print('k', k, 'v', v)
        response = funds_table.update_item(
            Key={
                'name': k,
            },
            UpdateExpression="set portfolio = :r, update_time = :s",
            ExpressionAttributeValues={
                ':r': v,
                ':s': str(date.today())
            },
            ReturnValues="UPDATED_NEW"
        )
        print('response', response)



