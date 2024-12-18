import hashlib
import json
import requests
from datetime import datetime, timedelta
import os
import pytz

tz = pytz.timezone('Asia/Bangkok')

STATUS_ALL = "ALL"
STATUS_COMPLETE = "COMPLETE"


class ShopeeAffiliate():
    def __init__(self, appid, secret) -> None:
        self.appid, self.secret = appid, secret

    def header(self, payload={}):
        time_stamp = int(datetime.now().timestamp())
        hash = ''.join([self.appid, str(time_stamp),
                       json.dumps(payload), self.secret])
        sign = hashlib.sha256(hash.encode("utf-8")).hexdigest()
        
        return {
            'Authorization': 'SHA256 Credential=%s, Signature=%s, Timestamp=%d' % (self.appid, sign, time_stamp),
            'Content-Type': 'application/json',
        }

    def req(self, payload={}):
        headers = self.header(payload)
        response = requests.post(
            'https://open-api.affiliate.shopee.vn/graphql',
            headers=headers,
            json=payload,
            timeout=20
        )
        return response.json()

    def generateShortLink(self, url, account, sosmed, sosmed1):
        keys=["{}".format(sosmed), "{}".format(sosmed1), "{}".format(account)]
        payload = {
            "query": 'mutation {  generateShortLink(input: {originUrl: "%s", subIds: %s}) { shortLink } }' %
            (url, json.dumps(keys))
        }
        res = self.req(payload)
        return res['data']['generateShortLink']['shortLink']

    def _report_(self, start: datetime = None, end: datetime = None, scrollId="", status=STATUS_ALL):
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = end.replace(hour=23, minute=59, second=59, microsecond=0)
        payload = {"query": """{
            conversionReport(purchaseTimeStart: %d, purchaseTimeEnd: %d, scrollId: "%s", limit:500, orderStatus: %s) {
            nodes {
            estimatedTotalCommission
            grossCommission
            cappedCommission
            totalBrandCommission
            checkoutId
            purchaseTime
            }
            pageInfo {
            scrollId
            hasNextPage
            }
            }
        }""" % (start.timestamp(), end.timestamp(), scrollId, status)}
        return self.req(payload)

    def report(self, start: datetime, end: datetime = None, status=STATUS_ALL):
        est = 0
        conv = 0
        scrollId = ""
        if not end:
            end = datetime.now()
        start = start.replace(tzinfo=tz)\
            .replace(hour=0, minute=0, second=0, microsecond=0)
        end = end.replace(tzinfo=tz)\
            .replace(hour=23, minute=59, second=59, microsecond=0)
        while True:
            try:
                response = self._report_(
                    start=start,
                    end=end,
                    scrollId=scrollId,
                    status=status
                )
                if not "data" in response:
                    break
                scrollId = response['data']['conversionReport']['pageInfo']['scrollId']
                for node in response['data']['conversionReport']['nodes']:
                    conv += 1
                    est += float(node['estimatedTotalCommission'])
                # print(" {:,} -> {:,.0f}".format(conv, est))
                if not response['data']['conversionReport']['pageInfo']['hasNextPage']:
                    break
            except Exception as e:
                print("Error:", e)
                break
        FORMAT_DATE = "%Y-%m-%d"
        return (
            "{:,.0f}".format(conv),
            "{:,.0f}".format(est),
            start.strftime(FORMAT_DATE),
            end.strftime(FORMAT_DATE)
        )

class ATAffiliate():
    def __init__(self, token) -> None:
        self.token = token

    def header(self, payload={}):
        
        return {
            'Authorization': 'Token %s' % (self.token),
            'Content-Type': 'application/json',
        }
        
    def req(self,payload):
        headers = self.header()
        response = requests.post(
            'https://api.accesstrade.vn/v1/product_link/create',
            headers=headers,
            json=payload,
            timeout=20
        )
        return response.json()
    
    def generateShortLink(self, url, campaign_id, account, sosmed, sosmed1):
        keys=["{}".format(sosmed), "{}".format(sosmed1), "{}".format(account)]
        payload = {
          "campaign_id" : campaign_id,
           "urls": url,
           "utm_source":account,
            "utm_medium":sosmed,
            "utm_content":sosmed1,
        }
        res = self.req(payload)
        print(res)
        return res['data']['success_link'][0]['short_link']
    
    def getATCampaign(self):
        headers = self.header()
        response = requests.get(
            'https://api.accesstrade.vn/v1/campaigns?limit=5',
            headers=headers,
            timeout=20
        )
        return response.json()