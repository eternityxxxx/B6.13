import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class AlreadyExists(Exception):
    pass

class Album(Base):
    """
        Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
        Устанавливает соединение к базе данных и возвращает объект сессии
    """

    engine = sa.create_engine(DB_PATH)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
        Ищет альбомы по заданному исполинтелю и возвращает список альбомов
    """

    session = data_connect()
    albums = session.query(Album).filter(Album.artist == artist).all()

    return albums

def save(year, artist, genre, album):
    """
        Валидирует полученные данные для создания нового альбма, и если такого
        альбома еще нет, добавляет альбом в БД
    """

    assert isinstance(year, int), "Неверно введен год"
    assert isinstance(artist, str), "Неверно введен артист"
    assert isinstance(genre, str), "Неверно введен жанр"
    assert isinstance(album, str), "Неверно введен альбом"

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists("Такой альбом уже создан")

    new_album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )

    session.add(new_album)
    session.commit()
