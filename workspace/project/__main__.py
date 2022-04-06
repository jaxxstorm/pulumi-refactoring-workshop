"""An Azure RM Python Pulumi program"""

import pulumi
import typing
import clusternetwork
from pulumi_azure_native import network, resources, containerservice

config = pulumi.Config()
vnet_cidr = config.require("vnet_cidr")
subnet_cidr = config.require("subnet_cidr")

tags = {"owner": "workshop", "purpose": "pulumi_workshop"}

rg = resources.ResourceGroup("workshop", tags=tags)

nw = clusternetwork.ClusterNetwork(
    "workshop", clusternetwork.ClusterNetworkArgs(
        vnet_cidr=vnet_cidr, 
        subnet_cidr=subnet_cidr,
        resource_group_name=rg.name,
        tags=tags)
)

pulumi.export("resource_group_name", rg.name)
pulumi.export("subnet_id", nw.subnet.id)


