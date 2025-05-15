import argparse
import logging
import os

from modules import nmap, xml

logger = logging.getLogger(__name__)


def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='''
        This Python script is designed to automate Nmap network scanning and export the parsed results in either CSV, MySQL or SQLite format.
        This tool is useful for network administrators and security professionals who need to store and analyze Nmap scan results in a structured and queryable format.
        '''
    )

    parser.add_argument(
        '-e', '--export',
        choices=['csv', 'mysql', 'sqlite'],
        help='export data in a specific format',
        metavar=('FORMAT'),
        nargs='+',
        required=True
    )

    return parser


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    current_working_directory = os.getcwd()
    nmap_network_file = f'{current_working_directory}/settings/network.txt'
    nmap_results_file = f'{current_working_directory}/results/results.xml'

    logging.basicConfig(filename='nmap_parser.log', level=logging.INFO)

    nmap.start_nmap_scan(nmap_network_file, nmap_results_file)

    nmap_scan_informations, nmap_hosts = xml.parse_nmap_results_file(
        nmap_results_file)

    if 'csv' in args.export:
        from modules import csv

        nmap_csv_file = f'{current_working_directory}/results/data.csv'
        csv.export_to_csv(nmap_hosts, nmap_csv_file)
    if 'mysql' in args.export:
        from dotenv import load_dotenv

        from modules import mysql

        load_dotenv()

        mysql.export_to_mysql(nmap_scan_informations, nmap_hosts)
    if 'sqlite' in args.export:
        from modules import sqlite

        nmap_sqlite_file = f'{current_working_directory}/results/data.db'
        sqlite.export_to_sqlite(
            nmap_sqlite_file, nmap_scan_informations, nmap_hosts)


if __name__ == '__main__':
    main()
