import json
from pyvi import ViTokenizer

with open('D:\\Project Github\\BK-THK_Search_Engine\\BK-THK-search-engine\\data\\merged_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Hàm để loại bỏ dấu ngoặc kép và tách từ với dấu '|'
def tokenize_and_format(text):
    # Tách từ bằng ViTokenizer
    tokenized_text = ViTokenizer.tokenize(text)
    
    # Tách và nối từ bằng dấu "|"
    words = tokenized_text.split()
    
    formatted_text = '|'.join(words)
    return formatted_text

output_data = []

# Lặp qua các phần tử trong danh sách data
for item in data:
    for field in ['title', 'description']:
        text = item.get(field, "")
        # Thêm vào danh sách output_data
        item[field] = tokenize_and_format(text)

    output_data.append(item)

# Ghi kết quả vào file output
with open('D:\\Project Github\\BK-THK_Search_Engine\\BK-THK-search-engine\\data\\vietokenized_data.json', 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)

print("Kết quả đã được ghi vào file 'output.json'.")
