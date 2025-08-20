import _pydrofoil
from cffi import FFI

ffibuilder = FFI()

# Emulate C API from `class DifftestRef` at https://github.com/OpenXiangShan/riscv-isa-sim/tree/difftest/difftest
ffibuilder.embedding_api("""
    typedef uint64_t reg_t;

    typedef struct {
      uint64_t gpr[32];
      uint64_t fpr[32];
      uint64_t priv;
      uint64_t mstatus;
      uint64_t sstatus;
      uint64_t mepc;
      uint64_t sepc;
      uint64_t mtval;
      uint64_t stval;
      uint64_t mtvec;
      uint64_t stvec;
      uint64_t mcause;
      uint64_t scause;
      uint64_t satp;
      uint64_t mip;
      uint64_t mie;
      uint64_t mscratch;
      uint64_t sscratch;
      uint64_t mideleg;
      uint64_t medeleg;
      uint64_t pc;

      uint64_t v;
      uint64_t mtval2;
      uint64_t mtinst;
      uint64_t hstatus;
      uint64_t hideleg;
      uint64_t hedeleg;
      uint64_t hcounteren;
      uint64_t htval;
      uint64_t htinst;
      uint64_t hgatp;
      uint64_t vsstatus;
      uint64_t vstvec;
      uint64_t vsepc;
      uint64_t vscause;
      uint64_t vstval;
      uint64_t vsatp;
      uint64_t vsscratch;

      union {
        uint64_t _64[2];
        uint32_t _32[4];
        uint16_t _16[8];
        uint8_t  _8[16];
      } vr[32];
      uint64_t vstart;
      uint64_t vxsat;
      uint64_t vxrm;
      uint64_t vcsr;
      uint64_t vl;
      uint64_t vtype;
      uint64_t vlenb;

      uint64_t fcsr;

      uint64_t tselect;
      uint64_t tdata1;
      uint64_t tinfo;

      uint64_t debugMode;
      uint64_t dcsr;
      uint64_t dpc;
      uint64_t dscratch0;
      uint64_t dscratch1;
    } diff_context_t;

    typedef struct {
      bool ignore_illegal_mem_access;
      bool debug_difftest;
    } diff_ref_config;

    typedef struct {
      uint64_t sc_failed;
    } diff_uarch_status;

    typedef struct {
        bool platform_irp_meip;
        bool platform_irp_mtip;
        bool platform_irp_msip;
        bool platform_irp_seip;
        bool platform_irp_stip;
        bool platform_irp_vseip;
        bool platform_irp_vstip;
        bool lcofi_req;
    } diff_non_reg_int;

    int difftest_disambiguation_state();

    void difftest_memcpy(uint64_t addr, void *buf, size_t n, bool direction);
    
    void difftest_regcpy(diff_context_t* dut, bool direction, bool on_demand);
    
    void difftest_csrcpy(void *dut, bool direction);
    
    void difftest_pmpcpy(void *dut, bool direction);    

    void difftest_pmp_cfg_cpy(void *dut, bool direction);
    
    void difftest_uarchstatus_sync(diff_uarch_status *dut);
    
    void update_dynamic_config(diff_ref_config *config);
    
    void difftest_exec(uint64_t n);
    
    void difftest_skip_one(bool isRVC, bool wen, uint32_t wdest, uint64_t wdata);
    
    void difftest_init(int port);
    
    void difftest_raise_intr(uint64_t NO);
    
    void difftest_dirty_fsvs(uint64_t dirties);
    
    bool difftest_raise_critical_error();
    
    void isa_reg_display();
    
    void difftest_display();
    
    int difftest_store_commit(uint64_t *addr, uint64_t *data, uint8_t *mask);
    
    uint64_t difftest_guided_exec(void *);    

    void debug_mem_sync(reg_t addr, void* buf, size_t n);
    
    void difftest_load_flash_v2(const uint8_t *flash_bin, size_t size);
    
    void difftest_load_flash(const char *flash_bin_file, size_t size);
    
    void difftest_set_mhartid(int mhartid);
    
    void difftest_close();
    
    void difftest_set_ramsize(size_t size);
    
    void difftest_non_reg_interrupt_pending(diff_non_reg_int *non_reg_interrupt_pending);
"""
)

ffibuilder.set_source("pypy-c-pydrofoil-riscv", "")

ffibuilder.embedding_init_code("""
    import _pydrofoil
    from collections import Counter


    @ffi.def_extern
    def difftest_disambiguation_state():
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_memcpy(addr, buf, n, direction):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_regcpy(dut, direction, on_demand):
        # TODO: implement this
        # cpu.read_register()
        pass

    @ffi.def_extern
    def difftest_csrcpy(dut, direction):
        # TODO: implement this
        # cpu.lowlevel.read_CSR()
        pass

    @ffi.def_extern
    def difftest_pmpcpy(dut, direction):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_pmp_cfg_cpy(dut, direction):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_uarchstatus_sync(dut):
        # TODO: implement this
        pass

    @ffi.def_extern
    def update_dynamic_config(config):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_exec(n):
        for _ in range(n):
            cpu.step()

    @ffi.def_extern
    def difftest_skip_one(isRVC, wen, wdest, wdata):
        # TODO: implement this
        # Currently Pydrofoil does not support this ?
        pass

    @ffi.def_extern
    def difftest_init(port):
        # WTF IS `port` ?
        # Spike does nothing with it!
        # TODO: select & load elf during build phase
        cpu = _pydrofoil.RISCV64("./riscv/input/rv64-linux-4.15.0-gcc-7.2.0-64mb.bbl", dtb=True)
        cpu.set_verbosity(0)
        
        # TODO: record variable with Counter
        # so that we can later dump extra info
        # cnt = Counter()

    @ffi.def_extern
    def difftest_raise_intr(NO):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_dirty_fsvs(dirties):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_raise_critical_error():
        # This simply change state variable on Spike's side
        # Not sure if we should mimic such behaviour...
        pass

    @ffi.def_extern
    def isa_reg_display():
        # TODO: pretty print
        print(cpu.register_info())

    @ffi.def_extern
    def difftest_display():
        # TODO: Check simpleprofiler.py
        # cpu.memory_info(), cpu.register_info(), etc.
        pass

    @ffi.def_extern
    def difftest_store_commit(addr, data, mask):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_guided_exec():
        cpu.step()

    @ffi.def_extern
    def debug_mem_sync(addr, buf, n):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_load_flash_v2(flash_bin, size):
        # Seem unsupported ?
        pass

    @ffi.def_extern
    def difftest_load_flash(flash_bin_file, size):
        # Seem unsupported ?
        pass

    @ffi.def_extern
    def difftest_set_mhartid(mhartid):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_close():
        exit(0)

    @ffi.def_extern
    def difftest_set_ramsize(size):
        # TODO: implement this
        pass

    @ffi.def_extern
    def difftest_non_reg_interrupt_pending(non_reg_interrupt_pending):
        # TODO: implement this
        pass
""")
