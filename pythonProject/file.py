import os
import shutil
import subprocess

def empty_directory(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # מחיקת קובץ
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # מחיקת תיקיה

def find_path(base_directory, target_name):
    for root, dirs, files in os.walk(base_directory):
        if target_name in dirs or target_name in files:
            return os.path.join(root, target_name)
    return None  # אם לא נמצא

# יצירת תיקייה חדשה
def create_new_folder_in_selected_location(folder_name, location):
    newpath = os.path.join(location, folder_name)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print(f"A folder is created in the path: {newpath}")
    else:
        print("The folder already exists.")


# יצירת תיקייה חדשה נסתרת
def create_hidden_folder_in_selected_location(folder_name, location):
    newpath = os.path.join(location, folder_name)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        # הפעלת פקודת cmd כדי להסתיר את התיקיה
        subprocess.call(['attrib', '+h', newpath])
        print(f"A hidden folder is created in the path: {newpath}")
    else:
        print("The folder already exists.")


def find_file_or_directory(path, name):
    for root, dirs, files in os.walk(path):
        if name in files or name in dirs:
            return os.path.join(root, name)
    print("הקובץ אינו קיים!!!!")
    return None


# קבלת ניתוב של תיקיה
def get_directory_path(base_directory, directory_name):
    return os.path.abspath(os.path.join(base_directory, directory_name))


# קבלת ניתוב של קובץ
def get_file_path(file_name):
    return os.path.abspath(file_name)

# הוספת קובץ לתיקייה
def add_file_to_directory(directory_source, directory_stage):
        if not os.path.exists(directory_stage):
            os.makedirs(directory_stage)
        for file_name in os.listdir(directory_source):
            # בודק את הנתיב המלא של הקובץ
            file_path = os.path.join(directory_source, file_name)
            # בודק אם זה קובץ ולא תיקייה
            if os.path.isfile(file_path):
                shutil.copy2(file_path, os.path.join(directory_stage, file_name))


#מחיקת קובץ
def delete_file(file_name):
    try:
        os.remove(file_name)
        print(f"File '{file_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_directory_empty(directory_path):
    # קבלת רשימת הקבצים בתיקייה
    files = os.listdir(directory_path)
    if not files:
        print(" status: The directory is empty.")
    else:
        print("status: The directory is not empty.")
        print("File names in the directory:")
        for file in files:
            print(file)

#פונקציה שמעבירה את הקבצים מSTAGE ל - VERSION
def copy_files_to_version(stage_directory, version_directory):
    # עובר על כל הקבצים בתיקיית ה-stage
    for file_name in os.listdir(stage_directory):
        # בודק את הנתיב המלא של הקובץ
        file_path = os.path.join(stage_directory, file_name)
        # בודק אם זה קובץ ולא תיקייה
        if os.path.isfile(file_path):
            # מעתיק את הקובץ לתיקיית ה-version (ידרס אם קיים קובץ עם אותו שם)
            shutil.copy(file_path, os.path.join(version_directory, file_name))

 # בודק אם התיקייה ריקה
def is_directory_empty(directory_path):
    if not os.path.exists(directory_path):
        raise ValueError("The specified directory does not exist.")
    return len(os.listdir(directory_path)) == 0


def copy_directory(source_directory, new_directory_name):
    # מגדיר את הנתיב החדש
    new_directory_path = os.path.join(os.path.dirname(source_directory), new_directory_name)
    # מעתיק את התיקיה
    shutil.copytree(source_directory, new_directory_path)

def copy_files(src_dir, dest_dir):
    # ודא שהתיקיה היעד קיימת, אם לא, צור אותה
    os.makedirs(dest_dir, exist_ok=True)

    # עבור על כל הפריטים בתיקיה המקורית
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        # אם זה קובץ, העתק אותו לתיקיה היעד
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)

#בדיקה האם הקובץ הוק קובץ PY
def get_python_files_to_push(files):
    return [f for f in files if f.endswith('.py')]


