"""An Azure RM Python Pulumi program"""

import pulumi
import typing
import pulumi_azuread as azuread
from pulumi_azure_native import network, resources, containerservice, managedidentity
import clusternetwork

config = pulumi.Config()
vnet_cidr = config.require("vnet_cidr")
subnet_cidr = config.require("subnet_cidr")

tags = {"owner": "lbriggs"}

rg = resources.ResourceGroup("workshop", tags=tags)

nw = clusternetwork.ClusterNetwork(
    "workshop",
    clusternetwork.ClusterNetworkArgs(
        vnet_cidr=vnet_cidr,
        subnet_cidr=subnet_cidr,
        resource_group_name=rg.name,
    ),
)

cluster = containerservice.ManagedCluster(
    "workshop-cluster",
    resource_group_name=rg.name,
    agent_pool_profiles=[
        containerservice.ManagedClusterAgentPoolProfileArgs(
            count=1,
            max_pods=50,
            mode="System",
            os_disk_size_gb=30,
            os_type="Linux",
            type="VirtualMachineScaleSets",
            vm_size="Standard_DS3_v2",
            vnet_subnet_id=nw.subnet.id,
            name="nodepool",
        )
    ],
    dns_prefix=rg.name,
    enable_rbac=True,
    identity=containerservice.ManagedClusterIdentityArgs(
        type="SystemAssigned",
    ),
    service_principal_profile=containerservice.ManagedClusterServicePrincipalProfileArgs(client_id="msi"),
)
