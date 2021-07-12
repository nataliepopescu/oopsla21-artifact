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

Now you can begin using the artifact. 

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

--TODO copy usage message--
```

For generating Figure 7 and Table 3, for example, run the following: 

```sh
$ python3 ExpDriver --port <portB> [--full] --figure7table3
```

Expected running times for all experiments are listed here:  

   * Figure 1 [fast]: 20 minutes
   * Figure 1 [full]: ?
   * Table 1: ?
   * Figures 5 and 9 [fast]: ?
   * Figures 5 and 9 [full]: ?
   * Figure 7 and Table 3 [fast]: 2 minutes
   * Figure 7 and Table 3 [full]: 20 minutes
   * Table 4: ?
   * Figure 8: ?

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

1. Last column of Table 3...
