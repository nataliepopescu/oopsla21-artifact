# Source Level Nader
# Only convert get_unchecked(_mut) for now
import os
import subprocess
import pickle
import time
import argparse
import random
from regexify import convertFile
from ExpStats import runExpWithName
from ParseCallgrind import sortByHot, getColdLines
from tqdm.auto import tqdm

cargo_root=""
EXP_ARG=""
CLANG_ARGS=""
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def getUnsafeLines(fname):
    line_nums = []
    with open(fname, 'r') as fd:
        lines = fd.readlines()

    for idx, line in enumerate(lines):
        # if "get_unchecked(" in line or "get_unchecked_mut(" in line:
        if "get_unchecked" in line:
            line_nums.append(idx + 1)

    return line_nums


# for multiple file, actually modify the file in place
def genSourceExp(cargo_root, explore_name, exp_num, fnames, line_nums):
    os.chdir(cargo_root) # go to cargo_root

    # compile to original.bc
    dir_name = os.path.join(cargo_root, explore_name, "exp-" + str(exp_num))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    

    fname_lines = {}
    for (old_fname, line) in line_nums:
        if old_fname not in fname_lines:
            fname_lines[old_fname] = [line]
        else:
            fname_lines[old_fname].append(line)

    for old_fname in fnames:
        new_fname = old_fname[:-7] # remove .unsafe
        if old_fname in fname_lines:
            bcs = convertFile(old_fname, new_fname, fname_lines[old_fname])
        else:
            bcs = convertFile(old_fname, new_fname, [])

    p = subprocess.Popen([ROOT_PATH + "/oneGenFromSource_multifile.sh", "test_bc", CLANG_ARGS]) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.wait()
    os.chdir(dir_name)
    os.rename("../../exp.exe", "./exp.exe")

    # dump the unsafe lines
    with open("unsafe_lines.txt", "w") as fd:
        fd.writelines([fname + str(num) + "\n" for (fname, num) in line_nums])


def genSourceExpNB(cargo_root, explore_name, old_fname, new_fname, exp_num, line_nums):
    os.chdir(cargo_root) # go to cargo_root

    # compile to original.bc
    dir_name = os.path.join(cargo_root, explore_name, "exp-" + str(exp_num))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    os.chdir(dir_name)
    # convert and save to new file
    os.makedirs("./src", exist_ok=True)
    old_fname = os.path.join(cargo_root, old_fname)
    new_fname = os.path.join(dir_name, new_fname)
    convertFile(old_fname, new_fname, line_nums)

    # dump the unsafe lines
    with open("unsafe_lines.txt", "w") as fd:
        fd.writelines([str(num) + "\n" for num in line_nums])

    # Compile from source to binary
    p = subprocess.Popen([ROOT_PATH + "/oneGenFromSource.sh", "test_bc", CLANG_ARGS]) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.2)
    return p


# keep everything unsafe, try one safe
def genAllFirstRoundExp(cargo_root, old_fname, new_fname, all_line_nums):
    explore_abs = os.path.join(cargo_root, "explore-src-r1")

    child_processes = []
    for idx, line_num in enumerate(all_line_nums):
        test_line_nums = all_line_nums.copy()
        test_line_nums.remove(line_num)

        child_processes.append(genSourceExpNB(cargo_root, explore_abs, old_fname, new_fname, idx, test_line_nums))

    for p in child_processes:
        p.wait()


# keep everything safe, try one unsafe
def genAllOneUncheckRoundExp(cargo_root, old_fname, new_fname, all_line_nums):
    explore_abs = os.path.join(cargo_root, "explore-src-one-uncheck")

    child_processes = []
    for idx, line_num in enumerate(all_line_nums):
        test_line_nums = [line_num]

        child_processes.append(genSourceExpNB(cargo_root, explore_abs, old_fname, new_fname, idx, test_line_nums))

    for p in child_processes:
        p.wait()

# keep everything safe, add unsafe one by one
def genAllSecondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums):
    explore_abs = os.path.join(cargo_root, "explore-src-r2")

    test_line_nums = []
    child_processes = []
    for idx, line_num in enumerate(sorted_line_nums):
        test_line_nums.append(line_num)

        child_processes.append(genSourceExpNB(cargo_root, explore_abs, old_fname, new_fname, idx, test_line_nums))

    for p in child_processes:
        p.wait()

# Get the impact of each bounds check, different method
def oneUncheckedExp(cargo_root, old_fname, new_fname, all_line_nums, arg=None, test_times=5):
    genAllOneUncheckRoundExp(cargo_root, old_fname, new_fname, all_line_nums)

    time_list = []
    for idx, line_num in enumerate(tqdm(all_line_nums, leave=True)):
        dir_name = os.path.join(cargo_root, "explore-src-one-uncheck", "exp-" + str(idx))
        exp_name = os.path.join(dir_name, "exp.exe")
        os.chdir(dir_name)
        time_exp, _, _ = runExpWithName(exp_name, arg, test_times=test_times)
        if time_exp is None:
            exit()

        time_list.append(time_exp)

    impact_tuple = list(zip(all_line_nums, time_list))

    # ordered it in descending order
    impact_tuple.sort(key=lambda x: x[1], reverse=True)

    return impact_tuple

# Get the impact of each bounds check
def oneCheckedExp(cargo_root, old_fname, new_fname, all_line_nums, arg=None, test_times=5):
    genAllFirstRoundExp(cargo_root, old_fname, new_fname, all_line_nums)

    time_list = []
    for idx, line_num in enumerate(tqdm(all_line_nums, leave=True)):
        dir_name = os.path.join(cargo_root, "explore-src-r1", "exp-" + str(idx))
        exp_name = os.path.join(dir_name, "exp.exe")
        os.chdir(dir_name)
        time_exp, _, _ = runExpWithName(exp_name, arg, test_times=test_times)
        if time_exp is None:
            exit()

        time_list.append(time_exp)

    impact_tuple = list(zip(all_line_nums, time_list))

    # ordered it in descending order
    impact_tuple.sort(key=lambda x: x[1], reverse=True)

    return impact_tuple


# Get the impact of combined bounds check
def secondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums, arg=None, test_times=5):
    genAllSecondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums)

    cur_lines = []
    lines_list = []
    time_list = []
    top_error_list = [] # longer
    bottom_error_list = [] # shorter
    time_list_list = []

    for idx, line_num in enumerate(tqdm(sorted_line_nums, leave=True)):
        dir_name = os.path.join(cargo_root, "explore-src-r2", "exp-" + str(idx))
        exp_name = os.path.join(dir_name, "exp.exe")
        os.chdir(dir_name)
        time_exp, shortest_run, longest_run, all_time_list = runExpWithName(exp_name, arg, test_times=test_times, getAllList=True)
        if time_exp is None:
            exit()

        cur_lines.append(line_num)
        time_list.append(time_exp)
        top_error_list.append(longest_run - time_exp)
        bottom_error_list.append(time_exp - shortest_run)
        lines_list.append(cur_lines.copy())
        time_list_list.append(all_time_list)

    final_tuple = list(zip(lines_list, time_list, top_error_list, bottom_error_list, time_list_list))

    return final_tuple


def argParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cargo-root", "-r",
            metavar="path",
            type=str,
            help="root path of the cargo directory")
    parser.add_argument("--arg", "-a",
            type=str,
            help="argument for the exp binary")
    parser.add_argument("--output", "-o",
            type=str,
            default="final_results",
            help="output pickle name")
    parser.add_argument("--clang-arg", "-c",
            type=str,
            help="additional clang args")
    parser.add_argument("--test-times", "-t",
            metavar="path",
            type=int,
            default=5,
            help="times to run the experiment")
    parser.add_argument("--calout-fname", "-g",
            default="cal.out",
            type=str,
            help="times to run the experiment")
    args = parser.parse_args()
    return args.cargo_root, args.arg, args.output, args.clang_arg, args.test_times, args.calout_fname


def iterativeExplore(threshold, inital_unsafe_list, test_times=3, sensitivity=0.001):

    cur_unsafe = inital_unsafe_list.copy()
    cur_baseline = quickTestBrotli(cur_unsafe, arg=EXP_ARG, test_times=test_times)[1]
    print("Initial baseline:", cur_baseline)
    runs_cnt = 0
    round_cnt = 0

    while len(cur_unsafe) > 0 and sensitivity > 0 and cur_baseline * (1 + sensitivity) < threshold:
        runs_count_this_round = len(cur_unsafe)
        # remove line one by one and test
        next_unsafe = cur_unsafe.copy()

        # generating exps
        # print("Generating", len(cur_unsafe), "exps")
        quickTestBrotliGenAllRoundExp(cur_unsafe)

        # run exps
        min_time = -1
        min_idx = -1
        for idx, line in enumerate(cur_unsafe):
            # print("Testing with", len(cur_unsafe) - 1, "get_unchecked, with", line, "removed")
            exp_time = quickTestExpWithName(idx, test_times, 1)
            # print(exp_time)
            if min_time == -1 or exp_time < min_time:
                min_time = exp_time
                min_idx = idx

            # if the new time does not exceed threshold and sensitivity
            if exp_time < threshold and exp_time < cur_baseline * (1 + sensitivity):
                next_unsafe.remove(line)

        runs_cnt += runs_count_this_round
        round_cnt += 1
        removed_lines = len(cur_unsafe) - len(next_unsafe)
        if removed_lines == 0:
            if min_time != -1 and min_time < threshold:
                print("Force remove one in a round")
                next_unsafe.remove(cur_unsafe[min_idx])
            else:
                sensitivity = -1 # a hack to end the exploration
                print("End of exploration")

        cur_unsafe = next_unsafe
        # remeasure the baseline, using the best count
        cur_baseline = quickTestBrotli(cur_unsafe, arg=EXP_ARG, test_times=test_times)[1]

        print("### Round", round_cnt, ": ", runs_count_this_round, "runs,", len(cur_unsafe), "get_unchecked left"  )
        print("### New baseline:", cur_baseline)

    return cur_unsafe, cur_baseline

def quickTestBrotli(unsafe_lines, arg, test_times=5):
    old_fname = "src/lib.rs.unsafe"
    new_fname = "src/lib.rs"

    p = genSourceExpNB(cargo_root, "baseline", old_fname, new_fname, "quick-test", unsafe_lines)
    p.wait()
    print("binary generated")
    exp_name = os.path.join(cargo_root, "baseline", "exp-quick-test/exp.exe")

    quick_result= runExpWithName(exp_name, arg, test_times=test_times)
    return quick_result


# keep everything unsafe, try one safe
def quickTestBrotliGenAllRoundExp(all_line_nums):
    old_fname = "src/lib.rs.unsafe"
    new_fname = "src/lib.rs"
    explore_abs = os.path.join(cargo_root, "explore-src-quick-test")

    child_processes = []
    for idx, line_num in enumerate(all_line_nums):
        test_line_nums = all_line_nums.copy()
        test_line_nums.remove(line_num)

        child_processes.append(genSourceExpNB(cargo_root, explore_abs, old_fname, new_fname, idx, test_line_nums))

    for p in child_processes:
        p.wait()

# Get the impact of combined bounds check
def quickTestExpWithName(idx, test_times=5, option=0):
    arg = EXP_ARG
    dir_name = os.path.join(cargo_root, "explore-src-quick-test", "exp-" + str(idx))
    exp_name = os.path.join(dir_name, "exp.exe")
    os.chdir(dir_name)
    time_exp = runExpWithName(exp_name, arg, test_times=test_times)
    # time_exp, shortest_run, longest_run = runExpWithName(exp_name, arg, test_times=test_times)
    # option 0, median, option 1, shortest, option 2 longest
    return time_exp[option]


# explorer
def explore(unsafe_time, initial_threshold, step, initial_unsafe_lines, total_unsafe_count):
    initial_unsafe_baseline  = unsafe_time
    final_unsafe = initial_unsafe_lines
    threshold = initial_threshold

    threshold_unsafe_map = {}
    safecount_speed_map = {}
    while len(final_unsafe) > 0:
        threshold_time = unsafe_time[0] * (1 + threshold)
        final_unsafe, final_baseline = iterativeExplore(threshold_time, final_unsafe)
        print("{:.2f}".format(threshold * 100) + "%", final_unsafe, final_baseline)
        threshold_unsafe_map[threshold] = final_unsafe.copy()
        safecount_speed_map[total_unsafe_count- len(final_unsafe)] = (initial_unsafe_baseline / final_baseline) - 1
        threshold += step

    return threshold_unsafe_map, safecount_speed_map


def runNader(cargo_root_, arg, pickle_name, clang_arg, test_times, calout_fname, quick_run=False):
    global cargo_root
    global EXP_ARG
    global CLANG_ARGS

    cargo_root = cargo_root_

    EXP_ARG = arg
    if not pickle_name.endswith("pkl"):
        pickle_name += ".pkl"

    if clang_arg is not None:
        CLANG_ARGS = clang_arg

    old_fname = "src/lib.rs.unsafe"
    new_fname = "src/lib.rs"

    # get all lines with unsafe
    os.chdir(cargo_root)
    line_nums = getUnsafeLines(old_fname)

    total_unsafe_count = len(line_nums)
    print("Running Nader on ", total_unsafe_count, " bounds checks")

    # all safe baseline
    print("Prep 1/4: Getting safe baseline (several minutes)")
    p = genSourceExpNB(cargo_root, "baseline", old_fname, new_fname, "safe", [])
    p.wait()
    exp_name = os.path.join(cargo_root, "baseline", "exp-safe/exp.exe")
    safe_time = runExpWithName(exp_name, arg, test_times=test_times)
    print("Safe baseline:", safe_time)

    # all unsafe baseline
    print("Prep 2/4: Getting unsafe baseline (several minutes)")
    p = genSourceExpNB(cargo_root, "baseline", old_fname, new_fname, "unsafe", line_nums)
    p.wait()
    exp_name = os.path.join(cargo_root, "baseline", "exp-unsafe/exp.exe")
    unsafe_time = runExpWithName(exp_name, arg, test_times=test_times)
    print("Unsafe baseline:", unsafe_time)

    # remove cold baseline
    hot_lines = line_nums.copy()
    rs_fname = "src/lib.rs"
    cold_lines = getColdLines(hot_lines, calout_fname, 1, single_file=rs_fname)
    if cold_lines is None:
        print("Cold parsing failed")
        exit()

    for i in cold_lines:
        hot_lines.remove(i)

    hot_lines = sortByHot(hot_lines, calout_fname, single_file=rs_fname)
    hot_lines.extend(cold_lines)
    # print("Hot code has", len(hot_lines))
    # p = genSourceExpNB(cargo_root, "baseline", old_fname, new_fname, "hot", hot_lines)
    # p.wait()
    # exp_name = os.path.join(cargo_root, "baseline", "exp-hot/exp.exe")
    # hot_time = runExpWithName(exp_name, arg, test_times=test_times)
    # print("Hot baseline:", hot_time)

    if quick_run:
        hot_lines = hot_lines[:10]
        line_nums = hot_lines

    # Get one-checked priority
    print("Prep 3/4: Getting one-checked priority (~30 mins)")
    impact_tuple_one_check = oneCheckedExp(cargo_root, old_fname, new_fname, line_nums, arg, test_times)

    results = {"impact_tuple": impact_tuple_one_check,
            "unsafe_baseline": unsafe_time, "safe_baseline": safe_time}
    os.chdir(cargo_root)

    with open(pickle_name + ".tmp", "wb") as fd:
        pickle.dump(results, fd)
    print("Partial result dumped (one unchecked)")
    # end of one checked

    # Get one-unchecked priority
    print("Prep 4/4: Getting one-unchecked priority (~30 mins)")
    impact_tuple_one_uncheck = oneUncheckedExp(cargo_root, old_fname, new_fname, line_nums, arg, test_times)

    results = {"impact_tuple": impact_tuple_one_check, "impact_tuple_one_uncheck": impact_tuple_one_uncheck,
            "unsafe_baseline": unsafe_time, "safe_baseline": safe_time}
    os.chdir(cargo_root)

    with open(pickle_name + ".tmp", "wb") as fd:
        pickle.dump(results, fd)
    print("Partial result dumped (one unchecked)")
    # end of one uncheck

    # Exp 1: sorted by from random
    print("Exp 1/4: Get random performance (might take up to 2 hours)")
    sorted_line_nums = line_nums.copy() 
    random.shuffle(sorted_line_nums)
    final_tuple_by_random = secondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums, arg, test_times)

    # Exp 2: sorted by from one checked
    print("Exp 2/4: Get one-checked performance (might take up to 2 hours)")
    sorted_line_nums = [x[0] for x in impact_tuple_one_check]
    final_tuple_by_one_checked = secondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums, arg, test_times)


    # Exp 3: sorted by from one unchecked
    print("Exp 3/4: Get one-unchecked performance (might take up to 2 hours)")
    impact_lines = [i[0] for i in impact_tuple_one_uncheck]
    impact_lines.reverse()
    sorted_line_nums = impact_lines
    final_tuple_by_one_unchecked = secondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums, arg, test_times)

    # Exp 4: sorted by hotness
    print("Exp 4/4: Get hotness performance (might take up to 2 hours)")
    sorted_line_nums = hot_lines
    final_tuple_by_hotness = secondRoundExp(cargo_root, old_fname, new_fname, sorted_line_nums, arg, test_times)

    # Dump Final Result
    results = {"impact_tuple": impact_tuple_one_check, "impact_tuple_one_uncheck": impact_tuple_one_uncheck,
            "final_tuple_one_checked": final_tuple_by_one_checked, "final_tuple_one_unchecked": final_tuple_by_one_unchecked,
            "final_tuple_hotness": final_tuple_by_hotness, "final_tuple_random": final_tuple_by_random,
            "unsafe_baseline": unsafe_time, "safe_baseline": safe_time}
    os.chdir(cargo_root)

    with open(pickle_name, "wb") as fd:
        pickle.dump(results, fd)

    threshold_unsafe_map, safecount_speed_map = explore(unsafe_time, initial_threshold=0.005, step=0.005, initial_unsafe_lines=hot_lines[:41], total_unsafe_count=total_unsafe_count)

    os.chdir(cargo_root)
    with open("threshold_unsafe_map.pkl", "wb") as fd:
        pickle.dump({"threshold_unsafe": threshold_unsafe_map, "safecount_speed": safecount_speed_map}, fd)


if __name__ == "__main__":
    cargo_root, arg, pickle_name, clang_arg, test_times, calout_fname = argParse()

    runNader(cargo_root, arg, pickle_name, clang_arg, test_times, calout_fname)

