"""An Azure RM Python Pulumi program"""

import pulumi
import typing
import pulumi_azuread as azuread
from pulumi_azure_native import network, resources, containerservice, managedidentity

config = pulumi.Config()
vnet_cidr = config.require("vnet_cidr")
subnet_cidr = config.require("subnet_cidr")

tags = {"owner": "lbriggs"}

rg = resources.ResourceGroup("workshop", tags=tags)

vnet = network.VirtualNetwork(
    "workshop",
    address_space=network.AddressSpaceArgs(
        address_prefixes=[vnet_cidr],
    ),
    resource_group_name=rg.name,
)

subnet = network.Subnet(
    "workshop", virtual_network_name=vnet.name, resource_group_name=rg.name, address_prefix=subnet_cidr
)

def id_to_dict(id_output) -> typing.Mapping[str, typing.Any]:
    my_dict = {}
    my_dict[id_output] = {}
    return my_dict

cluster_identity = managedidentity.UserAssignedIdentity(
    "workshop-useridentity",
    resource_group_name=rg.name,
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
            vnet_subnet_id=subnet.id,
            name="nodepool",
        )
    ],
    dns_prefix=rg.name,
    enable_rbac=True,
    identity=containerservice.ManagedClusterIdentityArgs(
        type="UserAssigned",
        user_assigned_identities=cluster_identity.id.apply(id_to_dict),
    ),
    service_principal_profile=containerservice.ManagedClusterServicePrincipalProfileArgs(client_id="msi"),
)
