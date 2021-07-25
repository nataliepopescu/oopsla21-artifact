import sys
sys.path.append('./scripts')
from scripts.ExpStats import runExpWithName
from scripts.Nader import genSourceExp, runOnlyNader
from scripts.Nader import runNader
from scripts.ResultPresenter import genFig5, genFig9, genFig8
import subprocess
import os
import filecmp
import shutil
import argparse

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def getUnsafeLines(directory, isBrotli=False):
    line_nums = []

    rs_files = subprocess.run(["find", directory, "-name", "*.rs.unsafe", "-o", "-name", "*.rs", "-type", "f"], 
            capture_output=True, text=True)
    filelist = rs_files.stdout.split()
    filelist = [fname.replace(directory, '') for fname in filelist]

    for fname in filelist:
        need_convert = False
        write_fname = fname
        if fname.endswith(".rs"):
            if fname + ".unsafe" in filelist:
                continue
            else:
                need_convert = True
                write_fname = fname + ".unsafe"

        with open(fname, 'r') as fd:
            lines = fd.readlines()

        found_unsafe = False
        for idx, line in enumerate(lines):
            # if "get_unchecked(" in line or "get_unchecked_mut(" in line:
            if "get_unchecked" in line:
                line_nums.append((write_fname, idx + 1))
                found_unsafe = True
        if need_convert and found_unsafe:
            shutil.move(fname, fname + ".unsafe")

    return line_nums

def genHotness(bmark_path, bin_name, arg):
    os.chdir(bmark_path)
    print("Generating hotness info with Callgrind")
    out = subprocess.Popen([ROOT_PATH + '/scripts/genHotness.sh', bin_name, arg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _  =out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes

    return bmark_path + "baseline/exp-genHotness/cal.out"


def genUncheckedReport(bmark_path):
    # get all lines with unsafe
    os.chdir(bmark_path)

    line_nums = getUnsafeLines(bmark_path)

    line_nums_str = [str(a) + " " + str(b) for a, b in line_nums]
    with open("unsafe_report.txt", "w") as fd:
        fd.writelines("\n".join(line_nums_str))

    return line_nums

def convertAndCompareBinaries(bmark_path, line_nums):
    os.chdir(bmark_path)

    fnames = set([i for i, _ in line_nums])
    # Generate unsafe version
    genSourceExp(bmark_path, "baseline", "safe", fnames, [])
    genSourceExp(bmark_path, "baseline", "unsafe", fnames, line_nums)

    # Compare binary
    ret = filecmp.cmp(bmark_path + "/baseline/exp-unsafe/exp.exe", bmark_path + "/baseline/exp-safe/exp.exe")
    return ret

def getPerfDiff(bmark_path, arg):
    os.chdir(bmark_path)

    time_exp_unsafe, _, _ = runExpWithName("baseline/exp-unsafe/exp.exe", arg, 5)
    print("Unsafe time: ", time_exp_unsafe)

    time_exp_safe, _, _ = runExpWithName("baseline/exp-safe/exp.exe", arg, 5)
    print("Safe time: ", time_exp_safe)

    return (time_exp_safe - time_exp_unsafe) / time_exp_unsafe

def genTable1():
    baseline = []
    workload = []
    compiler = []

    # Baseline
    print("Generating -Baseline- column...")
    bmark_path = ROOT_PATH + "/brotli-expanded/"
    arg = ROOT_PATH + "/data/silesia-5.brotli"
    line_nums = genUncheckedReport(bmark_path)
    convertAndCompareBinaries(bmark_path, line_nums)
    for i in range(10): 
        diff = getPerfDiff(bmark_path, arg)
        baseline.append(diff)
    print("\tOverhead == {}".format(sum(baseline)/10))

    # Different workload (compression level == 11, instead of 5)
    print("Generating -Different Workload- column...")
    arg = ROOT_PATH + "/data/silesia-11.brotli"
    for i in range(10): 
        diff = getPerfDiff(bmark_path, arg)
        workload.append(diff)
    print("\tOverhead == {}".format(sum(workload)/10))

    # rustc 1.46.0
    print("Generating -Different Compiler- column...")
    arg = ROOT_PATH + "/data/silesia-5.brotli"
    subprocess.run(["/home/.cargo/bin/rustup", "override", "set", "nightly-2020-08-27-x86_64-unknown-linux-gnu"])
    convertAndCompareBinaries(bmark_path, line_nums)
    for i in range(10): 
        diff = getPerfDiff(bmark_path, arg)
        compiler.append(diff)
    print("\tOverhead == {}".format(sum(compiler)/10))
    subprocess.run(["/home/.cargo/bin/rustup", "override", "unset"])

def genFigure1(root, quick_run=False):
    if full_run: 
        cratedir = "crates_full"
    else: 
        cratedir = "crates_fast"

    os.chdir(os.path.join(root, "figure1"))
    subprocess.run(["python3", "tool.py", "--dir", cratedir, 
            "--compile", "--bench", "3", "--local", "-g"])
    os.chdir(os.path.join(root, "figure1"))
    subprocess.run(["mv", "figure1_all.pdf", os.path.join(root, "images/")]) 
    subprocess.run(["mv", "figure1_histogram.pdf", os.path.join(root, "images/")]) 
    subprocess.run(["mv", "figure1_hurt.pdf", os.path.join(root, "images/")]) 
    subprocess.run(["mv", "figure1_improved.pdf", os.path.join(root, "images/")]) 
    subprocess.run(["mv", "figure1_insignificantly_affected.pdf", os.path.join(root, "images/")]) 
    os.chdir(root)

def genFigure7Table3(root, quick_run=False):
    if full_run: 
        suffix = "full"
    else: 
        suffix = "fast"

    os.chdir(os.path.join(root, "figure7"))
    subprocess.run(["python3", "uncover_uncheckeds.py", "--root", "apps_{}".format(suffix)])
    
    f7_from_path = os.path.join(root, "figure7", "apps_{}".format(suffix), "figure7.pdf")
    f7_to_path = os.path.join(root, "images") #, "figure7_{}.pdf".format(suffix))
    subprocess.run(["mv", f7_from_path, f7_to_path])

    t3_from_path = os.path.join(root, "figure7", "apps_{}".format(suffix), "table3.pdf")
    t3_to_path = os.path.join(root, "images") #, "table3_{}.pdf".format(suffix))
    subprocess.run(["mv", t3_from_path, t3_to_path])

    os.chdir(root)

def genFig8WithCOST(quick_run=False):
    if not os.path.exists(ROOT_PATH + "/exp-results"):
        os.mkdir(ROOT_PATH + "/exp-results")
    # prepare by vendoring
    print("Preparing COST vendor")
    out = subprocess.Popen([ROOT_PATH + '/scripts/prepareCOST.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out.wait()
    endToEnd("COST", ROOT_PATH + "/COST/" , "hilbert " + ROOT_PATH + "/data/soc-LiveJournal1 4847571", 0.02, False)


## Generate brotli figs (Fig5 and Fig9)
def genFig5and9(quick_run=False):
    #print("Running Nader on brotli, generating fig 5 and 9")
    bmark_path = ROOT_PATH + "/brotli-expanded/"
    arg = ROOT_PATH + "/data/silesia-5.brotli"
    calout_fname = ROOT_PATH + "/example-results/cal.out.brotli"
    runNader(cargo_root_=bmark_path, arg=arg, pickle_name="brotli.pkl", clang_arg=None, test_times=5, calout_fname=calout_fname, quick_run=quick_run)
    if not os.path.exists(ROOT_PATH + "/exp-results"):
        os.mkdir(ROOT_PATH + "/exp-results")
    shutil.move(bmark_path + "brotli.pkl", ROOT_PATH + "/exp-results/brotli.pkl")
    shutil.move(bmark_path + "threshold_unsafe_map.pkl", ROOT_PATH + "/exp-results/brotli-map.pkl")

    if not os.path.exists(ROOT_PATH + "/images"):
        os.mkdir(ROOT_PATH + "/images")
    print("Generating plots")
    genFig5(ROOT_PATH + "/exp-results", "brotli", ROOT_PATH + "/images/figure5.pdf")

    # use test.pkl to generate Fig 5
    genFig9(ROOT_PATH + "/exp-results", "brotli", ROOT_PATH + "/images/figure9.pdf")

def genTable4(): 
    subprocess.run(["./scripts/table4.sh"])


def endToEnd(bmark_name, bmark_path, arg=None, threshold=0.03, skip_callgrind=True):
    print("Step 1: Generating unchecked report")
    line_nums = genUncheckedReport(bmark_path)

    if len(line_nums) == 0:
        print("No unsafe usage, abort!")
        return
    else:
        print(len(line_nums), " unsafe usages, continue")

    print("Step 2: Convert unsafe to safe and compare binaries")
    ret = convertAndCompareBinaries(bmark_path, line_nums)

    if ret:
        print("Binaries are the same, abort!")
        return
    else:
        print("Binaries are different, continue!")

    print("Step 3: Identifying performance impact")
    perf_diff = getPerfDiff(bmark_path, arg)
    if perf_diff < threshold:
        print("Performance difference lower than threshold: ", threshold, ", abort!")
        return
    else:
        print("Performance difference higher than threshold: ", threshold, ", continue!")

    print("Step 4: Running Nader")

    if skip_callgrind:
        calout_fname = ROOT_PATH + "/example-results/cal.out." + bmark_name
    else:
        print("preparing hotness file")
        calout_fname = genHotness(bmark_path, "test_bc", arg)

    if "brotli" in bmark_path:
        isBrotli = True
    else:
        isBrotli = False
    runOnlyNader(cargo_root_=bmark_path, arg=arg, pickle_name=bmark_name+ ".pkl", clang_arg=None, test_times=10, calout_fname=calout_fname, isBrotli=isBrotli)
    shutil.move(bmark_path + "/" + bmark_name + ".pkl", ROOT_PATH + "/exp-results/" + bmark_name + ".pkl")
    shutil.move(bmark_path + "/threshold_unsafe_map.pkl", ROOT_PATH + "/exp-results/" + bmark_name + "-map.pkl")
    genFig8(ROOT_PATH + "/exp-results", bmark_name, ROOT_PATH + "/images/figure8.pdf")


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", "-a",
        action="store_true",
        required=False,
        help="generate all tables and figures")
    parser.add_argument("--figure1",
        action="store_true",
        required=False,
        help="generate figure 1")
    parser.add_argument("--table1",
        action="store_true",
        required=False,
        help="generate table 1")
    parser.add_argument("--figure59",
        action="store_true",
        required=False,
        help="generate figures 5 and 9")
    parser.add_argument("--figure7table3",
        action="store_true",
        required=False,
        help="generate figure 7 and table 3")
    parser.add_argument("--table4",
        action="store_true",
        required=False,
        help="generate table 4")
    parser.add_argument("--figure8",
        action="store_true",
        required=False,
        help="generate figure 8")
    parser.add_argument("--full", "-f",
        action="store_true",
        required=False,
        help="run the full version of plot generation instead of the fast version")
    args = parser.parse_args()
    return args.all, args.figure1, args.table1, args.figure59, args.figure7table3, args.table4, args.figure8, args.full


if __name__ == "__main__":
    gen_all, gen_f1, gen_t1, gen_f59, gen_f7t3, gen_t4, gen_f8, full_run = arg_parse()
    root = os.getcwd()

    quick_run = False if full_run else True
        
    # Figure 1
    if gen_all or gen_f1: 
        genFigure1(root, quick_run=quick_run)
    
    # Table 1
    if gen_all or gen_t1: 
        genTable1()

    # Figure 5 and 9
    if gen_all or gen_f59: 
        genFig5and9(quick_run=quick_run)
        
    # Figure 7 and Table 3
    if gen_all or gen_f7t3: 
        genFigure7Table3(root, quick_run=quick_run)
        
    # Table 4
    if gen_all or gen_t4: 
        genTable4()

    # Figure 8
    if gen_all or gen_f8: 
        genFig8WithCOST()

