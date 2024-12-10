from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, exceptions
import json
import logging

app = Flask(__name__)

# Cấu hình logging với mã hóa UTF-8
logging.basicConfig(
    filename="search_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"  # Đảm bảo file log sử dụng mã hóa UTF-8
)

# Kết nối Elasticsearch
try:
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        raise exceptions.ConnectionError("Không thể kết nối đến Elasticsearch.")
except exceptions.ConnectionError as e:
    print(f"Lỗi: {e}")
    es = None

# Route cho trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Ghi log thông tin tìm kiếm vào file log
def log_search(query, results):
    log_message = {
        "query": query,
        "results": results
    }
    logging.info(json.dumps(log_message, ensure_ascii=False))  

# Route xử lý tìm kiếm
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '').strip()  # Loại bỏ khoảng trắng thừa
    if not keyword:
        return render_template('search_results.html', keyword=keyword, documents=[])

    # Kiểm tra kết nối Elasticsearch
    if not es:
        return render_template(
            'search_results.html',
            keyword=keyword,
            documents=[],
            error="Không thể kết nối đến Elasticsearch. Vui lòng kiểm tra cấu hình."
        )

    try:
        # Tìm kiếm trong Elasticsearch
        response = es.search(
            index="documents_list",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["title", "description"]
                    }
                }
            }
        )

        # Xử lý kết quả
        documents = [
            {
                **hit["_source"],
                "short_description": hit["_source"]["description"][:500] + "..."
            }
            for hit in response["hits"]["hits"]
        ]

        # Ghi log tìm kiếm
        log_search(keyword, documents[:10])
        return render_template('search_results.html', keyword=keyword, documents=documents)

    except Exception as e:
        print(f"Lỗi trong quá trình tìm kiếm: {e}")
        return render_template(
            'search_results.html',
            keyword=keyword,
            documents=[],
            error="Đã xảy ra lỗi trong quá trình tìm kiếm. Vui lòng thử lại sau."
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
