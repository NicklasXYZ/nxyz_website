## NXYZ website deployment instructions

It is assumed that the following components are installed:
- [k3s](https://k3s.io/):
- [docker]https://www.docker.com/

### Build and push services

Assuming this repo `nxyz_website` has been cloned to the current directory enter into the `nxyz_website/services` directory. Build and push images to [dockerhub](https://hub.docker.com/):

```bash
cd nxyz_website/services
make build-all && make push-all
```

### Generate Kubernetes manifests

Generate all necessary manifests for deploying the built services:

```bash
# Go back to the `nxyz_website` root directory 
cd ..

# Install python dependencies
pip install -r requirements.txt

# Create kubernetes manifests
make all-manifests
```

### Apply Kubernetes manifests

Deploy the built services by applying the manifests that were placed in the `manifests` directory:

```bash
sudo k3s kubectl apply -f # Insert manifest directory here
# ... Change and apply additional manifests in directory 'extra_manifests' manually
```