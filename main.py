def _create_fn(cls, name, func):
    ns = {}
    exec(func, None, ns)
    method = ns[name]
    setattr(cls, name, method)

def _init_fn(cls, fields):
    args = ', '.join(fields)
    lines = [f"object.__setattr__(self, '{field}', {field})" for field in fields]
    body = "\n".join(f' {line}' for line in lines)
    txt = f"def __init__(self, {args}):\n{body}"
    _create_fn(cls, "__init__", txt)

def _frozen_get_del_attr(cls):
    setattr_txt = (
        "def __setattr__(self, name, val):\n"
        "   raise Exception(f'Cannot assign to field {name!r}')"
    )
    delattr_txt = (
        "def __delattr__(self, name):\n"
        "   raise Exception(f'Cannot delete field {name!r}')"
    )
    _create_fn(cls, "__setattr__", setattr_txt)
    _create_fn(cls, "__delattr__", delattr_txt)

def __repr_fn(cls, fields):
    txt = (
        "def __repr__(self):\n"
        "   fields = [f'{key}={val!r}' for key, val in self.__dict__.items()]\n"
        "   return f'{self.__class__.__name__}({\", \".join(fields)})'"
    )
    _create_fn(cls, "__repr__", txt)

def dataclass(cls = None, /, *,init=True, frozen=False, repr=True):
    def wrap(cls):
        fields = cls.__annotations__.keys()
        if init:
            _init_fn(cls, fields)
        if frozen:
            _frozen_get_del_attr(cls)
        if repr:
            __repr_fn(cls, fields)
        return cls
    if cls is None:
        return wrap
    return wrap(cls)


@dataclass(frozen=True)
class PersonInfo:
    first_name: str
    last_name: str
    age: int

person = PersonInfo(first_name="Augustine", last_name="Smith", age=30)
print(person)
