import os
import subprocess
from termcolor import colored

# Prompt user for action
print(colored("What would you like to do?", "cyan"))
print("1. Download all reports")
print("2. Generate aggregate reports")

choice = input(colored("Enter the number corresponding to your choice: ", "cyan"))

if choice == "1":
    # Run download_reports.py
    os.system("python Scripts/download_reports.py")
    
elif choice == "2":
    if not os.path.exists("Reports"):
        print(colored("No reports found. Please download reports before generating aggregate reports.", "red"))
    else:
        # Prompt user to choose artist folder
        artist_folders = [f for f in os.listdir("Reports") if os.path.isdir(os.path.join("Reports", f))]
        if len(artist_folders) == 0:
            print(colored("No artist folders found in Reports.", "red"))
            exit()
        elif len(artist_folders) == 1:
            artist_folder = artist_folders[0]
        else:
            print(colored("Multiple artist folders found in Reports. Please choose one.", "cyan"))
            for i, folder in enumerate(artist_folders):
                print(f"{i+1}. {folder}")
            artist_choice = int(input(colored("Enter the number corresponding to your choice: ", "cyan")))
            artist_folder = artist_folders[artist_choice - 1]
            
        # Prompt user to choose date_downloaded folder
        date_folders = [f for f in os.listdir(os.path.join("Reports", artist_folder)) if os.path.isdir(os.path.join("Reports", artist_folder, f))]
        if len(date_folders) == 0:
            print(colored("No report download folders found for selected artist.", "red"))
            exit()
        elif len(date_folders) == 1:
            date_folder = date_folders[0]
        else:
            print(colored("Multiple report download folders found for selected artist. Please choose one.", "cyan"))
            for i, folder in enumerate(date_folders):
                print(f"{i+1}. {folder}")
            date_choice = int(input(colored("Enter the number corresponding to your choice: ", "cyan")))
            date_folder = date_folders[date_choice - 1]
            
        # Run aggregate_reports.py
        os.system(f"python Scripts/aggregate_reports.py ")
        subprocess.run(["python", os.path.join("Scripts", "aggregate_reports.py"), artist_folder, date_folder])
        
        # Run aggregate_reports_detailed.py
        subprocess.run(["python", os.path.join("Scripts", "aggregate_reports_detailed.py"), artist_folder, date_folder])

else:
    print(colored("Invalid choice. Please try again.", "red"))
