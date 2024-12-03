from flask import Flask, request, jsonify
import pymysql
import pymysql.cursors

app = Flask(__name__)

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="abc",
    database="ISIS_DB"
)

cursor = mydb.cursor()
def populate_audio_library():
    audio_files = [
        ("1", "Song 1", "cartist 1", "meme", "chipichipi.mp3"),
        ("2", "Song 2", "cat thomas", "cartoon", "tom_scream.mp3"),
        ("3", "Song 3", "bg_myujik", "bg", "sample.mp3")
    ]
    sql = "INSERT INTO audio_library (id,audio_name, audio_artist, audio_genre, audio_path) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, audio_files)
    mydb.commit()
# def search_images(keyword):
#     sql = "SELECT * FROM uploaded_images WHERE image_name LIKE %s"
#     cursor.execute(sql, ('%' + keyword + '%',))
#     return cursor.fetchall()

# def search_audio(keyword):
#     sql = "SELECT * FROM audio_library WHERE audio_name LIKE %s OR audio_genre LIKE %s"
#     cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
#     return cursor.fetchall()

# @app.route('/search', methods=['GET'])
# def search_media():
#     keyword = request.args.get('keyword')
#     search_results = search_images(keyword)
#     search_results = search_audio(keyword)
#     return jsonify(search_results)

populate_audio_library()
if __name__ == '__main__':
    app.run(debug=True)
