import os
import csv


def get_cat(filename="cat.csv"):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["category", "type"])
            writer.writerow(["دسته بندی نشده", "income"])
            writer.writerow(["دسته بندی نشده", "expense"])
        return [["دسته بندی نشده", "income"], ["دسته بندی نشده", "expense"]]
    
    data = []
    with open(filename, "r", encoding="utf-8", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and len(row) == 2:
                data.append(row)
    return data


def add_cat(category, typ, filename="cat.csv"):
    with open(filename, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([category, typ])

def add_data(title, amount, in_date, category,type,filename="data.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["title", "amount", "date", "category","type"])
        writer.writerow([title, amount, in_date, category,type])

def read_data(filename="data.csv"):
    result = []

    # بررسی می‌کنیم فایل وجود داره یا نه
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # فقط هدر رو می‌نویسیم
            writer.writerow(["title", "amount", "date", "category", "type"])

    # خوندن داده‌ها
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['amount']:  # اگر فایل خالی بود یا فقط هدر داشت
                continue
            amount = int(row['amount'].replace(',', ''))
            item = {
                'title': row['title'],
                'type': row['type'],
                'amount': f'{amount:,}',
                'date': row['date'],
                'category': row['category']
            }
            result.append(item)
    return result

def aggregate_data(data, t_type):
    agg = {}
    for item in data:
        if item['type'] == t_type:
            amount = int(item['amount'].replace(',', ''))
            category = item['category']
            agg[category] = agg.get(category, 0) + amount
    return agg