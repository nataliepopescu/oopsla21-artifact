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
docker run -it -p 8050:8050 --name artifact oopsla21-nader
```

Once in the docker container you can begin using the artifact.

## Step by Step Instructions

### Paper claims supported by artifact

All of the following commands will assume that you start in the root directory
of this repository. 

1. To reproduce Figure 1: 

```sh
$ cd figure1 && python3 tool.py --dir crates --compile --bench {num_runs} --local
```

Where we suggest that {num_runs} = 2 or 3 ({num_runs} == 1 takes about X time to finish). [TODO maybe 1 run is enough...]
Then you can visualize the results by running: 

```sh
$ python3 result_presenter.py
```

and opening the listed webpage in your browser.

1. To reproduce Table 1... 

1. To reproduce Figure 5...

1. To reproduce Figure 7 and all but the last column of Table 3, run: 

```sh
$ cd figure7 && python3 uncover_uncheckeds.py --root apps
```

which should take about 10 minutes to complete. 

1. To reproduce Table 4... 

1. To reproduce Figure 9...

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

1. Last column of Table 3...

1. Figure 8...
