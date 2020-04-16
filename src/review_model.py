from datetime import date


class ReviewModel:
    def __init__(self, _id: str,
                 author_name: str = "",
                 title: str = "",
                 timestamp: date = date.today(),
                 rating: int = 0,
                 comment: str = "") -> None:
        self._id = _id
        self.author_name = author_name
        self.title = title
        self.timestamp = timestamp
        self.rating = rating
        self.comment = comment

    def get_id(self) -> str:
        return self._id

    @property
    def author_name(self) -> str:
        return self._author_name

    @author_name.setter
    def author_name(self, value: str) -> None:
        self._author_name = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def timestamp(self) -> date:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: date) -> None:
        self._timestamp = value

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        self._rating = value

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value
