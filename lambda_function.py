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

def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read('config.ini')

    mf_info, mf_links = [], []
    for source in config['DEFAULT']['sources'].split(','):
        html = FetchPage(source)
        
        _, info, links = ExtractTable(html, attrs={'id':'dataTableId'}, extract_links=True)
        mf_info.extend(info)
        mf_links.extend(links)

    # print(mf_info[0])
    # print(mf_links[0])

    for i, x in enumerate(mf_links):
        s = x.split('/')
        mf_links[i] = '/'.join(s[:-1] + ['portfolio-holdings', s[-1]])

    kvpairs = {}

    for i, l in zip(mf_info, mf_links):
        # print(i)
        # print(l)
        html = FetchPage(l)
        header, info = ExtractTable(html, attrs={'id':'equityTopSummaryTable'})
        # print('headeri', i)
        # print('header', header)
        # print('info', info)
        _, info = FormatTable(header, info)
        kvpairs[i[0]] = info #json.dumps(info)
        # break;

    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

    funds_table = dynamodb.Table('funds')

    for k,v in kvpairs.items():
        # print('k', k, 'v', v)
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



