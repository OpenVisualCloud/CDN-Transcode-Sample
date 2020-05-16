
The CDN Transcode Sample is an Open Visual Cloud software stack with all required open source ingredients well integrated to provide out-of-box CDN media transcode service, including live streaming and video on demand. It also provides docker-based media delivery software development environment upon which developer can easily build their specific applications.  

### Prerequisites:

The Sample assumes that you have a ready-to-use Kubernetes cluster environment with `helm` to manage the applicatoin deployment.  

### Build:

```bash
mkdir build
cd build
cmake ..
make
```

### Create Shared Volumes:

```bash
make volume
```

The `make volume` command creates local persistent volumes under the /tmp directory of the first two Kubernetes workers. This is a temporary solution for quick sample deployment. For scalability beyond a two-node cluster, consider rewriting the `mkvolume.sh` script.

`make volume` uses `scp` to copy volumes to the Kubernetes workers, assuming that the Kubernetes master can password-less access to the Kubernetes workers.  

### Start/Stop Sample:

```bash
make start_helm
make stop_helm
```

