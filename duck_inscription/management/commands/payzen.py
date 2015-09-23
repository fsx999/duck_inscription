# from __future__ import unicode_literals
import hashlib

__author__ = 'paulguichon'
# coding=utf-8
import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from suds.client import Client
from suds.sax.element import Element
import uuid
import hmac
import base64
class Command(BaseCommand):


    def handle(self, *args, **options):
        date = datetime.datetime.utcnow().replace(
                tzinfo=utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        certif = '5535052304931319'
        url = 'https://secure.payzen.eu/vads-ws/v5?wsdl'
        client = Client(url)
        shopId = Element('shopId').setText('58163425')
        rid = str(uuid.uuid1())
        requestId = Element('requestId').setText(rid)
        timestamp = Element('timestamp').setText(date)
        mode = Element('mode').setText('PRODUCTION')

        id = rid + date
        token = hmac.new(bytes(certif).encode("utf-8"), bytes(id).encode("utf-8"), hashlib.sha256).digest()
        token = base64.b64encode(token)
        authToken = Element('authToken').setText(token)
        client.set_options(soapheaders=(shopId, requestId, timestamp, mode, authToken))
        # print client
        p = client.factory.create('queryRequest')
        p.orderId = 693
        for x in client.service.findPayments(p)['transactionItem']:
            print x['amount']