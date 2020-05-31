from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

@route("/albums/<artist>")
def search(artist):
    """
        Ищет все альбомы заданного исполнителя, возвращает их список и кол-во
    """

    albums_list = album.find(artist)

    if not albums_list:
        result = HTTPError(400, "Альбомов {} не найдено".format(artist))
    else:
        albums_name = [album.album for album in albums_list]
        albums_count = len(albums_name)

        result = "Количество альбомов {}: {}".format(artist, albums_count)
        result += "<br>"
        for name in albums_name:
            result += name
            result += "<br>"

    return result

@route("/albums", method="POST")
def create_album():
    """
        Получает переданные данные и проверяет возможно ли занести альбом в БД
    """

    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        result = "Альбом успешно сохранен"

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
