"""Generate a bookmarklet link while preserving the surrounding HTML source."""

import os
import re
import sys
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote


class TargetLink(HTMLParser):
    def __init__(self, page, target):
        super().__init__()
        self.lines = page.split('\n')
        self.target = target
        self.matches = []
        self.feed(page)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag != 'a' or dict(attrs).get('id') != self.target:
            return
        line, column = self.getpos()
        start = sum(len(part) + 1 for part in self.lines[:line - 1]) + column
        raw = self.get_starttag_text()
        # Tokenize complete attributes so href-like text in a title is ignored.
        tokens = re.finditer(r"""([^\s=/>]+)(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?""", raw[2:-1])
        spans = [(start + 2 + m.start(), start + 2 + m.end())
                 for m in tokens if m[1].lower() == 'href']
        if len(spans) != 1:
            raise ValueError('The target link needs exactly one href attribute.')
        self.matches.extend(spans)


def generate(page_path, repo, target, code):
    name = escape(repo.rsplit('/', 1)[-1])
    if page_path.exists():
        page = page_path.read_text(encoding='utf-8')
    else:
        page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title data-repo-name>{name}</title>
</head>
<body>
  <h1 data-repo-name>{name}</h1>
  <p>Drag this link to your bookmarks bar to install the bookmarklet.</p>
  <a id="{escape(target)}" href="#">Install bookmarklet</a>
</body>
</html>
'''
    # Only template-owned headings follow the repository name on reuse.
    page = re.sub(r'(<(title|h1) data-repo-name>)[^<]*(</\2>)',
                  lambda match: match[1] + name + match[3], page)
    matches = TargetLink(page, target).matches
    if len(matches) != 1:
        raise ValueError(f'Expected one link with id {target!r}, found {len(matches)}.')
    start, end = matches[0]
    url = 'javascript:' + quote(code, safe="!()*-._~")
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(page[:start] + f'href="{url}"' + page[end:], encoding='utf-8')


if __name__ == '__main__':
    generate(Path(os.environ['TARGET_FILE']), os.environ['GITHUB_REPOSITORY'],
             os.environ['TARGET_ID'], Path(sys.argv[1]).read_text(encoding='utf-8').strip())
