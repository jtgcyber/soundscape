THIS IS THE PYTHON SCRIPT COMMAND AND ARGS TO BE RUN UNDER /soundscape/svcs/data

python soundscape_provision.py --subscription $AZURE_SUBSCRIPTION_ID --name "soundscape-poc" --resource-group "soundscape" --keyvault-name "jtgTestKV" --location "uksouth" --scale "test" --service-version "0.1" --azure-container-registry-name "jtgacr" --container-registry-RG "containerregistrytest" --kubernetes-version "1.27.1"

THESE ARE THE HELM COMMANDS CREATED BY THE SCRIPT AND DEPLOYED - BEEN USING FOR TESTING PURPOSES. A TLS CERTIFICATE RETRIEVED FROM AZURE KEYVAULT IS THE DEFAULT CONFIGURATION AS PER SOUNDSCAPE /svcs/data/soundscape/other/nginx-csi-patch which mounts the TLS CERT in the ingress container.

 helm upgrade -i --namespace soundscape soundscape-service soundscape --set soundscapeImageVersion=V1.0 --set containerRegistry=jtgacr.azurecr.io --set keyVault=jtgTestKV --set tenantId=b7133142-7e0e-48b3-90d8-ef7b5a7d6219 --set subscription_id=25eaed77-dc73-4d69-af3e-e475d5edb52c

 helm upgrade -i soundscape-ingress ingress-nginx/ingress-nginx  --namespace soundscape  --set controller.podLabels.aadpodidbinding=soundscape-identity --set-string controller.extraArgs.enable-ssl-chain-completion=false --set controller.image.digest=null --set controller.allowSnippetAnnotations=false --set controller.replicaCount=2 --set controller.service.loadBalancerIP=20.68.180.126 --set controller.service.externalTrafficPolicy=Local --set controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-dns-label-name=soundscape-poc-aks-soundscape  
 
 -f soundscape/other/nginx-csi-patch.yaml belongs to end of the ingress

 --set controller.podLabels.aadpodidbinding=soundscape-identity  belongs to helm nginx 


 --version 4.1.3

 Set the DSN as a kubernetes secret and use keyvault for the certificate secret.

 update create kube secret

Running Command:
 ['az', 'account', 'list-locations', '--output', 'none']
Running Command:
 ['az', 'ad', 'signed-in-user', 'show', '--output', 'json']
Running Command:
 ['az', 'role', 'assignment', 'list', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--assignee', 'john.greig_outlook.com#EXT#@johngreigoutlook.onmicrosoft.com', '--output', 'json']
TASK: Validated running as 'Owner' role
Running Command:
 ['az', 'version', '--output', 'json']
Running Command:
 ['az', 'feature', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--name', 'EnablePodIdentityPreview', '--namespace', 'Microsoft.ContainerService', '--output', 'json']
Running Command:
 ['az', 'feature', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--name', 'PodSubnetPreview', '--namespace', 'Microsoft.ContainerService', '--output', 'json']
Running Command:
 ['az', 'extension', 'show', '--name', 'aks-preview', '--output', 'json']
Running Command:
 ['az', 'provider', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--namespace', 'Microsoft.Compute', '--output', 'json']
Running Command:
 ['az', 'provider', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--namespace', 'Microsoft.OperationsManagement', '--output', 'json']
Running Command:
 ['az', 'provider', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--namespace', 'Microsoft.PolicyInsights', '--output', 'json']
Running Command:
 ['az', 'provider', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--namespace', 'Microsoft.Capacity', '--output', 'json']
Running Command:
 ['az', 'provider', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--namespace', 'Microsoft.Insights', '--output', 'json']
TASK: Created Resource group 'soundscape' in 'uksouth'
TASK: Service version '0.1'
TASK: Determine tenant: STARTED
Running Command:
 ['az', 'account', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--output', 'json']
TASK: Determine tenant: DONE
TASK: check kubernetes cluster name free: STARTED
Running Command:
 ['az', 'aks', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'soundscape-poc-aks', '--output', 'none']
TASK: check kubernetes cluster name free: DONE
TASK: setup environment: STARTED
TASK: create {cluster, pod} managed identity: STARTED
TASK: create virtual network and subnets: STARTED
Running Command:
 ['az', 'network', 'vnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--location', 'uksouth', '--name', 'soundscape-poc-vnet', '--resource-group', 'soundscape', '--address-prefixes', '10.0.0.0/8', '--output', 'none']
Running Command:
 ['az', 'identity', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--name', 'soundscape-poc-micluster', '--output', 'json']
Running Command:
 ['az', 'identity', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--name', 'soundscape-poc-mipod', '--output', 'json']
TASK: create {cluster,pod} managed identity: DONE
TASK: allow pod mi to retrieve certs from key vault: STARTED
Running Command:
 ['az', 'keyvault', 'set-policy', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--name', 'jtgTestKV', '--spn', '98ed6372-1157-4e07-ab0d-5c8634b18193', '--certificate-permissions', 'get', '--key-permissions', 'get', '--secret-permissions', 'get', '--output', 'none']
Unable to find user with spn '98ed6372-1157-4e07-ab0d-5c8634b18193'
Unable to get object id from principal name.
Running Command:
 ['az', 'network', 'vnet', 'subnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--vnet-name', 'soundscape-poc-vnet', '--name', 'soundscape-poc-vnet-podsnet', '--address-prefixes', '10.240.0.0/16', '--output', 'json']
Running Command:
 ['az', 'network', 'vnet', 'subnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--vnet-name', 'soundscape-poc-vnet', '--name', 'soundscape-poc-vnet-nodesnet', '--address-prefixes', '10.241.0.0/16', '--output', 'json']
TASK: allow pod mi to retrieve certs from key vault: DONE
Running Command:
 ['az', 'network', 'vnet', 'subnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--vnet-name', 'soundscape-poc-vnet', '--name', 'soundscape-poc-vnet-cmnsnet', '--address-prefixes', '10.242.0.0/16', '--output', 'json', '--disable-private-endpoint-network-policies', 'true']
Running Command:
 ['az', 'network', 'vnet', 'subnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--vnet-name', 'soundscape-poc-vnet', '--name', 'soundscape-poc-vnet-pgsnet', '--address-prefixes', '10.243.0.0/16', '--output', 'json', '--delegations', 'Microsoft.DBforPostgreSQL/flexibleServers', '--service-endpoints', 'Microsoft.Storage']
TASK: create virtual network and subnets: DONE
TASK: create private dns zone for postgres: STARTED
Running Command:
 ['az', 'network', 'private-dns', 'zone', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'soundscape-poc-db.privatelink.postgres.database.azure.com', '--output', 'none']
TASK: get keyvault access info: STARTED
Running Command:
 ['az', 'keyvault', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--name', 'jtgTestKV', '--output', 'json']
TASK: get keyvault access info: DONE
TASK: create private dns zone for keyvault: STARTED
Running Command:
 ['az', 'network', 'private-dns', 'zone', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'privatelink.vaultcore.azure.net', '--output', 'none']
TASK: get container registry docker access info: STARTED
TASK: get container registry docker access info: DONE
TASK: create private dns zone for acr: STARTED
Running Command:
 ['az', 'network', 'private-dns', 'zone', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'privatelink.azurecr.io', '--output', 'none']
TASK: create private dns zone for postgres: DONE
TASK: create private dns zone for keyvault: DONE
TASK: link private dns zone for keyvault to vnet: STARTED
Running Command:
 ['az', 'network', 'private-dns', 'link', 'vnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--registration-enabled', 'false', '--virtual-network', 'soundscape-poc-vnet', '--zone-name', 'privatelink.vaultcore.azure.net', '--name', 'soundscape-poc-kv-link', '--output', 'none']
TASK: create private dns zone for acr: DONE
TASK: link private dns zone for acr to vnet: STARTED
Running Command:
 ['az', 'network', 'private-dns', 'link', 'vnet', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--registration-enabled', 'false', '--virtual-network', 'soundscape-poc-vnet', '--zone-name', 'privatelink.azurecr.io', '--name', 'soundscape-poc-cr-link', '--output', 'none']
TASK: link private dns zone for keyvault to vnet: DONE
TASK: create keyvault private endpoint: STARTED
Running Command:
 ['az', 'network', 'private-endpoint', 'create', '--name', 'soundscape-poc-kv-endpt', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--vnet-name', 'soundscape-poc-vnet', '--subnet', 'soundscape-poc-vnet-cmnsnet', '--private-connection-resource-id', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/testKVRG/providers/Microsoft.KeyVault/vaults/jtgTestKV', '--group-id', 'vault', '--connection-name', 'soundscape-poc-kv-endpt', '--output', 'json']
TASK: link private dns zone for acr to vnet: DONE
TASK: create acr private endpoint: STARTED
Running Command:
 ['az', 'network', 'private-endpoint', 'create', '--name', 'soundscape-poc-cr-endpt', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--vnet-name', 'soundscape-poc-vnet', '--subnet', 'soundscape-poc-vnet-cmnsnet', '--private-connection-resource-id', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/containerregistrytest/providers/Microsoft.ContainerRegistry/registries/jtgacr', '--group-id', 'registry', '--connection-name', 'soundscape-poc-cr-endpt', '--output', 'json']
Running Command:
 ['az', 'network', 'nic', 'show', '--ids', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/networkInterfaces/soundscape-poc-cr-endpt.nic.c5d39cde-11e5-4315-a8df-543bb79705c7', '--output', 'json']
Running Command:
 ['az', 'network', 'nic', 'show', '--ids', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/networkInterfaces/soundscape-poc-kv-endpt.nic.e48a4f2b-5931-4944-9fae-b251f6c32308', '--output', 'json']
TASK: create keyvault private endpoint: DONE
TASK: create endpoint dns record in keyvault dns zone: STARTED
NAME: jtgtestkv
TASK:   jtgtestkv A 10.242.0.4
Running Command:
 ['az', 'network', 'private-dns', 'record-set', 'a', 'add-record', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--zone-name', 'privatelink.vaultcore.azure.net', '--record-set-name', 'jtgtestkv', '-a', '10.242.0.4', '--output', 'none']
TASK: create acr private endpoint: DONE
TASK: create endpoint dns record in acr dns zone: STARTED
NAME: jtgacr.uksouth.data
TASK:   jtgacr.uksouth.data A 10.242.0.5
Running Command:
 ['az', 'network', 'private-dns', 'record-set', 'a', 'add-record', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--zone-name', 'privatelink.azurecr.io', '--record-set-name', 'jtgacr.uksouth.data', '-a', '10.242.0.5', '--output', 'none']
TASK: create endpoint dns record in keyvault dns zone: DONE
NAME: jtgacr
TASK:   jtgacr A 10.242.0.6
Running Command:
 ['az', 'network', 'private-dns', 'record-set', 'a', 'add-record', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--zone-name', 'privatelink.azurecr.io', '--record-set-name', 'jtgacr', '-a', '10.242.0.6', '--output', 'none']
TASK: create endpoint dns record in acr dns zone: DONE
TASK: setup environment: DONE
TASK: assign roles to cluster managed identity: STARTED
Running Command:
 ['az', 'role', 'assignment', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--role', 'Network Contributor', '--assignee', 'e6a40e63-3e9f-4720-a40b-286fb9e79648', '--scope', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/virtualNetworks/soundscape-poc-vnet/subnets/soundscape-poc-vnet-nodesnet', '--output', 'none']
TASK: assign roles to cluster managed identity: DONE
TASK: create resources in parallel: STARTED
TASK:   create kubernetes cluster: STARTED
Running Command:
 ['az', 'aks', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--name', 'soundscape-poc-aks', '--generate-ssh-keys', '--node-count', '1', '--node-vm-size', 'Standard_DS3_v2', '--os-sku', 'AzureLinux', '--load-balancer-sku', 'standard', '--auto-upgrade-channel', 'node-image', '--enable-addons', 'monitoring,azure-keyvault-secrets-provider,azure-policy', '--enable-secret-rotation', '--attach-acr', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/containerregistrytest/providers/Microsoft.ContainerRegistry/registries/jtgacr', '--enable-managed-identity', '--assign-identity', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourcegroups/soundscape/providers/Microsoft.ManagedIdentity/userAssignedIdentities/soundscape-poc-micluster', '--enable-pod-identity', '--network-plugin', 'azure', '--vnet-subnet-id', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/virtualNetworks/soundscape-poc-vnet/subnets/soundscape-poc-vnet-nodesnet', '--pod-subnet-id', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/virtualNetworks/soundscape-poc-vnet/subnets/soundscape-poc-vnet-podsnet', '--output', 'none', '--kubernetes-version', '1.27.1', '--auto-upgrade-channel', 'rapid']
TASK:   create database: STARTED
Running Command:
 ['az', 'postgres', 'flexible-server', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--location', 'uksouth', '--name', 'soundscape-poc-db', '--admin-user', 'osm', '--tier', 'GeneralPurpose', '--sku-name', 'Standard_D2s_v3', '--subnet', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/soundscape/providers/Microsoft.Network/virtualNetworks/soundscape-poc-vnet/subnets/soundscape-poc-vnet-pgsnet', '--private-dns-zone', 'soundscape-poc-db.privatelink.postgres.database.azure.com', '--storage-size', '128', '--version', '13', '--tags', 'soundscapedb=true', '--output', 'json', '--only-show-errors']
The behavior of this command has been altered by the following extension: aks-preview
AAD role propagation done[############################################]  100.0000%TASK:   create kubernetes cluster: DONE took 226.44s
Running Command:
 ['az', 'postgres', 'flexible-server', 'parameter', 'set', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--server-name', 'soundscape-poc-db', '--name', 'azure.extensions', '--value', 'postgis,hstore', '--output', 'none']
configuration_name is not a known attribute of class <class 'azure.mgmt.rdbms.postgresql_flexibleservers.models._models_py3.Configuration'> and will be ignored
TASK:   create database: DONE - took 304.29s
TASK: create resources in parallel: DONE
Running Command:
 ['kubectl', 'apply', '-f', '/tmp/tmppo_51m15']
Command failed with exit code 1
Standard error:
Unable to connect to the server: dial tcp: lookup soundscape-soundscape-25eaed-i0obwhyz.hcp.uksouth.azmk8s.io on 127.0.0.53:53: no such host

Running Command:
 ['az', 'aks', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'soundscape-poc-aks', '--query', 'nodeResourceGroup', '-o', 'tsv']
WARNING: The behavior of this command has been altered by the following extension: aks-preview
TASK: assign roles to pod managed identity: STARTED
Running Command:
 ['az', 'group', 'show', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--name', 'MC_soundscape_soundscape-poc-aks_uksouth', '--output', 'json']
Running Command:
 ['az', 'role', 'assignment', 'create', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--role', 'Reader', '--assignee', '98ed6372-1157-4e07-ab0d-5c8634b18193', '--scope', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourceGroups/MC_soundscape_soundscape-poc-aks_uksouth', '--output', 'none']
TASK: assign roles to pod managed identity: DONE
TASK: create aad pod identity: STARTED
Running Command:
 ['az', 'aks', 'pod-identity', 'add', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--cluster-name', 'soundscape-poc-aks', '--namespace', 'soundscape', '--name', 'soundscape-identity', '--identity-resource-id', '/subscriptions/25eaed77-dc73-4d69-af3e-e475d5edb52c/resourcegroups/soundscape/providers/Microsoft.ManagedIdentity/userAssignedIdentities/soundscape-poc-mipod', '--output', 'none']
AAD role propagation done[############################################]  100.0000%
Wait 30 seconds for identity role assignment propagation.
TASK: create aad pod identity DONE
TASK: create public ip for ingress: STARTED
Running Command:
 ['az', 'network', 'public-ip', 'create', '--allocation-method', 'static', '--sku', 'Standard', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'MC_soundscape_soundscape-poc-aks_uksouth', '--name', 'soundscape-poc-ip']
WARNING: [Coming breaking change] In the coming release, the default behavior will be changed as follows when sku is Standard and zone is not provided: For zonal regions, you will get a zone-redundant IP indicated by zones:["1","2","3"]; For non-zonal regions, you will get a non zone-redundant IP indicated by zones:null.
TASK: create public ip for ingress: DONE
TASK: get kubernetes credentials: STARTED
Running Command:
 ['az', 'aks', 'get-credentials', '--subscription', '25eaed77-dc73-4d69-af3e-e475d5edb52c', '--resource-group', 'soundscape', '--name', 'soundscape-poc-aks', '--overwrite-existing']
The behavior of this command has been altered by the following extension: aks-preview
Merged "soundscape-poc-aks" as current context in /home/johng89/.kube/config
TASK: get kubernetes credentials: DONE
TASK: initialize HELM: STARTED
Running Command:
 ['helm', 'repo', 'add', '--namespace', 'soundscape', 'ingress-nginx', 'https://kubernetes.github.io/ingress-nginx']
"ingress-nginx" already exists with the same configuration, skipping
Running Command:
 ['helm', 'repo', 'update', '--namespace', 'soundscape']
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "ingress-nginx" chart repository
Update Complete. ⎈Happy Helming!⎈
TASK: initialize HELM: DONE
TASK: service install: STARTED
Running Command:
 ['helm', 'upgrade', '-i', '--namespace', 'soundscape', 'soundscape-service', 'soundscape', '--set', 'soundscapeImageVersion=0.1', '--set', 'containerRegistry=jtgacr.azurecr.io', '--set', 'keyVault=jtgTestKV', '--set', 'tenantId=b7133142-7e0e-48b3-90d8-ef7b5a7d6219', '--set', 'subscription_id=25eaed77-dc73-4d69-af3e-e475d5edb52c']
Release "soundscape-service" does not exist. Installing it now.
W0716 14:18:23.615471   12538 warnings.go:70] annotation "kubernetes.io/ingress.class" is deprecated, please use 'spec.ingressClassName' instead
NAME: soundscape-service
LAST DEPLOYED: Sun Jul 16 14:18:22 2023
NAMESPACE: soundscape
STATUS: deployed
REVISION: 1
TEST SUITE: None
TASK: service install: DONE
TASK: check secrets availability: STARTED
TASK: check secrets availability: DONE
TASK: nginx install into cluster: STARTED
Running Command:
 ['helm', 'upgrade', '-i', 'soundscape-ingress', 'ingress-nginx/ingress-nginx', '--namespace', 'soundscape', '--set-string', 'controller.extraArgs.enable-ssl-chain-completion=false', '--set', 'controller.image.registry=mcr.microsoft.com/oss/kubernetes', '--set', 'controller.image.digest=null', '--set', 'controller.allowSnippetAnnotations=false', '--set', 'controller.replicaCount=1', '--set', 'controller.service.loadBalancerIP=51.104.19.64', '--set', 'controller.service.externalTrafficPolicy=Local', '--set', 'controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-dns-label-name=soundscape-poc-aks-soundscape', '--set', 'controller.podLabels.aadpodidbinding=soundscape-identity', '-f', 'soundscape/other/nginx-csi-patch.yaml']
Release "soundscape-ingress" does not exist. Installing it now.
NAME: soundscape-ingress
LAST DEPLOYED: Sun Jul 16 14:18:24 2023
NAMESPACE: soundscape
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The ingress-nginx controller has been installed.
It may take a few minutes for the LoadBalancer IP to be available.
You can watch the status by running 'kubectl --namespace soundscape get services -o wide -w soundscape-ingress-ingress-nginx-controller'

An example Ingress that makes use of the controller:
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: example
    namespace: foo
  spec:
    ingressClassName: nginx
    rules:
      - host: www.example.com
        http:
          paths:
            - pathType: Prefix
              backend:
                service:
                  name: exampleService
                  port:
                    number: 80
              path: /
    # This section is only required if TLS is to be enabled for the Ingress
    tls:
      - hosts:
        - www.example.com
        secretName: example-tls

If TLS is enabled for the Ingress, a Secret containing the certificate and key must also be provided:

  apiVersion: v1
  kind: Secret
  metadata:
    name: example-tls
    namespace: foo
  data:
    tls.crt: <base64 encoded cert>
    tls.key: <base64 encoded key>
  type: kubernetes.io/tls
TASK: nginx install into cluster: DONE
SERVICE DNS: soundscape-poc-aks-soundscape.uksouth.cloudapp.azure.com
SERVICE PROVISION: complete





