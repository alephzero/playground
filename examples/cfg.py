import a0
import json

a0.Cfg("state").write(
    json.dumps(
        {
            "a": 1,
            "b": {"c": "Hello, World!"},
        }
    )
)


class Msg:
    def __init__(self, c):
        self.msg = c


whole = a0.cfg("state")
print(whole)

a = a0.cfg("state", "/a")
print(a)

ai = a0.cfg("state", "/a", int)
print(ai)

c = a0.cfg("state", "/b/c")
print(c)

cs = a0.cfg("state", "/b/c", Msg)
print(cs.msg)


a0.Cfg("state").write(
    json.dumps(
        {
            "a": 2,
            "b": {"c": "Goodbye, World!"},
        }
    )
)

print(cs.msg)

a0.update_configs()

print(cs.msg)
