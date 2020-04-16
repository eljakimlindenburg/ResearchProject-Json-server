import random
from typing import List
from review_model import ReviewModel


class BookModel:
    def __init__(self, _id: str,
                 title: str = "",
                 author: str = "",
                 desc: str = "",
                 average_rating: float = 0.0,
                 image_src: str = "",
                 price: float = 0.01) -> None:
        self._id = _id
        self.title = title
        self.author = author
        self.desc = desc
        self.price = price
        self.average_rating = average_rating
        self.image_src = image_src
        self._reviews: List[ReviewModel] = []

    def get_id(self) -> str:
        return self._id

    def get_reviews(self) -> List[ReviewModel]:
        return self._reviews

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        self._author = value

    @property
    def desc(self) -> str:
        return self._desc

    @desc.setter
    def desc(self, value: str) -> None:
        self._desc = value

    @property
    def average_rating(self) -> float:
        return self._average_rating

    @average_rating.setter
    def average_rating(self, value: int) -> None:
        self._average_rating = value

    @property
    def image_src(self) -> str:
        return self._image_src

    @image_src.setter
    def image_src(self, value: str) -> None:
        self._image_src = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = value
