# Makefile used for automatically generating kubernetes manifests...

# Set the k3s kubeconfig file (it should be the server-side kubeconfig)
KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Set the output directory for all generated manifests
OUTPUT_DIR=manifests

ROOT_DIR=settings

# Set service settings files
NXYZ_LANDINGPAGE_SETTINGS=$(ROOT_DIR)/nxyz-landingpage-settings.conf

manifests-nxyz-landingpage:
	python k8smanifests.py \
	--config_file $(NXYZ_LANDINGPAGE_SETTINGS) \
	--service_name nxyz-landingpage \
	--kubeconfig $(KUBECONFIG) \
	--output_dir $(OUTPUT_DIR)

all-manifests: manifests-nxyz-landingpage

apply-manifests:
	sudo k3s kubectl apply -f $(manifests)/.
