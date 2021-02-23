#!/usr/bin/python

import boto3
from bs4 import BeautifulSoup
import csv
import json
import configparser
from datetime import datetime, timedelta

from caching_urllib import FetchPage
from table_extractor import ExtractTable
from table_formatter import FormatTable
from util import Pool

EXPIRY_TTL = timedelta(days=180)

def Execute(ind, mf_info, link, funds_table):
    print('Fetching the', ind, 'th portfolio-holding:', link, mf_info)
    html = FetchPage(link)
    header, info = ExtractTable(html, attrs={'id':'equityCompleteHoldingTable'})
    if header == None:
        return
    # print('headeri', i)
    # print('header', header)
    # print('info', info)
    _, info = FormatTable(header, info)

    response = funds_table.update_item(
        Key={
            'name': mf_info[0],
        },
        UpdateExpression="set portfolio = :r, delete_after = :s",
        ExpressionAttributeValues={
            ':r': info,
            ':s': int((datetime.now() - datetime.utcfromtimestamp(0) + EXPIRY_TTL).total_seconds())
        },
        ReturnValues="UPDATED_NEW"
    )
    # print('response', response)

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
    # print('mf_links', mf_links)

    print('Tranforming the links to portfolio-holdings')
    for i, x in enumerate(mf_links):
        if (len(x) > 0):
            s = x.split('/')
            mf_links[i] = '/'.join(s[:-1] + ['portfolio-holdings', s[-1]])

    print('Creating the dynamodb resource')
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

    print('Getting the funds table')
    funds_table = dynamodb.Table('funds')

    params = []

    for ind, (i, l) in enumerate(zip(mf_info, mf_links)):
        if (i[1] == 'Regular' or len(l) == 0):
            continue
        params.append((ind, i, l, funds_table))

    print('Fetching the sources\' portfolio-holdings')
    Pool(Execute, params, max_workers=5)



