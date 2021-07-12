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
docker run -it -p <portA>:<portB> --cap-add=sys_nice --name artifact oopsla21-nader
```

4. Test that the artifact works by running: 

```sh
$ python3 ExpDriver.py --all --port <portB>
```

This command should complete in under an hour. We explain what it does in more 
detail in the next section. 

## Step by Step Instructions

### Paper claims supported by artifact

All of the following commands should be run from the `~/nader/` directory. 
Running all experiments fully takes almost two days to complete. 
We have therefore implemented a fast path that can run all experiments 
(on fewer libraries and applications) and finishes in under an hour. 
Our driver runs the fast path by default, so to run the full version of experiments, 
run: 

```sh
$ python3 ExpDriver.py --full [OPTIONS] --port <portB>
```

Where <portB> should be the same as the second one passed to `docker run`.

To run the __fast__ path on _all_ experiments, run: 

```sh
$ python3 ExpDriver.py --all --port <portB>
```

To run the __full__ path on _all_ experiments, run: 

```sh
$ python3 ExpDriver.py --all --full --port <portB>
```

To run individual experiments, simply replace `--all` with the flag corresponding 
to the desired experiment, found by running: 

```sh
$ python3 ExpDriver.py --help

  ...
  --figure1           generate figure 1
  --table1            generate table 1
  --figure59          generate figures 5 and 9
  --figure7table3     generate figure 7 and table 3
  --table4            generate table 4
  --figure8           generate figure 8
  ...
```

For generating Figure 7 and Table 3, for example, run the following: 

```sh
$ python3 ExpDriver --port <portB> [--full] --figure7table3
```

Expected running times for all experiments on a 
2.3 GHz Dual-Core Intel Core i5 Macbook Pro
are listed here:  

| | Figure 1 | Table 1 | Figures 5 and 9 | Figure 7 and Table 3 | Table 4 | Figure 8 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fast | 20 min | | | 2 min | | | |
| Full | 7 hrs | | 5 hrs | 20 min | | | |

TODO explain how to view results

TODO expected outputs? a.k.a. results we've already generated (examples)

TODO any warnings that are safe to be ignored 

TODO how to explain {claims} are supported by artifact? Explain how to interpret results
- generated results are analogous to those in the paper

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

1. Last column of Table 3...

1. [Maybe] Figure 8...
