
The CDN-Transcode sample can be deployed with Kubernetes. 

### Kubernetes Setup

- Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster.   

- Optional: setup password-less access from the Kubernetes controller to each worker node (required by `make update`):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

- Start/stop services as follows:   

```
mkdir build
cd build
cmake ..
make
make update # optional for private docker registry
make volume
make start_kubernetes
make stop_kubernetes
```

---

The command ```make update``` uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url> ..`, to push images to the private registry after each build.  
- The `make volume` command creates local persistent volumes under the `/tmp` directory of the first two Kubernetes workers. This is a temporary solution for quick sample deployment. For scalability beyond a two-node cluster, consider rewriting the persistent volume scripts.

---

### See Also 

- [Helm Charts](helm/cdn-transcode/README.md)
- [CMake Options](../../doc/cmake.md)  
- [Reference Architecture](https://networkbuilders.intel.com/solutionslibrary/container-bare-metal-for-2nd-generation-intel-xeon-scalable-processor)   


