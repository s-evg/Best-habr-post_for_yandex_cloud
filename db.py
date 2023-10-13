import uuid
import ydb
import os


# id = [uuid.uuid4() for i in range(10)]
#
# for _ in id:
#     print(_)
#     _ = str(_)
#     print(_)
#     print(type(_))


endpoint = os.getenv('YDB_ENDPOINT')
database = os.getenv('YDB_DATABASE')


# create driver in global space.
driver = ydb.Driver(endpoint, database)
# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)


def execute_query(session):
    # create the transaction and execute query.
    return session.transaction().execute(
        'select 1 as cnt;',
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )


def main():
    # Execute query with the retry_operation helper.
    result = pool.retry_operation_sync(execute_query)
    return {
        'statusCode': 200,
        'body': str(result[0].rows[0].cnt == 1),
    }


def run(endpoint, database):
    driver_config = ydb.DriverConfig(
        endpoint, database, credentials=ydb.construct_credentials_from_environ(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )
    with ydb.Driver(driver_config) as driver:
        try:
            driver.wait(timeout=5)
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(driver.discovery_debug_details())
            exit(1)
