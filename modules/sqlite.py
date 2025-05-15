import sqlite3


def export_to_sqlite(db, nmap_scan_informations, nmap_hosts):
    conn = connect_to_database(db)
    create_database(conn)
    insert_data(conn, nmap_scan_informations, nmap_hosts)


def connect_to_database(db):
    conn = sqlite3.connect(db)

    return conn


def create_database(conn):
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            args TEXT,
            version TEXT,
            start_time TEXT,
            elapsed_time TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT,
            ipv4_address TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER,
            protocol TEXT,
            port_id TEXT,
            service_name TEXT,
            service_product TEXT,
            service_version TEXT,
            FOREIGN KEY (host_id) REFERENCES hosts (id)
        )
        """
    )

    conn.commit()


def insert_data(conn, nmap_scan_informations, nmap_hosts):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO scan (args, version, start_time, elapsed_time)
        VALUES (?, ?, ?, ?)
        """,
        (nmap_scan_informations['args'], nmap_scan_informations['version'],
         nmap_scan_informations['start_time'], nmap_scan_informations['elapsed_time'])
    )

    for host in nmap_hosts:
        cur.execute(
            """
            INSERT INTO hosts (hostname, ipv4_address)
            VALUES (?, ?)
            """,
            (host['hostname'], host['ipv4_address'])
        )

        host_id = cur.lastrowid

        for port in host['ports']:
            cur.execute(
                """
                INSERT INTO ports (host_id, protocol, port_id, service_name, service_product, service_version)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (host_id, port['protocol'], port['port_id'], port['service_name'],
                 port['service_product'], port['service_version'])
            )

    conn.commit()
