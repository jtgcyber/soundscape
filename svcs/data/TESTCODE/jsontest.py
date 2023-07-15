
import argparse
from functools import cmp_to_key
import json
import os
import re
import asyncio
import subprocess
import time
import uuid
import semver

from kubescape import SoundscapeKube
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.graphrbac import GraphRbacManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient

with open('/home/johng/soundscape/svcs/data/test.json') as file:
    output=json.load(file)

print("\\n")
print(output)
print("\\n")

orchestrators = output['values']
if True:
    orchestrators = filter(lambda x: not x['isPreview'], orchestrators)
kube_versions = map(lambda o: str(o['version']), orchestrators)
kube_versions = sorted(kube_versions, key=cmp_to_key(semver.cmp), reverse=True)

print(kube_versions[0])