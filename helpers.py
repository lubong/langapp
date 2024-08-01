from bs4.element import Comment
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
