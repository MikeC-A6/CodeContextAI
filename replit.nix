{pkgs}: {
  deps = [
    pkgs.awsebcli
    pkgs.python312Packages.pathspec
    pkgs.python312Packages.gitpython
  ];
}
