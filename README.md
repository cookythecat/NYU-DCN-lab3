# Usage & Grading Guidance 
## Preparation
### Build Images
Build image for Authorative Server:
```
cd <path to AS folder>
docker build -t as:latest .
```
And build images for the remaining 2 servers accordingly.
### Run Containers of the 3 Servers
```
docker network create mynet
docker run --network=mynet -it as
docker run --network=mynet -p 8080:8080 -it us
docker run --network=mynet -p 9090:9090 -it fs
```
### Obtain the IP of authoritative Server and Fibonacci Server
```
C:\Users\cooky> Docker ps
CONTAINER ID   IMAGE     COMMAND             CREATED          STATUS          PORTS                    NAMES
<fs_id>   fs        "python ./run.py"   5 minutes ago    Up 5 minutes    0.0.0.0:9090->9090/tcp   infallible_elbakyan
88bfd8b85fc1   us        "python ./run.py"   5 minutes ago    Up 5 minutes    0.0.0.0:8080->8080/tcp   stoic_edison
<as_id>   as        "python ./run.py"   15 minutes ago   Up 15 minutes   53533/udp                nostalgic_thompson
```
### Inject the IP of Fibonacci Server into Authorative Server's Storage
> Recommendation: Use Postman to send the below JSON body to 	`http://localhost:9090/register`
```
{
"hostname": "fibonacci.com",
"ip": <fs_ip>,
"as_ip": <as_ip>,
"as_port": "53533"
}
```

Record the `<fs_id>` and `as_id`, and then Run `docker inspect <server_id>` to retrieve the **IP** of <fs_id>` and `as_id.

## Feature Verification

### a. US responds to requests in path /fibonacci as specified above. 
> Recommendation: send http GET request to the following URL
```
http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=11&as_ip=<as_ip>&as_port=53533
```
### b. FS accepts a registration request in /register as specified above. 

> Recommendation: Use Postman to send the some JSON body to 	`http://localhost:9090/register`
```
{
"hostname": <A_NAME>,
"ip": <canomical IP>,
"as_ip": <as_ip>,
"as_port": "53533"
}
```

### c. FS responds to GET requests in /fibonacci. 
> Recommendation: Use Postman to send the some requests body to 	`http://localhost:9090/fibonacci?number=X`

### d. AS performs a registration requests as specified above. 

> Recommendation: Directly send UDP packet to AS
### e. AS provides DNS record for a given query as specified above
> Recommendation: Check the response of step d.
