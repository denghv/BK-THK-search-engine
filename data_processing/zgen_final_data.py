import json

# Hàm thay dấu "_" thành khoảng trắng
def replace_underscore_with_space(text):
    return text.replace("_", " ")

# Đọc dữ liệu từ file JSON
with open(r'D:\\Project Github\\BK-THK_Search_Engine\\BK-THK-search-engine\\data\\vietokenized_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Kiểm tra dữ liệu là danh sách (nhiều đối tượng JSON)
if isinstance(data, list):
    for item in data:
        for field in ['title', 'description']:
            if field in item:
                item[field] = replace_underscore_with_space(item[field])

# Lưu kết quả vào file output
with open('D:\\Project Github\\BK-THK_Search_Engine\\BK-THK-search-engine\\data\\final_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Đã hoàn thành thay thế dấu gạch dưới và lưu vào data/final_data.json.")
