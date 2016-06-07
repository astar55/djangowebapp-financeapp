from django import template
import urllib.request
import re


register = template.Library()

''' get quote summary from morningstar'''
@register.simple_tag
def getCurrentPrice(ticker):
    try:
        url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=XNAS:%s&region=usa&culture=en-US&version=RET" % ticker)
        html = url.read()
        html = str(html, "utf8").split('<script type="text/javascript">')
    except IndexError:
        try:
            url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=PINX:%s&region=usa&culture=en-US&version=RET" % ticker)
            html = url.read()
            html = str(html, "utf8").split('<script type="text/javascript">')
        except IndexError:
            try:
                url = urllib.request.urlopen("http://quotes.morningstar.com/stock/c-header?&t=XNYS:%s&region=usa&culture=en-US&version=RET" % ticker)
                html = url.read()
                html = str(html, "utf8").split('<script type="text/javascript">')
            except IndexError:
                return None       
    return html[0]

'''get quote summary from yahoo '''
@register.simple_tag
def getSimpleSummary(ticker):
    url = urllib.request.urlopen("http://finance.yahoo.com/q?s=%s" % ticker)
    html = url.read()
    html = str(html, "utf8").split('<div id="yfi_quote_summary_data" class="rtq_table">')
    html = html[1].split("</div>")
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
