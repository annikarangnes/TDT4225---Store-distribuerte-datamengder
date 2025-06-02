import mysql.connector as mysql
from db_utils import DbUtils, get_label_match, process_and_insert_data
from part2 import Part2  
import os

def main():
    try:
        # Connect to database
        db_connection = mysql.connect(
            host="tdt4225-12.idi.ntnu.no",  
            database="tolv_db",             
            user="tolv",                    
            password="molde"                
        )

        # Initialize DbUtils
        db_utils = DbUtils(db_connection)

        # creates tables
        db_utils.create_tables()
        print("Tables created successfully!")

        # Checks if the data is already in the tables
        cursor = db_connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM User;")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Activity;")
        activity_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM TrackPoint;")
        trackpoint_count = cursor.fetchone()[0]

        
        if user_count == 0 or activity_count == 0 or trackpoint_count == 0:
            # Only insert data if the tables are empty
            print("One or more tables are empty. Loading data into database...")
            dataset_path = "./dataset"
            
            if not os.path.exists(dataset_path):
                print(f"Dataset directory not found: {dataset_path}")
                return

            # iterates through the datasets and userfiles
            for user_id in os.listdir(dataset_path):
                user_dir = os.path.join(dataset_path, user_id)

                if os.path.isdir(user_dir) and user_id.isdigit():
                    print(f"\nProcessing user {user_id}...")

                    # get labels from labels.txt
                    labels = get_label_match(user_id)
                    print(f"Found {len(labels)} labels for user {user_id}.")
                    db_utils.insert_user(user_id, has_labels=bool(labels))
                    process_and_insert_data(db_utils, user_id, labels)
        else:
            print(f"Data already exists in the tables:")
            print("Skipping data load.")

        part2 = Part2(db_connection)

        while True:
            print("\nWhat task would you like to execute? Type in the number:")
            print("1: Task 1\n2: Task 2\n3: Task 3\n4: Task 4\n5: Task 5\n6a: Task 6a\n6b: Task 6b\n7: Task 7\n8: Task 8\n9: Task 9\n10: Task 10\n11: Task 11\n0: Exit program")
            choice = input("Choose a task: ")

            # Pythom program for running the tasks
            if choice == "1":
                part2.task1()
            elif choice == "2":
                part2.task2()
            elif choice == "3":
                part2.task3()
            elif choice == "4":
                part2.task4()
            elif choice == "5":
                part2.task5()
            elif choice == "6a":
                part2.task6a()
            elif choice == "6b":
                part2.task6b()
            elif choice == "7":
                part2.task7()
            elif choice == "8":
                part2.task8()
            elif choice == "9":
                part2.task9()
            elif choice == "10":
                part2.task10()
            elif choice == "11":
                part2.task11()
            elif choice == "0":
                print("Bye :)")
                break
            else:
                print("Invalid choice. Try again!") 

    except mysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if db_connection.is_connected():
            db_utils.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    main()