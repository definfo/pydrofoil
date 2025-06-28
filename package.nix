{
  lib,
  stdenv,
  fetchFromGitHub,
  pkg-config,
  python3,
  pypy2,
  z3,
  sail-riscv,
  zlib,
  gmp,
  libffi,
  versionCheckHook,
}:
let
  pypy2PackageOverrides = [
    (self: super: {
      # Fix rply
      appdirs = super.appdirs.overridePythonAttrs (oldAttrs: {
        disabled = false;
      });

      # Fix hypothesis
      hypothesis = self.callPackage ./nix/hypothesis.nix { };
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

  # src = ./.;

  src = fetchFromGitHub {
    owner = "pydrofoil";
    repo = "pydrofoil";
    rev = "dc1e1749db7b0eb0756ceb69c5b5b518e57f0ab1";
    hash = "sha256-Q/W7kW2HRwit/WGbn6C9fqXOT4N5wl6tISLqE9ZMl4M=";
    fetchSubmodules = true;
  };

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
    libffi
  ];

  buildPhase = ''
    runHook preBuild

    make -C pydrofoil/softfloat/SoftFloat-3e/build/Linux-RISCV-GCC/ softfloat.o
    pkg-config libffi

    export PYTHONPATH=$PWD:${pypy2_}/lib/pypy2.7/site-packages
    ${pypy2_}/bin/pypy pypy2/rpython/bin/rpython -Ojit --output=pydrofoil-riscv riscv/targetriscv.py

    runHook postBuild
  '';

  doCheck = true;

  checkPhase = ''
    ${pypy2_}/bin/pypy pypy2/pytest.py -v pydrofoil/ riscv/
  '';

  doInstallCheck = true;

  nativeInstallCheckInputs = [
    versionCheckHook
  ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    install -Dm755 pydrofoil-riscv $out/bin

    runHook postInstall
  '';
})
