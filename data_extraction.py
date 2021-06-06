def load_data():
    myDataFrame = pd.DataFrame()
    #Live Extraction from data.gov.sg
    #urldata = ['https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards-2021-06-04T02-52-32Z.csv']
    #, 'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2015-to-dec-2016-2019-06-17T09-03-16Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-mar-2012-to-dec-2014-2019-06-17T09-04-34Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-2000-feb-2012-2019-06-28T10-14-13Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-1990-1999-2021-05-25T02-49-29Z.csv']
    #for links in urldata:
    #    req = Request(links)
    #    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
    #    content = urlopen(req)
    #    df = pd.read_csv(content)
    #    myDataFrame = myDataFrame.append(df)
    #    myDataFrame.sort_values(by = ['month'],ascending = False)
    #Saved in Github
    df = pd.read_csv('resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
    myDataFrame = myDataFrame.append(df)
    myDataFrame.sort_values(by = ['month'],ascending = False)
    return myDataFrame
df = load_data()