import re
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
# Book
class Book:
    def __init__(self, book_id="", title="", author="", publisher="", status="", importer="", quantity=0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.status = status
        self.importer = importer  
        self.quantity = quantity 

    def input_info(self):
        # BookID: 1 ký tự in hoa + 4 số, duy nhất
        while True:
            bid = input("Nhập mã sách (VD: A0001): ").strip()
            if re.match(r"^[A-Z]\d{4}$", bid):
                self.book_id = bid
                break
            print("Mã sách không hợp lệ.")

        # Title: Ít nhất 2 ký tự, chữ cái đầu viết hoa
        while True:
            title = input("Nhập tên sách: ").strip()
            if len(title) >= 2 and re.match(r"^[A-ZÀ-Ỹ][A-Za-zÀ-ỹ\s]*$", title):
                self.title = title
                break
            print("Tên sách không hợp lệ.")

        # Author: Viết hoa chữ cái đầu, không chứa số/ký tự đặc biệt
        while True:
            author = input("Nhập tác giả: ").strip()
            if author and author[0].isupper() and re.match(r"^[A-ZÀ-Ỹ][A-Za-zÀ-ỹ\s]*$", author):
                self.author = author
                break
            print("Tác giả không hợp lệ.")

        # Publisher: Không để trống
        while True:
            publisher = input("Nhập nhà xuất bản: ").strip()
            if publisher != "":
                self.publisher = publisher
                break
            print("Nhà xuất bản không được để trống.")

        # Status: Chỉ nhận 1 trong các giá trị cho phép
        while True:
            status = input("Nhập tình trạng (Còn/Đã mượn/Hư hỏng/Mất):").strip()
            if status in ["Còn","Đã mượn","Hư hỏng","Mất"]:
                self.status = status
                break
            print("Tình trạng không hợp lệ.")

        # Nhập người nhập sách (gộp họ tên + mã NV)

        while True:
            staff_id = input("Nhập mã nhân viên (VD: NV20251015_001): ").strip()
            if re.match(r"^NV\d{8}_\d{3}$", staff_id):
                break
            print(" Mã nhân viên không hợp lệ (phải có dạng NVYYYYMMDD_XXX).")

        # Gộp lại thành 1 chuỗi duy nhất
        self.importer = staff_id

        # Nhập số lượng
        while True:
            try:
                q = int(input("Nhập số lượng sách: "))
                if q > 0:
                    self.quantity = q
                    break
                print("Số lượng phải > 0.")
            except ValueError:
                print("Số lượng phải là số nguyên!")

    def display_info(self):
        print("\n===== THÔNG TIN SÁCH =====")    
        print(f"{'Mã sách':<8} | {'Tên sách':<25} | {'Tác giả':<20} | {'Nhà xuất bản':<20} | {'Trạng thái':<10} | {'Số lượng sách':<5} | {'Người nhập sách':<30}")
        print(f"{self.book_id:<8} | {self.title:<25} | {self.author:<20} | {self.publisher:<20} | {self.status:<10} | {self.quantity:<5} | {self.importer:<30}")

# Person
class Person(ABC):
    def __init__(self, full_name="", age=0):
        self.full_name = full_name
        self.age = age

    @abstractmethod
    def input_info(self): # Hàm ảo để nhập thông tin người
        pass

    @abstractmethod
    def display_info(self): # Hàm ảo để hiển thị thông tin người
        pass

class Reader(Person):
    def __init__(self, full_name="", age=0, reader_id="", class_name="", register_date="", borrowed_books=0,borrowed_books_list= [] ):
        super().__init__(full_name, age)
        self.reader_id = reader_id
        self.class_name = class_name
        self.register_date = register_date
        self.borrowed_books = borrowed_books
        self.borrowed_books_list = borrowed_books_list 
    def input_info(self):
        # FullName: Viết hoa chữ cái đầu mỗi từ, không chứa số/ký tự đặc biệt
        while True:
            name = input("Nhập họ tên: ").strip()
            if re.match(r"^[A-ZÀ-Ỹ][a-zà-ỹ]*(\s[A-ZÀ-Ỹ][a-zà-ỹ]*)*$", name):
                self.full_name = name
                break
            print("Họ tên không hợp lệ.")

        # Age: từ 18 đến 30 tuổi
        while True:
            try:
                age = int(input("Nhập tuổi: "))
                if 18 <= age <= 30:
                    self.age = age
                    break
                else:
                    print("Tuổi sinh viên phải từ 18–30.")
            except ValueError:
                print("Tuổi phải là số nguyên!")

        # ReaderID: R[Khóa/Năm][5 số] (VD: R24_00001)
        while True:
            rid = input("Nhập mã độc giả (VD: R24_00001): ").strip()
            if re.match(r"^R\d{2}_\d{5}$", rid):
                self.reader_id = rid
                break
            print("Mã độc giả không hợp lệ.")

        # Class: Không để trống, đúng định dạng (VD: K60S)
        while True:
            class_name = input("Nhập lớp (VD: K60S): ").strip()
            if class_name and re.match(r"^[A-Z]\d{2,3}[A-Z]\d?$", class_name):
                self.class_name = class_name
                break
            print("Lớp không hợp lệ.")

        # RegisterDate: Đúng định dạng ngày, nhỏ hơn hoặc bằng hiện tại
        while True:
            date = input("Nhập ngày đăng ký (DD/MM/YYYY): ").strip()
            try:
                reg_date = datetime.strptime(date, "%d/%m/%Y")
                if reg_date <= datetime.now():
                    self.register_date = date
                    break
                else:
                    print("Ngày đăng ký không được lớn hơn ngày hiện tại.")
            except:
                print("Ngày đăng ký sai định dạng (DD/MM/YYYY).")
        # Số sách mượn ban đầu là 0; danh sách sách mượn ban đầu là rỗng
        self.borrowed_books = 0
        self.borrowed_books_list = []
            
    def add_borrowed_book(self, book_id):
        if book_id not in self.borrowed_books_list:
            self.borrowed_books_list.append(book_id)

    def return_borrowed_book(self, book_id):
        if book_id in self.borrowed_books_list:
            self.borrowed_books_list.remove(book_id)

    def display_info(self):
        print("\n===== THÔNG TIN ĐỘC GIẢ =====")
        print(f"{'Mã độc giả':<10} | {'Họ tên':<25} | {'Tuổi':<6} | {'Lớp':<6} | {'Ngày đăng ký':<10} | {'Sách mượn':<5}")
        print(f"{self.reader_id:<10} | {self.full_name:<25} | {self.age:<6} | {self.class_name:<6} | {self.register_date:<10} | {self.borrowed_books:<5}")

class Staff(Person):
    def __init__(self, full_name="", age=0, staff_id="", position="",  start_date=""):
        super().__init__(full_name, age)
        self.staff_id = staff_id
        self.position = position
        self.start_date = start_date

    def input_info(self):
        # Họ tên
        while True:
            name = input("Nhập họ tên nhân viên: ").strip()
            if re.match(r"^[A-ZÀ-ỸĐ][a-zà-ỹđ]+(\s[A-ZÀ-ỸĐ][a-zà-ỹđ]+)*$", name):
                self.full_name = name
                break
            print("Họ tên không hợp lệ!")

        # Tuổi nhân viên: 18–65
        while True:
            try:
                age = int(input("Nhập tuổi: "))
                if 18 <= age <= 65:
                    self.age = age
                    break
                else:
                    print("Tuổi nhân viên phải từ 18–65.")
            except ValueError:
                print("Tuổi phải là số nguyên!")

        # Ngày vào làm
        while True:
            date = input("Nhập ngày vào làm (DD/MM/YYYY): ").strip()
            try:
                start_date = datetime.strptime(date, "%d/%m/%Y")
                if start_date <= datetime.now():
                    self.start_date = date
                    break
                else:
                    print("Ngày vào làm không được lớn hơn hiện tại!")
            except ValueError:
                print("Định dạng ngày không hợp lệ!")

        # Mã nhân viên: NV + YYYYMMDD + _ + STT (3 chữ số)
        while True:
            stt = input("Nhập số thứ tự (VD: 001, 002...): ").strip()
            if re.match(r"^\d{3}$", stt):
                date_str = datetime.strptime(self.start_date, "%d/%m/%Y").strftime("%Y%m%d")
                self.staff_id = f"NV{date_str}_{stt}"
                break
            print("Số thứ tự phải gồm 3 chữ số!")

        # Chức vụ
        while True:
            pos = input("Nhập chức vụ (VD: Thủ thư, Quản lý...): ").strip()
            if len(pos) >= 2:
                self.position = pos
                break
            print("Chức vụ không hợp lệ!")

    def display_info(self):
        print("\n--- THÔNG TIN NHÂN VIÊN ---")
        print(f"{'Mã NV':<15} | {'Họ tên':<25} | {'Tuổi':<6} | {'Chức vụ':<15} | {'Ngày vào làm':<10}")
        print(f"{self.staff_id:<15} | {self.full_name:<25} | {self.age:<6} | {self.position:<12} | {self.start_date:<10}")

# BorrowSlip
class BorrowSlip:
    def __init__(self, borrow_id="", book_id="", reader_id="", borrow_date="",due_date = "", return_date="", quantity=0, lender_id="", receiver_id=""):
        self.borrow_id = borrow_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.borrow_date = borrow_date          #Ngày mượn
        self.due_date = due_date                #Ngày trả dự kiến
        self.return_date = return_date          #Ngày trả thực tế
        self.quantity = quantity  
        self.lender_id = lender_id            # Người cho mượn
        self.receiver_id = receiver_id        # Người nhận trả 
    def input_info(self):
        # BorrowID: P[YYYYMMDD]_[4 số]
        while True:
            bid = input("Nhập mã phiếu mượn (VD: P20251009_0001): ").strip()
            if re.match(r"^P\d{8}_\d{4}$", bid):
                self.borrow_id = bid
                break
            print("Mã phiếu mượn không hợp lệ.")

        # BookID: 1 chữ in hoa + 4 số
        while True:
            bookid = input("Nhập mã sách mượn (VD: A0001): ").strip()
            if re.match(r"^[A-Z]\d{4}$", bookid):
                self.book_id = bookid
                break
            print("Mã sách không hợp lệ.")

        # ReaderID: R[Khóa/Năm]_[5 số]
        while True:
            rid = input("Nhập mã độc giả (VD: R24_00001): ").strip()
            if re.match(r"^R\d{2}_\d{5}$", rid):
                self.reader_id = rid
                break
            print("Mã độc giả không hợp lệ")

        # BorrowDate: Đúng định dạng ngày, nhỏ hơn hoặc bằng hôm nay
        while True:
            date = input("Nhập ngày mượn (DD/MM/YYYY): ").strip()
            try:
                borrow_date = datetime.strptime(date, "%d/%m/%Y")
                if borrow_date <= datetime.now():
                    self.borrow_date = date
                    break
                else:
                    print("Ngày mượn không được lớn hơn ngày hiện tại.")
            except:
                print("Ngày mượn sai định dạng (DD/MM/YYYY).")
        
        # DueDate: ngày trả dự kiến: 2 tháng sau ngày mượn
        if borrow_date:
            try:
                borrow_date_obj = datetime.strptime(borrow_date, "%d/%m/%Y")
                due_date_obj = borrow_date_obj + timedelta(days=60)
                self.due_date = due_date_obj.strftime("%d/%m/%Y")
            except ValueError:
                self.due_date = ""
        else:
            self.due_date = ""

        # ReturnDate: Có thể để trống, nếu nhập thì phải lớn hơn ngày mượn
        while True:
            rdate = input("Nhập ngày trả (DD/MM/YYYY, có thể bỏ trống): ").strip()
            if rdate == "":
                self.return_date = ""
                break
            try:
                return_date = datetime.strptime(rdate, "%d/%m/%Y")
                borrow_date = datetime.strptime(self.borrow_date, "%d/%m/%Y")
                if return_date > borrow_date:
                    self.return_date = rdate
                    break
                else:
                    print("Ngày trả phải lớn hơn ngày mượn.")
            except:
                print("Ngày trả sai định dạng (DD/MM/YYYY), hoặc lớn hơn ngày mượn.")
        # Số sách mượn
        while True:
            try:
                qty = int(input("Nhập số lượng sách mượn: "))
                if qty > 0:
                    self.quantity = qty
                    break
                print("Số lượng phải > 0.")
            except ValueError:
                print("Số lượng phải là số nguyên!")
        # Nhân viên cho mượn
        while True:
            lender_id = input("Nhập mã nhân viên cho mượn (VD: NV20251018_001): ").strip()
            if re.match(r"^NV\d{8}_\d{3}$", lender_id):
                self.lender_id = lender_id
                break
            print("Mã nhân viên cho mượn không hợp lệ. Định dạng: NVYYYYMMDD_001")
        # Nhân viên nhận trả (có thể bỏ trống)
        receiver_id = input("Nhập mã nhân viên nhận trả (VD: NV20251018_002, có thể bỏ trống): ").strip()
        if receiver_id and not re.match(r"^NV\d{8}_\d{3}$", receiver_id):
            print("Mã người nhận trả không hợp lệ, sẽ để trống.")
            receiver_id = ""
        self.receiver_id = receiver_id

    def display_info(self):
        print("\n===== THÔNG TIN PHIẾU MƯỢN =====")
        print(f"{'Mã phiếu':<15} | {'Mã sách':<8} | {'Mã độc giả':<10} | {'Ngày mượn':<12} | {'Ngày trả dự kiến':<12} | {'Ngày trả':<12} | {'SL':<5} | {'Cho mượn(ID)':<20} | {'Nhận trả(ID)':<20}")
        print(f"{self.borrow_id:<15} | {self.book_id:<8} | {self.reader_id:<10} | "
              f"{self.borrow_date:<12} | {self.due_date:<12} | {self.return_date if self.return_date else 'Chưa trả':<12} | "
              f"{self.quantity:<5} | {self.lender_id:<20} | {self.receiver_id if self.receiver_id else 'Chưa có':<20}")
