from dao.base_dao import BaseDAO
from models.album import Album

class AlbumDAO(BaseDAO):
    def __init__(self, file_path="data/albums.json"):
        super().__init__(file_path)

    def find_all(self):
        data = self._read_all()
        return [Album.from_dict(item) for item in data]

    def find_by_id(self, album_id):
        albums = self.find_all()
        for album in albums:
            if album.id == album_id:
                return album
        return None

    def insert(self, album):
        albums = self.find_all()
        max_id = max([a.id for a in albums if a.id is not None], default=0)
        album.id = max_id + 1
        
        albums.append(album)
        self._write_all([a.to_dict() for a in albums])
        return album

    def update(self, album):
        albums = self.find_all()
        for idx, a in enumerate(albums):
            if a.id == album.id:
                albums[idx] = album
                self._write_all([x.to_dict() for x in albums])
                return True
        return False

    def delete(self, album_id):
        albums = self.find_all()
        filtered_albums = [a for a in albums if a.id != album_id]
        if len(filtered_albums) < len(albums):
            self._write_all([x.to_dict() for x in filtered_albums])
            return True
        return False
