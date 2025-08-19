# NOTE:
# This is a copy from an example program in docs/scripting-api.md
import _pydrofoil
import time
from collections import Counter

cpu = _pydrofoil.RISCV64('riscv/input/rv64-linux-4.15.0-gcc-7.2.0-64mb.bbl', dtb=True)
cpu.set_verbosity(0)
instructions = 23_000_000
histogram_pcs = Counter()
histogram_instructions = Counter()
histogram_mnemonic = Counter()

t1 = time.time()
try:
    for i in range(instructions):
        cpu.step()
        histogram_pcs[str(cpu.read_register("pc"))] += 1
        dis = cpu.disassemble_last_instruction()
        histogram_instructions[dis] += 1
        histogram_mnemonic[dis.split()[0]] += 1
except KeyboardInterrupt:
    pass
t2 = time.time()
print(f"instructions: {i+1}, kips: {round(i/(t2-t1)/100,2)}")

print()

for pc, value in histogram_mnemonic.most_common(20):
    print(pc, value)

print()

for pc, value in histogram_instructions.most_common(20):
    print(pc, value)

print()

for pc, value in histogram_pcs.most_common(20):
    print(pc, value)

