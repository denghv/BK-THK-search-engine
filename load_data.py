import json
from elasticsearch import Elasticsearch

# Kết nối Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Cấu hình analyzer cho index `documents_list`
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "similarity": {
            "default": {
                "type": "BM25",
                "b": 0.75,
                "k1": 1.2
            }
        },
        "analysis": {
            "tokenizer": {
                "whitespace_tokenizer": {
                    "type": "whitespace"
                }
            },
            "filter": {
                "lowercase_filter": {
                    "type": "lowercase"
                },
                "stemmer_filter": {
                    "type": "stemmer",
                    "name": "light_english"
                },
                "ascii_folding_filter": {
                    "type": "asciifolding",
                    "preserve_original": True
                },
                "bigram_filter": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 3,
                    "output_unigrams": False
                }
            },
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace_tokenizer",
                    "filter": [
                        "lowercase_filter",
                        "ascii_folding_filter",
                        "stemmer_filter",
                        "bigram_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "similarity": "default"
            },
            "description": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "similarity": "default",
                "fielddata": True
            }
        }
    }
}

# Kiểm tra nếu index tồn tại và xóa trước khi tạo lại
if es.indices.exists(index="documents_list"):
    es.indices.delete(index="documents_list")

# Tạo index `documents_list` với cấu hình custom
es.indices.create(index="documents_list", body=index_settings)
print("Index `documents_list` đã được tạo với cấu hình custom.")

# Nạp dữ liệu từ file JSON
with open('D:\Project Github\Search_engine_start\merged_data.json', 'r', encoding='utf-8') as file:
    merged_data = json.load(file)

# Nạp từng tài liệu vào Elasticsearch
for i, document in enumerate(merged_data):
    es.index(index="documents_list", id=i, document=document)

print("Dữ liệu đã được nạp vào Elasticsearch.")
