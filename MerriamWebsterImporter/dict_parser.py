import urllib2
import re
from BeautifulSoup import BeautifulSoup


class DictParser:

    @classmethod
    def parse(cls, input):
        html = cls._get_html(input)

        if not html:
            return []
        soup = BeautifulSoup(html)

        definitions = []
        try:
            entry = soup.find('div', {'class': 'entry', 'id': 'entry-1'})
            containers = entry.findAll('div', {'class': 'sb has-sn'})

            for container in containers:
                senses = container.findAll('div', {'class': 'sense'})
                for sense in senses:
                    dts = sense.findAll('span', {'class': 'dt '})
                    for dt in dts:
                        text = cls._extract_text(str(dt))
                        text = cls._fix_utf8(text)
                        definitions.append(text)

        except AttributeError:
            pass
        finally:
            return definitions

    @classmethod
    def _get_html(cls, input):
        template = u"https://www.merriam-webster.com/dictionary/{}"
        url = template.format(urllib2.quote(input))

        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            return None
        return response.read()

    @classmethod
    def _fix_utf8(cls, extract):
        text = re.sub(r'\xe2\x80\x94', '-', extract)
        text = re.sub(r'&mdash;', '-- ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'\xe2\x80\xa6', '[...]', text)
        return text

    @classmethod
    def _extract_text(cls, original):
        # beginning, ending span
        text = re.sub(r'<span class="t">', '- ', original)
        text = re.sub(r'<span(.*?)>', '', text)
        text = re.sub(r'</span>', '', text)

        # beginning, ending strong
        text = re.sub(r'<strong(.*?)>', '', text)
        text = re.sub(r'</strong>', '', text)

        # beginning, ending a
        text = re.sub(r'<a(.*?)>', '', text)
        text = re.sub(r'</a>', '', text)

        # beginning, ending ul
        text = re.sub(r'<ul(.*?)>', '', text)
        text = re.sub(r'</ul>', '', text)

        # beginning, ending em
        text = re.sub(r'<em(.*?)>', '', text)
        text = re.sub(r'</em>', '', text)

        # li
        text = re.sub(r'</?li>', '', text)

        # div
        text = re.sub(r'</div>', '', text)

        # text references
        text = re.sub(r'\(see(.*?)\)', '', text)

        # new lines
        text = re.sub(r'\n', '', text)

        # multiple white spaces, or at the end
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r' $', ' ', text)

        # weird colon positions
        text = re.sub(r'^: ', '', text)
        text = re.sub(r' :', ':', text)

        # weird comma positions
        text = re.sub(r' ,', ':', text)

        # removing whitespace at the end
        return text[:-1]
