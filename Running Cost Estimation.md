Soundscape Azure SKU's Referenced
small_db_size = 90
large_db_size = 1100
small_cpu_sku = 'Standard_DS3_v2' PAYG Price = £155.68 PM
large_cpu_sku = 'Standard_DS4_v2' PAYG Price = ££311.95 PM
small_db_sku = 'Standard_D2s_v3'  PayG Price = £63.34
large_db_sku = 'Standard_D4s_v3'  PayG Price = £126.67

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
