import pytest

from pydrofoil import supportcode
from pydrofoil import bitvector
from pydrofoil.bitvector import Integer, SmallInteger, BigInteger

from rpython.rlib.rarithmetic import r_uint, intmask, r_ulonglong
from rpython.rlib.rbigint import rbigint

def gbv(size, val):
    return bitvector.GenericBitVector(size, rbigint.fromlong(val))

def bv(size, val):
    return bitvector.from_ruint(size, r_uint(val))

def si(val):
    return bitvector.SmallInteger(val)

def bi(val):
    return bitvector.BigInteger(rbigint.fromlong(val))

machine = "dummy"

def test_signed_bv():
    assert supportcode.signed_bv(machine, 0b0, 1) == 0
    assert supportcode.signed_bv(machine, 0b1, 1) == -1
    assert supportcode.signed_bv(machine, 0b0, 2) == 0
    assert supportcode.signed_bv(machine, 0b1, 2) == 1
    assert supportcode.signed_bv(machine, 0b10, 2) == -2
    assert supportcode.signed_bv(machine, 0b11, 2) == -1

def test_signed():
    for c in gbv, bv:
        assert supportcode.sail_signed(machine, c(1, 0b0)).toint() == 0
        assert supportcode.sail_signed(machine, c(1, 0b1)).toint() == -1
        assert supportcode.sail_signed(machine, c(2, 0b0)).toint() == 0
        assert supportcode.sail_signed(machine, c(2, 0b1)).toint() == 1
        assert supportcode.sail_signed(machine, c(2, 0b10)).toint() == -2
        assert supportcode.sail_signed(machine, c(2, 0b11)).toint() == -1
        assert supportcode.sail_signed(machine, c(64, 0xffffffffffffffff)).toint() == -1
        assert supportcode.sail_signed(machine, c(64, 0x1)).toint() == 1

def test_sign_extend():
    for c in gbv, bv:
        assert supportcode.sign_extend(machine, c(1, 0b0), Integer.fromint(2)).toint() == 0
        assert supportcode.sign_extend(machine, c(1, 0b1), Integer.fromint(2)).toint() == 0b11
        assert supportcode.sign_extend(machine, c(2, 0b00), Integer.fromint(4)).toint() == 0
        assert supportcode.sign_extend(machine, c(2, 0b01), Integer.fromint(4)).toint() == 1
        assert supportcode.sign_extend(machine, c(2, 0b10), Integer.fromint(4)).toint() == 0b1110
        assert supportcode.sign_extend(machine, c(2, 0b11), Integer.fromint(4)).toint() == 0b1111

        assert supportcode.sign_extend(machine, c(2, 0b00), Integer.fromint(100)).tobigint().tolong() == 0
        assert supportcode.sign_extend(machine, c(2, 0b01), Integer.fromint(100)).tobigint().tolong() == 1
        assert supportcode.sign_extend(machine, c(2, 0b10), Integer.fromint(100)).tobigint().tolong() == 0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110
        assert supportcode.sign_extend(machine, c(2, 0b11), Integer.fromint(100)).tobigint().tolong() == 0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

def test_zero_extend():
    for c in gbv, bv:
        assert supportcode.zero_extend(machine, c(1, 0b0), Integer.fromint(2)).size() == 2
        assert supportcode.zero_extend(machine, c(2, 0b00), Integer.fromint(100)).size() == 100
        assert supportcode.zero_extend(machine, c(1, 0b0), Integer.fromint(2)).toint() == 0
        assert supportcode.zero_extend(machine, c(1, 0b1), Integer.fromint(2)).toint() == 0b01
        assert supportcode.zero_extend(machine, c(2, 0b00), Integer.fromint(4)).toint() == 0
        assert supportcode.zero_extend(machine, c(2, 0b01), Integer.fromint(4)).toint() == 1
        assert supportcode.zero_extend(machine, c(2, 0b10), Integer.fromint(4)).toint() == 0b0010
        assert supportcode.zero_extend(machine, c(2, 0b11), Integer.fromint(4)).toint() == 0b0011

        assert supportcode.zero_extend(machine, c(2, 0b00), Integer.fromint(100)).tobigint().tolong() == 0
        assert supportcode.zero_extend(machine, c(2, 0b01), Integer.fromint(100)).tobigint().tolong() == 1
        assert supportcode.zero_extend(machine, c(2, 0b10), Integer.fromint(100)).tobigint().tolong() == 0b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010
        assert supportcode.zero_extend(machine, c(2, 0b11), Integer.fromint(100)).tobigint().tolong() == 0b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011


def test_unsigned():
    for c in gbv, bv:
        x = c(8, 0b10001101)
        assert x.unsigned().tolong() == 0b10001101
        x = c(64, 0b10001101)
        assert x.unsigned().tolong() == 0b10001101
        x = c(64, r_uint(-1))
        assert x.unsigned().tolong() == (1<<64)-1

def test_get_slice_int():
    for c in si, bi:
        assert supportcode.get_slice_int(machine, Integer.fromint(8), c(0b011010010000), Integer.fromint(4)).tolong() == 0b01101001
        assert supportcode.get_slice_int(machine, Integer.fromint(8), c(-1), Integer.fromint(4)).tolong() == 0b11111111
        assert supportcode.get_slice_int(machine, Integer.fromint(64), c(-1), Integer.fromint(5)).tolong() == 0xffffffffffffffff
        assert supportcode.get_slice_int(machine, Integer.fromint(100), c(-1), Integer.fromint(11)).tolong() == 0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
        assert supportcode.get_slice_int(machine, Integer.fromint(8), c(-1), Integer.fromint(1000)).tolong() == 0b11111111
        assert supportcode.get_slice_int(machine, Integer.fromint(64), c(-1), Integer.fromint(1000)).tolong() == 0xffffffffffffffff
        assert supportcode.get_slice_int(machine, Integer.fromint(100), c(-1), Integer.fromint(1000)).tolong() == 0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111


def test_vector_access():
    for c in gbv, bv:
        x = c(6, 0b101100)
        for i in range(6):
            assert x.read_bit(i) == [0, 0, 1, 1, 0, 1][i]

def test_vector_update():
    for c in gbv, bv:
        x = c(6, 1)
        res = x.update_bit(2, 1)
        assert res.size() == 6
        assert res.toint() == 0b101

        x = c(6, 1)
        res = x.update_bit(0, 1)
        assert res.size() == 6
        assert res.toint() == 0b1

        x = c(6, 0b11)
        res = x.update_bit(2, 0)
        assert res.size() == 6
        assert res.toint() == 0b011

        x = c(6, 0b111)
        res = x.update_bit(1, 0)
        assert res.size() == 6
        assert res.toint() == 0b101

def test_vector_subrange():
    for c in gbv, bv:
        x = c(6, 0b111)
        r = x.subrange(3, 2)
        assert r.size() == 2
        assert r.toint() == 1
        assert isinstance(r, bitvector.SmallBitVector)

    # regression bug
    b = gbv(128, 0x36000000000000001200L)
    x = b.subrange(63, 0)
    assert x.touint() == 0x1200

    b = gbv(128, 0x36000000000000001200L)
    x = b.subrange(66, 0)
    assert x.tolong() == 0x1200
    assert isinstance(x, bitvector.GenericBitVector)

def test_vector_update_subrange():
    for c1 in gbv, bv:
        for c2 in gbv, bv:
            x = c1(8, 0b10001101)
            x = x.update_subrange(5, 2, c2(4, 0b1010))
            assert x.toint() == 0b10101001
            x = c1(64, 0b10001101)
            y = c2(64, 0b1101001010010)
            x = x.update_subrange(63, 0, y)
            assert x.eq(y)

def test_vector_shift():
    for c in gbv, bv:
        x = c(8, 0b10001101)
        res = x.lshift(5)
        assert res.size() == 8
        assert res.toint() == 0b10100000

        x = c(8, 0b10001101)
        res = x.rshift(5)
        assert res.size() == 8
        assert res.toint() == 0b00000100

        x = c(8, 0b10001101)
        res = x.lshift(65)
        assert res.size() == 8
        assert res.toint() == 0

        x = c(8, 0b10001101)
        res = x.rshift(65)
        assert res.size() == 8
        assert res.toint() == 0

def test_vector_shift_bits():
    for c in gbv, bv:
        x = c(8, 0b10001101)
        res = x.lshift_bits(c(8, 5))
        assert res.size() == 8
        assert res.toint() == 0b10100000

        x = c(8, 0b10001101)
        res = x.rshift_bits(c(16, 5))
        assert res.size() == 8
        assert res.toint() == 0b00000100

        x = c(8, 0b10001101)
        res = x.lshift_bits(c(8, 65))
        assert res.size() == 8
        assert res.toint() == 0

        x = c(8, 0b10001101)
        res = x.rshift_bits(c(16, 65))
        assert res.size() == 8
        assert res.toint() == 0

def test_bitvector_touint():
    for size in [6, 6000]:
        assert bv(size, 0b11).touint() == r_uint(0b11)

def test_add_int():
    for c in bi, si:
        assert bv(6, 0b11).add_int(c(0b111111111)).touint() == (0b11 + 0b111111111) & 0b111111
        assert gbv(6000, 0b11).add_int(c(0b111111111)).touint() == 0b11 + 0b111111111

def test_bv_bitwise():
    for c in gbv, bv:
        i1 = c(8, 0b11110000)
        i2 = c(8, 0b11001100)
        res = i1.and_(i2)
        assert res.toint() == 0b11110000 & 0b11001100
        res = i1.or_(i2)
        assert res.toint() == 0b11110000 | 0b11001100
        res = i1.xor(i2)
        assert res.toint() == 0b11110000 ^ 0b11001100
        res = i1.invert()
        assert res.toint() == 0b00001111

def test_add_bv():
    for c in gbv, bv:
        assert supportcode.add_bits(None, c(6, 0b11), c(6, 0b111)).touint() == (0b11 + 0b111) & 0b111111
        assert supportcode.add_bits(None, c(6, 0b10000), c(6, 0b10001)).touint() == (0b10000 + 0b10001) & 0b111111
        assert supportcode.add_bits(None, c(6, 0b100000), c(6, 0b100001)).touint() == (0b100000 + 0b100001) & 0b111111

def test_sub_bv():
    for c in gbv, bv:
        assert supportcode.sub_bits(None, c(6, 0b111), c(6, 0b11)).touint() == (0b111 - 0b11) & 0b111111
        assert supportcode.sub_bits(None, c(6, 0b10000), c(6, 0b10001)).touint() == (0b10000 - 0b10001) & 0b111111
        assert supportcode.sub_bits(None, c(6, 0b100000), c(6, 0b100001)).touint() == (0b100000 - 0b100001) & 0b111111


def test_eq_int():
    for c1 in bi, si:
        for c2 in bi, si:
            assert c1(-12331).eq(c2(-12331))
            assert not c1(-12331).eq(c2(12331))

def test_op_int():
    for c1 in bi, si:
        for c2 in bi, si:
            for v1 in [-10, 223, 12311, 0, 1, 2**63-1]:
                a = c1(v1)
                for v2 in [-10, 223, 12311, 0, 1, 2**63-1, -2**45]:
                    b = c2(v2)
                    assert a.add(b).tolong() == v1 + v2
                    assert a.sub(b).tolong() == v1 - v2
                    assert a.mul(b).tolong() == v1 * v2
                    if v2:
                        assert c1(abs(v1)).tdiv(c2(abs(v2))).tolong() == abs(v1) // abs(v2)
                        assert c1(abs(v1)).tmod(c2(abs(v2))).tolong() == abs(v1) % abs(v2)
                        # (a/b) * b + a%b == a
                        assert a.tdiv(b).mul(b).add(a.tmod(b)).eq(a)

                    assert a.eq(b) == (v1 == v2)
                    assert a.lt(b) == (v1 < v2)
                    assert a.gt(b) == (v1 > v2)
                    assert a.le(b) == (v1 <= v2)
                    assert a.ge(b) == (v1 >= v2)
                with pytest.raises(ZeroDivisionError):
                    c1(v1).tdiv(c2(0))
                    c1(v1).tmod(c2(0))

def test_op_int_div_mod():
    for c1 in bi, si:
        for c2 in bi, si:
            # round towards zero
            assert c1(1).tdiv(c2(2)).tolong() == 0
            assert c1(-1).tdiv(c2(2)).tolong() == 0
            assert c1(1).tdiv(c2(-2)).tolong() == 0
            assert c1(-1).tdiv(c2(-2)).tolong() == 0

            # mod signs
            assert c1(5).tmod(c2(3)).tolong() == 2
            assert c1(5).tmod(c2(-3)).tolong() == 2
            assert c1(-5).tmod(c2(3)).tolong() == -2
            assert c1(-5).tmod(c2(-3)).tolong() == -2

            # ovf correctly
            assert c1(-2**63).tdiv(c2(-1)).tolong() == 2 ** 63
            assert c1(-2**63).tmod(c2(-1)).tolong() == 0


def test_op_gv_int():
    for c1 in gbv, bv:
        for c2 in bi, si:
            assert c1(16, 4).add_int(c2(9)).touint() == 13
            assert c1(16, 4).sub_int(c2(9)).touint() == r_uint((-5) & 0xffff)


def test_string_of_bits():
    for c in gbv, bv:
        assert c(32, 0x1245ab).string_of_bits() == "0x001245AB"
        assert c(64, 0x1245ab).string_of_bits() == "0x00000000001245AB"
        assert c(3, 0b1).string_of_bits() == "0b001"
        assert c(9, 0b1101).string_of_bits() == "0b000001101"


def test_append():
    for c1 in gbv, bv:
        for c2 in gbv, bv:
            assert c1(16, 0xa9e3).append(c2(16, 0x04fb)).toint() == 0xa9e304fb

        
# softfloat

class DummyMachine(object): pass


def test_softfloat_f16add():
    machine = DummyMachine()
    supportcode.softfloat_f16add(machine, 0, 0b0011110000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b0011111000000000

def test_softfloat_f16div():
    machine = DummyMachine()
    supportcode.softfloat_f16div(machine, 0, 0b0011110000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b0100000000000000

def test_softfloat_f16eq():
    machine = DummyMachine()
    supportcode.softfloat_f16eq(machine, 0b0011100000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f16le():
    machine = DummyMachine()
    supportcode.softfloat_f16le(machine, 0b0011100000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f16lt():
    machine = DummyMachine()
    supportcode.softfloat_f16lt(machine, 0b0011100000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0

def test_softfloat_f16mul():
    machine = DummyMachine()
    supportcode.softfloat_f16mul(machine, 0, 0b0011110000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b0011100000000000

def test_softfloat_f16muladd():
    machine = DummyMachine()
    supportcode.softfloat_f16muladd(machine, 0, 0b0011110000000000, 0b0011100000000000, 0b0011110000000000)
    assert machine._reg_zfloat_result == 0b0011111000000000

def test_softfloat_f16sqrt():
    machine = DummyMachine()
    supportcode.softfloat_f16sqrt(machine, 0, 0b0100010000000000)
    assert machine._reg_zfloat_result == 0b0100000000000000

def test_softfloat_f16sub():
    machine = DummyMachine()
    supportcode.softfloat_f16sub(machine, 0, 0b0011110000000000, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b0011100000000000

def test_softfloat_f32add():
    machine = DummyMachine()
    supportcode.softfloat_f32add(machine, 0, 0b00111111000000000000000000000000, 0b00111111100000000000000000000000)
    assert machine._reg_zfloat_result == 0b00111111110000000000000000000000

def test_softfloat_f32div():
    machine = DummyMachine()
    supportcode.softfloat_f32div(machine, 0, 0b00111111100000000000000000000000, 0b01000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b00111111000000000000000000000000

def test_softfloat_f32eq():
    machine = DummyMachine()
    supportcode.softfloat_f32eq(machine, 0b00111111000000000000000000000000, 0b00111111000000000000000000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f32le():
    machine = DummyMachine()
    supportcode.softfloat_f32le(machine, 0b00111111000000000000000000000000, 0b00111111000000000000000000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f32lt():
    machine = DummyMachine()
    supportcode.softfloat_f32lt(machine, 0b00111111000000000000000000000000, 0b00111111000000000000000000000000)
    assert machine._reg_zfloat_result == 0

def test_softfloat_f32mul():
    machine = DummyMachine()
    supportcode.softfloat_f32mul(machine, 0, 0b00111111100000000000000000000000, 0b01000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b01000000000000000000000000000000

def test_softfloat_f32muladd():
    machine = DummyMachine()
    supportcode.softfloat_f32muladd(machine, 0, 0b00111111100000000000000000000000, 0b00111111000000000000000000000000, 0b00111111100000000000000000000000)
    assert machine._reg_zfloat_result == 0b00111111110000000000000000000000

def test_softfloat_f32sqrt():
    machine = DummyMachine()
    supportcode.softfloat_f32sqrt(machine, 0, 0b01000000100000000000000000000000)
    assert machine._reg_zfloat_result == 0b01000000000000000000000000000000

def test_softfloat_f32sub():
    machine = DummyMachine()
    supportcode.softfloat_f32sub(machine, 0, 0b01000000000000000000000000000000, 0b00111111100000000000000000000000)
    assert machine._reg_zfloat_result == 0b00111111100000000000000000000000

def test_softfloat_f64add():
    machine = DummyMachine()
    supportcode.softfloat_f64add(machine, 0, 0b0011111111110000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011111111111000000000000000000000000000000000000000000000000000

def test_softfloat_f64div():
    machine = DummyMachine()
    supportcode.softfloat_f64div(machine, 0, 0b0011111111110000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0100000000000000000000000000000000000000000000000000000000000000

def test_softfloat_f64eq():
    machine = DummyMachine()
    supportcode.softfloat_f64eq(machine, 0b0011111111100000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f64le():
    machine = DummyMachine()
    supportcode.softfloat_f64le(machine, 0b0011111111100000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 1

def test_softfloat_f64lt():
    machine = DummyMachine()
    supportcode.softfloat_f64lt(machine, 0b0011111111100000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0

def test_softfloat_f64mul():
    machine = DummyMachine()
    supportcode.softfloat_f64mul(machine, 0, 0b0011111111110000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011111111100000000000000000000000000000000000000000000000000000

def test_softfloat_f64muladd():
    machine = DummyMachine()
    supportcode.softfloat_f64muladd(machine, 0, 0b0011111111110000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000, 0b0011111111110000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011111111111000000000000000000000000000000000000000000000000000

def test_softfloat_f64sqrt():
    machine = DummyMachine()
    supportcode.softfloat_f64sqrt(machine, 0, 0b0100000000010000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0100000000000000000000000000000000000000000000000000000000000000

def test_softfloat_f64sub():
    machine = DummyMachine()
    supportcode.softfloat_f64sub(machine, 0, 0b0011111111110000000000000000000000000000000000000000000000000000, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011111111100000000000000000000000000000000000000000000000000000
    
def test_softfloat_f16tof32():
    machine = DummyMachine()
    supportcode.softfloat_f16tof32(machine, 0, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b00111111000000000000000000000000
    
def test_softfloat_f32tof16():
    machine = DummyMachine()
    supportcode.softfloat_f32tof16(machine, 0, 0b00111111000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011100000000000
    
def test_softfloat_f16tof64():
    machine = DummyMachine()
    supportcode.softfloat_f16tof64(machine, 0, 0b0011100000000000)
    assert machine._reg_zfloat_result == 0b0011111111100000000000000000000000000000000000000000000000000000
    
def test_softfloat_f64tof16():
    machine = DummyMachine()
    supportcode.softfloat_f64tof16(machine, 0, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011100000000000
    
def test_softfloat_f32tof64():
    machine = DummyMachine()
    supportcode.softfloat_f32tof64(machine, 0, 0b00111111000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0011111111100000000000000000000000000000000000000000000000000000
    
def test_softfloat_f64tof32():
    machine = DummyMachine()
    supportcode.softfloat_f64tof32(machine, 0, 0b0011111111100000000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b00111111000000000000000000000000

def test_softfloat_f16toi32():
    machine = DummyMachine()
    supportcode.softfloat_f16toi32(machine, 0, 0b1100010100000000)
    assert machine._reg_zfloat_result == 0b11111111111111111111111111111011

def test_softfloat_f16toi64():
    machine = DummyMachine()
    supportcode.softfloat_f16toi64(machine, 0, 0b1100010100000000)
    assert machine._reg_zfloat_result == 0b1111111111111111111111111111111111111111111111111111111111111011

def test_softfloat_f16toui32():
    machine = DummyMachine()
    supportcode.softfloat_f16toui32(machine, 0, 0b0100010100000000)
    assert machine._reg_zfloat_result == 0b00000000000000000000000000000101

def test_softfloat_f16toui64():
    machine = DummyMachine()
    supportcode.softfloat_f16toui64(machine, 0, 0b0100010100000000)
    assert machine._reg_zfloat_result == 0b0000000000000000000000000000000000000000000000000000000000000101

def test_softfloat_f32toi32():
    machine = DummyMachine()
    supportcode.softfloat_f32toi32(machine, 0, 0b11000000101000000000000000000000)
    assert machine._reg_zfloat_result == 0b11111111111111111111111111111011

def test_softfloat_f32toi64():
    machine = DummyMachine()
    supportcode.softfloat_f32toi64(machine, 0, 0b11000000101000000000000000000000)
    assert machine._reg_zfloat_result == 0b1111111111111111111111111111111111111111111111111111111111111011

def test_softfloat_f32toui32():
    machine = DummyMachine()
    supportcode.softfloat_f32toui32(machine, 0, 0b01000000101000000000000000000000)
    assert machine._reg_zfloat_result == 0b00000000000000000000000000000101

def test_softfloat_f32toui64():
    machine = DummyMachine()
    supportcode.softfloat_f32toui64(machine, 0, 0b01000000101000000000000000000000)
    assert machine._reg_zfloat_result == 0b0000000000000000000000000000000000000000000000000000000000000101

def test_softfloat_f64toi32():
    machine = DummyMachine()
    supportcode.softfloat_f64toi32(machine, 0, r_ulonglong(0b1100000000010100000000000000000000000000000000000000000000000000))
    assert machine._reg_zfloat_result == 0b11111111111111111111111111111011

def test_softfloat_f64toi64():
    machine = DummyMachine()
    supportcode.softfloat_f64toi64(machine, 0, r_ulonglong(0b1100000000010100000000000000000000000000000000000000000000000000))
    assert machine._reg_zfloat_result == 0b1111111111111111111111111111111111111111111111111111111111111011

def test_softfloat_f64toui32():
    machine = DummyMachine()
    supportcode.softfloat_f64toui32(machine, 0, 0b0100000000010100000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b00000000000000000000000000000101

def test_softfloat_f64toui64():
    machine = DummyMachine()
    supportcode.softfloat_f64toui64(machine, 0, 0b0100000000010100000000000000000000000000000000000000000000000000)
    assert machine._reg_zfloat_result == 0b0000000000000000000000000000000000000000000000000000000000000101

def test_softfloat_i32tof16():
    machine = DummyMachine()
    supportcode.softfloat_i32tof16(machine, 0, 0b11111111111111111111111111111011)
    assert machine._reg_zfloat_result == 0b1100010100000000

def test_softfloat_i32tof32():
    machine = DummyMachine()
    supportcode.softfloat_i32tof32(machine, 0, 0b11111111111111111111111111111011)
    assert machine._reg_zfloat_result == 0b11000000101000000000000000000000

def test_softfloat_i32tof64():
    machine = DummyMachine()
    supportcode.softfloat_i32tof64(machine, 0, 0b11111111111111111111111111111011)
    assert machine._reg_zfloat_result == 0b1100000000010100000000000000000000000000000000000000000000000000

def test_softfloat_i64tof16():
    machine = DummyMachine()
    supportcode.softfloat_i64tof16(machine, 0, r_ulonglong(0b1111111111111111111111111111111111111111111111111111111111111011))
    assert machine._reg_zfloat_result == 0b1100010100000000

def test_softfloat_i64tof32():
    machine = DummyMachine()
    supportcode.softfloat_i64tof32(machine, 0, r_ulonglong(0b1111111111111111111111111111111111111111111111111111111111111011))
    assert machine._reg_zfloat_result == 0b11000000101000000000000000000000

def test_softfloat_i64tof64():
    machine = DummyMachine()
    supportcode.softfloat_i64tof64(machine, 0, r_ulonglong(0b1111111111111111111111111111111111111111111111111111111111111011))
    assert machine._reg_zfloat_result == 0b1100000000010100000000000000000000000000000000000000000000000000

def test_softfloat_ui32tof16():
    machine = DummyMachine()
    supportcode.softfloat_ui32tof16(machine, 0, 0b00000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b0100010100000000

def test_softfloat_ui32tof32():
    machine = DummyMachine()
    supportcode.softfloat_ui32tof32(machine, 0, 0b00000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b01000000101000000000000000000000

def test_softfloat_ui32tof64():
    machine = DummyMachine()
    supportcode.softfloat_ui32tof64(machine, 0, 0b00000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b0100000000010100000000000000000000000000000000000000000000000000

def test_softfloat_ui64tof16():
    machine = DummyMachine()
    supportcode.softfloat_ui64tof16(machine, 0, 0b0000000000000000000000000000000000000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b0100010100000000

def test_softfloat_ui64tof32():
    machine = DummyMachine()
    supportcode.softfloat_ui64tof32(machine, 0, 0b0000000000000000000000000000000000000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b01000000101000000000000000000000

def test_softfloat_ui64tof64():
    machine = DummyMachine()
    supportcode.softfloat_ui64tof64(machine, 0, 0b0000000000000000000000000000000000000000000000000000000000000101)
    assert machine._reg_zfloat_result == 0b0100000000010100000000000000000000000000000000000000000000000000
