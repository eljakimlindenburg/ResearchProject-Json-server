import requests
import traceback
import jsonpickle  # type: ignore
from book_model import BookModel
from review_model import ReviewModel
from bs4 import BeautifulSoup, Tag  # type: ignore
from typing import List, Dict
from datetime import date

months_nl: Dict[str, int] = {
    "januari": 1,
    "februari": 2,
    "maart": 3,
    "april": 4,
    "mei": 5,
    "juni": 6,
    "juli": 7,
    "augustus": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "december": 12,
}


def book_page_spider(start_page: int, end_page: int) -> None:
    for i in range(start_page, end_page + 1):
        url: str = "https://www.bol.com/nl/l/boeken/N/8299/?page=" + str(i)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        books: List[BookModel] = []
        for element in soup.find_all("li", {"class": "js_item_root"}):
            element_tag: Tag = element
            link: Tag = element_tag.find("a")
            href = "https://www.bol.com" + link.get("href")
            try:
                books.append(deserialize_page_into_book_model(href))
            except Exception as err:
                print("Could not deserialize link on page {}:\n{}".format(i, href))
                traceback.print_exc()
        books_json: str = str(jsonpickle.encode(books, unpicklable=False, indent=2))
        file = open("json_pages/page{}.json".format(i), "w+")
        file.write(books_json)
        file.close()


def deserialize_page_into_book_model(url: str) -> BookModel:
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    book_page_body_tag: Tag = soup.find("body")
    book_page_h1_tag: Tag = book_page_body_tag.find("h1")
    book_page_h1_title_tag: Tag = book_page_h1_tag.find("span", {"data-test": "title"})
    book_page_author_tag: Tag = book_page_body_tag.find("a", {"data-role": "AUTHOR"})
    book_reviews_tag: Tag = book_page_body_tag.find("div", {"class": "reviews"})
    book_page_desc_tag = book_page_body_tag.find("div", {"data-test": "description", "itemprop": "description"})
    if book_page_desc_tag is None:
        book_page_desc_tag = book_page_body_tag.find("p", {"data-test": "text-short"})
    book_page_img_src_tag: Tag = book_page_body_tag.find("img", {"class": "js_product_thumb"})
    if book_page_img_src_tag is None:
        book_page_img_src_tag = book_page_body_tag.find("img", {"class": "js_product_img"})

    url_sections = url.split("/")
    book_id: str = url_sections[len(url_sections) - 2]
    book_title: str = str(book_page_h1_title_tag.text)
    book_desc: str = str(book_page_desc_tag.text)
    book_author: str
    if book_page_author_tag is None:
        book_author = "Anonymous"
    else:
        book_author = str(book_page_author_tag.text)
    book_average_rating: float
    book_img_src: str = str(book_page_img_src_tag.get("src"))
    book_reviews: List[ReviewModel] = []

    if book_reviews_tag is None:
        book_average_rating = 0
    else:
        book_page_average_rating_tag: Tag = book_reviews_tag.find("div", {"class", "rating-horizontal__average-score"})
        book_average_rating = float(str(book_page_average_rating_tag.text))
        for review in book_reviews_tag.find_all("li", {"class": "review"}):
            review_tag: Tag = review
            review_title_tag: Tag = review_tag.find("strong", {"class": "review__title"})
            review_author_name_tag: Tag = review_tag.find("li", {"data-test": "review-author-name"})
            review_timestamp_tag: Tag = review_tag.find("li", {"data-test": "review-author-date"})
            review_rating_tag: Tag = review_tag.find("input")
            review_comment_tag: Tag = review_tag.find("p", {"data-test": "review-body"})

            review_timestamp_sections = str(review_timestamp_tag.text).split(" ")

            review_id: str = str(review_tag.get("id")).split("-")[1]
            review_title: str = str(review_title_tag.text)
            review_author_name: str
            if review_author_name_tag is None:
                review_author_name = "Anonymous"
            else:
                review_author_name = str(review_author_name_tag.text)
            review_timestamp_month = months_nl.get(review_timestamp_sections[1])
            if review_timestamp_month is None:
                review_timestamp_month = 1
            review_timestamp: date = date(int(review_timestamp_sections[2]),
                                          review_timestamp_month,
                                          int(review_timestamp_sections[0]))
            review_rating: int = int(review_rating_tag.get("value"))
            review_comment: str = str(review_comment_tag.text)

            new_review: ReviewModel = ReviewModel(_id=review_id,
                                                  author_name=review_author_name,
                                                  title=review_title,
                                                  timestamp=review_timestamp,
                                                  rating=review_rating,
                                                  comment=review_comment)
            book_reviews.append(new_review)

    book = BookModel(book_id,
                     title=book_title,
                     author=book_author,
                     desc=book_desc,
                     average_rating=book_average_rating,
                     image_src=book_img_src)
    for review in book_reviews:
        book.get_reviews().append(review)
    return book


book_page_spider(1, 20)
