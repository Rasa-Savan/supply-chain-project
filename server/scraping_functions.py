### Import the libraries needed to perform the webscraping.
import time
import urllib.request
from bs4 import BeautifulSoup
from file_handling import write_domain_to_json, write_comments_to_json, write_comments_to_csv

### Defining the url, to be scraped 
base_url = "https://www.trustpilot.com"
domain_url = ""

### Creating an empty list to fetch data
list_domain_url = []
list_items = []

### Defining variable
time_delay = 5 #time delay between scraping each url
comment_min = 100
comment_max = 150
domain_step = 3


def main_scraping(r_url):
    ### Finding total number of pages of URL
    pages = get_soup_data(r_url).find("nav", class_ = "pagination_pagination___F1qS").findAll("a")[-2].text
    print("Total number of page: " + pages)

    ### Loop each page of URL and store each domain item in the list
    # list_items = []
    global list_items
    for page in range(int(pages)):
        url_page = r_url if page == 0 else r_url + "?page=" + str(page + 1)
        print("Page: " + url_page + " >>>>>> DONE")
        soup_data = get_soup_data(url_page)
        items_in_page = get_item_list_in_page(soup_data)
        list_items.extend(items_in_page)


    ### Getting all data of each domain and store in dictionary document
    print("\n\nPleae wait while system is running...")
    raw_data = get_item_info_by_page(list_items)
    print("Web scraping execution is 'COMPLETED'")

    write_domain_to_json(raw_data)
    return raw_data


### Function of getting soup data base on URL
def get_soup_data(r_url):
    page = urllib.request.urlopen(r_url)
    soup_data = BeautifulSoup(page, "html.parser")
    return soup_data


### Getting domain list in first page
def get_item_list_in_page(r_soup_data):
    list_items = r_soup_data.find_all("div", class_ = "paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2")
    return list_items


### Getting information of each domain
def get_item_info_by_page(r_list_items):
    raw_data = []
    for i in range(len(r_list_items)):
        domain_name = r_list_items[i].find("p").text.replace("'","")
        has_address = r_list_items[i].find("div", { "class": "styles_metadataRow__pgwwW"})

        ### Getting Domain name and URL
        sub_domain_url = r_list_items[i].find("a")["href"]

        ### Getting TrustScore and Reviewer number, both will be null if not applicable
        trust_scores = ""
        reviewers = ""
        overal_rate = ""
        website = ""
        star = {"star_5": "", "star_4": "", "star_3": "", "star_2": "", "star_1": ""}
        
        is_scores_reviewers = r_list_items[i].find("div", class_= "styles_rating__pY5Pk")
        if is_scores_reviewers is not None:
            scores_reviewers = r_list_items[i].find("div", class_= "styles_rating__pY5Pk").find("p").text.split("|")
            trust_scores = scores_reviewers[0].split(" ")[1]
            reviewers = scores_reviewers[1].split(" ")[0]

            global domain_url, list_domain_url
            domain_url= base_url + sub_domain_url
            list_domain_url.append(domain_url)
            soup_domain_data = get_soup_data(domain_url)
            overal_rate = soup_domain_data.find("div", id = "business-unit-title").findAll("span")[2].text.split("\xa0")[-1]
            website = soup_domain_data.find("div", class_ = "styles_summary__gEFdQ").find("a")["href"]
            
            ### Getting category classification rate
            categ_len = len(soup_domain_data.findAll("label", class_ = "styles_row__wvn4i"))
            for i in range(categ_len):
                categ = soup_domain_data.findAll("label", class_ = "styles_row__wvn4i")[i].findAll("p")[0].text
                rate = soup_domain_data.findAll("label", class_ = "styles_row__wvn4i")[i].findAll("p")[1].text
                # display(categ + " = " + rate)
                star["star_" + str(categ_len - i)] = rate
        ### storing data under various column heads        
        data = {
            "domain_name": domain_name,
            "trust_scores": trust_scores,
            "reviewers": reviewers,
            "domain_address": has_address.text.replace("\xa0", " ") if has_address is not None else "",
            "overal_rate": overal_rate,
            "star_5": star["star_5"],
            "star_4": star["star_4"],
            "star_3": star["star_3"],
            "star_2": star["star_2"],
            "star_1": star["star_1"],
            "domain_url": base_url + sub_domain_url,
            "website": website
        }

        raw_data.append(data)
    return raw_data



###======= Getting data of each comment which will have over 10,000 reviewer of a company
def get_comment_of_each_domain(r_list_domain_url):

    list_all_comments = []
    for r_domain_url in r_list_domain_url:
        list_all_comments_per_domain = []
        ### Checking total pages
        is_last_page = get_soup_data(r_domain_url).find("a", attrs = {"name":"pagination-button-last"})
        domain_pages = "1" if is_last_page is None else is_last_page.text
        print("\n\nTotal page: " + domain_pages)

        ### Looping each page for getting each comment and reply data
        for page in range(int(domain_pages)):
            # ### Getting 10 pages for sample
            # if page == 10:
            #     break
                
            list_comment_per_page = []
            sub_page_domain_url = r_domain_url if page == 0 else r_domain_url + "?page=" + str(page + 1)
            print("page domain_url: " + sub_page_domain_url + " >>>>>> DONE")
            # get_domain_review_by_page(get_soup_data(sub_page_domain_url), raw_data_reviewer_comment)
            soup_domain_data = get_soup_data(sub_page_domain_url)
            domain_name = soup_domain_data.find("div", id = "business-unit-title").findAll("span")[0].text.split("\xa0")[0]
            
            # Review description
            reviews_desc = soup_domain_data.findAll("div", class_ = "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ")
            for i in range(len(reviews_desc)):
                reviewer_name = reviews_desc[i].find("span", attrs = {"data-consumer-name-typography": "true"}).text
                has_reviewer_country = reviews_desc[i].find("div", attrs = {"data-consumer-country-typography": "true"})
                reviewer_rate = reviews_desc[i].find("section").find("div", class_ = "styles_reviewHeader__iU9Px")["data-service-review-rating"]
                reviewer_date = reviews_desc[i].find("section").find("time")["datetime"]
                reviewer_title = reviews_desc[i].find("section").find("h2", attrs = {"data-service-review-title-typography": "true"}).text
                has_reviewer_message = reviews_desc[i].find("section").find("p", attrs = {"data-service-review-text-typography": "true"})
                # reviewer_exp_date = reviews_desc[i].find("section").find("p", attrs = {"data-service-review-date-of-experience-typography": "true"}).text
                has_reviewer_exp_date = reviews_desc[i].find("section").find("p", attrs = {"data-service-review-date-of-experience-typography": "true"})
                reviewer_exp_date = has_reviewer_exp_date.text if has_reviewer_exp_date is not None else "",
                
                ### Reply to reviewer        
                has_reply_comment = reviews_desc[i].find("div", class_ = "styles_content__Hl2Mi")
                
                ### Get all comments information of each domain
                raw_data_reviewer_comment = {
                    "domain_name": domain_name,
                    "reviewer_name": reviewer_name,
                    "reviewer_country": has_reviewer_country.text if has_reviewer_country is not None else "",
                    "reviewer_rate": reviewer_rate,
                    "reviewer_date": reviewer_date,
                    "reviewer_title": reviewer_title,
                    "reviewer_message": has_reviewer_message.text if has_reviewer_message is not None else "",
                    "reviewer_exp_date": reviewer_exp_date[0],
                    "reply_title": has_reply_comment.find("p", attrs = {"data-service-review-business-reply-title-typography": "true"}).text if has_reply_comment is not None else "",
                    "reply_message": has_reply_comment.find("p", attrs = {"data-service-review-business-reply-text-typography": "true"}).text if has_reply_comment is not None else "",
                    "reply_date": has_reply_comment.find("time")["datetime"] if has_reply_comment is not None else ""
                }

                list_comment_per_page.append(raw_data_reviewer_comment)
            list_all_comments_per_domain.extend(list_comment_per_page)

            if time_delay != 0: time.sleep(time_delay)

        list_all_comments.extend(list_all_comments_per_domain)
    
    write_comments_to_json(list_all_comments)
    write_comments_to_csv(list_all_comments)

    return list_all_comments


### Getting domain URL which a company with more than 10000 reviews
def check_reviewer_in_each_domain(r_raw_data_domains):
    list_domain_url = []
    
    print("\n\n")
    for i in range(len(r_raw_data_domains)):
        if r_raw_data_domains[i]["reviewers"] != "" and comment_min < int(r_raw_data_domains[i]["reviewers"].replace(",", "")) < comment_max:
            print(r_raw_data_domains[i]["domain_url"])
            list_domain_url.append(r_raw_data_domains[i]["domain_url"])
            if len(list_domain_url) == domain_step: break
    
    return get_comment_of_each_domain(list_domain_url)
