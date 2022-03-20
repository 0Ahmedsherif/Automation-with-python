import boto3

client = boto3.client('eks', region_name='eu-west-3')
clusters = client.list_clusters()['clusters']

for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )
    cluster_info = response['cluster']  # var to avoid repetitive code
    # cluster_status = response['cluster']['status']  # not optimum way to write the code.
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']
    print(f"Cluster name: {cluster}\nStatus: {cluster_status}\nEndpoint: {cluster_endpoint}\n"
          f"Version: {cluster_version}")


