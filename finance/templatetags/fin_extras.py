from django import template
import urllib.request
import re, datetime
from pandas_datareader.data import DataReader


register = template.Library()

''' get quote summary from morningstar'''
@register.simple_tag
def getCurrentPrice(ticker):
    url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=XNAS:%s&region=usa&culture=en-US&version=RET" % ticker)
    html = url.read()
    if len(html) != 0:
        html = str(html, "utf8").split('<script type="text/javascript">')
    else:
        url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=PINX:%s&region=usa&culture=en-US&version=RET" % ticker)
        html = url.read()
        if len(html) != 0:
                html = str(html, "utf8").split('<script type="text/javascript">')
        else:
            url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=XNYS:%s&region=usa&culture=en-US&version=RET" % ticker)
            html = url.read()
            if len(html) != 0:
                html = str(html, "utf8").split('<script type="text/javascript">')
            else:
                return None       
    return html[0]

'''get quote summary from yahoo '''
@register.simple_tag
def getSimpleSummary(ticker):
    url = urllib.request.urlopen("http://finance.yahoo.com/quote/%s" % ticker)
    html = url.read()
    html = str(html, "utf8").split('<div id=\"quote-summary\"')
    html[1] = '<div id=\"quote-summary\"' + html[1]    
    html = html[1].split("Trade prices are not sourced from all markets")
    html[0] = html[0]+'</span></div>'
    return html[0]

'''gets financials from morningstar'''
@register.simple_tag
def getFinancials(ticker):
    try:
        url = urllib.request.urlopen("http://financials.morningstar.com/financials/getFinancePart.html?&callback=?&t=XNAS:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
        html = url.read()
        html = str(html, "utf-8").split('?({"componentData":"')
        html = html[1].split('"})')
        html = re.sub(r'\\', "", html[0])
        html = html.split('<table')
        html = '<table'+html[1]
    except IndexError:
        try:
            url = urllib.request.urlopen("http://financials.morningstar.com/financials/getFinancePart.html?&callback=?&t=PINX:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
            html = url.read()
            html = str(html, "utf-8").split('?({"componentData":"')
            html = html[1].split('"})')
            html = re.sub(r'\\', "", html[0])
            html = html.split('<table')
            html = '<table'+html[1]
        except IndexError: 
            try:
                url = urllib.request.urlopen("http://financials.morningstar.com/financials/getFinancePart.html?&callback=?&t=XNYS:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
                html = url.read()
                html = str(html, "utf-8").split('?({"componentData":"')
                html = html[1].split('"})')
                html = re.sub(r'\\', "", html[0])
                html = html.split('<table')
                html = '<table'+html[1]
            except IndexError:
                html = "No Data"
    return html

'''find recommend stocks based on whether for the past week, 
if the closing prices have been consective higher than the previous day's'''
@register.simple_tag
def getRecommendation(ticker):
    recommendlist = []
    industrypeerlist = []
    weekdatelist = []
    stringdata = ""
    try: 
        url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=XNAS:%s&region=usa&culture=en-US&cur=" % ticker)
        html = url.read()
        html = str(html, "utf-8").split('<tbody>')
        data = html[2].split('</tbody>')
        data = data[0].split('</a>')
        for line in data:
            stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
            stringdata += stuff        
        stringdata = stringdata.split('<td align="left" scope="row" >')
        for i in range(2, len(stringdata)+1, 2):
            inddata = stringdata[i].split('</td>')
            industrypeerlist.append(inddata[0])
        startdate = datetime.date.today()- datetime.timedelta(1)    
        for i in range(7):
            nextdate = startdate -datetime.timedelta(i)
            if nextdate.isoweekday() < 6:
                weekdatelist.append(nextdate)        
        for peers in industrypeerlist:
            comp = peers.strip()
            try:
                count = 0
                data = DataReader(comp, 'yahoo', weekdatelist[len(weekdatelist)-1], weekdatelist[0])
                for i in range(len(weekdatelist)-1, 0, -1):
                    try:
                        if data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] > 0:
                            count += 1
                        elif data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] < 0:
                            count = 0
                    except KeyError:
                        continue
                if count >= 2:
                    recommendlist.append(comp)
            except OSError:
                continue
    except IndexError:
        try: 
            url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=PINX:%s&region=usa&culture=en-US&cur=" % ticker)
            html = url.read()
            html = str(html, "utf-8").split('<tbody>')
            data = html[2].split('</tbody>')
            data = data[0].split('</a>')
            for line in data:
                stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                stringdata += stuff        
            stringdata = stringdata.split('<td align="left" scope="row" >')
            for i in range(2, len(stringdata)+1, 2):
                inddata = stringdata[i].split('</td>')
                industrypeerlist.append(inddata[0])
            startdate = datetime.date.today()- datetime.timedelta(1)    
            for i in range(7):
                nextdate = startdate -datetime.timedelta(i)
                if nextdate.isoweekday() < 6:
                    weekdatelist.append(nextdate)        
            for peers in industrypeerlist:
                comp = peers.strip()
                try:
                    count = 0
                    data = DataReader(comp, 'yahoo', weekdatelist[len(weekdatelist)-1], weekdatelist[0])
                    for i in range(len(weekdatelist)-1):
                        try:
                            if data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] > 0:
                                count += 1
                            elif data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] < 0:
                                count = 0
                        except KeyError:
                            continue
                    if count >= 2:
                        recommendlist.append(comp)
                except OSError:
                    continue
        except IndexError:
            try: 
                url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=XNYS:%s&region=usa&culture=en-US&cur=" % ticker)
                html = url.read()
                html = str(html, "utf-8").split('<tbody>')
                data = html[2].split('</tbody>')
                data = data[0].split('</a>')
                for line in data:
                    stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                    stringdata += stuff        
                stringdata = stringdata.split('<td align="left" scope="row" >')
                for i in range(2, len(stringdata)+1, 2):
                    inddata = stringdata[i].split('</td>')
                    industrypeerlist.append(inddata[0])
                startdate = datetime.date.today()- datetime.timedelta(1)    
                for i in range(7):
                    nextdate = startdate -datetime.timedelta(i)
                    if nextdate.isoweekday() < 6:
                        weekdatelist.append(nextdate)        
                for peers in industrypeerlist:
                    comp = peers.strip()
                    try:
                        count = 0
                        data = DataReader(comp, 'yahoo', weekdatelist[len(weekdatelist)-1], weekdatelist[0])
                        for i in range(len(weekdatelist)-1):
                            try:
                                if data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] > 0:
                                    count += 1
                                elif data.ix[str(weekdatelist[i-1])]['Close']-data.ix[str(weekdatelist[i])]['Close'] < 0:
                                    count = 0
                            except KeyError:
                                continue
                        if count >= 2:
                            recommendlist.append(comp)
                    except OSError:
                        continue
            except IndexError:
                recommendlist = None
    return recommendlist

'''get Key Ratios data from MorningStar'''
@register.simple_tag
def getKeyRatios(ticker):
    try:
        url = urllib.request.urlopen("http://financials.morningstar.com/financials/getKeyStatPart.html?&callback=?&t=XNAS:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
        html = url.read()
        html = str(html, "utf-8").split('?({"componentData":"')
        html = html[1].split('"})')
        html = re.sub(r'\\', "", html[0])
        html = html.split('</ul>')
        html = html[1].split('style="display:none;"')
        data = ""
        for line in html:
            data += line
        data = data.split("</table>")
        for i in range(len(data)-1):
            splitdata = data[i].split("<table")
            data[i] = "<table" + splitdata[1] + "</table>"
    except IndexError:
        try:
                url = urllib.request.urlopen("http://financials.morningstar.com/financials/getKeyStatPart.html?&callback=?&t=PINX:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
                html = url.read()
                html = str(html, "utf-8").split('?({"componentData":"')
                html = html[1].split('"})')
                html = re.sub(r'\\', "", html[0])
                html = html.split('</ul>')
                html = html[1].split('style="display:none;"')
                data = ""
                for line in html:
                    data += line
                data = data.split("</table>")
                for i in range(len(data)-1):
                    splitdata = data[i].split("<table")
                    data[i] = "<table" + splitdata[1] + "</table>"
        except IndexError:
            try:
                    url = urllib.request.urlopen("http://financials.morningstar.com/financials/getKeyStatPart.html?&callback=?&t=XNYS:%s&region=usa&culture=en-US&ops=clear&cur=&order=" % ticker)
                    html = url.read()
                    html = str(html, "utf-8").split('?({"componentData":"')
                    html = html[1].split('"})')
                    html = re.sub(r'\\', "", html[0])
                    html = html.split('</ul>')
                    html = html[1].split('style="display:none;"')
                    data = ""
                    for line in html:
                        data += line
                    data = data.split("</table>")
                    for i in range(len(data)-1):
                        splitdata = data[i].split("<table")
                        data[i] = "<table" + splitdata[1] + "</table>"
            except IndexError:
                    data = "No Data"
    return data

'''gets the Price Quotes of Industry Peers from MorningStar'''
@register.simple_tag
def getIndustyPeersQuote(ticker):
    stringdata = ""
    try:
        url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=XNAS:%s&region=usa&culture=en-US&cur=" % ticker)
        html = url.read()
        html = str(html, "utf-8").split('<tbody>')
        data = html[2].split('</tbody>')
        data = data[0].split('</a>')
        for line in data:
            stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
            stringdata += stuff        
    except IndexError:
        try:
            url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=PINX:%s&region=usa&culture=en-US&cur=" % ticker)
            html = url.read()
            html = str(html, "utf-8").split('<tbody>')
            data = html[2].split('</tbody>')
            data = data[0].split('</a>')
            for line in data:
                stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                stringdata += stuff        
        except IndexError:
            try:
                url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-quote.action?type=com&t=XNYS:%s&region=usa&culture=en-US&cur=" % ticker)
                html = url.read()
                html = str(html, "utf-8").split('<tbody>')
                data = html[2].split('</tbody>')
                data = data[0].split('</a>')
                for line in data:
                    stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                    stringdata += stuff        
            except IndexError:
                stringdata = "No Data"
    return(stringdata)

'''get Industry Peers from MorningStar'''
@register.simple_tag
def getIndustryPeers(ticker):
    stringdata = ""
    try:
        url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-data.action?type=com&t=XNAS:%s&region=usa&culture=en-US&cur=" % ticker)
        html = url.read()
        html = str(html, "utf-8").split('<tbody>')
        data = html[2].split('</tbody>')
        data = data[0].split('</a>')
        for line in data:
            stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
            stringdata += stuff        
    except IndexError:
        try:
            url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-data.action?type=com&t=PINX:%s&region=usa&culture=en-US&ops=p&cur=" % ticker)
            html = url.read()
            html = str(html, "utf-8").split('<tbody>')
            data = html[2].split('</tbody>')
            data = data[0].split('</a>')
            for line in data:
                stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                stringdata += stuff        
        except IndexError:
            try:
                url = urllib.request.urlopen("http://financials.morningstar.com/competitors/industry-peer-data.action?type=com&t=XNYS:%s&region=usa&culture=en-US&cur=" % ticker)
                html = url.read()
                html = str(html, "utf-8").split('<tbody>')
                data = html[2].split('</tbody>')
                data = data[0].split('</a>')
                for line in data:
                    stuff = re.sub('[\<]{1}[aA]{1}[0-9a-zA-Z\D]*[\"]{1}[\>]{1}', "", line)
                    stringdata += stuff        
            except IndexError:
                stringdata = "No Data"
    return stringdata
