import os

import mysql.connector


def export_to_mysql(nmap_scan_informations, nmap_hosts):
    conn = connect_to_database()
    truncate_tables(conn)
    create_tables(conn)
    insert_data(conn, nmap_scan_informations, nmap_hosts)


def connect_to_database():
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=3306,
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

    return conn


def truncate_tables(conn):
    cur = conn.cursor()

    cur.execute("SET FOREIGN_KEY_CHECKS = 0;")

    cur.execute("SHOW TABLES;")
    tables = cur.fetchall()

    for table in tables:
        cur.execute(f"TRUNCATE TABLE {table[0]};")

    cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

    conn.commit()


def create_tables(conn):
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scan (
            id INT AUTO_INCREMENT PRIMARY KEY,
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
            id INT AUTO_INCREMENT PRIMARY KEY,
            hostname TEXT,
            ipv4_address TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host_id INT,
            protocol TEXT,
            port_id TEXT,
            service_name TEXT,
            service_product TEXT,
            service_version TEXT,
            FOREIGN KEY (host_id) REFERENCES hosts(id)
        )
        """
    )

    conn.commit()


def insert_data(conn, nmap_scan_informations, nmap_hosts):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO scan (args, version, start_time, elapsed_time)
        VALUES (%s, %s, %s, %s)
        """,
        (nmap_scan_informations['args'], nmap_scan_informations['version'],
         nmap_scan_informations['start_time'], nmap_scan_informations['elapsed_time'])
    )

    for host in nmap_hosts:
        cur.execute(
            """
            INSERT INTO hosts (hostname, ipv4_address)
            VALUES (%s, %s)
            """,
            (host['hostname'], host['ipv4_address'])
        )

        host_id = cur.lastrowid

        for port in host['ports']:
            cur.execute(
                """
                INSERT INTO ports (host_id, protocol, port_id, service_name, service_product, service_version)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (host_id, port['protocol'], port['port_id'], port['service_name'],
                 port['service_product'], port['service_version'])
            )

    conn.commit()
