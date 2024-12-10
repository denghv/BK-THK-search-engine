import json

# Đọc dữ liệu từ file JSON
with open('path:\\old_dataset\\sol3_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Xóa các trường thừa và bổ sung trường 'link' nếu thiếu
for document in data:
    # Xóa các trường thừa
    for field in ['author', 'category', 'tags', 'tag_links', 'chapter_count', 'comment_count', 
                  'next_page', 'content', 'alt_name', 'comments']:
        if field in document:
            del document[field]
    
    # Bổ sung trường 'link' nếu không có
    if 'link' not in document:
        document['link'] = ""

# Ghi lại dữ liệu đã xóa trường vào một file JSON mới
with open('path:\\cleaned_data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Dữ liệu đã được lưu vào 'cleaned_data.json'.")
