class Album:
    def __init__(self, title, artist, genre, price, stock, id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "price": self.price,
            "stock": self.stock,
            "genre": self.genre
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            artist=data.get("artist"),
            genre=data.get("genre"),
            price=data.get("price"),
            stock=data.get("stock")
        )
