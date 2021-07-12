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
docker run -it -p <port>:<port> --cap-add=sys_nice --name artifact oopsla21-nader
```

Once in the docker container you can begin using the artifact.

## Step by Step Instructions

### Paper claims supported by artifact

All of the following commands should be run from the `~/nader/` directory. 
Running all experiments fully takes 1-2 days total. 
We have therefore implemented a "fast path" that can run all experiments 
on fewer libraries/applications, which finishes in under an hour. 
Our driver will run the fast path by default, so if you wish to run the full 
experiments, run: 

```sh
$ python3 ExpDriver.py --full [OPTIONS] --port <port>
```

Where <port> should be the same as the one you passed to `docker run`.

To run the fast path on all experiments, run: 

```sh
$ python3 ExpDriver.py --all --port <port>
```

To run the full path on all experiments, run: 

```sh
$ python3 ExpDriver.py --all --full --port <port>
```

We describe how to run each individual experiment below. 

1. To reproduce Figure 1: 

```sh
$ python3 ExpDriver.py --figure1 {--full} --port <port>
```

The figure 1 fast path should take around 20 minutes to complete. 
TODO what to do with the generated plots...

1. To reproduce Table 1: 

```sh
$ python3 ExpDriver.py --table1 {--full} --port <port>
```

1. To reproduce Figures 5 and 9: 

```sh
$ python3 ExpDriver.py --figure59 {--full} --port <port>
```

1. To reproduce Figure 7 and all but the last column of Table 3, run: 

```sh
$ python3 ExpDriver.py --figure7table3 {--full} --port <port>
```

This will only take a couple of minutes to complete. 

1. To reproduce Table 4: 

```sh
$ python3 ExpDriver.py --table4 {--full} --port <port>
```

1. To reproduce Figure 8:

```sh
$ python3 ExpDriver.py --figure8 {--full} --port <port>
```

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

1. Last column of Table 3...
