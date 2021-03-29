from core import DB, ConfigData

all_connections = []

# Конфиг для Delle6440
# db_obj_result = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="result", port='3306', conn_name='db1')
# db2 = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="example", port='3307', conn_name='db2')
# db3 = DB(host='127.0.0.1', user='salkov', password="1ddorog3", database="example", port='3308', conn_name='db3')

# Конфиг для KeyUA work machine
db_obj_result = DB(host='127.0.0.1', user='salkov', password="Artyom.salkov1", database="result", port='3306', conn_name='db_obj_result')
print("db_obj_result")
db2 = DB(host='127.0.0.1', user='completecase', password="fh47gTwdf#8@dfsg", database="completecase", port='3308', conn_name='db2')
print("db2")
db3 = DB(host='127.0.0.1', user='completecase', password="fh47gTwdf#8@dfsg", database="completecase", port='3309', conn_name='db3')
print("db3")

all_connections.append(db2)
all_connections.append(db3)

for connection in all_connections:
    conf_obj = ConfigData(connection_name=connection.conn_name)
    conf_obj.check_config_file_exists()
    last_pos = conf_obj.get_last_pos_from_file()
    # Конфиг для Delle6440
    # query_get_reports = f'SELECT * FROM report WHERE id > {last_pos}'
    # Конфиг для KeyUA work machine
    query_get_reports = f'SELECT * FROM reporting_grandprofitabilityreport WHERE id > {last_pos} ORDER BY id ASC'
    connection.execute(query_get_reports)

    res = results = query = None
    results = connection.get_cursor().fetchall()

    for res in results:
        # Конфиг для Delle6440
        # query = f"INSERT INTO report(`id`, `data`, `type`, `from_server`, `from_server_id`) " \
        #         f"VALUES (0, \"{res['data']}\", {res['type']}, \"{connection.conn_name}\", {res['id']})"

        # Конфиг для KeyUA work machine
        # query = f"INSERT INTO report(`id`, `created`, `created_for`, `data`, `type`, `from_server`, `from_id`) " \
        #         f"VALUES (0, {res['created']}, {res['created_for']}, {res['data']}, {res['type']}, " \
        #         f"{int(connection.conn_name[2::])}, {res['id']})"
        # db_obj_result.execute(query=query)

        # Конфиг2 для KeyUA work machine
        query = f"INSERT INTO reporting_grandprofitabilityreport(`id`, `created`, `created_for`, `data`, `type`, `from_server`, `from_id`) " \
                f"VALUES (0, \"{res['created']}\", \"{res['created_for']}\", \"{res['data']}\", {res['type']}, " \
                f"{int(connection.conn_name[2::])}, {res['id']})"

        db_obj_result.execute(query=query)
        print(query)

    if isinstance(results, (tuple)):
        pass
    else:
        db_obj_result.get_connection().commit()
        conf_obj.set_last_pos_to_file(val=res['id'])

all_connections.append(db_obj_result)
for connection in all_connections:
    connection.close()

print(f'......end...........')
