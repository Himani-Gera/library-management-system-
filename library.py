import pymysql
from datetime import date , timedelta
import os
from dotenv import load_dotenv
connection = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_DATABASE")
)
cursor=connection.cursor()

def login():
     print("Library Management System\n")
     print("Admin\n")
     print("student\n")
     choice=input("admin/student : ")
     password="himani"
     if choice=='admin':
          give=input("password : ")
          if give== password:
               main_menu()
          else:
               print("Incorrect password")
               return
     elif choice=='student':
          stu_dashboard()
     else:
        print("Invalid choice. Please try again.")
def main_menu():
    while True:
        print("\n Library Management System\n")
        print("1.Add student\n")
        print("2.Add book\n")
        print("3.Issue book\n")
        print("4.Return book\n")
        print("5.Dues\n")
        print("6. View list of books\n")
        print("7.search for a book\n")
        print("8. View a student's history\n")
        print("9.Delete books\n")
        print("10.remove student\n")
        print("11.Exit\n")
        choice=int(input("Enter step number: "))
        if choice==1:
                add_student()
        elif choice==2:
             add_book()
        elif choice==3:
             book_issue()
        elif choice==4:
             return_book()
        elif choice==5:
             check_dues()
        elif choice==6:
             view_books()
        elif choice==7:
             search_book()
        elif choice==8:
             stu_history()
        elif choice==9:
             delete_book()
        elif choice==10:
             remove_student()
        elif choice==11:
                cursor.close()
                connection.close()
                print("Exiting the program.")
                break
             
        else:
             print("Invalid choice. Please try again.")

def stu_dashboard():
     while True:
             print("\n Library Management System\n")
             print("1.Dues\n")
             print("2. View list of books\n")
             print("3.search for a book\n")
             print("4.Exit\n")
             choice=int(input("Enter step number: "))
            
             if choice==1:
                  check_dues()
             elif choice==2:
                   view_books()
             elif choice==3:
                  search_book()
             elif choice==4:
                     cursor.close()
                     connection.close()
                     print("Exiting the program.")
                     break
                  
             else:
                  print("Invalid choice. Please try again.")
def add_student():
    
    name = input("student name : ")
    id = input("student id : ")
    year = input("College year : ")
    course = input("course name : ")
   
    cursor.execute("insert into student_info (student_id,student_name,year,course) values(%s,%s,%s,%s);",(id,name,year,course))
    connection.commit()
def book_issue():
     student_id =input("student id : ")
     cursor.execute("select * from student_info where student_id=%s;",(student_id))
     result=cursor.fetchone()
     if result:
          book_id = input("book id : ")
          cursor.execute("select available_copies from books where book_id=%s;",(book_id))
          book=cursor.fetchone()
          if book:
               date_of_issue=date.today()
               date_of_submission=date_of_issue+timedelta(days = 14)
               cursor.execute("update books set available_copies=available_copies-1 where book_id=%s",(book_id))
               cursor.execute("insert into book_issue (student_id,book_id,date_of_issue,date_of_submission,date_of_return) values(%s,%s,%s,%s,%s);",(student_id,book_id,date_of_issue,date_of_submission,None))
               connection.commit()
          else: 
               print("book not found")
     else :
          print("student is not registered")

def add_book():
     book_id=input("book id : ")
     book_name=input("book name : ")
     total_copies=int(input("total books : "))
     available_copies=total_copies
     cursor.execute("insert into books(book_id,book_name,total_copies,available_copies) values(%s,%s,%s,%s);",(book_id,book_name,total_copies,available_copies))
     connection.commit()
def return_book():
     student_id=input("student_id : ")
     cursor.execute("select * from book_issue where student_id=%s and date_of_return is %s;",(student_id,None))
     result=cursor.fetchone()
     if result:
        book_id=input("return book id : ")
        cursor.execute("select* from book_issue where book_id=%s and date_of_return is %s;",(book_id,None))
        date_of_return=date.today()
        cursor.execute("update books set available_copies=available_copies+1 where book_id=%s;",(book_id))
        cursor.execute("update book_issue set date_of_return=%s where student_id=%s and book_id=%s;",(date_of_return,student_id,book_id) )

        connection.commit()

     else:
          print("no book is issued under this student_id")
def check_dues():
    student_id = input("Student ID: ")
    cursor.execute(
        "SELECT book_id, date_of_submission, date_of_return FROM book_issue WHERE student_id=%s",
        (student_id,))
    records = cursor.fetchall()
    if not records:
        print("No records found for this student.")
        return
    total_fine = 0
    for book_id, date_of_submission, date_of_return in records:
        if date_of_return is None:
            print(f"Book {book_id}: not yet returned.")
            continue
        if date_of_return > date_of_submission:
            late_days = (date_of_return - date_of_submission).days
            fine = late_days * 5
            total_fine += fine
            print(f"Book {book_id}: {late_days} days late, fine = {fine}")
        else:
            print(f"Book {book_id}: returned on time, no fine.")
    print(f"\nTotal due amount: {total_fine}")
    connection.commit()

def view_books():
     cursor.execute("select* from books;")
     books=cursor.fetchall()
     print( books)
     connection.commit()
def search_book():
     search=input("book name/id : ")
     cursor.execute("select book_id,book_name,available_copies from books where book_id like %s  or book_name like %s",( '%'+search+'%','%'+search+'%' ))
     book=cursor.fetchall()
     print(book)
     connection.commit()

def stu_history():
     student_id = input("student id : ")
     cursor.execute("select * from student_info where student_id=%s;",(student_id))
     existance=cursor.fetchone()
     if existance:
        cursor.execute("select * from book_issue where student_id=%s;",(student_id))
        history=cursor.fetchall()
        if history==None:
             print("no record for this student")
        else:
            print(history)
     else:
          print("no student registered under this id ")
     
def delete_book():
     book_id=input("book id :")
     cursor.execute("select * from books where book_id =%s;",(book_id))
     record=cursor.fetchone()
     if record:
          print("1.delete all copies")
          print("2.delete few copies")
          choose=int(input(" enter choice to delete : "))
          if choose==1:
               cursor.execute("delete * from books where book_id=%s;",(book_id))
               connection.commit()
          elif choose==2:
               copies=int(input("no. of copies :"))
               cursor.execute("update books set total_copies=total_copies-%s , available_copies=available_copies-%s where book_id=%s;",(copies,copies,book_id))
               connection.commit()
          else:
               print("error in choice please select again ")
               return
def remove_student():
     info =input("student id : ")
     cursor.execute("delete from book_issue where student_id=%s;",(info))
     cursor.execute("select* from student_info where student_id=%s;",(info))
     yes=cursor.fetchone()
     if yes:
        cursor.execute("delete from student_info where student_id=%s; ",(info))
        connection.commit()
        print("student is removed from records")
     else:
          print("no such student exits ")




login()
