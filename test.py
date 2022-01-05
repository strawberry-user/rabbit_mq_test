def f(a, **kwargs):
    print(a, kwargs)
    pass

a=1
reqdict={
    'maimai_reqid': None,
    'uid': 231995955
}
f(a, **reqdict)