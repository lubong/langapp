import os, json
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from werkzeug.utils import secure_filename
import whisper
from whisper.utils import get_writer
import jieba
import jieba.posseg as pseg
import sqlite3
import json
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
from helpers import *

model = whisper.load_model("tiny")
app = Flask(__name__)
INPUT_DIR = "./static/"
LESSON_ROOT = "./lessons"
DB = "dictionary.db"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/lessons_text")
def lessons_text():
    return render_template('lessons_text.html')

@app.route("/audio_lessons", methods=["GET", "POST"])
def audio_lessons():
    if request.method == "POST":
        audio = request.files['audio']
        if not audio:
            abort(400)
        filename = secure_filename(audio.filename)
        filepath = INPUT_DIR + filename
        audio.save(filepath)
        result = model.transcribe(filepath, language = 'zh', fp16=False)
        json_writer = get_writer("json", INPUT_DIR)
        json_writer(result, filepath)
        return redirect(url_for('audio_lessons', filename = filename))
    
    filename = request.args.get('filename', None)
    if not filename:
        return render_template('audiolessons.html')
    try:
        rootname = filename.split(".", 1)[0]
        pathJSON = INPUT_DIR + rootname + '.json'
        with open(pathJSON) as f:
            raw_data = json.load(f)
            f.close
    except FileNotFoundError:
        return render_template('audiolessons.html')
    src = INPUT_DIR + filename

    data = { "data" : [] }
    for i in raw_data['segments']:
        item = {}
        item['id'] = i['id']
        item['start'] = i['start']
        item['end'] = i['end']
        item['text'] = jieba.lcut(i['text'], cut_all=False)
        data['data'].append(item)
    return render_template('audiolessons.html', data=data, src=src)

@app.route("/video_lessons")
def video_lessons():
    return render_template('videolessons.html')


@app.route("/api/lessons/text/")
def get_all_lesson_texts():
    path = LESSON_ROOT + "/text"
    dir_list = os.listdir(path)
    response = jsonify(dir_list)
    return response, 200

@app.route("/api/lessons/text/<filename>")
def get_single_lesson_texts(filename):
    file_name = filename.split(".")[0]
    text_path = LESSON_ROOT + "/text/" + filename
    json_path = LESSON_ROOT + "/text_json/" + file_name + ".json"
    os_m_time = os.path.getmtime(text_path)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    json_file_exists = cursor.execute("SELECT * FROM file_manager WHERE file_name = ? AND file_type = ?", (file_name, ".json")).fetchall()
    if json_file_exists: #check if json exists -> return res if no modifications
        json_file = json_file_exists[0]
        if os_m_time <= json_file['modification_time']:
            print("re_used json")
            with open(json_file['file_path']) as f:
                data = json.load(f)
            con.close()
            response = jsonify(data)
            return response, 200
    # use jieba for modification case or not inside file case
    print("using jieba")
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
        seg_words = pseg.lcut(text)
        data = []
        for w in seg_words:
            word = {}
            word['word'] = w.word
            word['pos'] = w.flag
            data.append(word)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file)
    os_m_time = os.path.getmtime(json_path)
    cursor.execute('''INSERT INTO file_manager (file_name, file_type, file_path, modification_time) 
                   VALUES (:name, :type, :path, :mtime) ON CONFLICT(file_name, file_type) DO UPDATE SET modification_time = :mtime ;
                    ''', {"name": file_name, "type": ".json", "path": json_path, "mtime": os_m_time})
    con.commit()
    response = jsonify(data) #returns array of dictionaries {word, pos}
    return response, 200


@app.route("/api/dict/<word>")
def apiDict(word):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor = cursor.execute("SELECT * FROM dict_data WHERE simplified = :word OR traditional = :word;", {"word": word}).fetchall()
    con.close()
    data = []
    for i in cursor:
        entry = {}
        entry['traditional'] = i['traditional']
        entry['simplified'] = i['simplified']
        entry['pinyin'] = i['pinyin']
        entry['english'] = i['english']
        data.append(entry)
    if not data:
        response = jsonify("no definition found")
        response.status_code = 200
        return response
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route("/api/parse/text/")
def apiTextParser():
    url = request.args.get('url', None)
    print(url)
    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'html.parser')
    texts = recursion(soup.body)
    arr = []
    for t in texts:
        arr.append(t.text)
    return arr

@app.route("/api/knowledge_level", methods=['POST'])
def apiGetKnowledgeLevel():
    batch = request.get_json()
    if not batch:
        return jsonify(0), 300

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()
    batch_levels = []
    for word in batch['batch']:
        word_id_exists = cursor.execute("SELECT word_id FROM dict_data WHERE simplified = ? LIMIT 1", (word['word'],)).fetchall()
        if word_id_exists:
            batch_levels.append(word_id_exists[0]['word_id'])
        else:
            batch_levels.append(0)
    for index, level in enumerate(batch_levels):
        if level > 0:
            check_level = cursor.execute("SELECT level FROM knowledge_level WHERE word_id = ?;", (level,)).fetchall()
            if check_level:
                batch_levels[index] = check_level[0]['level']
            else:
                batch_levels[index] = 0
    con.close()
    response = jsonify(batch_levels)
    response.status_code = 200
    return response

# @app.route("/api/knowledge_level", methods=['GET'])
# def apiGetKnowledgeLevel():
#     word = request.args.get('word', None)
#     if not word:
#         return jsonify(0), 300

#     con = sqlite3.connect(DB)
#     con.row_factory = sqlite3.Row
#     con.execute("PRAGMA foreign_keys = ON")
#     cursor = con.cursor()
#     word_in_dict = cursor.execute("SELECT simplified FROM dict_data WHERE simplified = ?;", (word,)).fetchall()
#     if not word_in_dict: #not inside dict_data
#         con.close()
#         return jsonify(0), 200
#     word_in_level = cursor.execute("SELECT level FROM knowledge_level AS KL JOIN dict_data AS DD ON KL.word_id = DD.word_id WHERE simplified = ?;", (word,)).fetchall()
#     con.close()
#     if not word_in_level: # not inside level
#         return jsonify(0), 200
#     response = jsonify(word_in_level[0]['level'])
#     response.status_code = 200
#     return response

@app.route("/api/knowledge_level", methods=['PUT'])
def apiPutKnowledgeLevel():
    jsonData = request.get_json()
    
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()
    get_id = cursor.execute("SELECT word_id FROM dict_data WHERE simplified = :word", {'word' : jsonData['word']}).fetchall()[0]['word_id']
    cursor.execute('''INSERT INTO knowledge_level(word_id, level) VALUES(:word_id, :level)
                                    ON CONFLICT(word_id) DO UPDATE SET level= :level
    ;''', {'word_id': get_id , 'level': jsonData['level']})
    con.commit()
    con.close()
    return jsonify("ok"), 200