from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404 , HttpResponse, HttpRequest
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render
from . import data as getdata

# Create your views here.

'''index page controller'''
def index(request):
	return render(request, 'finance/index.html', {})


''' details page controller'''
def details(request):
	if request.GET['ticker'] != "":
		stock = request.GET['ticker']
		try:
			getdata.getdata(stock)
			return render(request, 'finance/details.html', {'openclose': getdata.getOpenClosegraph(stock),
		'highlow': getdata.getHighLowgraph(stock), 'industrydata': getdata.getIndustryPeers(stock),
		'keyratios': getdata.getKeyRatios(stock), 'financials': getdata.getFinancials(stock),
		'simplesum': getdata.getSimpleSummary(stock), 'currentprice': getdata.getCurrentPrice(stock),
		'industryprice': getdata.getIndustyPeersQuote(stock), 'recommendindustry': getdata.getRecommendation(stock),
		 'stock': stock}, )
		except OSError:
			messages.add_message(request, messages.ERROR, 'Invalid Ticker')
			return redirect(reverse('finance:index'))
	else:
		messages.add_message(request, messages.INFO, 'No Input was Inputted')
		return redirect(reverse('finance:index'))

	
	
	
