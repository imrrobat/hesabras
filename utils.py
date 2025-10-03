import os
import csv

def get_cat(filename="cat.csv"):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["category", "type"])
            writer.writerow(["دسته بندی نشده", "income"])
            writer.writerow(["دسته بندی نشده", "expense"])
        return {"دسته بندی نشده": ["income", "expense"]}  # چند نوع ممکن برای دسته
    
    data = {}
    with open(filename, "r", encoding="utf-8", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and len(row) == 2:
                cat, typ = row
                if cat in data:
                    data[cat].append(typ)
                else:
                    data[cat] = [typ]
    return data


def add_cat(category, typ='income', filename="cat.csv"):
    with open(filename, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([category, typ])


def add_income(title, amount, income_date, category, filename="income.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["title", "amount", "date", "category"])
        writer.writerow([title, amount, income_date, category])
