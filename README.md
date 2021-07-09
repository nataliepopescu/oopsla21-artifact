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

1. To reproduce Figure 1...

1. To reproduce Table 1... 

1. To reproduce Figure 5...

1. To reproduce Figure 7 (TODO and Table 3?)
   1. Hello
   1. World

1. To reproduce Table 4... 

1. To reproduce Figure 9...

### Paper claims _not_ supported by artifact

1. "Different Architecture" column in Table 1...

2. Figure 8...
