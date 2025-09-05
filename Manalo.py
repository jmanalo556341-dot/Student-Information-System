import csv

# Dorado, Arfred A.

# Key: student_id (str), Value: dict with 'info' (tuple), 'age' (int), 'grades' (list)

students = {}

# Global filename for saving/loading

FILENAME = "students.csv"

# Lambda function to calculate average grade

average_grade = lambda grades: sum(grades) / len(grades) if grades else 0


def add_student(student_id, name, age=18, *grades):
    if student_id in students:
        print(f"Student with ID {student_id} already exists.")

        return False

    # Tuple for fixed info: (student_id, name)

    info = (student_id, name)

    # Grades stored as list

    grades_list = list(grades)

    students[student_id] = {'info': info, 'age': age, 'grades': grades_list}

    print(f"Added student {name} with ID {student_id}.")

    return True


def display_students(from_file=False):
    """

    Display all students.

    If from_file is True, load from file and display.

    Otherwise display from current memory.

    """

    data = students

    if from_file:

        data = load_from_file()

        if data is None:
            print("No data to display from file.")

            return

    if not data:
        print("No students to display.")

        return

    print(f"\n{'ID':<10} {'Name':<20} {'Age':<5} Grades")

    print("-" * 50)

    # For loop to display students

    for sid, details in data.items():

        info = details['info']  # tuple (student_id, name)

        age = details['age']

        grades = details['grades']

        print(f"{info[0]:<10} {info[1]:<20} {age:<5} ", end="")

        # Nested loop to print each grade

        for g in grades:
            print(f"{g} ", end="")

        print()

    print("-" * 50)


def update_student(student_id, **kwargs):
    """

    Update student information.

    kwargs can include 'name', 'age', 'grades' (list)

    """

    if student_id not in students:
        print(f"No student found with ID {student_id}")

        return False

    student = students[student_id]

    info = list(student['info'])

    # Update name (tuple is immutable, so recreate)

    if 'name' in kwargs:
        old_name = info[1]

        info[1] = kwargs['name']

        print(f"Updated name from {old_name} to {info[1]}")

    # Update age

    if 'age' in kwargs:
        old_age = student['age']

        student['age'] = kwargs['age']

        print(f"Updated age from {old_age} to {student['age']}")

    # Update grades (replace entire list if provided)

    if 'grades' in kwargs:
        old_grades = student['grades']

        student['grades'] = kwargs['grades']

        print(f"Updated grades from {old_grades} to {student['grades']}")

    # Reassign the updated tuple info

    student['info'] = tuple(info)

    return True


def delete_student(student_id):
    """

    Delete a student record.

    """

    if student_id in students:

        del students[student_id]

        print(f"Deleted student with ID {student_id}.")

        return True

    else:

        print(f"No student found with ID {student_id}.")

        return False


def save_to_file(filename=FILENAME):
    """

    Save students data to a CSV file.

    """

    try:

        with open(filename, mode='w', newline='') as file:

            writer = csv.writer(file)

            # Write header

            writer.writerow(['ID', 'Name', 'Age', 'Grades'])

            for sid, details in students.items():
                info = details['info']

                age = details['age']

                grades = details['grades']

                # Convert grades list to string separated by ;

                grades_str = ';'.join(map(str, grades))

                writer.writerow([info[0], info[1], age, grades_str])

        print(f"Data saved to {filename}")

        return True

    except Exception as e:

        print(f"Failed to save data: {e}")

        return False


def load_from_file(filename=FILENAME):
    """

    Load students data from a CSV file.

    Returns a dictionary similar to global students or None on failure.

    """

    data = {}

    try:

        with open(filename, mode='r') as file:

            reader = csv.DictReader(file)

            for row in reader:
                sid = row['ID']

                name = row['Name']

                age = int(row['Age'])

                grades_str = row['Grades']

                grades = list(map(int, grades_str.split(';'))) if grades_str else []

                info = (sid, name)

                data[sid] = {'info': info, 'age': age, 'grades': grades}

        print(f"Data loaded from {filename}")

        return data

    except FileNotFoundError:

        print(f"No file named {filename} found.")

        return None

    except Exception as e:

        print(f"Failed to load data: {e}")

        return None


def main_menu():
    global students

    while True:

        print("""

===== Student Information System =====

1. Add Student

2. Display Students (from memory)

3. Display Students (from file)

4. Update Student

5. Delete Student

6. Save to File

7. Load from File

8. Exit

""")

        choice = input("Enter your choice: ").strip()

        # Demonstrate break and continue

        if choice == '8':

            print("Exiting program.")

            break

        elif choice not in map(str, range(1, 9)):

            print("Invalid choice. Please try again.")

            continue

        if choice == '1':

            sid = input("Enter Student ID: ").strip()

            name = input("Enter Name: ").strip()

            try:

                age = int(input("Enter Age (default 18): ").strip() or 18)

            except ValueError:

                age = 18

            grades_input = input("Enter grades separated by spaces: ").strip()

            grades = []

            if grades_input:

                try:

                    grades = list(map(int, grades_input.split()))

                except ValueError:

                    print("Invalid grades input. No grades added.")

            add_student(sid, name, age, *grades)

            save_to_file()  # save after operation



        elif choice == '2':

            display_students(from_file=False)

        elif choice == '3':

            data = load_from_file()

            if data:

                # Temporarily display data from file without changing global students

                print("\nStudents from file:")

                print(f"\n{'ID':<10} {'Name':<20} {'Age':<5} Grades")

                print("-" * 50)

                for sid, details in data.items():

                    info = details['info']

                    age = details['age']

                    grades = details['grades']

                    print(f"{info[0]:<10} {info[1]:<20} {age:<5} ", end="")

                    for g in grades:
                        print(f"{g} ", end="")

                    print()

                print("-" * 50)

            else:

                print("No data loaded from file.")

        elif choice == '4':

            sid = input("Enter Student ID to update: ").strip()

            if sid not in students:
                print("Student not found.")

                continue

            print("Leave field empty if no change.")

            new_name = input("New Name: ").strip()

            new_age_str = input("New Age: ").strip()

            new_grades_str = input("New grades separated by spaces (replaces old grades): ").strip()

            kwargs = {}

            if new_name:
                kwargs['name'] = new_name

            if new_age_str:

                try:

                    kwargs['age'] = int(new_age_str)

                except ValueError:

                    print("Invalid age input; age not updated.")

            if new_grades_str:

                try:

                    kwargs['grades'] = list(map(int, new_grades_str.split()))

                except ValueError:

                    print("Invalid grades input; grades not updated.")

            update_student(sid, **kwargs)

            save_to_file()

        elif choice == '5':

            sid = input("Enter Student ID to delete: ").strip()

            if delete_student(sid):
                save_to_file()

        elif choice == '6':

            save_to_file()

        elif choice == '7':

            loaded = load_from_file()

            if loaded:
                students = loaded  # Update global dictionary

        else:

            # Just in case, though handled above

            print("Invalid choice. Try again.")


# At program start, load data from file

if __name__ == "__main__":

    loaded_data = load_from_file()

    if loaded_data:
        students = loaded_data

    main_menu()



