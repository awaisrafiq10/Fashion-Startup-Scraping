import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Fashion Startup')
root.geometry("500x500")
root.minsize(width=800, height=450)
root.maxsize(width=800, height=450)


# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "put your google custom search api key"
# get your Search Engine ID on your Google CSE(Custom Search Engine) control panel
SEARCH_ENGINE_ID = "put your google custom search engine id"

keywords = ["FASHION", "CLOTHING", "APPAREL", "FASHION STARTUP", "APPAREL STARTUP", "CLOTHING STARTUP", "RENTAL FASHION", 
"CUSTOM CLOTHING", "SLOW FASHION", "ETHICAL FASHION", "SMART FABRICS", "WEBSITE", "WEBPAGE", "PERSONAL WEBSITE",]

exclude_keywords = ["Why", "What", "How", "Where", "When", "Who", "Which", "Whose", "Can", "May", "Should", "Will", "Would", "Could", "Might", "Is", "Are", "Do", "Did", "Does", "Have", "Has", "Was", "Were", "Am", "Been", "Be", "Isn't", "Aren't", "Don't", "Didn't", "Doesn't", "Haven't", "Hasn't", "Wasn't", "Weren't", "Amn't", "Been", "Being",
"NEWS", "HEADLINES", "BREAKING NEWS", "UPDATES", "CURRENT EVENTS", "JOURNALISM", "REPORT", "STORY", "COVERAGE", "DICTIONARY", "WIKTIONARY"
"ARTICLE", "ESSAY", "PIECE", "WRITE-UP", "REPORT", "FEATURE", "COLUMN", "REVIEW",
"BEST", "TOP", "EXCELLENT", "SUPERIOR", "OUTSTANDING", "EXCEPTIONAL", "TOP-RATED", "FIRST-CLASS", "FIRST-RATE", "PREMIUM", "QUALITY", "HIGH-QUALITY",
"TOP", "BEST", "LEADING", "FOREMOST", "PREMIER", "HIGHEST", "SUPERIOR", "OUTSTANDING", "EXCEPTIONAL", "ELITE", "NUMBER ONE", "FIRST-CLASS", "FIRST-RATE",
"BLOG", "ONLINE JOURNAL", "WEB LOG", "DIGITAL DIARY", "POST", "ENTRY", "TV", "SHOW", "SERIES" "WEEK", "DAY", "YEAR",
"FACEBOOK", "TWITTER", "INSTAGRAM", "PINTEREST", "LINKEDIN", "YOUTUBE", "TIKTOK", "SNAPCHAT", "AMAZON", "EBAY", "ALIBABA", "WALMART", "TARGET", "BEST BUY", "SHOPIFY", "WISH", "ETSY", "POSHMARK", "ZOOM", "TELEGRAM", "WECHAT", "WHATSAPP", "MESSENGER", "DISCORD", "SKYPE", "SIGNAL", "LINE", "KAKAO", "VIBER", "WEIBO", "DOUYIN", "XIAOHONGSHU", "ENCYCLOPEDIA", "WIKIPEDIA"
"SCHOOL", "UNIVERSITY", "COLLEGE", "INSTITUTE" "SCHOLARSHIPS"
"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
def scraping():
    query = str(searchvalue.get())                   # the search query you want
    page = int(pagevalue.get())                            # using the first page
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

    # make the API request
    data = requests.get(url).json()

    # get the result items
    search_items = data.get("items")                # OR    search_items = data["items"]
    # print(search_items)

    content = {"TITLE":[], "URL":[]}

    # iterate over 10 results found
    for i, search_item in enumerate(search_items, start=1):
        # try:
        #     long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        # except KeyError:
        #     long_description = "N/A"
        # get the page title
        title = search_item.get("title")
        # # page snippet
        # snippet = search_item.get("snippet")
        # # alternatively, you can get the HTML snippet (bolded keywords)
        # html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        link = search_item.get("link")
        print("Title:", title)
        if any(word in title.upper() for word in keywords) and (not any(word in title.upper() for word in exclude_keywords)):
            # print the results
            # print("="*10, f"Result #{i+start-1}", "="*10)
            # print("Title:", title)
            # print("Description:", snippet)
            # print("Long description:", long_description)
            # print("URL:", link, "\n")

            parts = urlparse(link)
            domain_url = str(parts.scheme) +"://"+ str(parts.netloc)
            req = requests.get(domain_url)
            soup = BeautifulSoup(req.text, "html.parser")
            # print(soup.title)
            title_tag = soup.find("title")
            if title_tag:
                domain_title = title_tag.string
            else:
                domain_title = "Title not found"
            if any(word in title.upper() for word in keywords) and not any(word in domain_title.upper() for word in exclude_keywords):
                content["TITLE"].append(domain_title)
                content["URL"].append(domain_url)
        else:
            print("INVALID WEBSITE")

    df = pd.DataFrame(content)
    df_existing = pd.read_excel('file.xlsx')
    df1 = pd.concat([df_existing, df], ignore_index=True)
    df1.to_excel("file.xlsx", index=False)

    df2 = pd.read_excel('file.xlsx')
    df3 = df2.drop_duplicates()
    df4 = pd.DataFrame(df3)
    df4['URL'] = df4['URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
    df4.to_excel("file.xlsx", index=False)
    print("DONE")
    messagebox.showinfo("Completion", "Successfully Scraped Websites.")
    # messagebox.showwarning("showwarning", "Warning")
    # messagebox.showerror("showerror", "Error")

# Variable classes in tkinter
# BooleanVar(0,1), DoubleVar(0.0), IntVar(123), StringVar(abcd)
searchvalue = StringVar()
pagevalue = IntVar()
label = Label(root, text = "WELCOME TO FASHION STARTUP SCRAPING", font = ("Calibri", 27, "bold" ), bg = "red", fg = "white").place(x=60, y=30, width=700, height=50)
label = Label(root, text = "QUERY | SEARCH", font = ("Calibri", 25, "bold")).place(x=60, y=100, width=700, height=50)
searchentry = Entry(root, textvariable = searchvalue, font = ("Calibri", 20, "bold" )).place(x=60, y=155, width=700, height=50)
label = Label(root, text = "PAGE", font = ("Calibri", 25, "bold")).place(x=60, y=220, width=700, height=50)
pageentry = Entry(root, textvariable = pagevalue, font = ("Calibri", 20, "bold" )).place(x=60, y=275, width=700, height=50)
button = Button(root, text = "START SCRAPING", font = ("Calibri", 27, "bold"), relief=RAISED, command=scraping).place(x=60, y=350, width=700, height=50)

root.mainloop()