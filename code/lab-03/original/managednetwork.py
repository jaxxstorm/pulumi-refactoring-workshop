import pulumi
from pulumi_azure_native import network


class ManagedNetworkArgs:
    def __init__(
        self,
        resource_group_name: pulumi.Input[str],
        vnet_cidr: pulumi.Input[str],
        subnet_cidr: pulumi.Input[str],
    ):
        self.vnet_cidr = vnet_cidr
        self.subnet_cidr = subnet_cidr
        self.resource_group_name = resource_group_name


class ManagedNetwork(pulumi.ComponentResource):
    vnet: network.VirtualNetwork
    subnet: network.Subnet

    def __init__(self, name: str, args: ManagedNetworkArgs, opts: pulumi.ResourceOptions = None):
        super().__init__("jaxxstorm:index:ManagedNetwork", name, {}, opts)

        self.vnet = network.VirtualNetwork(
            "workshop",
            address_space=network.AddressSpaceArgs(
                address_prefixes=[args.vnet_cidr],
            ),
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self, aliases=[pulumi.Alias(name="workshop", parent=None)])
        )

        self.subnet = network.Subnet(
            "workshop",
            virtual_network_name=self.vnet.name,
            resource_group_name=args.resource_group_name,
            address_prefix=args.subnet_cidr,
            opts=pulumi.ResourceOptions(parent=self.vnet, aliases=["urn:pulumi:dev::refactor-workshop-lab-01::azure-native:network:Subnet::workshop"])
        )
        
        self.register_outputs({
            "vnet": self.vnet,
            "subnet": self.subnet
        })
