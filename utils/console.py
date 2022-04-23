from re import S


class Console:
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple

    @staticmethod
    def print_info(info):
        print(info)

    @staticmethod
    def print_success(info):
        print(f'{Console.G}{info}{Console.W}')

    @staticmethod
    def print_warn(info):
        print(f'{Console.O}{info}{Console.W}')

    @staticmethod
    def print_err(info):
        print(f'{Console.R}{info}{Console.W}')

    @staticmethod
    def print_fail(info):
        Console.print_err(info)
