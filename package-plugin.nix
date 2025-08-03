{
  lib,
  stdenv,
  hypothesis ? null,
  pkg-config,
  python3,
  pypy2,
  z3,
  sail-riscv,
  zlib,
  gmp,
  libffi,
  ncurses5,
  bzip2,
  openssl,
  sqlite,
  tk,
  gdbm,
  xz,
}:
let
  pypy2PackageOverrides = [
    (self: super: {
      # Fix rply
      appdirs = super.appdirs.overridePythonAttrs (oldAttrs: {
        disabled = false;
      });

      # Fix hypothesis
      inherit hypothesis;
    })
  ];

  pypy2_ =
    (pypy2.override {
      packageOverrides = lib.composeManyExtensions pypy2PackageOverrides;
    }).withPackages
      (
        ps: with ps; [
          rply
          hypothesis
          junit-xml
          coverage
          typing
        ]
      );

  python3_ = python3.withPackages (
    ps: with ps; [
      pip
      pytest
      setuptools
    ]
  );
in
stdenv.mkDerivation (finalAttrs: {
  pname = "pydrofoil-riscv";
  version = "0.0.1-alpha0";

  # NOTE: requires Nix 2.28 or later
  # otherwise `inputs.self.submodules` will fail in flake.nix
  src = ./.;

  nativeBuildInputs = [
    pkg-config
    pypy2_
    python3_
    z3
    sail-riscv
  ];

  buildInputs = [
    zlib
    gmp
    libffi.dev
    ncurses5.dev
    bzip2
    openssl.dev
    sqlite.dev
    tk.dev
    gdbm.dev
    xz.dev
    # boehmgc.dev
    # expat.dev
  ];

  buildPhase = ''
    runHook preBuild

    make -C pydrofoil/softfloat/SoftFloat-3e/build/Linux-RISCV-GCC/ softfloat.o
    pkg-config libffi

    cd pypy2/pypy/goal && \
    PYTHONPATH=../../../ ${pypy2_}/bin/pypy ../../rpython/bin/rpython -Ojit targetpypystandalone.py --ext=riscv.pypymodule && \
    mv pypy3.11-c pypy-c-pydrofoil-riscv && \
    ./pypy-c-pydrofoil-riscv ../../lib_pypy/pypy_tools/build_cffi_imports.py && \
    cd -
    ln -s pypy2/pypy/goal/pypy-c-pydrofoil-riscv pypy-c-pydrofoil-riscv

    runHook postBuild
  '';

  doCheck = false;

  checkPhase = ''
    ./pypy-c-pydrofoil-riscv -m pytest riscv/pypymodule/test/apptest_plugin.py
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cd pypy2/pypy/goal && \
    ../tool/release/package.py --override_pypy_c=pypy-c-pydrofoil-riscv \
      --make-portable \
      --archive-name=pypy-pydrofoil-scripting-experimental \
      --targetdir=$out/bin

    runHook postInstall
  '';
})
