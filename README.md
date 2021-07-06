# oopsla21-artifact

## Build Docker image

```sh
$ docker build --tag <image-tag>  .
```

This builds our versions of LLVM and the Rust compiler so will likely take 
a few hours to complete.

TODO publish image so reviewers just have to download it. 

## Run NADER in Container

```sh
$ docker run -it -p 8050:8050 --name <container-name> <image-tag>
root/...:~/bencher_scrape# python3 tool.py --scrape 250 --compile --bench 32 --local
```

This command requires _ of space and will take about W time on a Z machine. 

## Visualize Results in Container

While still in the container and once the above command has finished, run: 

```sh
root/...:~/bencher_scrape# python3 result_presenter.py
```

and paste the URL into your browser to view the results. 
