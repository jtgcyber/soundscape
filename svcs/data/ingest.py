# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# This script is a command-line tool for managing the ingestion of OpenStreetMap (OSM) data into a PostgreSQL database. 
# It uses Kubernetes to manage the database and services, and the Imposm tool to import the data. 
# The script is designed to be highly configurable, with many options that can be set via command-line arguments.

# Here's a brief overview of what the script does:

# Argument Parsing: The script begins by defining a number of command-line arguments that can be used to configure its behavior.
# These include options to skip certain tasks, specify the update model, set various file and directory paths, and more.

# Data Import Functions: The script defines a number of functions for importing data. 
# These include fetch_extract to download a specific extract of OSM data, import_extract to import a specific extract into the database, and import_extracts_and_write to import multiple extracts and write them to the database.

# Database Provisioning Functions: The script also includes functions for provisioning the database. 
# These include provision_database_async to create the database and enable necessary PostgreSQL extensions, and provision_database_soundscape_async to execute additional SQL scripts.

# Kubernetes Management Functions: The script includes functions for managing the Kubernetes deployments associated with the database. 
# These include execute_kube_updatemodel_provision_and_import to provision the database and import data, execute_kube_sync_deployments to synchronize the Kubernetes deployments with the current state of the databases, and execute_kube_sync_tile_services to manage the tile services.

# Telemetry Logging: If the --telemetry argument is provided, the script logs telemetry data for various operations.

# Main Execution: The script parses the command-line arguments, sets up logging, and then calls execute_kube_updatemodel to start the data import and database provisioning process. 
# If the --where or --sourceupdate arguments are provided, it filters the list of OSM extracts to import based on these arguments.

# Error Handling and Cleanup: The script includes a finally block to ensure that logging is properly shut down even if an error occurs during execution.

import os
import subprocess
import argparse
import json
from datetime import datetime
import time
import urllib.parse
import asyncio
import logging

import aiopg
import psycopg2

from kubescape import SoundscapeKube

dsn_default_base = 'host=localhost '
dsn_init_default = dsn_default_base + 'dbname=postgres'
dsn_default = dsn_default_base + 'user=osm password=osm dbname=osm'

parser = argparse.ArgumentParser(description='ingestion engine for Soundscape')

# configuration of what the ingestion will do
parser.add_argument('--skipimport', action='store_true', help='skips import task', default=False)
parser.add_argument('--updatemodel', type=str, help='choose update model', choices=['imposmauto', 'importloop', 'none'], default='none')
parser.add_argument('--sourceupdate', action='store_true', help='update source data', default=True)
parser.add_argument('--telemetry', action='store_true', help='generate telemetry')

parser.add_argument('--delay', type=int, help='loop delay time', default=60 * 60 * 8)

# configuration of files, directories and necessary configuration
parser.add_argument('--extracts', type=str, default='extracts.json', help='extracts file')
parser.add_argument('--mapping', type=str, help='mapping file path', default='mapping.yml')
parser.add_argument('--imposm', type=str, help='imposm executable', default='imposm')
parser.add_argument('--where', metavar='region', nargs='+', type=str, help='area names')
parser.add_argument('--cachedir', type=str, help='imposm temp directory', default='/tmp/imposm3')
parser.add_argument('--diffdir', type=str, help='imposm diff directory', default='/tmp/imposm3_diffdir')
parser.add_argument('--pbfdir', type=str, help='pbf directory', default='.')
parser.add_argument('--expiredir', type=str, help='expired tiles directory', default='/tmp/imposm3_expiredir')
parser.add_argument('--config', type=str, help='config file', default='config.json')
parser.add_argument('--provision', help='provision the database', action='store_true', default=False)
parser.add_argument('--dsn_init', type=str, help='postgres dsn init', default=dsn_init_default)
parser.add_argument('--dynamic_db', help='provision databases dynamically', action='store_true', default=False)
parser.add_argument('--dsn', type=str, help='postgres dsn', default=dsn_default)
parser.add_argument('--always_update', action='store_true', default=False)

parser.add_argument('--verbose', action='store_true', help='verbose')
# update_imposmauto(config): This function performs an incremental update of the database using the Imposm tool.
def update_imposmauto(config):
    logger.info('Incremental update - STARTED')
    subprocess.run([config.imposm, 'run', '-config', config.config, '-mapping', config.mapping, '-connection', config.dsn, '-srid', '4326', '-cachedir', config.cachedir, '-diffdir', config.diffdir, '-expiretiles-dir', config.expiredir, '-expiretiles-zoom', '16'], check=True)
    logger.info('Incremental update - DONE')

def fetch_extract(config, url):
    #
    # a local PBF may already be present
    #

    logger.info('Fetching {0}'.format(url))

    #
    # N.B. wget won't overwrite data unless it's in timestamp mode
    #

    local_pbf = os.path.join(config.pbfdir, os.path.basename(url))

    try:
        before_token = os.path.getmtime(local_pbf)
    except OSError:
        before_token = None

    try:
        subprocess.run(['wget', '-N', url, '--directory-prefix', config.pbfdir], check=True)
        after_token = os.path.getmtime(local_pbf)
    except Exception:
        raise

    logger.info('Fetching {0}: DONE'.format(url))
    if before_token == after_token:
        return False
    else:
        return True
    


def fetch_extracts(config, extracts):# fetch_extract(config, url): This function downloads a specific extract of OSM data from a given URL.
    start = datetime.utcnow()
    logger.info('Fetch extracts: START')
    fetched = False
    for e in extracts:
        fetched_extract = fetch_extract(config, e['url'])
        fetched = fetched or fetched_extract
    logger.info('Fetch extracts: DONE')
    end = datetime.utcnow()
    telemetry_log('fetch_extracts', start, end)
    return fetched

def import_extract(config, pbf, cache, incremental): # import_extract(config, pbf, cache, incremental): This function imports a specific extract into the database.
    logger.info('Import of {0} : START'.format(pbf))
    start = datetime.utcnow()
    imposm_args = [config.imposm, 'import', '-mapping', config.mapping, '-read', config.pbfdir + "/" + pbf, '-srid', '4326', cache, '-cachedir', config.cachedir]
    if incremental:
        imposm_args.extend(['-diff', '-diffdir', config.diffdir])
    subprocess.run(imposm_args, check=True)
    end = datetime.utcnow()
    telemetry_log('import_extract', start, end)
    logger.info('import of {0}: DONE'.format(pbf))

def import_write(config, incremental):# import_write(config, incremental): This function writes the imported data to the database.
    logger.info('writing of OSM tables: START')
    start = datetime.utcnow()
    imposm_args = [config.imposm, 'import', '-mapping', config.mapping, '-write', '-connection', config.dsn, '-srid', '4326', '-cachedir', config.cachedir]
    if incremental:
        imposm_args.extend(['-diff', '-diffdir', config.diffdir])
    subprocess.run(imposm_args, check=True)
    end = datetime.utcnow()
    telemetry_log('import_write', start, end, {'dsn': config.dsn})
    logger.info('Write of OSM tables: DONE')

def import_rotate(config, incremental):# import_rotate(config, incremental): This function rotates the tables in the database after data has been written.

    logger.info('Table rotation: START')
    start = datetime.utcnow()
    imposm_args = [config.imposm, 'import', '-mapping', config.mapping, '-connection', config.dsn, '-srid', '4326', '-deployproduction', '-cachedir', config.cachedir]

    if incremental:
        imposm_args.extend(['-diff', '-diffdir', config.diffdir])
    subprocess.run(imposm_args, check=True)
    end = datetime.utcnow()
    telemetry_log('import_rotate', start, end, {'dsn': config.dsn})
    logger.info('Table rotation: DONE')

def import_extracts(config, extracts, incremental):# import_extracts(config, extracts, incremental): This function imports multiple extracts into the database.

    imported = {}
    for e, i in zip(extracts, range(len(extracts))):
        if i == 0:
            cache = '-overwritecache'
        else:
            cache = '-appendcache'
        urlbits = urllib.parse.urlsplit(e['url'])
        pbf = os.path.basename(urlbits.path)
        if pbf in imported:
            continue
        imported[pbf] = True
        import_extract(config, pbf, cache, incremental)

def import_extracts_and_write(config, extracts, incremental):# import_extracts_and_write(config, extracts, incremental): This function imports multiple extracts and writes them to the database
    import_extracts(config, extracts, incremental)
    import_write(config, incremental)
    import_rotate(config, incremental)

async def provision_database_async(postgres_dsn, osm_dsn):# provision_database_async(postgres_dsn, osm_dsn): This function creates the database and enables necessary PostgreSQL extensions.

    async with aiopg.connect(dsn=postgres_dsn) as conn:
        cursor = await conn.cursor()
        try:
            await cursor.execute('CREATE DATABASE osm')
        except psycopg2.ProgrammingError:
            logger.warning('Database already existed at "{0}"'.format(postgres_dsn))
    async with aiopg.connect(dsn=osm_dsn) as conn:
        cursor = await conn.cursor()
        await cursor.execute('CREATE EXTENSION IF NOT EXISTS postgis')
        await cursor.execute('CREATE EXTENSION IF NOT EXISTS hstore')

async def provision_database_soundscape_async(osm_dsn): # provision_database_soundscape_async(osm_dsn): This function executes additional SQL scripts in the database.
    ingest_path = os.environ['INGEST']
    async with aiopg.connect(dsn=osm_dsn) as conn:
        cursor = await conn.cursor()
        with open(ingest_path + '/' + 'postgis-vt-util.sql', 'r') as sql:
            await cursor.execute(sql.read())
        with open(ingest_path + '/' + 'tilefunc.sql', 'r') as sql:
            await cursor.execute(sql.read())

def provision_database(postgres_dsn, osm_dsn):# provision_database(postgres_dsn, osm_dsn): This function calls provision_database_async and logs the time taken.
    start = datetime.utcnow()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(provision_database_async(postgres_dsn, osm_dsn))
    end = datetime.utcnow()
    telemetry_log('provision_database', start, end, {'dsn': postgres_dsn})

def provision_database_soundscape(osm_dsn):# provision_database_soundscape(osm_dsn): This function calls provision_database_soundscape_async.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(provision_database_soundscape_async(osm_dsn))

def execute_kube_updatemodel_provision_and_import(config, updated):# execute_kube_updatemodel_provision_and_import(config, updated): This function provisions the database and imports data, and updates the status of the database in Kubernetes.
    namespace = os.environ['NAMESPACE']
    kube = SoundscapeKube(None, namespace)
    kube.connect()

    logger.info('Provision and import: START')
    logger.info('Provisioning databases: START')
    for d in kube.enumerate_databases():
        dbstatus = d['dbstatus']

        if dbstatus == None or dbstatus == 'INIT':
            try:
                logger.info('Provisioning database "{0}" : START'.format(d['name']))
                kube.set_database_status(d['name'], 'PROVISIONING')
                dsn = d['dsn2']
                dsn_init = d['dsn2'].replace('dbname=osm', 'dbname=postgres')
                logger.info(dsn)
                provision_database(dsn_init, dsn)
                kube.set_database_status(d['name'], 'PROVISIONED')
                logger.info('Provisioning database "{0}": DONE'.format(d['name']))
            except Exception as e:
                logger.warning('Provisioning database "{0}: {1}": FAILED'.format(d['name'], e))
                kube.set_database_status(d['name'], 'INIT')
    logger.info('Provision databases: DONE')

    if updated:
        logger.info('Importing extracts')
        import_extracts(config, osm_extracts, False)

    logger.info('Updating databases')
    for d in kube.enumerate_databases():
        dbstatus = d['dbstatus']

        if dbstatus != 'PROVISIONED' and dbstatus != 'HASMAPDATA':
            continue

        if dbstatus == 'HASMAPDATA' and not updated:
            logger.info('Updating databases, skipping \'{0}\''.format(d['name']))
            continue

        try:
            logger.info('Importing to "{0}"'.format(d['name']))
            args.dsn = kube.get_url_dsn(d['dsn2']) + '?sslmode=require'
            import_write(config, False)
            import_rotate(config, False)
            provision_database_soundscape(d['dsn2'])
            # kubernetes connection may have expired
            retry_count = 5
            while True:
                if retry_count == 0:
                    kube.set_database_status(d['name'], 'HASMAPDATA')
                    break
                else:
                    try:
                        kube.set_database_status(d['name'], 'HASMAPDATA')
                        break
                    except Exception as e:
                        logger.warning('failed provisioning database "{0}: {1}" retrying'.format(d['name'], e))
                retry_count -= 1
            logger.info('imported to "{0}"'.format(d['name']))

        except Exception as e:
            logger.warning('failed provisioning database "{0}: {1}"'.format(d['name'], e))
    logger.info('Completed provision and import')

def execute_kube_sync_deployments(manager, desc):# execute_kube_sync_deployments(manager, desc): This function synchronizes the Kubernetes deployments with the current state of the databases.
    logger.info('Synchronize {0} with databases'.format(desc))

    seen_dbs = []
    for db in manager.enumerate_ready_databases():
        seen_dbs.append(db['name'])

        if manager.exist_deployment_for_db(db):
            logger.info('Deployment {0} for \'{1}\' exists'.format(desc, db['name']))
        else:
            try:
                manager.create_deployment_for_db(db)
                logger.info('Created {0} for \'{1}\''.format(desc, db['name']))
            except Exception:
                logger.warning('Failed to created {0} for \'{1}\''.format(desc, db['name']))
    logger.info('Synchronize {0} with databases: DONE'.format(desc))

    for db in manager.enumerate_deployments():
        if db['name'] not in seen_dbs:
            try:
                manager.delete_deployment_for_db(db)
                logger.info('Deployment for \'{0}\' was deleted'.format(db['name']))
            except Exception:
                logger.warning('Deployment for \'{0}\' failed deletion'.format(db['name']))
        else:
            logger.info('Deployment for \'{0}\' is running'.format(db['name']))

def execute_kube_sync_tile_services(config):# execute_kube_sync_tile_services(config): This function manages the tile services in Kubernetes.
    start = datetime.utcnow()
    namespace = os.environ['NAMESPACE']
    kube = SoundscapeKube(None, namespace)
    kube.connect()

    tile_server_manager = kube.manage_tile_servers('/templates/tile-server-deployment-template')
    execute_kube_sync_deployments(tile_server_manager, 'tile service')
    end = datetime.utcnow()
    telemetry_log('sync_tile_services', start, end)

def execute_kube_sync_database_services(config):# execute_kube_sync_database_services(config): This function calls execute_kube_sync_tile_services.
    execute_kube_sync_tile_services(config)

def execute_kube_updatemodel(config):# execute_kube_updatemodel(config): This function is the main function that manages the entire process of fetching extracts, provisioning databases, importing data, and managing Kubernetes deployments.
    # N.B. launch tile services and metrics for already functioning databases
    #      since import of new data can/will take a while
    if config.dynamic_db:
        execute_kube_sync_database_services(config)

    rescan_delay = 60
    initial_import = True
    while True:
        fetch_delay = config.delay
        updated = fetch_extracts(config, osm_extracts)
        if config.always_update:
            updated = True

        while fetch_delay >= 0:
            execute_kube_updatemodel_provision_and_import(config, updated or initial_import)
            updated = False
            initial_import = False

            if config.dynamic_db:
                execute_kube_sync_database_services(config)

            time.sleep(rescan_delay)
            fetch_delay -= rescan_delay
        initial_import = False

def telemetry_log(event_name, start, end, extra=None):# telemetry_log(event_name, start, end, extra=None): This function logs telemetry data for various operations.
    if args.telemetry:
        if extra == None:
            extra = {}
        extra['start'] = start.isoformat()
        extra['end'] = end.isoformat()
        pass

args = parser.parse_args()

if args.verbose:
    loglevel = logging.INFO
else:
    loglevel = logging.WARNING

if args.where or args.sourceupdate:
    extracts_f = open(args.extracts, 'r')
    osm_extracts = json.load(extracts_f)

if args.where:
    osm_extracts = list(filter(lambda e: e['name'] in args.where, osm_extracts))

logging.basicConfig(level=loglevel,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger()

if args.telemetry:
    pass

try:
    execute_kube_updatemodel(args)

finally:
    print('terminating logging')
    logging.shutdown()
 






















