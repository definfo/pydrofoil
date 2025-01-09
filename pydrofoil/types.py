from rpython.tool.pairtype import extendabletype

def unique(cls):
    instances = {}
    def __new__(cls, *args):
        res = instances.get(args, None)
        if res is not None:
            return res
        res = object.__new__(cls, *args)
        instances[args] = res
        return res
    cls.__new__ = staticmethod(__new__)
    return cls

def singleton(cls):
    cls._INSTANCE = cls()

    def __new__(cls):
        return cls._INSTANCE
    cls.__new__ = staticmethod(__new__)

    return cls

class Type(object):
    __metaclass__ = extendabletype
    uninitialized_value = '"uninitialized_value"' # often fine for rpython!


@unique
class Union(Type):
    def __init__(self, name, names, typs):
        self.name = name
        self.names = names
        self.typs = typs
        assert len(self.names) == len(self.typs)
        self.variants = {}
        for name, typ in zip(names, typs):
            self.variants[name] = typ

    def __repr__(self):
        return "%s(%r, %s, %s)" % (type(self).__name__, self.name, self.names, self.typs)


@unique
class Enum(Type):
    uninitialized_value = '-1'

    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.name, self.elements)


@unique
class Struct(Type):
    def __init__(self, name, names, typs, tuplestruct=False):
        assert isinstance(name, str)
        self.name = name
        self.names = names
        self.typs = typs
        self.fieldtyps = {}
        assert len(names) == len(typs)
        for name, typ in zip(names, typs):
            self.fieldtyps[name] = typ
        self.tuplestruct = tuplestruct

    def __repr__(self):
        extra = ''
        if self.tuplestruct:
            extra = ', True'
        return "%s(%r, %r, %r%s)" % (type(self).__name__, self.name, self.names, self.typs, extra)

@unique
class Ref(Type):
    def __init__(self, typ):
        assert isinstance(typ, Type)
        self.typ = typ

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.typ)

@unique
class Vec(Type):
    def __init__(self, typ):
        assert isinstance(typ, Type)
        self.typ = typ

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.typ)

@unique
class FVec(Type):
    uninitialized_value = 'None'

    def __init__(self, number, typ):
        assert isinstance(typ, Type)
        self.number = number
        self.typ = typ

    def __repr__(self):
        return "%s(%s, %r)" % (type(self).__name__, self.number, self.typ)

@unique
class Function(Type):
    def __init__(self, argtype, restype):
        assert isinstance(argtype, Type)
        assert isinstance(restype, Type)
        self.argtype = argtype
        self.restype = restype

    def __repr__(self):
        return "%s(%s, %r)" % (type(self).__name__, self.argtype, self.restype)

@unique
class Tuple(Type):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.elements)


@unique
class List(Type):
    # a linked list
    uninitialized_value = "None"

    def __init__(self, typ):
        assert isinstance(typ, Type)
        self.typ = typ

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.typ)

@singleton
class NullType(Type):
    uninitialized_value = "None"

    def __init__(self):
        pass

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@unique
class SmallFixedBitVector(Type):
    uninitialized_value = "r_uint(0)"

    def __init__(self, width):
        # size known at compile time
        assert 0 <= width <= 64
        self.width = width

    def __repr__(self):
        return "SmallFixedBitVector(%s)" % (self.width, )

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, self.width)

@unique
class BigFixedBitVector(Type):

    def __init__(self, width):
        # size known at compile time
        assert width > 64
        self.width = width
        self.uninitialized_value = "bitvector.SparseBitVector(%s, r_uint(0))" % width

    def __repr__(self):
        return "BigFixedBitVector(%s)" % (self.width, )


@singleton
class GenericBitVector(Type):
    uninitialized_value = "bitvector.UNITIALIZED_BV"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@singleton
class MachineInt(Type):
    uninitialized_value = "-0xfefe"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@singleton
class Int(Type):
    uninitialized_value = "UninitInt"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@singleton
class Bool(Type):
    uninitialized_value = "False"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@singleton
class Unit(Type):
    uninitialized_value = "()"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

Bit = lambda : SmallFixedBitVector(1)

@singleton
class String(Type):
    uninitialized_value = "None"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@singleton
class Real(Type):
    uninitialized_value = "None"

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

@unique
class Packed(Type):
    def __init__(self, typ):
        self.uninitialized_value = "%s.unpack()" % typ.uninitialized_value
        self.typ = typ

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, self.typ)

