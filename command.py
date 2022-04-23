import sys
from tasks.users import main as init_user
from tasks.crawl import main as crawl

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('init\t\tInitialize.')
        print('crawl\t\tCrawl and update database.')
    cmd = sys.argv[1]
    if cmd == 'init':
        init_user(sys.argv[2:])
    if cmd == 'crawl':
        crawl(sys.argv[2:])
