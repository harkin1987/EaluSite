from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2
)


class CloudformationCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        #create the VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
            )
        #selected image
        amazon_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )
        #security group
        sg = ec2.SecurityGroup(
            self,
            id = "sg_cloudformationcdk",
            vpc = vpc,
            security_group_name = "sg_cloudformationcdk"
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443)
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80)
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv6(),
            connection=ec2.Port.tcp(443)
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv6(),
            connection=ec2.Port.tcp(80)
        )
        #execute userdata script
        shell = ec2.UserData.for_linux()
        shell.add_commands("sudo yum update -y",
        "sudo yum install -y httpd git",
        "sudo systemctl start httpd",
        "sudo systemctl enable httpd",
        "git clone https://github.com/harkin1987/EaluSite.git",
        "sudo cp -rT ./EaluSite/sitefiles/ /var/www/html/"
        )
        #create instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amazon_linux,
            vpc = vpc,
            security_group=sg,
            key_name='ealuweb',
            user_data=shell
            )
        
        
