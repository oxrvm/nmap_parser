import xml.etree.ElementTree as ET


def parse_nmap_results_file(nmap_results_file):
    tree = ET.parse(nmap_results_file)
    root = tree.getroot()

    nmap_scan_informations = parse_nmap_scan_informations(root)
    nmap_hosts = parse_nmap_hosts(root)

    return nmap_scan_informations, nmap_hosts


def parse_nmap_scan_informations(root):
    nmap_args = root.get('args')
    nmap_version = root.get('version')
    nmap_start_time = root.get('start')
    nmap_elapsed_time_elem = root.find('runstats/finished')
    if nmap_elapsed_time_elem is not None:
        nmap_elapsed_time = nmap_elapsed_time_elem.get('elapsed')

    return (
        {
            'args': nmap_args,
            'version': nmap_version,
            'start_time': nmap_start_time,
            'elapsed_time': nmap_elapsed_time
        }
    )


def parse_nmap_hosts(root):
    hosts = []
    for host in root.findall('host'):
        status_elem = host.find('status')
        if status_elem is None or status_elem.get('state') != 'up':
            continue

        hostname_elem = host.find('hostnames/hostname')
        hostname = hostname_elem.get(
            'name') if hostname_elem is not None else 'Unknown'

        ipv4_address_elem = host.find('address')
        ipv4_address = ipv4_address_elem.get(
            'addr') if ipv4_address_elem is not None else 'Unknown'

        ports = parse_nmap_host_ports(host)

        hosts.append(
            {
                'hostname': hostname,
                'ipv4_address': ipv4_address,
                'ports': ports
            }
        )

    return hosts


def parse_nmap_host_ports(host):
    ports = []
    ports_elem = host.find('ports')
    if ports_elem is not None:
        for port in ports_elem.findall('port'):
            protocol = port.get('protocol')
            port_id = port.get('portid')

            service_name, service_product, service_version = parse_port_service(
                port)

            ports.append(
                {
                    'protocol': protocol,
                    'port_id': port_id,
                    'service_name': service_name,
                    'service_product': service_product,
                    'service_version': service_version
                }
            )

    return ports


def parse_port_service(port):
    service = port.find('service')
    if service is not None:
        service_name = service.get('name')
        service_product = service.get('product')
        service_version = service.get('version')
    else:
        service_name = service_product = service_version = 'Unknown'

    return service_name, service_product, service_version
