# import jieba
# import jieba.posseg as pseg

from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import re

def recursion(soup):
    if soup.name in ['style', 'script', 'head', 'title', 'meta','footer','a']:
        return None
    if isinstance(soup, Comment):
        return None
    if soup.has_attr('class'):
        # check if the class is nav type
        class_string = ' '.join(t for t in soup['class'])
        is_nav = re.search(r"nav", class_string)
        if is_nav:
            return None
    if soup.name in ['h1','h2','h3','h4','h5','h6','p']:
        return [soup]
    else:
        array = []
        for s in soup.find_all(recursive=False):
            result = recursion(s)
            if result:
                array = array + result
        return array

html_content = '''
<body> 
<div class="html-content">
    <h2 class="navbar"><strong>h2 navbar </strong> </h2>
    <h3 class="ok ok"><strong>h3 text to parse </strong> </h3>
    <p class="ok">ptag text part 1 <a href="https://mcc.gse.harvard.edu/s/mcc_the_talk_final.pdf" target="_blank"><em>Ptag text part2</p>
</div>
<div class="navbar">
    <h2> h2 do not parse </h2>
</div>
</body>
'''
url = "https://www.xonecole.com/questions-related-to-childhood/if-you-could-change-anything-about-your-childhood-what-would-it-be"
req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
html_content = urlopen(req).read()
soup = BeautifulSoup(html_content, 'html.parser')
texts = recursion(soup.body)
for t in texts:
    print(t.text)
# texts = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])
# print(texts)
# for t in texts:
#     if t.has_attr('class'):
#         class_string = ' '.join(t for t in t['class'])
#         x = re.search(r"nav", class_string)
#         if x:
#             print(x.string)
#             continue
#     if t.parent.name in ['div']:
#         print('body')



# words = pseg.lcut("我来到北京清华大学。你是谁啊？")
# print(words)
# for w in words:
#     print(w)
#     print(w.word)
#     print(w.flag)
    # print('%s %s' % (w.word, w.flag))
# seg_list = jieba.lcut("我来到北京清华大学", cut_all=False)
# print(seg_list)




# import sqlite3

# DB = "dictionary.db"
# con = sqlite3.connect(DB)

# with open('cedict_ts.u8', encoding="utf8") as file:
#     text = file.read()
#     lines = text.split('\n')
#     dict_lines = list(lines)

# #define functions

#     def parse_line(line):
#         parsed = {}
#         if line == '':
#             dict_lines.remove(line)
#             return 0
#         line = line.rstrip('/')
#         line = line.split('/')
#         if len(line) <= 1:
#             return 0
#         english = line[1]
#         char_and_pinyin = line[0].split('[')
#         characters = char_and_pinyin[0]
#         characters = characters.split()
#         traditional = characters[0]
#         simplified = characters[1]
#         pinyin = char_and_pinyin[1]
#         pinyin = pinyin.rstrip()
#         pinyin = pinyin.rstrip("]")
#         parsed['traditional'] = traditional
#         parsed['simplified'] = simplified
#         parsed['pinyin'] = pinyin
#         parsed['english'] = english
#         list_of_dicts.append(parsed)


#     def main():

#         #make each line into a dictionary
#         print("Parsing dictionary . . .")
#         for line in dict_lines:
#                 parse_line(line)
        
#         return list_of_dicts


#         #If you want to save to a database as JSON objects, create a class Word in the Models file of your Django project:

#         # print("Saving to database (this may take a few minutes) . . .")
#         # for one_dict in list_of_dicts:
#         #     new_word = Word(traditional = one_dict["traditional"], simplified = one_dict["simplified"], english = one_dict["english"], pinyin = one_dict["pinyin"], hsk = one_dict["hsk"])
#         #     new_word.save()
#         print('Done!')

# list_of_dicts = []
# parsed_dict = main()

# print('dictionary parsed')
# for item in parsed_dict:
#      con.execute("INSERT INTO dict_data (traditional, simplified, pinyin, english) VALUES (?,?,?,?)", (item['traditional'], item['simplified'], item['pinyin'], item['english']))

# con.commit()
# print('dictionary committed')
# con.close()
