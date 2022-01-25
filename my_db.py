import sqlite3 as sqlite
import os

db_file = os.path.join(os.path.dirname(__file__), 'sqlite3/my.db')


def execute_select(sql):
    conn = sqlite.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(sql)
    data_info = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data_info


def execute_up(sql):
    conn = sqlite.connect(db_file)
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
    # test_sql = 'select num from bp_node_produced_blocks where public_key = "040bcbc49d65a89e49dc7152b2720f5769e6132a2c2d8742d0b7d6efb7bc1a977355f5dbd05f565e3c8848cbce8c8a0250a8a2296dc74b3d4fa0335637de5b1ec7"'
    test_sql = 'select * from bp_node_produced_blocks'
    print(execute_select(test_sql))
    # test_sql = "insert into bp_node_produced_blocks values('042f7cab8272e1f4e90e59e91bbe2c211f1a0e15a5b670aff517a02f625d678607a96723b6ce3232fcf6ad0fc988e3e198cdedebcc10cd4d86b4dddfd8a99edcf0', 113277)"
    # print(execute_up(test_sql))




