# OOPSLA 2021 Artifact

## Getting Started Guide

1. [Install Docker](https://docs.docker.com/engine/install/) and start up the 
docker daemon, either 
[manually](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
or through the 
[system utility](https://docs.docker.com/config/daemon/#start-the-daemon-using-operating-system-utilities).

2. Build the docker image (TODO publish image so it can just be downloaded in this step): 

```sh
docker build --tag oopsla21-nader .
```

3. Run a docker container using the image you just built: 

```sh
docker run -it -p 8050:8050 --cap-add=sys_nice --name artifact oopsla21-nader
```

Once in the docker container you can begin using the artifact.

## Step by Step Instructions

### Paper claims supported by artifact

All of the following commands should be run in `~/nader/`. 
To print out options for running the script, run: 

```sh
$ python3 ExpDriver.py --help
```

1. To reproduce Figure 1: 

Old command: 

```sh
$ cd figure1 && python3 tool.py --dir crates --compile --bench <num_runs> --local
```

New command: 

```sh
$ python3 ExpDriver.py --genf1 --{fast/full} --bench <num_runs>
```

Where the expected durations for generating results for one library [fast] are as follows: 
   * 8 minutes to compile two versions of the library's benchmarks
   * 25 minutes to run one round of benchmarks x <num_runs>
   * <1 minute to aggregate results

And the expected durations for generating all results [full] are as follows: 
   * 50 minutes to compile two versions of each library's benchmarks
   * ?? minutes to run one round of benchmarks for all 7 libraries x <num_runs>
   * 1 minute to aggregate results

We suggest that <num_runs> == 2 or 3 to balance completion speed and precision. 
Visualize the results by running: 

Old command: 

```sh
$ python3 result_presenter.py
```

New command: 

```sh
$ python3 ExpDriver --viewf1 --{fast/full} --port <port>
```

and opening the first listed webpage (0.0.0.0:<port>) in your browser. The specified port should be the same as the one you passed to the `docker run` command earlier. 

1. To reproduce Table 1... 

1. To reproduce Figure 5...

1. To reproduce Figure 7 and all but the last column of Table 3, run: 

```sh
$ cd figure7 && python3 uncover_uncheckeds.py --root apps
```

which should take about 10 minutes to complete. 

1. To reproduce Table 4... 

```sh
cd data && ./create_silesia.sh
```

```sh
cd .. && python3 ExpDriver.py
```

1. To reproduce Figure 9...

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

1. Last column of Table 3...

1. Figure 8...
