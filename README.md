# osdi21-artifact

## Build Docker image

```sh
$ docker build --tag <image-tag>  .
```

This command will take about X time on a Y machine. 

TODO publish image so reviewers just have to download it. 

## Run Corvair in Container

```sh
$ docker run -it -p 8050:8050 --name <container-name> <image-tag>
...bencher_scrape# python3 tool.py --scrape 250 --compile --bench 32 --local
```

This command will take about W time on a Z machine. 

## Visualize Results in Container

While still in the container and once the above command has finished, run: 

```sh
...bencher_scrape# python3 result_presenter.py
```

and paste the URL into your browser to view the results. 
