from pymongo import MongoClient
from datetime import datetime

def connect_mongodb():
    client = MongoClient('localhost', 27017)
    client.admin.command('ping')
    print("✅ Подключение к MongoDB успешно!")
    return client

def parse_data_file(filename):
    """Парсит файл с данными в формате ключ: значение"""
    data = {}
    current_key = None
    current_value = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    current_record = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if ':' in line and not line.startswith(' '):
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ''
            
            if key == '---' or key.startswith('#'):
                if current_record:
                    result.append(current_record)
                    current_record = {}
            else:
                current_record[key] = value
        else:
            if current_record:
                last_key = list(current_record.keys())[-1]
                current_record[last_key] = current_record.get(last_key, '') + ' ' + line
    
    if current_record:
        result.append(current_record)
    
    print(f"Загружено {len(result)} записей из {filename}")
    return result

def add_only_new_data(data_list, collection):
    added_count = 0
    skipped_count = 0
    
    for doc in data_list:
        existing = collection.find_one({"url": doc.get("url", "")}) if doc.get("url") else None
        
        if existing is None:
            doc['parsed_at'] = datetime.now()
            collection.insert_one(doc)
            added_count += 1
            print(f"  ➕ Добавлено: {doc.get('title', doc.get('ЗАГОЛОВОК', 'без названия'))[:50]}")
        else:
            skipped_count += 1
    
    print(f"\n📊 Результат: добавлено {added_count}, пропущено {skipped_count}")
    return added_count

def main():
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА: ЗАПИСЬ ДАННЫХ ИЗ ЗАДАЧ 4-5 В MONGODB")
    print("=" * 60)
    
    print("\n🔌 Подключение к MongoDB...")
    try:
        client = connect_mongodb()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Убедись, что MongoDB сервер запущен")
        return
    
    db = client['ria_news']
    collection = db['articles']
    print(f"📁 База: {db.name}, Коллекция: {collection.name}")
    
    print("\n📂 Загрузка данных из файлов...")
    xpath_data = parse_data_file('xpath_data.txt')
    bs4_data = parse_data_file('bs4_data.txt')
    
    all_data = xpath_data + bs4_data
    print(f"\nВсего записей для добавления: {len(all_data)}")
    
    print("\n💾 Добавление данных в MongoDB...")
    add_only_new_data(all_data, collection)
    
    total = collection.count_documents({})
    print(f"\n📊 Всего записей в базе: {total}")
    
    print("\n✅ Лабораторная работа выполнена!")

if __name__ == "__main__":
    main()