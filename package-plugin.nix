{
  lib,
  breakpointHook,
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
  ncurses,
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
    # breakpointHook
    pkg-config
    pypy2_
    python3_
    z3
    sail-riscv
  ];

  buildInputs = [
    zlib
    gmp
    libffi
    ncurses.dev
    bzip2
    openssl.out
    openssl.dev
    sqlite.out
    sqlite.dev
    tk
    gdbm
    xz
    # boehmgc.dev
    # expat.dev
  ];

  buildPhase = ''
    runHook preBuild

    make -C pydrofoil/softfloat/SoftFloat-3e/build/Linux-RISCV-GCC/ softfloat.o
    pkg-config libffi

    cd pypy2/pypy/goal
    PYTHONPATH=../../..:${pypy2_}/lib/pypy2.7/site-packages ${pypy2_}/bin/pypy ../../rpython/bin/rpython \
      --batch \
      --make-jobs="$NIX_BUILD_CORES" \
      -Ojit \
      targetpypystandalone.py \
      --ext=riscv.pypymodule
	  mv pypy3.11-c pypy-c-pydrofoil-riscv
	  ./pypy-c-pydrofoil-riscv ../../lib_pypy/pypy_tools/build_cffi_imports.py
	  cd -
	  ln -s pypy2/pypy/goal/pypy-c-pydrofoil-riscv pypy-c-pydrofoil-riscv
    # TODO: move all build artifacts

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    cd pypy2/pypy/goal
    .${pypy2_}/bin/pypy \
      ./tool/release/package.py \
      --override_pypy_c=pypy-c-pydrofoil-riscv \
      --make-portable \
      --archive-name=pypy-pydrofoil-scripting-experimental \
      --targetdir=../../../
    cp pypy-pydrofoil-scripting-experimental.tar.bz2 $out/
    
    runHook postInstall
  '';
})
