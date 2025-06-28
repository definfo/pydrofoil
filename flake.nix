{
  description = "Pydrofoil development environment with flake-parts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
    treefmt-nix.url = "github:numtide/treefmt-nix";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.treefmt-nix.flakeModule
        inputs.pre-commit-hooks.flakeModule
      ];

      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        {
          self',
          config,
          pkgs,
          ...
        }:
        {
          # https://flake.parts/options/treefmt-nix.html
          # Example: https://github.com/nix-community/buildbot-nix/blob/main/nix/treefmt/flake-module.nix
          treefmt = {
            projectRootFile = "flake.nix";
            settings.global.excludes = [ ];

            programs = {
              nixfmt.enable = true;
              shellcheck.enable = true;
              shfmt.enable = true;
            };
          };

          # https://flake.parts/options/git-hooks-nix.html
          # Example: https://github.com/cachix/git-hooks.nix/blob/master/template/flake.nix
          pre-commit.settings.hooks = {
            commitizen.enable = true;
            eclint.enable = true;
            treefmt.enable = true;
          };

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
            pkgs.mkShell {
              inputsFrom = [
                config.treefmt.build.devShell
                config.pre-commit.devShell
              ];

              shellHook = ''
                echo 1>&2 "Welcome to the development shell!"
                echo 1>&2 "PyPy location: $(which pypy)"
              '';

              buildInputs = with pkgs; [
                zlib
                gmp
                libffi
              ];

              packages = with pkgs; [
                pypy2_
                python3_
                pkg-config
                z3
                sail-riscv
              ];
            };

          packages = rec {
            hypothesis = pkgs.callPackage ./nix/hypothesis.nix { };
            pydrofoil-riscv = pkgs.callPackage ./package.nix { };
            default = pydrofoil-riscv;
          };
        };
    };
}
