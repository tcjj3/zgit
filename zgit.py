#! /usr/bin/env python3

import os
import sys
import shutil
import subprocess

G_DEFAULT_GIT_EXE = r"/usr/bin/git"
G_URL_GITHUB = r"https://github.com/"
G_URL_MIRROR = r"https://github.com.cnpmjs.org/"
G_URL_MIRROR2 = r"https://gitclone.com/github.com/"
G_DEFAULT_URL_PROTOCOL = r"https://"
G_OPTION_ORIGIN_REPO = r"-0"


def usage():
    doc = """Clone usage:
    -h, --help:     help.
    -0 url0:        (hyphen zero), give the original repo url, which will be set automatically after clone done.


    Usage 1: clone `github` repo from mirror:
        Same as: git clone mirror_url; cd ...; git remote set-url origin github_url
        e.g:  zgit clone https://github.com/tensorflow/tensorflow.git
    
    Usage 2: clone repo, then change origin url to 'url0' given following `-0`(zero).
        If the left repo is a `github` repo, mirror will be applied.
        Same as: zgit clone ...; cd ...; git remote set-url origin url0
        e.g:  zgit clone https://github.com/aosp-mirror/platform_bionic.git -0 https://android.googlesource.com/platform/bionic
    """
    print(doc)


def main(args):
    argv = args
    # home_dir = os.getenv("HOME")  # TODO: read config rc file

    orig_repo = None
    cloned_folder = None

    # 0. git
    git_exe = shutil.which("git")
    if not git_exe:
        git_exe = os.getenv("GIT", default=G_DEFAULT_GIT_EXE)
    assert shutil.which(git_exe), "git command not found!"

    # use "-0" option to set original repo url:
    if G_OPTION_ORIGIN_REPO in argv:
        orig_opt_position = argv.index(G_OPTION_ORIGIN_REPO)
        orig_repo = argv.pop(orig_opt_position + 1)
        del argv[orig_opt_position]

    # 1. git clone
    clone_action_flag = False
    if len(argv) > 2 and argv[1] == "clone":
        clone_action_flag = True
        for i, s in enumerate(argv[2:], start=2):  # auto mode: use mirror for github.com
            if s.startswith(G_URL_GITHUB):
                # url
                if not orig_repo:
                    orig_repo = s
                mirr_repo = s.replace(G_URL_GITHUB, G_URL_MIRROR)
                argv[i] = mirr_repo
                # local folder
                cloned_folder = os.path.basename(s)[:-4] if s.endswith(".git") else os.path.basename(s)
                break
        if not cloned_folder:  # others: not github.com
            for i, s in enumerate(argv[1:], start=1):
                if s.startswith(G_DEFAULT_URL_PROTOCOL):
                    cloned_folder = os.path.basename(s)[:-4] if s.endswith(".git") else os.path.basename(s)
                    break
    ret_p = subprocess.run([git_exe, *argv[1:]])

    # 2. check status
    if (ret_p.returncode != 0) or (not os.path.exists(cloned_folder)):
        return

    # 3. restore url in .git/config
    if clone_action_flag and cloned_folder and orig_repo:
        print("set-url origin: {}".format(orig_repo))
        os.chdir(cloned_folder)
        ret_p = subprocess.run([git_exe, "remote", "set-url", "origin", orig_repo])

    # 4. git pull
    if clone_action_flag and orig_repo:
        print("git pull ...")
        ret_p = subprocess.run([git_exe, "pull", '--verbose'])


if __name__ == '__main__':
    if (len(sys.argv) < 2) or (sys.argv[1] in ("--help", "-h")):
        usage()
        sys.exit()
    main(sys.argv)
