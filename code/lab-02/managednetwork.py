import pulumi
from pulumi_azure_native import network


class ManagedNetworkArgs:
    def __init__(
        self,
        vnet_cidr: pulumi.Input[str],
        subnet_cidr: pulumi.Input[str],
        rg_name: pulumi.Input[str],
    ):
        self.vnet_cidr = vnet_cidr
        self.subnet_cidr = subnet_cidr
        self.rg_name: rg_name


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
            resource_group_name=args.rg_name,
        )

        self.subnet = network.Subnet(
            "workshop",
            virtual_network_name=self.vnet.name,
            resource_group_name="foo",
            address_prefix=args.subnet_cidr,
        )
        
        self.register_outputs({
            "vnet": self.vnet,
            "subnet": self.subnet
        })
