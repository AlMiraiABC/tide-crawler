import sys
from tasks.users import main as init_user
if __name__ == '__main__':
    init_user(sys.argv[1:])
