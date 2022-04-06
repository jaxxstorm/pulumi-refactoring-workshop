"""An Azure RM Python Pulumi program"""

import pulumi
import typing
import pulumi_azuread as azuread
from pulumi_azure_native import network, resources, containerservice, managedidentity
import managednetwork

config = pulumi.Config()
vnet_cidr = config.require("vnet_cidr")
subnet_cidr = config.require("subnet_cidr")

tags = {"owner": "lbriggs"}

rg = resources.ResourceGroup("workshop", tags=tags)

nw = managednetwork.ManagedNetwork(
    "workshop",
    managednetwork.ManagedNetworkArgs(
        vnet_cidr=vnet_cidr,
        subnet_cidr=subnet_cidr,
        resource_group_name=rg.name,
    ),
)

pulumi.export("resource_group_name", rg.name)
pulumi.export("subnet_id", nw.subnet.id)
