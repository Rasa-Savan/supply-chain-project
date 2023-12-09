# from elasticsearch import Elasticsearch

# # Fingerprint either from Elasticsearch startup or above script.
# # Colons and uppercase/lowercase don't matter when using
# # the 'ssl_assert_fingerprint' parameter
# CERT_FINGERPRINT = "13:DF:CE:25:BD:28:F1:C4:81:03:BD:D5:5F:37:08:E5:16:06:4D:B3:11:E2:C2:1C:45:EC:00:6E:40:02:27:B9"

# # Password for the 'elastic' user generated by Elasticsearch
# ELASTIC_PASSWORD = "2+jSOZ4fp5-U_UjIUNC7"

# client = Elasticsearch(
#     "https://127.0.0.1:9200",
#     ssl_assert_fingerprint=CERT_FINGERPRINT,
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )

# # Successful response!
# print(client.info())
# # {'name': 'instance-0000000000', 'cluster_name': ...}


from elasticsearch import Elasticsearch

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "u6PoRpkVMUIpzw_PORGf"

# Create the client instance
client = Elasticsearch(
    "https://127.0.0.1:9200",
    ca_certs="/etc/ssl/certs/http_ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Successful response!
print(client.info())
# {'name': 'instance-0000000000', 'cluster_name': ...}