import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        gCode = request.form['code']
        h,l,o,b,a,rRecommend = quote(gCode)
        nTitle, nUrl, nZhTw = meta_ZhTw(gCode)
        if request.values['search']=='搜尋':
            return render_template("index2.html",high=h, low=l, open=o, zh_tw=nZhTw, code=gCode,
            bids1=b[0], bids2=b[1], bids3=b[2], bids4=b[3], bids5=b[4],
            asks1=a[0], asks2=a[1], asks3=a[2], asks4=a[3], asks5=a[4], recommend=rRecommend,
            news_title1=nTitle[0], news_url1=nUrl[0], news_title2=nTitle[1], news_url2=nUrl[1], news_title3=nTitle[2], news_url3=nUrl[2],
            news_title4=nTitle[3], news_url4=nUrl[3], news_title5=nTitle[4], news_url5=nUrl[4])
    return render_template("index1.html")


# 新聞
def news(keyword):
    input_file = open ('C:\\Users\\User\\Desktop\\0056\\news.json', encoding="utf-8")
    resJson = json.load(input_file)

    title_list = []
    url_list = []

    for resNews in resJson['result']:
        title_list.append(resNews["title"])
        url_list.append(resNews['url'])
    return title_list, url_list
    

# 集保護股權分散
def rawContent(symbolId,price):
    input_file = open ('C:\\Users\\User\\Desktop\\0056\\0056_FCNT000022.json', encoding="utf-8")
    resJson = json.load(input_file)
    
    list_month =[]
    list = []
    sum = 0
    scale_text =""
    for resRaw in resJson["data"]["content"]["rawContent"]:
        for resData in resRaw ["data"]:
            range_start = resData["range_start"]
            proportion = resData["proportion"]
            list_month.append(range_start)
            list_month.append(proportion)
    
    if price >= 50:
        for i in range(23,31,2):
            list.append(list_month[i])
        for total in list:
            sum += total
        scale_text = text(sum)
    else:
        small = list_month[29]
        scale_text = text(small)
    return scale_text

def text(scale):
    text =""
    if scale < 40: text = "散戶人數多，致主力不易炒作，可獲利機會較低，故不建議持有"
    elif scale < 80: text = "散戶持股比例未太高，主力可能透過吸取籌碼增加持股比例，未來炒作機率大，可以買進等待主力拉抬"
    else :text = "大戶持有股數過多，較無炒作空間，若非熱門股 ，不建議持有"
    return text


# meta抓取中文名字當keyword
def meta_ZhTw(symbolId):
    input_file = open ('C:\\Users\\User\\Desktop\\0056\\0056_meta.json', encoding="utf-8")
    resJson = json.load(input_file)
    resMeta = resJson["data"]["meta"]
    nameZhTw = '"' + resMeta["nameZhTw"] + '"'
    meta_title,meta_url = news(nameZhTw)
    return meta_title,meta_url,resMeta["nameZhTw"]


# meta抓取參考金額金額
def meta(symbolId):
    input_file = open ('C:\\Users\\User\\Desktop\\0056\\0056_meta.json', encoding="utf-8")
    resJson = json.load(input_file)
    resMeta = resJson["data"]["meta"]
    priceReference = float(resMeta["priceReference"])
    meta_recommend = rawContent(symbolId,priceReference)
    return meta_recommend


# quote
def quote(symbolId):
    input_file = open ('C:\\Users\\User\\Desktop\\0056\\0056_quote.json', encoding="utf-8")
    resJson = json.load(input_file)
    resQuote = resJson["data"]["quote"]

    bids_list = []
    asks_list = []

    priceHigh = str(resQuote["priceHigh"]["price"])
    priceLow = str(resQuote["priceLow"]["price"])
    priceOpen = str(resQuote["priceOpen"]["price"])
    for bestBids in resQuote["order"]["bestBids"]:
        bPrice = bestBids["price"]
        bUnit = bestBids["unit"]
        priceBids = "金額： " + str(bPrice) + " 張數： " + str(bUnit)
        bids_list.append(priceBids)
    for bestAsks in resQuote["order"]["bestAsks"]:
        aPrice = bestAsks["price"]
        aUnit = bestAsks["unit"]
        priceAsks = "金額： " + str(aPrice) + " 張數： " + str(aUnit)
        asks_list.append(priceAsks)
    get_recommend = meta(symbolId)
    return priceHigh, priceLow, priceOpen, bids_list, asks_list, get_recommend

if __name__ == '__main__':
    app.run(port = 5000)
    