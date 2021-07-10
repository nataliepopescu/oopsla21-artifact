from scripts.ExpStats import runExpWithName
from scripts.Nader import genSourceExp
from scripts.Nader import runNader
import subprocess
import os
import filecmp

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def getUnsafeLines(directory):
    line_nums = []

    rs_files = subprocess.run(["find", directory, "-name", "*.rs.unsafe", "-type", "f"], 
            capture_output=True, text=True)
    filelist = rs_files.stdout.split()

    for fname in filelist:
        with open(fname, 'r') as fd:
            lines = fd.readlines()

        for idx, line in enumerate(lines):
            # if "get_unchecked(" in line or "get_unchecked_mut(" in line:
            if "get_unchecked" in line:
                line_nums.append((fname, idx + 1))

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

    # Generate unsafe version
    fnames = set([i for i, _ in line_nums])
    genSourceExp(bmark_path, "baseline", "unsafe", fnames, line_nums)
    
    genSourceExp(bmark_path, "baseline", "safe", fnames, [])

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


def endToEnd(bmark_path, arg=None, threshold=0.03, skip_callgrind=True):
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
        calout_fname = ROOT_PATH + "/example-results/cal.out.original"
    else:
        print("preparing hotness file")
        calout_fname = genHotness(bmark_path, "test_bc", arg)

    print("Running Nader on", bmark_path)
    runNader(cargo_root_=bmark_path, arg=arg, pickle_name="test.pkl", clang_arg=None, p2_src=None, test_times=5, calout_fname=calout_fname)

if __name__ == "__main__":
    cwd = os.getcwd()
    endToEnd("{}/brotli-expanded/".format(cwd), "{}/data/silesia-5.brotli".format(cwd))
