import sqlite3 as sqlite


def execute_select(sql):
    conn = sqlite.connect("sqlite3/my.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    data_info = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data_info


def execute_up(sql):
    conn = sqlite.connect("sqlite3/my.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()


def create_table_bp_node_produced_blocks():
    sql = 'create table bp_node_produced_blocks(public_key varchar(255) not null, num int)'
    execute_up(sql)


if __name__ == '__main__':
    # create_table_bp_node_produced_blocks()
    test_sql = "insert into bp_node_produced_blocks values('042f7cab8272e1f4e90e59e91bbe2c211f1a0e15a5b670aff517a02f625d678607a96723b6ce3232fcf6ad0fc988e3e198cdedebcc10cd4d86b4dddfd8a99edcf0', 113277)"
    print(execute_up(test_sql))




