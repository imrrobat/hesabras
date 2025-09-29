import os

def get_cat(filename="cat.csv"):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("category\n")
        return []
    
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if line: 
                data.append(line)
    return data

def add_cat(category, filename="cat.csv"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{category}\n")


