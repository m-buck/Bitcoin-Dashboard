#!/usr/bin/python
#
# nicehash.py
#
# Pull BTC wallet/price info and generate html page to be displayed on kitchen tv
#
from datetime import datetime, timedelta
import requests
import json

CoinDesk_base_url = 'http://api.coindesk.com/v1/bpi/'
current_price_url = "{}currentprice.json".format(CoinDesk_base_url)
day_change_url = 'https://api.coinmarketcap.com/v2/ticker/?convert=BTC&limit=1'
time_format = '%Y-%m-%d'
date_format = '%m-%d'

# Create dates
today = datetime.now()
last_year = datetime.strftime(today - timedelta(days=365), time_format)
last_year2 = datetime.strftime(today - timedelta(days=366), time_format)
last_month = datetime.strftime(today - timedelta(days=32), time_format)
last_week = datetime.strftime(today - timedelta(days=8), time_format)

historic_price_url = "{}historical/close.json?start={}&end={}".format(
    CoinDesk_base_url,
    last_year2,
    last_year,)
month_price_url = "{}historical/close.json?start={}&end={}".format(
    CoinDesk_base_url,
    last_month,
    datetime.strftime(today, time_format))
week_price_url = "{}historical/close.json?start={}&end={}".format(
    CoinDesk_base_url,
    last_week,
    datetime.strftime(today, time_format))
# Query CoinDesk Current price API
current_price_response = requests.get(current_price_url).json()
# Query CoinDesk historical API
historic_price_response = requests.get(historic_price_url).json()
# Query CoinDesk month
month_price_response = requests.get(month_price_url).json()
# Query CoinDesk wekk
week_price_response = requests.get(week_price_url).json()

current_price = "$" + str('{:.2f}'.format(round(current_price_response['bpi']['USD']['rate_float'], 2)))
historic_price = "$" + str('{:.2f}'.format(round(historic_price_response['bpi'][last_year], 2)))
month_price = "$" + str('{:.2f}'.format(round(month_price_response['bpi'][last_month], 2)))
week_price = "$" + str('{:.2f}'.format(round(week_price_response['bpi'][last_week], 2)))

print "Current price: " + str(current_price)
print "Last week's price: " + str(week_price)
print "Last month's price: " + str(month_price)
print "Last year's price: " + str(historic_price)

#coindesk json fetch
url = "https://api.coindesk.com/v1/bpi/historical/close.json"
data = requests.get(url).json()
day_change = requests.get(day_change_url).json()
day_change = str(day_change["data"]["1"]["quotes"]["USD"]["percent_change_24h"])
if "-" in str(day_change):
    #make text red
    day_change = day_change  +"%"
    day_change = "<font color=\"red\">"+day_change+"</font>"
    print "negative"
elif -5 > float(day_change):
    print "24hr change < -5"
    day_change = day_change  +"%"
    day_change = "<font color=\"red\">"+day_change+"</font>" + "&nbsp<img src=\"poop.png\" height=\"14\" width=\"14\">"
elif 5 < float(day_change):
    print "24hr change > 5"
    day_change = day_change  +"%"
    day_change = "<font color=\"green\">"+day_change+"</font>" + "&nbsp<img src=\"fire.png\" height=\"16\" width=\"16\">"
else:
    #make text green
    day_change = day_change  +"%"
    day_change = "<font color=\"green\">"+day_change+"</font>"
    print "positive"

print "24hr change: " + day_change
count = 32
prices = "["
days = "["
while count > 0:    
    day = datetime.strftime(today - timedelta(days=count), time_format) 
    price = round(month_price_response['bpi'][day], 2)
    prices = prices + str(price) + ","
    day = datetime.strftime(today - timedelta(days=count), date_format)
    days = days + "\""+str(day)+"\"" + ","
    #print ('{} {}'.format(day, price))
    count = count - 1
prices = prices[:-1]
days = days[:-1]
prices = prices + "]"
days = days + "]"
print prices
print days

#blockchain api for wallet balance
wal1_blkChain = "https://blockchain.info/rawaddr/<wallet address 1>"
wal2_blkChain = "https://blockchain.info/rawaddr/<wallet address 2>"
wal3_blkChain = "https://blockchain.info/rawaddr/<wallet address 3>"
wal1_wallet = requests.get(wal1_blkChain).json()
wal2_wallet = requests.get(wal2_blkChain).json()
wal3_wallet = requests.get(wal3_blkChain).json()
#get btc wallet balance
wal1_walletBal = str('{:.8f}'.format(float(wal1_wallet["final_balance"])/100000000))
wal2_walletBal = str('{:.8f}'.format(float(wal2_wallet["final_balance"])/100000000))
wal3_walletBal = str('{:.8f}'.format(float(wal3_wallet["final_balance"])/100000000))

wal1_USD = "$"+str('{:.2f}'.format(round((float(wal1_walletBal)*float(current_price[1:])),2)))
wal2_USD = "$"+str('{:.2f}'.format(round(float(wal2_walletBal)*float(current_price[1:]),2)))
wal3_USD = "$"+str('{:.2f}'.format(round(float(wal3_walletBal)*float(current_price[1:]),2)))


print "Wallet1: " + wal1_walletBal + " USD: " + wal1_USD
print "Wallet2: " + wal2_walletBal + " USD: " + wal2_USD
print "Wallet3: " + wal3_walletBal + " USD: " + wal3_USD

#vairables needed for html
#Current price: current_price
#Last Week: week_price
#Last Month: month_price
#Last Year: historic_price
#24hr change: day_change
#Wallet1 - wallet: wal1_walletBal - usd: wal1_USD
#Wallet2 - wallet: wal2_walletBal - usd: wal2_USD
#Wallet1 - wallet: wal3_walletBal - usd: wal3_USD


#Define HTML Template
contents = '''<!DOCTYPE HTML>
<html>
<head>
<title>Bitcoin Wallets</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="assets/css/main.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js" integrity="sha256-JG6hsuMjFnQ2spWq0UiaDRJBaarzhFbUxiUTxQDA9Lk=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js" integrity="sha256-XF29CBwU1MWLaGEnsELogU6Y6rcc5nCkhhx89nFMIDQ=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.js" integrity="sha256-J2sc79NPV/osLcIpzL3K8uJyAD7T5gaEFKlLDM18oxY=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.js" integrity="sha256-J2sc79NPV/osLcIpzL3K8uJyAD7T5gaEFKlLDM18oxY=" crossorigin="anonymous"></script>
<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
</head>
<body class="">

<br /><br /><br />
<center><img src="btc.png" height="80">



<div id="wrapper">
<section id="main">
<header>
<table width="*">
<tr>
<td width="428">
<span class="avatar"><img src="images/avatar.jpg" alt="" /></span>
<h1>Wallet1</h1>
<p>%s BTC<font color="green"><h3>%s</h3></font></p>
</td>
<td width="428">
<span class="avatar"><img src="images/avatar.jpg" alt="" /></span>
<h1>Wallet2</h1>
<p>%s BTC<font color="green"><h3>%s</h3></font></p>
</td>
<td width="428">
<span class="avatar"><img src="images/avatar.jpg" alt="" /></span>
<h1>Wallet3</h1>
<p>%s BTC<font color="green"><h3>%s</h3></font></p>
</td>
</tr>
</table>
</header>
</section><br /><br />
<section id="main">
<header>

<table width="*"><tr><td width="257"><h2>Current</h2><h3>%s</h3></td><td width="257"><h2>24-hr Change</h2>%s</td><td width="257"><h2>Last Week</h2>%s</td><td width="257"><h2>Last Month</h2>%s</td><td width="257"><h2>Last Year</h2>%s</td></tr><tr ><td colspan="5">
<br />
    <canvas id="myChart" width="1285" height="400"></canvas>
<script>
var ctx = document.getElementById("myChart").getContext('2d');
var gradientStroke = ctx.createLinearGradient(0, 0, 2000, 0);
gradientStroke.addColorStop(0, "rgba(124, 77, 255, .3)");
gradientStroke.addColorStop(0.3, "rgba(68, 138, 255, .3)");
gradientStroke.addColorStop(0.6, "rgba(0, 188, 212, .5)");
gradientStroke.addColorStop(1, "rgba(29, 233, 182, .6)");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: %s,
        datasets: [{
            label: 'Price USD',
            data: %s,
            lineTension: 0,
            lineTension: 0,
            //borderDash: [2, 2],
            //backgroundColor: [ 
            //    'rgba(54, 162, 235, 0.2)'
                //gradientStroke
            //],
            //borderColor: [
                //gradientStroke
            //    'rgba(54, 162, 235, 1)'
            //],
            borderColor:               gradientStroke,
            pointBorderColor:          gradientStroke,
            pointBackgroundColor:      gradientStroke,
            pointHoverBackgroundColor: gradientStroke,
            pointHoverBorderColor:     gradientStroke,
            backgroundColor:           gradientStroke,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:false,
                    callback: function(value, index, values) {
                        return '$' + value;}
                }
            }],
            xAxes: [{
                ticks: {
                    autoSkip: false,
                    maxRotation: 40,
                    minRotation: 40
                }
            }]
        }
    }
});
</script><br></td></tr>

</table>
</header>
</section>
</div>
</body>
</html>''' % (wal1_walletBal,wal1_USD,wal2_walletBal,wal2_USD,wal3_walletBal,wal3_USD,current_price,day_change,week_price,month_price,historic_price,days,prices)
u = unicode(contents, "utf-8" )

def main(): 
    browseLocal(u)

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='index.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import os.path
    strToFile(webpageText, filename)   

main()