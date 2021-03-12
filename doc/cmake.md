
### CMake Options:

Use the following definitions to customize the building process:   
- **REGISTRY**: Specify the URL of the privcay docker registry.    
- **PLATFORM**: Specify the target platform: `Xeon` , `XeonE3` or `SG1`.
- **SCENARIO**: Specify the sample scenario(s): `transcode` or `cdn`.  
- **NLIVES**: Specify the number of live streaming services in the deployment. 
- **NVODS**: Specify the number of vod transcoding services in the deployment.  

### Examples:   

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DNVODS=1 -DPLATFORM=Xeon ..
```

```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=cdn ..
```

### Make Commands:

- **build**: Build the sample (docker) images.  
- **update**: Distribute the sample images to the worker nodes.  
- **start/stop_kubernetes**: Start/stop the sample orchestrated by Kubernetes.   
- **start/stop_helm**: Start/stop the sample orchestrated by Kubernetes Helm Charts.   

