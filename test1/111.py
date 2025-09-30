import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    major TEXT
    )
               
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS courses(
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    instructor TEXT
    )
                      
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS student_courses(
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY  (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
    )
    
''')



while True:
    print("1.Додати студента")
    print("2.Додати курс")
    print("3.показати студентыв")
    print("4.Показати курси")
    print("5.Заєреструвати на курс")
    print("6.Показати студентів на курсі")
    print("7.Вийти")
    choice=input("Оберыть выд 1-7")
    
    if choice=="1":
        name = input("Ведыть ымя")
        age = int(input("Введыть вык"))
        major = input("Ввудыть спец.студента")
        cursor.execute("INSERT INTO students(name,age,major) VALUES (?,?,?)", (name,age,major))
        conn.commit()
    elif choice == "2":
        course_name = input("Введіь назву курсу")
        inst = input("Введіть прізвище інструктора")
        cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?,?)",(course_name,inst))
        conn.commit()
    elif choice == "3":
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if not students:
            print("У базі немає студентів")
        else:
            print("Список студентів")
            for s in students:
                print(f"Імя {s[1]},Спеціалізація {s[3]}")
    elif choice=="4":
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        if not courses:
            print("У базі немає курсів")
        else:
            print("Список курсів")
            for c in courses:
                print(f"ID {c[0]},Назва курсу {c[1]}, прізвище {c[2]}")
    elif choice=="5":
        st_id = int(input("Введіть id студента"))
        c_id = int(input("Введіть id курсу"))

        cursor.execute("INSERT INTO student_courses(student_id, course_id) VALUES (?,?)",(st_id,c_id))            
        conn.commit()
    elif choice == "6":
        course_id = int(input("Введіть ід курсу"))
        cursor.execute("SELECT students.id, students.name,students.age,students.major FROM students, student_courses WHERE students.id = student_courses.student_id AND student_courses.course_id = ?",(course_id,))
        student_on_course = cursor.fetchall()
        if not student_on_course:
            print("На курсі не зареєстровано студентів ")
        else:
            print("Список студентів")
            for s in student_on_course:
                print(f"ID : {s[0]}, імя {s[1]},")
    elif choice == "7":
        break
    else:
        print("Не правильний вибір введіть від 1 до 7")
conn.close()