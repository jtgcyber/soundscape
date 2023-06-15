
Default Soundscape provisioning is production which is what is priced below - You can generally resize cloud infrastructure to cope with extra or reduced demand.I am assuming the Microsoft deployment would have been this configuration. Also this pricing is for Azure UK South, which is a more expensive region, so you can shave 10% off for a cheaper region.

Things missing from price calculations 
    1.Internet e-gress costs - I dont know how much data is downloaded to each client. 1st 100GB per month is free, charged at 8P per GB after So this may not be relevant
    2.Data Storage outside the database tier. Will be relevant if it needs to be DISK storage. However content that sits as BLOB is a lot cheaper.
    3.How this application is designed to scale if at all? Can someone account for this in the code? My guess  scaling up instaed of out eg bigger servers.
    4.In the deployment sizing there are references to kubernetes notes, assuming that these nodes run on the single server.
    5.No point in pricing up test and dev infrastructure. As you turn this on to use it then turn it back off again making cost negligable.

Azure UK South Pricing
Compute Costs Per Anum Backend £
    Large CPU SKU = PAYG 4986.48    1yr Res 2249.40
    Large DB SKU  = PAYG 1647.96    1yr Res 1044.36

Azure App Service Authoring App Cost PA £ 
    Premium p2v3 4 cores(guess) = PAYG 2457.72     1yr Res 1598.16

Storage Costs Per Anum £
    Large DB Disk Size 1024GB = £1591.44
    Small DB Disk Size 128GB  = £232.08
    OS Disks 4x 32GB          = £248.64

Cost Total = PAYG 11181     1yr Res 6964.08


Soundscape Azure SKU's Referenced  - Pricing UK South
Operating System Disk = P4 32GB   PAYG Price = £5.18
small_db_size = 90                PAYG Price = £19.34
large_db_size = 1100 -P30 Disk    PAYG Price = £132.62
small_cpu_sku = 'Standard_DS3_v2' PAYG Price = £207.77 PM
large_cpu_sku = 'Standard_DS4_v2' PAYG Price = ££415.54 PM
small_db_sku = 'Standard_D2s_v3'  PayG Price = £68.66
large_db_sku = 'Standard_D4s_v3'  PayG Price = £137.33


Soundsscape Deployment mode sizes

scale_parameters = {
    'test': {
        'node_count': 1,
        'nginx_count': 1,
        'vm_sku': small_cpu_sku,
        'db_sku': small_db_sku,
        'db_size': small_db_size,
        'nginx_log': True,
        'values': None,
    },
    'stress': {
        'node_count': 1,
        'nginx_count': 1,
        'vm_sku': small_cpu_sku,
        'db_sku': small_db_sku,
        'db_size': small_db_size,
        'nginx_log': True,
        'values': ['values-stress.yaml'],
        'stress': True
    },
    'production-test': {
        'node_count': 1,
        'nginx_count': 1,
        'vm_sku': small_cpu_sku,
        'db_sku': small_db_sku,
        'db_size': small_db_size,
        'nginx_log': True,
        'values': None,
    },
    'test-big': {
        'node_count': 3,
        'nginx_count': 1,
        'vm_sku': large_cpu_sku,
        'db_sku': large_db_sku,
        'db_size': large_db_size,
        'nginx_log': False,
        'values': ['values-production.yaml']
    },
    'stress-big': {
        'node_count': 3,
        'nginx_count': 1,
        'vm_sku': large_cpu_sku,
        'db_sku': large_db_sku,
        'db_size': large_db_size,
        'nginx_log': False,
        'values': ['values-production.yaml', 'values-stress.yaml', 'values-stress-big.yaml'],
        'stress': True
    },
    'production': {
        'node_count': 3,
        'nginx_count': 2,
        'vm_sku': large_cpu_sku,
        'db_sku': large_db_sku,
        'db_size': large_db_size,
        'nginx_log': False,
        'values': ['values-production.yaml']
    },
    'production-backup': {
        'node_count': 1,
        'nginx_count': 2,
        'vm_sku': large_cpu_sku,
        'db_sku': large_db_sku,
        'db_size': large_db_size,
        'nginx_log': False,
        'values': ['values-production.yaml', 'values-backup.yaml']
    }
}
