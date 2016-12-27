
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import mistune
from blog import get_posts_num, get_posts_by_index


print(get_posts_num())