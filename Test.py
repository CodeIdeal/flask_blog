import markdown

s = open('route.md', 'r', encoding='utf-8').read()
html = markdown.markdown(s, extensions=['markdown.extensions.extra', 'codehilite'])
print(html)