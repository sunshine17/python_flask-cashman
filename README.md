# Run with the manaul way(non-container)

## Start tha server

```shell
start.sh
```

# Run with the docker way

## Build the image locally

docker build -t cashman .

## Run the container in port 5000

```shell
docker run --name cashman \
    -d -p 5000:5000 \
    cashman 
```

# After the server is up, run some casual tests

## Fetch incomes from the dockerized instance

curl http://localhost:5000/incomes/

## Helper shell script for testing

```shell
./test-1.sh
```


