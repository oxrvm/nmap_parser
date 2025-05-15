import subprocess


def start_nmap_scan(nmap_network_file, nmap_results_file):
    subprocess.call(
        [
            'nmap',
            '-iL',
            f'{nmap_network_file}',
            '-p-',
            '-sV',
            '-oX',
            f'{nmap_results_file}'
        ],
        stdout=subprocess.DEVNULL
    )
