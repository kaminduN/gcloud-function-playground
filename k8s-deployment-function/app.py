from google.auth import compute_engine
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client


DEPLOYMENT_NAME = "hello-deployment"

def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="hello-server",
        image="gcr.io/google-samples/hello-app:1.0",
        ports=[client.V1ContainerPort(container_port=8080)])

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "hello"}),
        spec=client.V1PodSpec(containers=[container]))

    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=1,
        template=template)

    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))



def update_deployment(api_instance, deployment):
    # Update container replica count 
    deployment.spec.replicas = 3

    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=deployment)

    print("Deployment updated. status='%s'" % str(api_response.status))



def test_gke(request):
	
    request_json = request.get_json()
    print(request_json)

    project_id = "my-gcp-project"
    zone = "my-zone"
    cluster_id = "my-existing-cluster"

    credentials = compute_engine.Credentials()

    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    # Create a deployment object with client-python API.
    deployment = create_deployment_object()

    if request_json and 'create' in request_json:
        create_deployment(extensions_v1beta1, deployment)
        return f'create deployment!'
    elif request_json and 'update' in request_json:
        update_deployment(extensions_v1beta1, deployment)
        return f'update deployment!'        
    else:
        return f'nothing happens to cluster'

