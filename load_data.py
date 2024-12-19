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
                "pipe_and_space_tokenizer": {
                    "type": "pattern",
                    "pattern": "[\\s\\|]+"
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
                    "max_shingle_size": 5,
                    "output_unigrams": False
                }
            },
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "pipe_and_space_tokenizer",
                    "filter": [
                        "lowercase_filter",
                        "ascii_folding_filter",
                        "stemmer_filter"
                    ]
                },
                "bigram_analyzer": {
                    "type": "custom",
                    "tokenizer": "pipe_and_space_tokenizer",
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
                "analyzer": "bigram_analyzer",
                "similarity": "default"
            }
        }
    }
}


# Kiểm tra nếu index tồn tại và xóa trước khi tạo lại
if es.indices.exists(index="vie_documents_list"):
    es.indices.delete(index="vie_documents_list")

# Tạo index `documents_list` với cấu hình custom
es.indices.create(index="vie_documents_list", body=index_settings)
print("Index `vie_documents_list` đã được tạo với cấu hình custom.")

# Nạp dữ liệu từ file JSON
with open('D:\\Project Github\\BK-THK_Search_Engine\\BK-THK-search-engine\\data\\final_data.json', 'r', encoding='utf-8') as file:
    final_data = json.load(file)

# Nạp từng tài liệu vào Elasticsearch
for i, document in enumerate(final_data):
    es.index(index="vie_documents_list", id=i, document=document)

print("Dữ liệu đã được nạp vào Elasticsearch.")
