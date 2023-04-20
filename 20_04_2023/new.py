def utils(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> any:
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as error:
            print(error)
            return "Emil"

    return wrapper


@utils
def requ(a):
    print(1 / a)
    return True


@utils
def requ1(a):
    print(1 / a)
    return True


@utils
def requ2(a):
    print(1 / a)
    return True


print(requ(0))
print(requ(1))
