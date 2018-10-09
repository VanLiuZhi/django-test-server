import snowflake.client

# host = '0.0.0.0'
# port = 30001
# snowflake.client.setup(host, port)
res = snowflake.client.get_guid()

print(res)