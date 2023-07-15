small_db_size = 90
large_db_size = 1100
small_cpu_sku = 'Standard_DS3_v2'
large_cpu_sku = 'Standard_DS4_v2'
small_db_sku = 'Standard_D2s_v3'
large_db_sku = 'Standard_D4s_v3'

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


config = {

    'parameters' : scale_parameters['test'],
    'namespace'  : 'soundscape'

}
args = [
        'helm',
        'upgrade',
        '-i',
        '--namespace', config['namespace'],
        'soundscape-service',
        'soundscape',
    ]

parameters = config['parameters']
if parameters.get('values'):
    for v in parameters['values']:
        args.extend(['--values', 'soundscape/' + v])

print("Running Command:\n",str(args))