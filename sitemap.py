import os
import time

from jinja2 import Environment
from jinja2 import PackageLoader, FileSystemLoader

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.join(SITE_ROOT, 'media')
jinja_env = Environment(loader= FileSystemLoader(os.path.join(SITE_ROOT, 'source/_templates')))


class FileInfo(object):
    """Wrapper around filesystem file: collects info"""

    def __init__(self, dirpath, filename):
        fullpath = os.path.join(dirpath, filename)
        self.path = dirpath.replace('build/html', '')
        self.path = self.path + '/' + filename
        self.last_modified = time.gmtime(os.path.getmtime(fullpath))
        self.last_modified = time.strftime('%Y-%m-%d', self.last_modified)

    @property
    def priority(self):
        if '/weblog/tags' in self.path:
            return '0.1'
        if self.path in ['/index.html',
                         '/weblog/index.html']:
            return '1.0'
        if '/me/' in self.path:
            return '0.8'
        if '/bc/' in self.path:
            return '0.8'
        if '/ligfiets/' in self.path:
            return '0.9'
        return '0.5'

    @property
    def changefreq(self):
        if self.path in ['/index.html',
                         '/weblog/index.html']:
            return 'hourly'
        return 'monthly'


def files():
    for dirpath, dirnames, filenames in os.walk('build/html'):
        if '_sources' in dirpath:
            continue
        if '_static' in dirpath:
            continue
        if '.svn' in dirpath:
            continue
        for filename in filenames:
            if filename in ['favicon.ico',
                            'genindex.html',
                            'objects.inv',
                            'search.html',
                            '.buildinfo',
                            '.DS_Store',
                            'searchindex.js']:
                continue
            yield FileInfo(dirpath, filename)


def main():
    outfile = open('build/html/sitemap.xml', 'w')
    sitemap_templ = jinja_env.get_template('sitemap.xml')
    outfile.write(sitemap_templ.render(files=files()))
    outfile.close()
    
if __name__ == "__main__":
    main()
