import pulumi
import pulumi_azure_native as azure_native

cluster = azure_native.containerservice.ManagedCluster("cluster",
    agent_pool_profiles=[azure_native.containerservice.ManagedClusterAgentPoolProfileArgs(
        count=1,
        enable_fips=False,
        kubelet_disk_type="OS",
        max_pods=50,
        mode="System",
        name="nodepool",
        orchestrator_version="1.21.9",
        os_disk_size_gb=30,
        os_disk_type="Ephemeral",
        os_sku="Ubuntu",
        os_type="Linux",
        type="VirtualMachineScaleSets",
        vm_size="Standard_DS3_v2",
        vnet_subnet_id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourceGroups/workshop0e2eb622/providers/Microsoft.Network/virtualNetworks/workshop44dc0dd6/subnets/workshop",
    )],
    dns_prefix="workshop0e2eb622",
    enable_rbac=True,
    identity=azure_native.containerservice.ManagedClusterIdentityArgs(
        type="SystemAssigned",
    ),
    identity_profile={
        "kubeletidentity": azure_native.containerservice.ManagedClusterPropertiesIdentityProfileArgs(
            client_id="0d34de6d-772a-4087-a7e9-fbeb38fd3e12",
            object_id="2587d780-833c-4b99-baed-765c6add0dfc",
            resource_id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourcegroups/MC_workshop0e2eb622_workshop-cluster4bdb372f_westus/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workshop-cluster4bdb372f-agentpool",
        ),
    },
    kubernetes_version="1.21.9",
    location="westus",
    network_profile=azure_native.containerservice.ContainerServiceNetworkProfileArgs(
        dns_service_ip="10.0.0.10",
        docker_bridge_cidr="172.17.0.1/16",
        load_balancer_profile=azure_native.containerservice.ManagedClusterLoadBalancerProfileArgs(
            effective_outbound_ips=[azure_native.containerservice.ResourceReferenceArgs(
                id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourceGroups/MC_workshop0e2eb622_workshop-cluster4bdb372f_westus/providers/Microsoft.Network/publicIPAddresses/8fb08152-9185-4c60-beea-970a6c30f061",
            )],
            managed_outbound_ips=azure_native.containerservice.ManagedClusterLoadBalancerProfileManagedOutboundIPsArgs(
                count=1,
            ),
        ),
        load_balancer_sku="Standard",
        network_plugin="kubenet",
        outbound_type="loadBalancer",
        pod_cidr="10.244.0.0/16",
        service_cidr="10.0.0.0/16",
    ),
    node_resource_group="MC_workshop0e2eb622_workshop-cluster4bdb372f_westus",
    resource_group_name="workshop0e2eb622",
    service_principal_profile=azure_native.containerservice.ManagedClusterServicePrincipalProfileArgs(
        client_id="msi",
    ),
    sku=azure_native.containerservice.ManagedClusterSKUArgs(
        name="Basic",
        tier="Free",
    ),
    tags={
        "owner": "workshop",
        "purpose": "pulumi_workshop",
    })