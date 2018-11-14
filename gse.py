#!/usr/bin/env python
# -*- coding:utf-8 -*-


import argparse
import os
import sys
import shutil
import subprocess



def git_find_root(tdir):
    # os.chdir을 사용하지 않고, os.path.isdir만 사용해서 체크한다.
    curdir = tdir
    while True:
        if os.path.isdir(os.path.join(curdir, ".git")):
            return curdir
        parent = os.path.normpath(os.path.join(curdir, ".."))
        if os.path.normpath(curdir) == os.path.normpath(parent):
            return ""
        curdir = parent


def git_svn_url():
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    p = subprocess.Popen("git svn info".split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return ""

    for line in out.splitlines():
        if line.startswith("URL: "):
            return line.split(' ', 1)[1]


def git_ls_files():
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    p = subprocess.Popen("git ls-files".split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print("[error] p.communicate error")
        return []

    dirs = set()
    for line in out.splitlines():
        dirs.add(os.path.dirname(line))
    return list(dirs)


def svn_path_normpath(svnpath):
    str = ""
    if svnpath.startswith("svn:/"):
        str = "svn:/" + os.path.normpath(svnpath[5:])
    elif svnpath.startswith("svn+ssh:/"):
        str = "svn+ssh:/" + os.path.normpath(svnpath[9:])
    elif svnpath.startswith("file:/"):
        str = "file:/" + os.path.normpath(svnpath[6:])
    elif svnpath.startswith("http:/"):
        str = "http:/" + os.path.normpath(svnpath[6:])
    elif svnpath.startswith("https:/"):
        str =  "https:/" + os.path.normpath(svnpath[7:])
    else:
        return ""

    return str.replace(os.sep, '/')


def git_svn_get_externals():
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    FNULL = open(os.devnull, "w")
    p = subprocess.Popen("git svn propget svn:externals".split(), env=my_env, stdout=subprocess.PIPE, stderr=FNULL)
    out, err = p.communicate()
    if err:
        print("[error] p.communicate error.")
        return []
    
    extinfo = []
    for line in out.splitlines():
        if line:
            extinfo.append(line.split(' ', 1))

    return extinfo


def git_svn_get_extfile(inf):
    extinfo = []
    while True:
        line = inf.readline()

        if not line: break

        line = line.strip()
        if line:
            extinfo.append(line.split(' ', 1))

    return extinfo


def svn_checkout(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if os.path.exists(abspath):
            print("[error] %s is already exist." % abspath)
            continue
        svnuuu = svn_path_normpath(svnurl + '/' + exi[0])
        cmd = "svn checkout %s %s" % (svnuuu, abspath)
        #print(cmd)
        os.system(cmd)


def svn_switch(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        svnuuu = svn_path_normpath(svnurl + '/' + exi[0])
        cmd = "svn switch %s %s" % (svnuuu, abspath)
        #print(cmd)
        os.system(cmd)


def svn_update(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn update %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_status(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn status %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_info(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn info %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_revert(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn revert -R %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_remove(tardir, svnurl, extinfo):
    print("remove list:\n")
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            continue
        print('\t' + abspath)

    ans = raw_input("\nAre you sure remove the list[y/n]?")
    if ans != 'y' and ans != "yes":
        return

    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            continue
        if os.path.isdir(abspath):
            shutil.rmtree(abspath)
        else:
            os.remove(abspath)


def svn_list(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        #abspath = os.path.join(tardir, exi[1])
        #print(abspath)
        print(exi[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('command', help='{checkout[co]|switch[sw]|update[up]|status[st]|info|revert|remove[rm]|list[ls]}')
    parser.add_argument('targetdir', nargs='?', default='')
    parser.add_argument('extfile', nargs='?', default='')

    args = parser.parse_args()

    CURDIR = os.getcwd()
    TARGETDIR = "."
    if args.targetdir != '':
        TARGETDIR = args.targetdir

    if not os.path.exists(TARGETDIR):
        print("[error] target directory is not exist.")
        sys.exit(1)

    ROOTDIR = git_find_root(CURDIR)
    if not ROOTDIR:
        print("[error] is not git repository.")
        sys.exit(1)

    ROOTDIR = git_find_root(TARGETDIR)
    if not ROOTDIR:
        print("[error] is not git repository.")
        sys.exit(1)


    CURDIR = os.path.abspath(CURDIR)
    TARGETDIR = os.path.abspath(TARGETDIR)
    ROOTDIR = os.path.abspath(ROOTDIR)

    #print("CURDIR : ", CURDIR)
    #print("TARGETDIR : ", TARGETDIR)
    #print("ROOTDIR : ", ROOTDIR)


    os.chdir(ROOTDIR)
    SVNROOTURL = git_svn_url()
    #print("SVNROOTURL : ", SVNROOTURL)
    if not SVNROOTURL:
        print("[error] git svn info command error.")
        sys.exit(1)
    os.chdir(CURDIR)



    if args.extfile != '':
        if args.extfile == '-':
            extf = sys.stdin
        else:
            extf = open(args.extfile, "r")


    os.chdir(TARGETDIR)


    dirs = ['']
    if args.recursive and args.extfile == '':
        dirs = git_ls_files()
    else:
        dirs = ['']
    #print(dirs)

    for dir in dirs:
        tdir = os.path.join(CURDIR, TARGETDIR, dir)

        try:
            os.chdir(tdir)
        except:
            continue

        if args.extfile == '':
            extinfo = git_svn_get_externals()
        else:
            extinfo = git_svn_get_extfile(extf)
        #print(extinfo)
        if not extinfo:
            continue


        # svnurl에 상태경로를 더해서 실제 svnurl 경로를 구한다.
        svnurl = svn_path_normpath(SVNROOTURL + '/' + os.path.abspath(tdir).replace(os.path.abspath(ROOTDIR), ""))
        #print("svnurl : ", svnurl)


        if args.command in ["checkout", "co"]:
            svn_checkout(tdir, svnurl, extinfo)
        elif args.command in ["switch", "sw"]:
            svn_switch(tdir, svnurl, extinfo)
        elif args.command in ["update", "up"]:
            svn_update(tdir, svnurl, extinfo)
        elif args.command in ["status", "st"]:
            svn_status(tdir, svnurl, extinfo)
        elif args.command in ["info"]:
            svn_info(tdir, svnurl, extinfo)
        elif args.command in ["revert"]:
            svn_revert(tdir, svnurl, extinfo)
        elif args.command in ["remove", "rm"]:
            svn_remove(tdir, svnurl, extinfo)
        elif args.command in ["list", "ls"]:
            svn_list(tdir, svnurl, extinfo)
        else:
            print("[error] invalid subcommand.")
            sys.exit(1)

    sys.exit(0)
