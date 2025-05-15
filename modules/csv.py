import csv


def export_to_csv(hosts, nmap_csv_file):
    with open(nmap_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                'Hostname',
                'IP Address',
                'Protocol',
                'Port',
                'Service name',
                'Service product',
                'Service version'
            ]
        )

        for host in hosts:
            for port in host['ports']:
                writer.writerow(
                    [
                        host['hostname'],
                        host['ipv4_address'],
                        port['protocol'],
                        port['port_id'],
                        port['service_name'],
                        port['service_product'],
                        port['service_version']
                    ]
                )
