# OOPSLA 2021 Artifact

## System Requirements

Linux OS (we've tested on Ubuntu 18.04 STD)

Docker version 20+

40GB memory

## Getting Started

To install Docker on Linux, run: 

$ sudo apt-get update
$ sudo apt-get install -y docker-ce

Make sure the docker daemon is running, then download the compressed artifact 
from the provided link and load it like so: 

$ docker load < oopsla21ae.tar.gz

This might take some time. Once done, start the docker container:

$ docker run -it --cap-add=sys_nice --name artifact oopsla21ae

And finally test that the artifact works: 

$ python3 ExpDriver.py --figure1 --figure59 --figure7table3

This should complete in about an hour.

## Step by Step Instructions

Any commands should be run from /home/oopsla21ae/. 
Running all experiments fully takes almost two days to complete, so
we have implemented a fast path that can run all experiments 
(on fewer libraries and applications) in about three hours. 
The fast path is enabled by default, so use the '--full' flag 
to run the full versions of experiments: 

$ python3 ExpDriver.py [OPTIONS] --full

To run _all_ experiments, run: 

$ python3 ExpDriver.py --all [--full]

Expected running times for all experiments on 
[this](https://www.clemson.cloudlab.us/portal/show-nodetype.php?type=c6320) 
machine, running Ubuntu 18.04 STD and Docker 20.10.2,
are listed here:  

| | Figure 1 | Table 1 | Figures 5 and 9 | Figure 7 and Table 3 | Table 4 | Figure 8 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fast | 20 min | - | 40 min | 2 min | - | - | 1 hr |
| Full | 7 hrs | 20 min | 9 hrs | 20 min | 1 hr | 1 hr | ~19 hrs |

### Generating results

To run individual experiments, simply replace '--all' with the corresponding 
experiment's flag, found by running: 

$ python3 ExpDriver.py --help

  ...
  --figure1           generate figure 1
  --table1            generate table 1
  --figure59          generate figures 5 and 9
  --figure7table3     generate figure 7 and table 3
  --table4            generate table 4
  --figure8           generate figure 8
  ...

To generate Figure 7 and Table 3, for example, run the following: 

$ python3 ExpDriver.py --figure7table3 [--full]

### Viewing results

Some expected output is in /home/oopsla21ae/example-results/; you can compare your generated plots to those as a sanity check. 
Our artifact generates PDFs that can be copied out of the docker container using
[docker cp](https://docs.docker.com/engine/reference/commandline/cp/): 

$ docker cp <container_id>:/home/oopsla21ae/images/ .

- To get the <container_id> of a _running_ container, run: 

$ docker container ps

  CONTAINER ID     IMAGE        COMMAND  CREATED  STATUS   PORTS   NAMES
  <container_id>   oopsla21ae   ...      ...      ...              artifact

- To get the <container_id> of a _stopped_ container, run: 

$ docker container ps -a

Descriptions of each generated PDF file in /home/oopsla21ae/images/ are listed in the following subsections. Once the generated PDFs have been copied locally, reviewers can view them using their favorite PDF viewer.

In general, the figures and tables produced here are analogous to the figures and 
tables presented in the paper, but we describe how to interpret results in more 
detail below. 

#### Figure 1 Expectations

Generated files: 
  figure1_all.pdf
  figure1_histogram.pdf
  figure1_hurt.pdf
  figure1_improved.pdf
  figure1_insignificantly_affected.pdf

figure1_histogram.pdf is analogous to Figure 1 in the paper: 
- Clustering around the vertical speedup == 1 line shows that the overhead of checked indexing is insignificant in most cases (~65% of benchmarks)
- The left tail depicts benchmarks where checked indexing did have significant overhead (~24% of benchmarks)
- The right tail depicts benchmarks where checked indexing, surprisingly, improves performance (~11% of benchmarks)

figure1_all.pdf contains the same information available in figure1_histogram.pdf but shows it in a slightly different way: 
- Bars clustered around the horizontal speedup == 1 line represent the benchmarks where the overhead of checked indexing is insignificant (~65% of benchmarks)
- Bars below the line represent benchmarks where checked indexing does have significant overhead (~24% of benchmarks)
- Bars above the line represents benchmarks where checked indexing, surprisingly, improves performance (~11% of benchmarks)

figure1_hurt.pdf zooms in on the ~24% of benchmarks where we expect checked indexing to have significant overhead. 

figure1_improved.pdf zooms in on the ~11% of benchmarks where we expect checked indexing to, surprisingly, improve performance. 

figure1_insignificantly_affected.pdf zooms in on the ~65% of benchmarks where we expect checked indexing to have insignificant overhead. 

#### Table 1 Expectations

No generated files. 

The three contexts are: 

  1. A baseline context: rustc 1.52, compression level = 5
  2. A different workload: rustc 1.52, compression level = 11
  3. A different compiler: rustc 1.46, compression level = 5

See [this](https://github.com/nataliepopescu/oopsla21-artifact#paper-claims-not-supported-by-artifact) section for why we do not reproduce the "different architecture" column. 

We expect the overhead of checked indexing to be around: 

$ python3 ExpDriver.py --table1
  Getting overheads for baseline context... [Context 1]
          Overhead == 0.0852062889815508
  Getting overheads for different workload... [Context 2]
          Overhead == 0.05165770297643811
  Getting overheads for different compiler... [Context 3]
          Overhead == 0.1482833160361338

The difference in overheads of checked indexing across these three contexts 
shows that developers cannot attribute a flat cost to checked indexing in 
every context they are used. 
Furthermore, we expect reviewers to have different results if any part of 
their underlying context (architecture, operating system and version, etc) is 
different, as this is exactly the point we are trying to make. 

#### Figures 5 and 9 Expectations

Generated files: 
  figure5.pdf
  figure9.pdf

figure5.pdf compares four different heuristics for reintroducing bounds checks 
in the rust-brotli benchmark: 

- Random
- Hotness
- One-checked slowdown
- One-unchecked speedup

With more "successful" heuristics reintroducing more bounds checks within a 
certain threshold, i.e. hugging the black 0% line the longest. 
We expect the random heuristic (red line) to reintroduce the smallest 
number of bounds checks before hitting the threshold, then one-unchecked (yellow line). 
Hotness (orange line) should perform best until the very end, where it is surpassed by 
one-checked (blue line). 

figure9.pdf compares the random and hotness heuristics to NADER's combined-heuristic 
approach on the rust-brotli benchmark. Similarly to figure5.pdf, the hotness line 
(orange) should be above the random line (red). At the far right of the graph, a 
dark blue line shows when NADER switches from the hotness heuristic to the 
one-checked heuristic, and should be above both hotness and random lines. 

#### Figure 7 and Table 3 Expectations

Generated files: 
  figure7.pdf
  table3.pdf
                                                                                     
figure7.pdf shows, for each of the 27 applications we selected, the number of 
direct and indirect unchecked indexing used in a bar chart. On average, we expect 
there to be 86 times more indirect unchecked indexing than direct 
unchecked indexing, which would be evidenced by bar charts with much more (about 86 
times more, per application) red than blue. 

table3.pdf presents the results from figure7.pdf in a table, and also includes, 
per application, the total number of dependencies and the number of dependencies 
with at least one use of unchecked indexing. Please see the table3.pdf in 
/home/oopsla21ae/example-results/ for approximate expectations. We use Cargo.lock files in effort to keep dependency versions constant but they are not always respected; reviewers may thus observe some slight variation in these results due to different dependency versions. 

#### Table 4 Expectations

No generated files. 

The four steps of NADER are: 

1. Check for any unchecked indexing

2. Compare original binary with one generated after converted all unchecked indexing to checked indexing

3. Measure overhead of all converted checked indexing (applicable to current context only)

4. If significant, run NADER to only reintroduce bounds checks up to a threshold

We expect the applications we evaluate to stop after the following steps: 

- tantivy after step 2 (binaries are identical)
- rage after step 2 (binaries are identical)
- swc after step 3 (checked indexing overhead == 0.13%)
- warp after step 3 (checked indexing overhead == -0.31%)
- iron after step 3 (checked indexing overhead == -2.01%)
- RustPython after step 3 (checked indexing overhead == 0.71%)
- zola after step 3 (checked indexing overhead == 0.25%)
- COST after step 4 (not generated here, see [figure 8](https://github.com/nataliepopescu/oopsla21-artifact#figure-8-expectations))
- rust-brotli after step 4 (not generated here, see [figure 9](https://github.com/nataliepopescu/oopsla21-artifact#figures-5-and-9-expectations))

#### Figure 8 Expectations

Generated files: 
  figure8.pdf
  
figure8.pdf presents the same information as figure9.pdf (excluding the 
random line) for the COST benchmark instead of rust-brotli. Specifically, 
the dark blue line at the far right of the graph shows when NADER switches 
from the hotness heuristic to the one-checked heuristic and should be above 
the orange hotness line. 

### Paper claims _not_ supported by artifact

1. The "different architecture" column in Table 1 is not supported by our artifact because 
the reviewers may not have access to two or more different architectures on which to 
run our experiments. 

2. The last column of Table 3 is also not supported by our artifact because it was 
the result of a manual process. We proceeded with applications that had 
reasonable synthetic profiling workloads, although there is room for a more 
rigorous process of elimination here. 

### Functional Badge Requirements
                                                                                          
- Artifact supports all major claims made by paper (outlined in this document by the Figures and Tables)
- Artifact documents detailed steps for result reproduction and lists any potential deviations from what the paper claims

Deviations: 

- All but Figure 7 and Table 3 are performance results and will vary, but we describe trends and patterns to look for
- A full evaluation takes almost 19 hours, but we offer reviewers a fast path that can complete in about three hours

### Reusable Badge Requirements

- Future researchers can run this artifact on more libraries and applications by cloning their source code
- Future researchers building off this artifact can do so by adding new benchmarks and their arguments
- Future researchers can directly modify /home/oopsla21ae/scripts/Nader.py to improve its exploration algorithm
- Artifact source code can be reused as separate components much in the same way as the individual plots are generated 
- Others can learn about our benchmarking and large-scale application analysis techniques
- Others can extend the artifact beyond bounds checks to other code patterns by modifying /home/oopsla21ae/scripts/regexify.py
