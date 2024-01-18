import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class DesktopOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Organizer")

        self.create_gui()

    def create_gui(self):
        self.create_folder_btn = tk.Button(self.root, text="Create Folder", command=self.create_folder)
        self.organize_by_type_btn = tk.Button(self.root, text="Organize by Type", command=self.organize_by_type)
        self.organize_into_folders_btn = tk.Button(self.root, text="Organize into Folders", command=self.organize_into_folders)

        self.create_folder_btn.pack(pady=10)
        self.organize_by_type_btn.pack(pady=10)
        self.organize_into_folders_btn.pack(pady=10)

    def create_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder Location")
        if folder_path:
            folder_name = filedialog.askstring("Folder Name", "Enter Folder Name:")
            if folder_name:
                new_folder_path = os.path.join(folder_path, folder_name)
                os.makedirs(new_folder_path)
                messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully!")

    def organize_by_type(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        extensions_order = {
            "Shortcuts": ["lnk", "url", "ink"],
            "Documents": ["pdf", "docx", "rtf", "txt"],
            "Recycle Bin": ["$recycle.bin"],
            "Images": ["jpg", "png", "gif", "bmp", "jpeg"],
            "Others": []  # Add other file types here
        }

        # Get a list of all files on the desktop
        desktop_files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
        desktop_folders = [f for f in os.listdir(desktop_path) if os.path.isdir(os.path.join(desktop_path, f))]

        # Separate folders from files
        folder_files = [f for f in desktop_files if os.path.splitext(f)[1] == '.folder']
        desktop_files = [f for f in desktop_files if os.path.splitext(f)[1] != '.folder']

        # Custom sorting function
        def custom_sort(file_name):
            file_extension = file_name.split(".")[-1].lower()
            for idx, ext_list in enumerate(extensions_order.values()):
                if file_extension in ext_list:
                    return idx, file_name.lower()
            return len(extensions_order), file_name.lower()

        # Sort folders separately
        sorted_folders = sorted(desktop_folders, key=lambda f: f.lower(), reverse=True)

        # Move folders to the top right
        for idx, folder_name in enumerate(sorted_folders):
            source_path = os.path.join(desktop_path, folder_name)
            destination_path = os.path.join(desktop_path, f"{idx+1:02d}_{folder_name}")
            shutil.move(source_path, destination_path)

        # Sort the files based on the custom order
        sorted_files = sorted(desktop_files, key=custom_sort)

        # Move files to their ordered positions on the desktop
        for idx, file_name in enumerate(sorted_files):
            source_path = os.path.join(desktop_path, file_name)
            if "recycle" in file_name.lower():
                destination_path = os.path.join(desktop_path, f"{idx+1+len(sorted_folders):02d}_Recycle Bin_{file_name}")
            else:
                destination_path = os.path.join(desktop_path, f"{idx+1+len(sorted_folders):02d}_{file_name}")
            shutil.move(source_path, destination_path)

        # Move .folder files to the top right
        for idx, folder_file in enumerate(folder_files):
            source_path = os.path.join(desktop_path, folder_file)
            destination_path = os.path.join(desktop_path, f"{idx+1:02d}_{folder_file}")
            shutil.move(source_path, destination_path)

        messagebox.showinfo("Success", "Desktop organized by type successfully!")




    def organize_into_folders(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        folders = {
            "Documents": ["pdf", "docx", "rtf", "txt", "odt"],
            "Images": ["jpg", "png", "gif", "bmp", "jpeg", "webp", "svg", "avif"],
            "Games and Others": ["lnk", "url", "lnk"],
            "Others": ["zip", "mp3", "mp4", "rb", "exe", "jsx", "json", "rar", "7z"]  # Add other file types here
        }

        for folder, extensions in folders.items():
            folder_path = os.path.join(desktop_path, folder)
            os.makedirs(folder_path, exist_ok=True)

            for item in os.listdir(desktop_path):
                item_path = os.path.join(desktop_path, item)
                if os.path.isfile(item_path):
                    file_extension = item.split(".")[-1].lower()
                    if file_extension in extensions:
                        destination_folder = os.path.join(folder_path, item)

                        # Check if the destination folder already exists
                        if not os.path.exists(destination_folder):
                            shutil.move(item_path, destination_folder)

        messagebox.showinfo("Success", "Desktop organized into folders successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopOrganizer(root)
    root.mainloop()


