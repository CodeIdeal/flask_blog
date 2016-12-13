import os
from blog import allowed_file
import mistune


md = open("route.md")
content = md.read()
md_htlm = mistune.markdown(content)
print(md_htlm)