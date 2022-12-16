#!/usr/bin/env python3

import aws_cdk as cdk

from cloudformation_cdk.cloudformation_cdk_stack import CloudformationCdkStack


app = cdk.App()
CloudformationCdkStack(app, "cloudformation-cdk")

app.synth()
