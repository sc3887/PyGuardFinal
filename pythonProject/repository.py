import requests
import os
import shutil
import csv
from version import Version
from file import (create_new_folder_in_selected_location,
                          get_directory_path, add_file_to_directory,
                          create_hidden_folder_in_selected_location,
                          check_directory_empty, is_directory_empty
                          ,find_path, empty_directory)
class Repository:
    def __init__(self, current):
        self.location = current
        self.versions = {}

    def wit_init(self):
        create_hidden_folder_in_selected_location(".wit", self.location)
        path = get_directory_path(self.location, ".wit")
        create_new_folder_in_selected_location("stage", path)
        create_new_folder_in_selected_location("version", path)
        versions_path = os.path.join(find_path(self.location, ".wit"), "versions.csv")
        log_path = os.path.join(find_path(self.location, ".wit"), "log.csv")
        # log_path = os.path.join(find_path(self.location,".wit"), "log.csv")
        with open(versions_path, "a", newline='') as version:
            ver = csv.writer(version)  # טוען את כל השורות לרשימה
        with open(log_path, "a", newline='') as log:
            log = csv.writer(log)  # טוען את כל השורות לרשימה

    def wit_add(self):
        add_file_to_directory(self.location, get_directory_path(get_directory_path(self.location, ".wit"), "stage"))

    def wit_commit(self):
        summary = input("summary(required): ")
        description = input("Description: ")
        new_version = Version(summary, description)
        self.versions[summary] = new_version

        log_path = find_path(self.location, "log.csv")
        with open(log_path, "a", newline="") as log:
            writer = csv.writer(log)
            writer.writerow(["hashCode", new_version.hashCode, "summary", new_version.summary, "description",
                             new_version.description, "date", new_version.date])

        file_path = find_path(self.location, "versions.csv")
        with open(file_path, "a", newline="") as version:
            writer = csv.writer(version)
            writer.writerow([new_version.summary])
            print("Version added successfully.")

        path = find_path(self.location, "version")

        if is_directory_empty(path):
            create_new_folder_in_selected_location(new_version.summary, path)
            for item in os.listdir(find_path(self.location, "stage")):
                item_path = os.path.join(find_path(self.location, "stage"), item)
                if not os.path.isdir(item_path):
                    shutil.copy(item_path, find_path(self.location, new_version.summary))
            empty_directory(find_path(self.location, "stage"))
        else:
            file_path = find_path(self.location, "versions.csv")
            with open(file_path, "r") as csv_versions:
                rows = list(csv.reader(csv_versions))
                prev_version = str(rows[-2][0])
                new_version = str(rows[-1][0])
                new_path = find_path(self.location, "version")
                create_new_folder_in_selected_location(new_version, new_path)
                for item in os.listdir(find_path(self.location, prev_version)):
                    item_path = os.path.join(find_path(self.location, prev_version), item)
                    if not os.path.isdir(item_path):
                        destination_path = find_path(path, new_version)
                        if item_path != os.path.join(destination_path, item):  # בדוק אם זה לא אותו קובץ
                            shutil.copy(item_path, destination_path)
                for item in os.listdir(find_path(self.location, "stage")):
                    item_path = os.path.join(find_path(self.location, "stage"), item)
                    if not os.path.isdir(item_path):
                        destination_path = os.path.join(find_path(path, new_version), item)
                        if item_path != destination_path:  # בדוק אם זה לא אותו קובץ
                            shutil.copy(item_path, destination_path)
                empty_directory(find_path(self.location, "stage"))
                summary_path = os.path.join(find_path(path, new_version), f"{summary}.txt")
                with open(summary_path, "w") as file:
                    file.write(description)

    def wit_log(self):
        print(
            "--------------------------------------------------log------------------------------------------------------------------")
        with open(find_path(self.location, "log.csv"), "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)

    def wit_status(self):
        path = find_path(self.location, "stage")
        check_directory_empty(path)

    def wit_checkout(self):
        print("enter commit you want to checkout:")
        with open(find_path(self.location, "versions.csv"), "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row[-1])
        version_prev = input("version: ")
        prev_version = find_path(self.location, version_prev)
        while prev_version == None:
            print("enter again commit you want to checkout:")
            with open(find_path(self.location, "versions.csv"), "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    print(row[-1])
            version_prev = input("version: ")
            prev_version = find_path(self.location, version_prev)
        log_path = find_path(self.location, "log.csv")
        # print(log_path)
        for item in os.listdir(self.location):
            item_path = os.path.join(self.location, item)
            if not os.path.isdir(item_path):  # אם זה לא תיקיה
                os.remove(item_path)
        for item in os.listdir(find_path(self.location, version_prev)):
            item_path = os.path.join(find_path(self.location, version_prev), item)
            if not os.path.isdir(item_path):  # אם זה לא תיקיה
                shutil.copy(item_path, self.location)  # העתק את הקובץ לתיקיה היעד


    def wit_push(self):
        # 1. מוצאים את נתיב תיקיית ה-stage
        stage_path = os.getcwd()
        #stage_path = get_directory_path(get_directory_path(self.location, ".wit"), "stage")
        server_url = "http://localhost:8000"  # כתובת השרת שלך

        # 2. עוברים על כל קובץ בתיקיה
        for filename in os.listdir(stage_path):
            file_path = os.path.join(stage_path, filename)
            # 3. בודקים אם הסיומת היא .py
            if os.path.isfile(file_path) and filename.endswith(".py"):
                with open(file_path, "rb") as f:
                    files = {"file": (filename, f, "text/x-python")}
                    # 4. שולחים ל/analyze
                    analyze_resp = requests.post(f"{server_url}/analyze", files=files)
                    if analyze_resp.status_code == 200:
                        # 5. שומרים את קובץ ה-zip (לא חובה)
                        with open(os.path.join(stage_path, f"{filename}_analysis.zip"), "wb") as out:
                            out.write(analyze_resp.content)
                        print(f"Analysis for {filename} sent and saved.")
                    else:
                        print(f"Failed to analyze {filename}: {analyze_resp.text}")

                    f.seek(0)  # מחזירים את המצביע להתחלה
                    # 6. שולחים ל/alerts
                    alerts_resp = requests.post(f"{server_url}/alerts", files=files)
                    if alerts_resp.status_code == 200:
                        # 7. שומרים את קובץ ה-issues (לא חובה)
                        with open(os.path.join(stage_path, f"{filename}_issues.txt"), "wb") as out:
                            out.write(alerts_resp.content)
                        print(f"Issues for {filename} sent and saved.")
                    else:
                        print(f"Failed to get alerts for {filename}: {alerts_resp.text}")


repo = Repository("C:\\Users\\user1\\Desktop\\pythonProject")
#repo = Repository("C:\\Users\\user1\\Pictures\\Saved Pictures")
#repo.wit_init()
#repo.wit_add()
# repo.wit_commit()
# repo.wit_log()
# repo.wit_status()
# repo.wit_checkout()
