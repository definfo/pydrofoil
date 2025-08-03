import _pydrofoil
from cffi import FFI

ffibuilder = FFI()

# Define C API
ffibuilder.embedding_api("""
    typedef struct {
        uint64_t pc;
        uint64_t registers[32];  // x0 to x31
    } RiscvState;

    void* init_cpu(const char* elf_path, int dtb_enabled, int verbosity);
    int step_cpu(void* cpu_handle, int count);
    void get_state(void* cpu_handle, RiscvState* state_out);
    uint64_t get_register(void* cpu_handle, const char* reg_name);
    void set_register(void* cpu_handle, const char* reg_name, uint64_t value);
    uint64_t read_memory(void* cpu_handle, uint64_t address, int size);
    void write_memory(void* cpu_handle, uint64_t address, uint64_t value, int size);
    void free_cpu(void* cpu_handle);
""")

# Source code for the shared library (embeds Python initialization)
# Include the struct definition here to make it visible in the generated C
ffibuilder.set_source(
    "_pydrofoil_difftest",
    """
    #include <stdint.h>  // For uint64_t

    typedef struct {
        uint64_t pc;
        uint64_t registers[32];  // x0 to x31
    } RiscvState;
""",
    # Specify the PyPy shared library for linking
    # TODO: move to a separate Makefile ?
    libraries=["pypy-c-pydrofoil-riscv"],  # Adjust if the lib name is different
    library_dirs=["pypy2/pypy/goal"],  # Path where the shared lib is built
    extra_link_args=["-Wl,-rpath,pypy2/pypy/goal"],  # Runtime path for the lib
)

# Python initialization code (runs when the .so is loaded)
ffibuilder.embedding_init_code("""
    from _pydrofoil_difftest import ffi, lib

    class PydrofoilCPUWrapper:
        def __init__(self, elf_path, dtb_enabled, verbosity):
            self.cpu = _pydrofoil.RISCV64(elf_path, dtb=bool(dtb_enabled))
            self.cpu.set_verbosity(verbosity)

    global_wrappers = {}  # Dict to store wrappers by handle (for thread safety)

    @ffi.def_extern()
    def init_cpu(elf_path, dtb_enabled, verbosity):
        elf_str = ffi.string(elf_path).decode('utf-8')
        wrapper = PydrofoilCPUWrapper(elf_str, dtb_enabled, verbosity)
        handle = id(wrapper)
        global_wrappers[handle] = wrapper  # Store in global dict
        return ffi.cast("void*", handle)

    @ffi.def_extern()
    def step_cpu(cpu_handle, count):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return -1  # Error: invalid handle
        executed = 0
        for _ in range(count):
            try:
                wrapper.cpu.step()
                executed += 1
            except Exception:
                break
        return executed

    @ffi.def_extern()
    def get_state(cpu_handle, state_out):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return
        state_out.pc = int(wrapper.cpu.read_register('pc'))
        for i in range(32):
            reg_name = f'x{i}'
            state_out.registers[i] = int(wrapper.cpu.read_register(reg_name))

    @ffi.def_extern()
    def get_register(cpu_handle, reg_name):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return 0
        reg_str = ffi.string(reg_name).decode('utf-8')
        return int(wrapper.cpu.read_register(reg_str))

    @ffi.def_extern()
    def set_register(cpu_handle, reg_name, value):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return
        reg_str = ffi.string(reg_name).decode('utf-8')
        wrapper.cpu.write_register(reg_str, value)

    @ffi.def_extern()
    def read_memory(cpu_handle, address, size):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return 0
        return wrapper.cpu.read_memory(address, size)

    @ffi.def_extern()
    def write_memory(cpu_handle, address, value, size):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        wrapper = global_wrappers.get(handle)
        if not wrapper:
            return
        wrapper.cpu.write_memory(address, value, size)

    @ffi.def_extern()
    def free_cpu(cpu_handle):
        handle = int(ffi.cast("uintptr_t", cpu_handle))
        if handle in global_wrappers:
            del global_wrappers[handle]
""")

if __name__ == "__main__":
    ffibuilder.compile(target="libpydrofoil_ref.*", verbose=True)


