#!/usr/bin/env python3.8

import argparse
import os
import re
import subprocess
import shutil
import numpy
from result_presenter_fig7 import gen_figure7_table3
from make_patch import patchAll
from regexify import findTargetFiles

VENDOR = "vendor"
DIRECT_DEF = "direct_loc_def.txt"
INDIRECT_DEF = "indirect_loc_def.txt"
DIRECT_USES = "direct_uses.txt"
INDIRECT_USES = "indirect_uses.txt"
CHANGES = "changes.txt"
V_CHANGES = "vendored_changes.txt"
SUMM_DIRECT_USES = "summary_direct_num_uses.txt"
SUMM_INDIRECT_DEPS = "summary_indirect_num_deps.txt"
SUMM_INDIRECT_USES = "summary_indirect_num_uses.txt"
SUMM_TOTAL = "summary_total_uses.txt"

#apps = {
#    "zola-3bedb42b0b8ef06967eecaa63b8faa82dbe9cd00": {
#        "flag": "--bins",
#    },
#    "tantivy-f6cf6e889b1f8595dbd6b62f30c71562c1465d01": {
#        "flag": "--benches",
#    },
#    "RustPython-b33f72eb4d329b7ad409ba454b0b800802294cbb": {
#        "flag": "--bins",
#    },
#    "wasmer-a3a73d35e3ba4880a31009bfba6b10fe4dd812a9": {
#        "flag": "--benches",
#    },
#    "splinter-7382303182863a3f2ca575a3c421fdf4361885de": {
#        "flag": "--bins",
#    },
#    "gfx-bc77309afdb0829605982370a3e17382c5968071": {
#        "flag": "--bins",
#    },
#    "quiche": {
#        "flag": "--examples",
#    },
#    "warp-ffe49abb5626934fbcc807dbeb7824d437a53cd4": {
#        "flag": "--examples",
#    },
#    "fnm-fd584746a6206d4138f35966629c000026f5fe96": {
#        "flag": "--bins",
#    },
#    "tonic-efe0865d26b7cfcb4b5755dc2b723d96a581dd95": {
#        "flag": "--bins",
#    },
#    "vector-53fe64d7487a166c822485a0e74422fd05c1f633": {
#        "flag": "--bins",
#    },
#    "flatbuffers-a7b527d9427485c9758a36e1ffdb148ac2b0124a": {
#        "flag": "",
#    },
#}

class State:

    def __init__(self, root): #, regexify):
        self.root = root
        #self.regexify = regexify
        #self.loc_def = []
        #self.num_deps = dict()
        #self.direct_uses = dict()
        #self.indirect_deps = dict()
        #self.indirect_uses = dict()
        #self.vendor_dir = VENDOR
        #self.app_dirs = dict()
        #for app in os.listdir(self.root):
        #    path = os.path.join(self.root, app)
        #    if os.path.isdir(path): 
        #        if "flatbuffers" in app: 
        #            app_dir = os.path.join(path, "rust", "flatbuffers")
        #        elif "flux" in app: 
        #            app_dir = os.path.join(path, "libflux", "flux")
        #        elif "splinter" in app:
        #            app_dir = os.path.join(path, "splinter")
        #        else: 
        #            app_dir = path
        #        self.app_dirs.update({app: {"top-dir": path, "cargo-dir": app_dir}})

    #def get_loc_def_gu(self, indirect=False):
    #    for app in self.app_dirs: 
    #        any_gu = subprocess.run(["grep", "-rn", "fn get_unchecked", 
    #                self.app_dirs.get(app).get("top-dir")], 
    #                capture_output=True, text=True)
    #        num_gu = len(any_gu.stdout.split())
    #        # record any crates with locally-defined get_unchecked[_mut]s
    #        if num_gu > 0: 
    #            self.loc_def.append(app)
    #    if indirect == True: 
    #        loc_def_crates = open(os.path.join(self.root, INDIRECT_DEF), "w")
    #    else:
    #        loc_def_crates = open(os.path.join(self.root, DIRECT_DEF), "w")
    #    for c in self.loc_def: 
    #        loc_def_crates.write("{}\n".format(c))

    #def convert(self):
    #    for app in self.app_dirs:
    #        os.chdir(self.app_dirs.get(app).get("top-dir"))
    #        subprocess.run(["python3.8", "regexify.py", "--root", "."], 
    #                stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    #        directs = open(DIRECT_USES, "w")
    #        changes = open(CHANGES, "r")

    #        temp = []
    #        for line in changes.readlines():
    #            changed_file = line.split()[2]
    #            crate = changed_file.split("/")[0]
    #            temp.append(crate)
    #        arr = numpy.array(temp)
    #        crates, counts = numpy.unique(arr, return_counts=True)
    #        crate_counts = zip(crates, counts)
    #        for c, i in crate_counts: 
    #            directs.write("{}:\t{}\n".format(c, i))
    #        os.chdir(self.root)

    def filter(self):
        # get list of all vendored crates
        all_deps = []
        contents = os.listdir(self.vendor_dir)
        for c in contents:
            if os.path.isdir(os.path.join(self.vendor_dir, c)):
                all_deps.append(c)
        # get list of all non-dev dependencies
        no_dev_dep_tree = subprocess.run(["cargo", "tree", "-e", "no-dev", 
                "--prefix", "none"], capture_output=True, text=True)
        lines = no_dev_dep_tree.stdout.split("\n")
        non_dev_deps = []
        for line in lines:
            non_dev_deps.append(line.replace(" v", "-"))
        # delete any vendored crates that are not in the non-dev dep list
        # (i.e. delete anything that is _only_ a dev dep)
        to_delete = [x for x in all_deps if x not in non_dev_deps]
        for d in to_delete:
            path = os.path.join(self.vendor_dir, d)
            #print("deleting {}".format(d))
            try: 
                shutil.rmtree(path)
            except OSError as err: 
                print("Error: {} : {}".format(path, err.strerror))

    #def vendor(self):
    #    # count the number of crates that have indirectly been converted
    #    for app in self.app_dirs:
    #        app_dir = self.app_dirs.get(app).get("cargo-dir")
    #        os.chdir(app_dir)
    #        #print()
    #        #print("***** current app: {} *****".format(app))
    #        #print("  vendor dir: {}".format(self.vendor_dir))
    #        #print()

    #        # vendor crates for this app
    #        subprocess.run(["rustup", "override", "set", "nightly-2021-02-11"], 
    #                stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    #        subprocess.run(["cargo", "vendor", "--versioned-dirs"], 
    #                stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    #        num_vendored = subprocess.run(["ls", self.vendor_dir], 
    #                capture_output=True, text=True)
    #        if len(num_vendored.stdout) == 0:
    #            os.chdir(self.root)
    #            continue

    #        # filter out dev deps
    #        #print("filtering out dev deps not otherwise used")
    #        self.filter()
    #        os.chdir(self.root)
#
#    def convert_vendor(self):
#        for app in self.app_dirs:
#            app_dir = self.app_dirs.get(app).get("cargo-dir")
#            os.chdir(app_dir)
#            # convert vendored crates
#            #print("converting vendored crates for {}".format(app))
#            subprocess.run(["python3.8", "regexify.py", "--root", self.vendor_dir], 
#                    stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
#            v_changes_file = os.path.join(self.vendor_dir, CHANGES)
#            v_changes = open(v_changes_file, "r")
#            indirects = open(INDIRECT_USES, "w")
#            temp = []
#            for line in v_changes.readlines():
#                v_changed_file = line.split()[2]
#                v_crate = v_changed_file.split("/")[0]
#                temp.append(v_crate)
#            v_arr = numpy.array(temp)
#            v_crates, v_counts = numpy.unique(v_arr, return_counts=True)
#            v_crate_counts = zip(v_crates, v_counts)
#            for v, i in v_crate_counts: 
#                # log indirect conversions to a file
#                indirects.write("{}:\t{}\n".format(v, i))

            ## delete vendor dir
            #subprocess.run(["mv", v_changes_file, V_CHANGES])
            #print("deleting vendor dir for space")
            #try: 
            #    shutil.rmtree(self.vendor_dir)
            #except OSError as err: 
            #    print("Error: {} : {}".format(self.vendor_dir, err.strerror))
    #        os.chdir(self.root)

    #def get_direct_gus(self):
    #    for app in self.app_dirs:
    #        app_dir = self.app_dirs.get(app).get("top-dir")
    #        directs = open(os.path.join(app_dir, DIRECT_USES), "r").read()
    #        lines = directs.split("\n")
    #        count = 0
    #        for line in lines:
    #            if len(line) == 0:
    #                break
    #            parts = line.split()
    #            count += int(parts[1])
    #        self.direct_uses.update({app: count})

    #    # write all direct gu uses to file
    #    summary_directs = open(os.path.join(self.root, SUMM_DIRECT_USES), "w")
    #    sorted_directs = {k: v for k, v in 
    #            sorted(self.direct_uses.items(), key=lambda item: item[1])}
    #    for app, count in sorted_directs.items(): 
    #        summary_directs.write("{}: {}\n".format(app, count))

    def get_num_deps(self):
        for app in self.app_dirs:
            app_dir = self.app_dirs.get(app).get("cargo-dir")
            os.chdir(app_dir)
            # get list of all non-dev dependencies
            num_deps = subprocess.run(["cargo", "tree", "-e", "no-dev", 
                    "--prefix", "none"], capture_output=True, text=True)
            deps = num_deps.stdout.split("\n")
            dedup_deps = []
            for d in deps: 
                if "(*)" not in d: 
                    dedup_deps.append(d)
            num_deps = len(dedup_deps)
            self.num_deps.update({app: num_deps})
            os.chdir(self.root)

    #def get_indirect_deps(self): 
    #    for app in self.app_dirs:
    #        app_dir = self.app_dirs.get(app).get("cargo-dir")
    #        indirects = open(os.path.join(app_dir, INDIRECT_USES), "r").read()
    #        lines = indirects.split("\n")
    #        count = 0
    #        for line in lines:
    #            if len(line) == 0:
    #                break
    #            count += 1
    #        self.indirect_deps.update({app: count})

    #    # write indirect gu deps per app to file
    #    summ_indirect_deps = open(os.path.join(self.root, SUMM_INDIRECT_DEPS), "w")
    #    sorted_indirect_deps = {k: v for k, v in
    #            sorted(self.indirect_deps.items(), key=lambda item: item[1])}
    #    for app, count in sorted_indirect_deps.items():
    #        summ_indirect_deps.write("{}: {}\n".format(app, count))

    #def get_indirect_uses(self): 
    #    for app in self.app_dirs:
    #        app_dir = self.app_dirs.get(app).get("cargo-dir")
    #        indirects = open(os.path.join(app_dir, INDIRECT_USES), "r").read()
    #        lines = indirects.split("\n")
    #        count = 0
    #        for line in lines:
    #            if len(line) == 0:
    #                break
    #            parts = line.split()
    #            count += int(parts[1])
    #        self.indirect_uses.update({app: count})

    #    # write indirect gu num per app to file
    #    summ_indirect_uses = open(os.path.join(self.root, SUMM_INDIRECT_USES), "w")
    #    sorted_indirect_uses = {k: v for k, v in
    #            sorted(self.indirect_uses.items(), key=lambda item: item[1])}
    #    for app, count in sorted_indirect_uses.items():
    #        summ_indirect_uses.write("{}: {}\n".format(app, count))

    #def get_total_uses(self):
    #    summ_total_uses = open(os.path.join(self.root, SUMM_TOTAL), "w")
    #    sorted_indirects = {k: v for k, v in 
    #        sorted(self.indirect_uses.items(), key=lambda item: item[1])}
    #    for app, indirect in sorted_indirects.items():
    #        direct = self.direct_uses.get(app)
    #        all_deps = self.num_deps.get(app)
    #        unchecked_deps = self.indirect_deps.get(app)
    #        summ_total_uses.write("{} {} {} {} {}\n" 
    #                .format(app, direct, indirect, all_deps, unchecked_deps))

#def old_main(): 
#    #print("Getting locally-defined get_unchecked...")
#    print("Getting direct get_unchecked uses...")
#    s.get_loc_def_gu()
#    #print("Converting locally-defined get_unchecked...")
#    s.convert()
#    #print("Vendoring dependencies...")
#    print("Getting dependencies...")
#    s.vendor()
#    #print("Getting get_unchecked uses in dependencies...")
#    print("Getting indirect get_unchecked uses...")
#    s.get_loc_def_gu(indirect=True)
#    s.convert_vendor()
#    s.get_direct_gus()
#    s.get_num_deps()
#    print("Counting number of dependencies with indirect get_unchecked uses...")
#    s.get_indirect_deps()
#    s.get_indirect_uses()
#    #print("Getting total uses...")
#    s.get_total_uses()
#    print("Generating pdfs...")
#    gen_figure7_table3(root)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", "-r",
            metavar="path/to/deps/",
            type=str,
            required=True,
            help="path to the directory containing the source code to convert")
    parser.add_argument("--single", "-s",
            action="store_true",
            help="script assumes that root contains many projects to iterate "\
                    "through - pass this flag if your root path only points to "\
                    "a single project")
    args = parser.parse_args()
    return args.root, args.single

if __name__ == "__main__":
    root, single = arg_parse()
    if single: 
        exit("not implemented")
    root = os.path.join(os.getcwd(), root)
    s = State(root)
    dirs = os.listdir(root)
    summ_total_uses = open(os.path.join(root, SUMM_TOTAL), "w")
    os.environ["RUSTFLAGS"] = "-Z convert-unchecked-indexing"
    for d in dirs: 
        print()
        print(d)
        curdir = os.path.join(root, d)
        if not os.path.isdir(curdir):
            continue
        if "flatbuffers" in d: 
            curdir = os.path.join(curdir, "rust", "flatbuffers")
        elif "flux" in d: 
            curdir = os.path.join(curdir, "libflux", "flux")
        elif "splinter" in d:
            curdir = os.path.join(curdir, "splinter")
        os.chdir(curdir)
        subprocess.run(["rustup", "override", "set", "rust-mod-mir"])
            #stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
        subprocess.run(["cargo", "clean"])
        print("Vendoring")
        v_out = open("vendor.out", "w")
        v_err = open("vendor.err", "w")
        subprocess.run(["cargo", "vendor", "--versioned-dirs"],
            stdout=v_out, stderr=v_err)
        dirs = subprocess.run(["ls", "vendor"], text=True, capture_output=True)
        # get list of all non-dev dependencies
        no_dev_dep_tree = subprocess.run(["cargo", "tree", "-e", "no-dev", "--prefix", "none", "--no-dedupe"], 
                capture_output=True, text=True)
        lines = no_dev_dep_tree.stdout.split("\n")
        non_dev_deps = []
        for line in lines:
            non_dev_deps.append(line.replace(" v", "-").replace(" (*)", ""))
        num_deps = len(dirs.stdout.split("\n")) - 1
        f_out = open("compile.out", "w")
        f_err = open("compile.err", "w")
        print("Compiling")
        subprocess.run(["cargo", "build", "--verbose", "--release"], #, apps.get(d).get("flag"), apps.get(d).get("name")], 
            text=True, stdout=f_out, stderr=f_err)
        f_out.close()
        f_err.close()

        fd = open("compile.out", 'r')
        print("Counting")
        ui = findTargetFiles(fd)
        f_out.close()
        dep_files_w_ui = []
        indirect = 0
        direct = 0
        for crate, lines in ui.items():
            if ".cargo/registry/src/github.com" in crate: 
                dep_files_w_ui.append(crate)
                indirect += len(lines)
            else: 
                direct += len(lines)

        dep_set = set()
        for dep_file in dep_files_w_ui:
            dep_set.add(dep_file.split("/")[7])
        for dep in dep_set: 
            if not dep in non_dev_deps: 
                print("removing dev dep: {}".format(dep_file))

        num_deps = len(set(non_dev_deps))
        deps_w_ui = len(dep_set)
        perc_w_ui = 100 * deps_w_ui / num_deps

        summ_total_uses.write("{} & {} & {} & {} & {} ({}\%)\n".format(d, direct, indirect, num_deps, deps_w_ui, perc_w_ui))
        summ_total_uses.flush()
        print(direct)
        print(indirect)
        # total deps
        print(num_deps)
        # deps w ui
        print(deps_w_ui)
        # percent of deps w ui
        print(perc_w_ui)

    summ_total_uses.close()
