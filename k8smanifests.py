"""
Python script for automatically generating a subset of the necessary Kubernetes
manifests for the NYXZ website.

Resource: https://github.com/kubernetes-client/python/tree/master/kubernetes/docs

TODO: Simplify... Duplicate code can be collected in certain places.
"""
import os
import argparse
import yaml
from tempfile import TemporaryDirectory
from types import MethodType
from kubernetes import client
import configparser
import subprocess
import shutil

# Kubernetes manifests output directory
# The value is set in main()
OUTPUT_DIR = ""
 
def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None

def run_subprocess(commandline_args):
    """
    """
    print("::SUBPROCESS COMMANDLINE ARGS: ", commandline_args)
    s = subprocess.Popen(commandline_args, stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT, shell=True)
    (stdout_data, stderr_data) = s.communicate()
    print("::SUBPROCESS STDOUT          : ")
    for string in stdout_data.decode("utf-8").split("\n"):
        print(string)
    print("::SUBPROCESS STDERR          : ")
    for string in str(stderr_data).split("\n"):
        print(string)
    # Check the returncode to see whether the process terminated normally
    if s.returncode == 0:
        print("INFO: Subprocess exited normally with return code: " + str(s.returncode))
    else:
        print("INFO: Subprocess exited with non-zero return code: " + str(s.returncode))
        raise SystemExit

def parse_commandline_args(args_list = None):
    """ Setup, parse and validate given commandline arguments.
    """
    # Create main parser
    parser = argparse.ArgumentParser(description = "")
    add_parser_arguments(parser)
    # Parse commandline arguments
    args = parser.parse_args(args_list)
    return args

def add_required_parser_arguments(parser):
    parser.add_argument("-config_file", "--config_file",
        required = False,
        type = str,
        help = "Specify the name of the config file to parse.",
    )
    parser.add_argument("-xconfig_files", "--xconfig_files",
        required = False,
        default=None,
        type = str,
        help = "Specify an additional config file to parse.",
        nargs="+",
    )
    parser.add_argument("-account_name", "--account_name",
        required = False,
        default="nicklasxyz",
        type = str,
        help = "Specify a dockerhub account where docker images are stored.",
    )
    parser.add_argument("-service_name", "--service_name",
        required = True,
        type = str,
        help = "Specify the name of the service to generate files for."
    )
    parser.add_argument("-namespace", "--namespace",
        required = False,
        default="default",
        type = str,
        help = "Specify the name of the service to generate files for.",
    )
    parser.add_argument("-kubeconfig", "--kubeconfig",
        required = False,
        default = None,
        type = str,
        help = "Used by SealedSecrets. Specify the path to the KUBECONFIG " + \
            "of the target kubernetes cluster.",
    )
    parser.add_argument("-sealed_secrets_namespace", "--sealed_secrets_namespace",
        required = False,
        default = "sealed-secrets",
        type = str,
        help = "Used by SealedSecrets. Specify the namespace of the " + \
            "SealedSecrets controller.",
    )
    parser.add_argument("-output_dir", "--output_dir",
        required = False,
        default = "manifests",
        type = str,
        help = "Specify the output directory for the generated " + \
            "manifests.",
    )

def add_parser_arguments(parser):
    # Add required commandline arguments:
    add_required_parser_arguments(parser)

def parse_config(args):
    _args = [args.config_file]
    try:
        if args.xconfig_files is not None:
            _args.extend([f for f in args.xconfig_files])    
    except AttributeError:
        pass
    config = configparser.ConfigParser()
    try:
        config.read(_args)
        return config
    except IOError as e:
        print("INFO : File ", args.config_file, " not accessible!")
        print("Error: ", e)
        raise SystemExit

def _camelized_to_dict(self):
    """Override the default k8s object to_dict to camelize it's keys"""
    result = {}
    for attr, camel_attr in self.attribute_map.items():
        value = getattr(self, attr)

        if isinstance(value, list):
            result[camel_attr] = list(
                map(
                    lambda x: _camelized_to_dict(x) if hasattr(x, "to_dict") else x,
                    value,
                )
            )
        elif hasattr(value, "to_dict"):
            result[camel_attr] = _camelized_to_dict(value)
        elif isinstance(value, dict):
            result[camel_attr] = dict(
                map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict")
                    else item,
                    value.items(),
                )
            )
        else:
            # ignore None values - we don't need them for the output
            if value is not None:
                result[camel_attr] = value
    return result

def persistent_volume_claim_template(pvc_name, pvc_resources):
    pvc = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(
            name=pvc_name,
            labels={"io.service": pvc_name},
        ),
        spec=client.V1PersistentVolumeClaimSpec(
            # Use k3s native storage class for local path storage
            storage_class_name="local-path",
            access_modes=["ReadWriteOnce"],
            resources=pvc_resources,
        ),
    )
    return pvc

def deployment_template(
    service_name,
    image_name,
    image_version,
    container_ports=None,
    container_args=None,
    container_env_from=None,
    container_resources=None,
    container_volume_mounts=None,
    volumes=None,
    startup_probe=None,
    liveness_probe=None,
    lifecycle=None,
    security_context=None,
    host_network=False,
    container_replicas=1,
    ):
    # Configure Pod template container
    container = client.V1Container(
        name=service_name,
        image="{}:{}".format(image_name, image_version),
        ports=container_ports,
        args=container_args,
        env_from=container_env_from,
        resources=container_resources,
        volume_mounts=container_volume_mounts,
        startup_probe=startup_probe,
        liveness_probe=liveness_probe,
        lifecycle=lifecycle,
        security_context=security_context,
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(
            labels={"io.service": service_name},
        ),
        spec=client.V1PodSpec(
            containers=[container],
            volumes=volumes,
            host_network=host_network,
        ),
    )
    # Create the specification of the deployment
    spec = client.V1DeploymentSpec(
        replicas=container_replicas,
        template=template,
        selector={"matchLabels": {"io.service": service_name}},
        strategy=client.V1DeploymentStrategy(type="Recreate"),
    )
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=service_name),
        spec=spec,
    )
    return deployment

def service_template(service_name, service_type, service_ports):
    pvc = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=service_name,
            labels={"io.service": service_name},
        ),
        spec=client.V1ServiceSpec(
            type=service_type,
            ports=service_ports,
            selector={"io.service": service_name},
        ),
    )
    return pvc

def create_target_dir(dirname):
    # Create target directory & all intermediate directories if they do no exist
    try:
        os.makedirs(os.path.join(OUTPUT_DIR, dirname))
        print("--> Creating directory: " , dirname)
    except FileExistsError:
        pass

def to_yaml(k8s_object, filename, dirname):
    """Convert a k8s object to a yaml file"""
    create_target_dir(dirname)
    print("--> Creating file     : ", os.path.join(OUTPUT_DIR, dirname, filename))
    with open(os.path.join(OUTPUT_DIR, dirname, filename), "w+") as file:
        yaml.dump(
            k8s_object,
            file,
            default_flow_style=False
        )

def create_nxyz_service_manifests(
    config,
    account_name,
    service_name,
    parent_service_name=None,
    secret_ref_name=None
    ):
    """Generate k8s manifests pertaining to the 'nxyz' microservice."""
    port = int(config._sections.get("nxyz-landingpage").get("nginx_port"))

    ###
    ### Deployment
    ###
    k8s_deployment_obj = deployment_template(
        service_name=service_name,
        image_name=os.path.join(account_name, service_name),
        image_version="latest",
        container_replicas=2,
    )
    # Override the default to_dict method so we can update the k8s keys
    k8s_deployment_obj.to_dict = MethodType(_camelized_to_dict, k8s_deployment_obj)
    k8s_deployment_obj = k8s_deployment_obj.to_dict()
    to_yaml(k8s_deployment_obj, service_name + "-deployment.yaml", service_name)

    ###
    ### Service
    ###
    k8s_service_obj = service_template(
        service_name = service_name,
        service_type = "ClusterIP",
        service_ports = [
            client.V1ServicePort(
                name=str(port),
                # Port that is exposed by the service
                port=port,
                # Number or name of the port to access on the pods targeted by the service
                target_port=port,
            ),
        ]
    )
    # Override the default to_dict method so we can update the k8s keys
    k8s_service_obj.to_dict = MethodType(_camelized_to_dict, k8s_service_obj)
    k8s_service_obj = k8s_service_obj.to_dict()
    to_yaml(k8s_service_obj, service_name + "-service.yaml", service_name)


def checks():
    # Make sure the appropriate programs are installed
    required_programs = ["k3s"]
    for program in required_programs:
        if not is_tool(program):
            raise Exception("Program %r is not installed " % (program))
    
def main(account_name, config, args):
    global OUTPUT_DIR
    OUTPUT_DIR = args.output_dir
    if args.service_name == "nxyz-landingpage":
        service_name = args.service_name
        ###
        ### Create 'nxyz-landingpage' manifests
        ###
        create_nxyz_service_manifests(
            config=config,
            account_name=account_name,
            service_name=service_name,
        )

if __name__ == "__main__":
    # Run checks before generating files...
    checks()
    # Parse commandline arguments and configs
    args = parse_commandline_args()
    config = parse_config(args)
    # Generate manifests for a particular service
    main(args.account_name, config, args)
