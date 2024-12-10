import os
import json

# Đường dẫn đến thư mục chứa các file JSON
directory = "path:\\main_dataset"  # Chỉnh sửa đường dẫn 

merged_data = []

# Lặp qua tất cả các file trong thư mục
for filename in os.listdir(directory):
    # Kiểm tra chỉ lấy các file JSON
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        
        try:
            # Mở và đọc file JSON
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Lọc chỉ lấy các trường cần thiết và thêm vào danh sách merged_data
                for item in data:
                    merged_data.append({
                        "title": item.get("title", ""),
                        "description": item.get("description", ""),
                        "link": item.get("link", "")
                    })
        except Exception as e:
            print(f"Không thể đọc file {filename}: {e}")

# Lưu dữ liệu gộp thành một file JSON mới
output_file = "path/merged_data.json"
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=4)

print(f"Dữ liệu đã được gộp vào file {output_file}")
