from core import DB, ConfigData, DataPD
import io

all_connections = []

db_obj_result = DB(host='127.0.0.1', user='salkov', password="Artyom.salkov1", database="result", port='3306', conn_name='db_obj_result')
print("db_obj_result")
db2 = DB(host='127.0.0.1', user='completecase', password="fh47gTwdf#8@dfsg", database="completecase", port='3308', conn_name='db2')
print("db2")
db3 = DB(host='127.0.0.1', user='completecase', password="fh47gTwdf#8@dfsg", database="completecase", port='3309', conn_name='db3')
print("db3")

all_connections.append(db2)
all_connections.append(db3)

# Copy reports
for connection in all_connections:
    conf_obj = ConfigData(connection_name=connection.conn_name)
    conf_obj.check_config_file_exists()
    last_pos = conf_obj.get_report_position()
    query_get_reports = f'SELECT * FROM reporting_grandprofitabilityreport WHERE id > {last_pos} ORDER BY id ASC'
    connection.execute(query_get_reports)

    res = results = query = None
    results = connection.get_cursor().fetchall()

    for res in results:
        query = f"INSERT INTO reporting_grandprofitabilityreport(`id`, `created`, `created_for`, `data`, `type`, `from_server`, `from_id`) " \
                f"VALUES (0, \"{res['created']}\", \"{res['created_for']}\", \"{res['data']}\", {res['type']}, " \
                f"{int(connection.conn_name[2::])}, {res['id']})"

        db_obj_result.execute(query=query)
        print(query)

        try:
            pd_data_obj = DataPD(data=res['data'])
            print(pd_data_obj.data_frame)
        except Exception:
            pass

    if isinstance(results, (tuple)):
        pass
    else:
        db_obj_result.get_connection().commit()
        conf_obj.set_report_position(val=res['id'])
# ----------------------------/ Copy reports ---------------------------------

# Copy sites
for connection in all_connections:
    conf_obj = ConfigData(connection_name=connection.conn_name)
    conf_obj.check_config_file_exists()
    last_pos = conf_obj.get_sites_position()
    query_get_sites = f'SELECT * FROM django_site WHERE id > {last_pos} ORDER BY id ASC'
    connection.execute(query_get_sites)

    res = results = query = None
    results = connection.get_cursor().fetchall()

    print(results)

    for res in results:

        query = f'INSERT INTO reporting_sitesonservers(`id`, `domain`, `name`, `from_server`, `from_id`) ' \
                f'VALUES (0, \'{res["domain"]}\', \'{res["name"]}\', \'{int(connection.conn_name[2::])}\', \'{res["id"]}\')'

        db_obj_result.execute(query=query)
        print(query)

    if isinstance(results, (tuple)):
        pass
    else:
        db_obj_result.get_connection().commit()
        conf_obj.set_sites_position(val=res['id'])
# --------------------------- /Copy sites ------------------------



all_connections.append(db_obj_result)
for connection in all_connections:
    connection.close()

print(f'......end...........')
