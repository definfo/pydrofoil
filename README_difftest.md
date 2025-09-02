# Pydrofoil difftest reference model

(WIP) This Python script aims to provide a reference model for XiangShan's difftest framework.

It depends on Pydrofoil scripting API and PyPy C FFI, also refers to [Spike](https://github.com/OpenXiangShan/riscv-isa-sim) for implmentation.

## Usage

First build pypy-c-pydrofoil-riscv (PyPy3 with external module for scripting API).

```sh
make pypy-c-pydrofoil-riscv
```

Then run C FFI to export workload `pypy-c-pydrofoil-riscv.so`.

```sh
./pypy-c-pydrofoil-riscv ./pydrofoil_cffi_difftest.py
```

Currently the target workload is hardcoded in `def difftest_init()`, please modify when using different ELF workloads.

For integration with difftest, please refer to [XiangShan docs](https://docs.xiangshan.cc/zh-cn/latest/tools/xsenv/#_7).

