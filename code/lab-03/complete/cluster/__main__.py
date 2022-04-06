"""An Azure RM Python Pulumi program"""

import pulumi
import typing
from pulumi_azure_native import managedidentity, containerservice
from pulumi_azure_native import resources

def id_to_dict(id_output) -> typing.Mapping[str, typing.Any]:
    my_dict = {}
    my_dict[id_output] = {}
    return my_dict

stack_ref = pulumi.StackReference("jaxxstorm/refactor-workshop-lab-01/dev")
resource_group_name = stack_ref.get_output("resource_group_name")
subnet_id = stack_ref.get_output("subnet_id")


cluster_identity = managedidentity.UserAssignedIdentity(
    "workshop-useridentity",
    resource_group_name=resource_group_name,
    opts=pulumi.ResourceOptions(import_="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourcegroups/workshop55f3b294/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workshop-useridentityb2893dee")
)

cluster = containerservice.ManagedCluster(
    "workshop-cluster",
    resource_group_name=resource_group_name,
    agent_pool_profiles=[
        containerservice.ManagedClusterAgentPoolProfileArgs(
            count=1,
            max_pods=50,
            mode="System",
            os_disk_size_gb=30,
            os_type="Linux",
            type="VirtualMachineScaleSets",
            vm_size="Standard_DS3_v2",
            vnet_subnet_id=subnet_id,
            name="nodepool",
        )
    ],
    dns_prefix=resource_group_name,
    enable_rbac=True,
    identity=containerservice.ManagedClusterIdentityArgs(
        type="UserAssigned",
        user_assigned_identities=cluster_identity.id.apply(id_to_dict),
    ),
    service_principal_profile=containerservice.ManagedClusterServicePrincipalProfileArgs(client_id="msi"),
    opts=pulumi.ResourceOptions(import_="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourcegroups/workshop55f3b294/providers/Microsoft.ContainerService/managedClusters/workshop-cluster2f8348c0")
)
