{
  description = "Pydrofoil development environment with flake-parts";

  inputs = {
    self.submodules = true;
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        { self', config, pkgs, system, ... }:
        {
          devShells.default =
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
                (pkgs.pypy2.override {
                  packageOverrides = pkgs.lib.composeManyExtensions pypy2PackageOverrides;
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

              python3_ = pkgs.python3.withPackages (
                ps: with ps; [
                  pip
                  pytest
                  setuptools
                ]
              );
            in
            pkgs.mkShell rec {
              shellHook = ''
                echo 1>&2 "Welcome to the development shell!"
                echo 1>&2 "PyPy location: $(which pypy)"
              '';

              buildInputs = with pkgs; [
                zlib
                gmp
                libffi
                zlib
                gmp
                libffi
                ncurses.dev
                bzip2
                openssl.dev
                sqlite.out
                tk
                gdbm
                xz
              ];

              packages = with pkgs; [
                pypy2_
                python3_
                pkg-config
                z3
                # TODO:
                # bump to unstable version after upstream refactor PR is merged
                sail-riscv
              ];

              env = {
                PYTHONPATH = "${pypy2_}/lib/pypy2.7/site-packages";
                LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath buildInputs}";
              };
            };

          packages = {
            pydrofoil-riscv = pkgs.callPackage ./package.nix {
              hypothesis = pkgs.pypy2Packages.callPackage ./nix/hypothesis.nix { };
            };
            pydrofoil-riscv-plugin = pkgs.callPackage ./package-plugin.nix {
              hypothesis = pkgs.pypy2Packages.callPackage ./nix/hypothesis.nix { };
            };
            default = self'.${system}.packages.pydrofoil-riscv;
          };
        };
    };
}
