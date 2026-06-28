from dao.album_dao import AlbumDAO
from models.album import Album

class AlbumService:
    def __init__(self, album_dao=None):
        self.album_dao = album_dao or AlbumDAO()

    def get_all_albums(self):
        return self.album_dao.find_all()

    def get_album_by_id(self, album_id):
        return self.album_dao.find_by_id(album_id)

    def search_albums(self, keyword, search_type="title"):
        albums = self.album_dao.find_all()
        result = []
        keyword = keyword.lower()
        
        for album in albums:
            if search_type == "title" and keyword in album.title.lower():
                result.append(album)
            elif search_type == "artist" and keyword in album.artist.lower():
                result.append(album)
            elif search_type == "genre" and keyword in album.genre.lower():
                result.append(album)
        return result

    def add_album(self, title, artist, genre, price, stock):
        if price < 0 or stock < 0:
            raise ValueError("Price and Stock must be non-negative.")
        
        album = Album(title=title, artist=artist, genre=genre, price=price, stock=stock)
        return self.album_dao.insert(album)

    def update_album(self, album_id, title=None, artist=None, genre=None, price=None, stock=None):
        album = self.album_dao.find_by_id(album_id)
        if not album:
            raise ValueError(f"Album with ID {album_id} not found.")

        if title is not None:
            album.title = title
        if artist is not None:
            album.artist = artist
        if genre is not None:
            album.genre = genre
        if price is not None:
            if price < 0:
                raise ValueError("Price must be non-negative.")
            album.price = price
        if stock is not None:
            if stock < 0:
                raise ValueError("Stock must be non-negative.")
            album.stock = stock

        self.album_dao.update(album)
        return album

    def delete_album(self, album_id):
        if not self.album_dao.find_by_id(album_id):
            raise ValueError(f"Album with ID {album_id} not found.")
        return self.album_dao.delete(album_id)
