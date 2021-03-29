from core import DB, ConfigData

all_connections = []

db_obj_result = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="result", port='3306', conn_name='db1')
db2 = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="example", port='3307', conn_name='db2')
db3 = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="example", port='3308', conn_name='db3')

all_connections.append(db2)
all_connections.append(db3)

for connection in all_connections:
    conf_obj = ConfigData(connection_name=connection.conn_name)
    conf_obj.check_config_file_exists()
    last_pos = conf_obj.get_last_pos()
    connection.execute(f'SELECT * FROM report WHERE id > {last_pos}')
    results = connection.get_cursor().fetchall()
    for res in results:
        query = f"INSERT INTO report(`id`, `data`, `type`, `from_server`, `from_server_id`) " \
                f"VALUES (0, \"{res['data']}\", {res['type']}, \"{connection.conn_name}\", {res['id']})"
        db1.execute(query=query)
        print(query)

    db1.get_connection().commit()

all_connections.append(db_obj_result)
for connection in all_connections:
    connection.close()

print(f'......end...........')
