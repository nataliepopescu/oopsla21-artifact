# We have original bc
# Need to generate a list of  remove-bc-exp.sh
import subprocess
import re
import os
import argparse
from numpy import median

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def runOneTest(bc_fname, arg=None):
    if arg is not None:
        out = subprocess.Popen([ROOT_PATH + '/exp.sh', bc_fname, arg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        out = subprocess.Popen([ROOT_PATH + '/exp.sh', bc_fname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    out, _ = out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes

    try:
        m = re.search(r'Time ([0-9,.]+)', out)
        # m = re.search(r'([0-9,]+) ns/iter', out)
        s = m.group(1)
        result  = float(s.strip())
        #s = s.replace(',', '')
        #result = int(s)
    except Exception:
        print(out)
        print("Run experiment failed")
        return None

    return result


def runExpWithName(exp_name, arg=None, test_times=10, getAllList=False):

    time_list = []
    for i in range(test_times):
        if arg is not None:
            out = subprocess.Popen([ROOT_PATH + '/runExp.sh',  exp_name, arg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            out = subprocess.Popen([ROOT_PATH + '/runExp.sh',  exp_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        out, _ = out.communicate()
        out = out.decode("utf-8")  # convert to string from bytes

        try:
            m = re.search(r'Time ([0-9,.]+)', out)
            # m = re.search(r'([0-9,]+) ns/iter', out)
            s = m.group(1)
            result  = float(s.strip())
            time_list.append(result)

            with open("exp.out", "w") as fd:
                fd.write(out)
            #s = s.replace(',', '')
            #result = int(s)
        except Exception:
            print(out)
            print("Run experiment failed")
            return None, None, None

    time_list.sort()
    # #r emove the first
    # time_list = time_list[2:]

    # # remove the last
    # time_list = time_list[:-2]

    median_run = median(time_list)
    shortest_run = time_list[0]
    longest_run = time_list[-1]
    # print("Median: ", median_run)
    # print("Long: ", longest_run)
    # print("Short: ", shortest_run)
    # print("All: ", time_list)

    if getAllList:
        return median_run, shortest_run, longest_run, time_list # sum(time_list) / len(time_list)
    else:
        return median_run, shortest_run, longest_run # sum(time_list) / len(time_list)

def argParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp-name", "-e",
            type=str, help="experiment name")
    parser.add_argument("--arg", "-a",
            type=str, default=None,
            help="argument for the exp binary")
    parser.add_argument("--test-times", "-t",
            type=int,
            default=5,
            help="times to run the experiment")
    args = parser.parse_args()
    return args.exp_name, args.arg, args.test_times


if __name__ == "__main__":
    exp_name, arg, test_times = argParse()
    median, shortest, longest = runExpWithName(exp_name, arg, test_times, False)
    print(test_times, "runs: median(", median, ") shortest(", shortest, "longest, (", longest, ")")
