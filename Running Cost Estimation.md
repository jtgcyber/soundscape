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
