# Pydrofoil C FFI 笔记

## Difftest C API

（以下源码片段均来自 `github:OpenXiangShan/riscv-isa-sim`）

```c difftest/difftest.h:13
enum { DIFFTEST_TO_DUT, DIFFTEST_TO_REF };
/* 
 * (DIFFTEST ==> DUT) := 0/False;
 * (DIFFTEST ==> REF) := 1/True;
*/
```

```c
state_t * const state;
```

```c riscv/processor.h
// architectural state of a RISC-V hart
struct state_t
{
  void reset(processor_t* const proc, reg_t max_isa);
  void add_csr(reg_t addr, const csr_t_p& csr);

  reg_t pc;
  regfile_t<reg_t, NXPR, true> XPR;
  regfile_t<freg_t, NFPR, false> FPR;

  // control and status registers
  std::unordered_map<reg_t, csr_t_p> csrmap;
  reg_t prv;    // TODO: Can this be an enum instead?
  reg_t prev_prv;
  bool prv_changed;
  bool v_changed;
  bool v;
  bool prev_v;
  misa_csr_t_p misa;
  mstatus_csr_t_p mstatus;
  csr_t_p mstatush;
  csr_t_p mepc;
  csr_t_p mtval;
  csr_t_p mscratch;                 // ADD by XiangShan
  csr_t_p mtvec;
  csr_t_p mcause;
  wide_counter_csr_t_p minstret;
  wide_counter_csr_t_p mcycle;
  mie_csr_t_p mie;
  mip_csr_t_p mip;
  csr_t_p medeleg;
  csr_t_p mideleg;
  csr_t_p mcounteren;
  csr_t_p mcountinhibit;
  csr_t_p mevent[N_HPMCOUNTERS];
  mnstatus_csr_t_p mnstatus;
  csr_t_p mnepc;
  csr_t_p mncause;
  csr_t_p scounteren;
  csr_t_p sepc;
  csr_t_p stval;
  csr_t_p sscratch;                 // ADD by XiangShan
  csr_t_p stvec;
  virtualized_csr_t_p satp;
  csr_t_p scause;

// When taking a trap into HS-mode, we must access the nonvirtualized HS-mode CSRs directly:
  csr_t_p nonvirtual_stvec;
  satp_csr_t_p nonvirtual_satp;     // ADD by XiangShan
  csr_t_p nonvirtual_scause;
  csr_t_p nonvirtual_sepc;
  csr_t_p nonvirtual_stval;
  csr_t_p nonvirtual_sscratch;      // ADD by XiangShan
  sstatus_proxy_csr_t_p nonvirtual_sstatus;

  csr_t_p mtval2;
  csr_t_p mtinst;
  csr_t_p hstatus;
  csr_t_p hideleg;
  csr_t_p hedeleg;
  csr_t_p hcounteren;
  csr_t_p htval;
  csr_t_p htinst;
  csr_t_p hgatp;
  hvip_csr_t_p hvip;
  sstatus_csr_t_p sstatus;
  vsstatus_csr_t_p vsstatus;
  csr_t_p vstvec;
  csr_t_p vsepc;
  csr_t_p vsscratch;                // ADD by XiangShan
  csr_t_p vscause;
  csr_t_p vstval;
  csr_t_p vsatp;

  csr_t_p dpc;
  dcsr_csr_t_p dcsr;
  csr_t_p tselect;
  csr_t_p tdata2;
  csr_t_p tcontrol;
  csr_t_p scontext;
  csr_t_p mcontext;

  csr_t_p jvt;

  bool debug_mode;

  mseccfg_csr_t_p mseccfg;

#ifdef CONFIG_PMP_MAX_NUM
  static const int max_pmp = CONFIG_PMP_MAX_NUM;
#else
  static const int max_pmp = 64;
#endif
  pmpaddr_csr_t_p pmpaddr[max_pmp];

  float_csr_t_p fflags;
  float_csr_t_p frm;

  csr_t_p menvcfg;
  csr_t_p senvcfg;
  csr_t_p henvcfg;

  csr_t_p mstateen[4];
  csr_t_p sstateen[4];
  csr_t_p hstateen[4];

  csr_t_p htimedelta;
  time_counter_csr_t_p time;
  csr_t_p time_proxy;

  csr_t_p stimecmp;
  csr_t_p vstimecmp;

  csr_t_p ssp;

  bool serialized; // whether timer CSRs are in a well-defined state

  // When true, execute a single instruction and then enter debug mode.  This
  // can only be set by executing dret.
  enum {
      STEP_NONE,
      STEP_STEPPING,
      STEP_STEPPED
  } single_step;

  commit_log_reg_t log_reg_write;
  commit_log_mem_t log_mem_read;
  commit_log_mem_t log_mem_write;
  reg_t last_inst_priv;
  int last_inst_xlen;
  int last_inst_flen;

  elp_t elp;

  bool critical_error;

 private:
  void csr_init(processor_t* const proc, reg_t max_isa);
```





