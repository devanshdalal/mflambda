#!/usr/bin/python

import boto3
from bs4 import BeautifulSoup
import csv
import json
import sys
import configparser
from datetime import datetime, timedelta

from caching_urllib import FetchPage
from table_extractor import ExtractTable
from table_formatter import FormatTable
from util import Pool
from threading import Lock
s_print_lock = Lock()

def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


EXPIRY_TTL = timedelta(days=180)

def Execute(ind, mf_info, link, funds_table):
    s_print('Fetching the', ind, 'th portfolio-holding:', link, mf_info)
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
    for s in config['SOURCES']:
        print('config[SOURCES]', s)
    for source in config['SOURCES'][event['resources'][0].split('/')[-1]].split(','):
        html = FetchPage(source)
        _, info, links = ExtractTable(html, attrs={'id':'dataTableId'}, extract_links=True)
        mf_info.extend(info)
        mf_links.extend(links)

    print('Tranforming the links to portfolio-holdings')
    for i, x in enumerate(mf_links):
        if (len(x) > 0):
            s = x.split('/')
            mf_links[i] = '/'.join(s[:-1] + ['portfolio-holdings', s[-1]])

    print('Creating the dynamodb resource')
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

    # client = boto3.client('dynamodb',
    #   aws_access_key_id='AKIA2VLYX2H6IG7HOBBR',
    #   aws_secret_access_key='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',
    #   region_name='ap-south-1')
    # print(client.scan(TableName='baskets'))
    # sys.exit()


    print('Getting the funds table')
    funds_table = dynamodb.Table('funds')

    params = []

    for ind, (i, l) in enumerate(zip(mf_info, mf_links)):
        if (i[1] == 'Regular' or len(l) == 0):
            continue
        params.append((ind, i, l, funds_table))

    print('Fetching the sources\' portfolio-holdings')
    # Execute(params[0][0], params[0][1], params[0][2], funds_table)
    Pool(Execute, params, max_workers=5)



