from DataBook import DataBook
from DataPerson import DataReader, DataStaff
from DataBorrowService import BorrowService
from Lop_doi_tuong import Staff, Reader


def main():
    data_book = DataBook()
    data_reader = DataReader()
    data_staff = DataStaff()
    borrow_service = BorrowService()

    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ THƯ VIỆN =====")
        print("1. Quản lý nhân viên")
        print("2. Quản lý độc giả")
        print("3. Quản lý sách")
        print("4. Quản lý phiếu mượn / trả")
        print("0. Thoát chương trình")
        choice = input("Chọn: ").strip()

        if choice == "1":
            menu_staffs(data_staff)
        elif choice == "2":
            menu_readers(data_reader)
        elif choice == "3":
            menu_book(data_book)
        elif choice == "4":
            menu_borrow(data_book, data_reader, data_staff, borrow_service)
        elif choice == "0":
            data_book.save_to_csv()
            data_reader.save_to_file()
            data_staff.save_to_file()
            borrow_service.save_to_csv()
            print("Dữ liệu đã được lưu. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ!")


# ========================= MENU NHÂN VIÊN =========================
def menu_staffs(data_staff):
    while True:
        print("\n===== QUẢN LÝ NHÂN VIÊN =====")
        print("1. Thêm nhân viên mới")
        print("2. Sửa thông tin nhân viên")
        print("3. Xóa nhân viên")
        print("4. Tìm kiếm nhân viên")
        print("5. Hiển thị toàn bộ nhân viên")
        print("0. Quay lại")
        choice = input("Chọn: ").strip()

        if choice == "1":
            staff = Staff()
            staff.input_info()
            data_staff.add_item(staff)
        elif choice == "2":
            sid = input("Nhập mã nhân viên cần sửa: ").strip()
            data_staff.update_item(sid)
        elif choice == "3":
            sid = input("Nhập mã nhân viên cần xóa: ").strip()
            data_staff.delete_item(sid)
        elif choice == "4":
            kw = input("Nhập từ khóa tìm kiếm: ").strip()
            results = data_staff.search_item(kw)
            if results:
                print(f"\n{'Mã NV':<15} | {'Họ tên':<25} | {'Tuổi':<5} | {'Chức vụ':<20} | {'Ngày bắt đầu':<15}")
                print("-" * 85)
                for s in results:
                    print(f"{s.staff_id:<15} | {s.full_name:<25} | {s.age:<5} | {s.position:<20} | {s.start_date:<15}")
            else:
                print("Không tìm thấy kết quả nào.")
        elif choice == "5":
            data_staff.display_all()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")


# ========================= MENU ĐỘC GIẢ =========================
def menu_readers(data_reader):
    while True:
        print("\n===== QUẢN LÝ ĐỘC GIẢ =====")
        print("1. Thêm độc giả mới")
        print("2. Sửa thông tin độc giả")
        print("3. Xóa độc giả")
        print("4. Tìm kiếm độc giả")
        print("5. Hiển thị toàn bộ độc giả")
        print("0. Quay lại")
        choice = input("Chọn: ").strip()

        if choice == "1":
            reader = Reader()
            reader.input_info()
            data_reader.add_item(reader)
        elif choice == "2":
            rid = input("Nhập mã độc giả cần sửa: ").strip()
            data_reader.update_item(rid)
        elif choice == "3":
            rid = input("Nhập mã độc giả cần xóa: ").strip()
            data_reader.delete_item(rid)
        elif choice == "4":
            kw = input("Nhập từ khóa tìm kiếm: ").strip()
            results = data_reader.search_item(kw)
            if results:
                print(f"\n{'Mã độc giả':<12} | {'Họ tên':<25} | {'Tuổi':<5} | {'Lớp':<10} | {'Ngày ĐK':<12} | {'SL sách':<8} | {'Sách mượn':<30}")
                print("-" * 120)
                for r in results:
                    borrowed_list = ','.join(r.borrowed_books_list) if r.borrowed_books_list else "Không có"
                    print(f"{r.reader_id:<12} | {r.full_name:<25} | {r.age:<5} | {r.class_name:<10} | {r.register_date:<12} | {r.borrowed_books:<8} | {borrowed_list:<30}")
            else:
                print("Không tìm thấy kết quả nào.")
        elif choice == "5":
            data_reader.display_all()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")


# ========================= MENU SÁCH =========================
def menu_book(data):
    while True:
        print("\n===== QUẢN LÝ SÁCH =====")
        print("1. Thêm sách mới")
        print("2. Sửa thông tin sách")
        print("3. Xóa sách")
        print("4. Tìm kiếm sách")
        print("5. Hiển thị toàn bộ sách")
        print("0. Quay lại")
        choice = input("Chọn: ").strip()

        if choice == "1":
            data.add_book()
        elif choice == "2":
            data.update_book()
        elif choice == "3":
            data.delete_book()
        elif choice == "4":
            data.search_book()
        elif choice == "5":
            data.display_all()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")


# ========================= MENU MƯỢN / TRẢ =========================
def menu_borrow(book_data, reader_data, staff_data, borrow_service):
    while True:
        print("\n===== MƯỢN / TRẢ SÁCH =====")
        print("1. Mượn sách")
        print("2. Trả sách")
        print("3. Kiểm tra quá hạn")
        print("4. Hiển thị tất cả phiếu mượn")
        print("0. Quay lại")
        choice = input("Chọn: ").strip()

        if choice == "1":
            book_id = input("Nhập mã sách: ").strip()
            reader_id = input("Nhập mã độc giả: ").strip()
            lender_id = input("Nhập mã nhân viên cho mượn: ").strip()
            try:
                quantity = int(input("Nhập số lượng sách mượn: ").strip())
            except ValueError:
                print("Số lượng không hợp lệ!")
                continue

            msg = borrow_service.borrow_book(
                book_list=book_data.books,
                reader_list=reader_data.items,
                staff_list=staff_data.items,
                book_id=book_id,
                reader_id=reader_id,
                lender_id=lender_id,
                quantity=quantity
            )

            print(msg)
            borrow_service.save_to_csv()
            reader_data.save_to_file()
            book_data.save_to_csv()

        elif choice == "2":
            slip_id = input("Nhập mã phiếu mượn: ").strip()
            return_date = input("Nhập ngày trả (DD/MM/YYYY): ").strip()
            receiver_id = input("Nhập mã nhân viên nhận trả: ").strip()

            msg = borrow_service.return_book(
                book_data.books,
                reader_data.items,
                staff_data.items,  # <-- truyền staff objects
                slip_id,
                return_date,
                receiver_id
            )

            print(msg)
            borrow_service.save_to_csv()
            reader_data.save_to_file()
            book_data.save_to_csv()

        elif choice == "3":
            overdue = borrow_service.check_overdue()
            if not overdue:
                print("Không có phiếu mượn quá hạn.")
            else:
                print(f"\n{'Mã phiếu':<15} | {'Mã sách':<10} | {'Mã độc giả':<10} | {'Hạn trả':<12} | {'Quá hạn (ngày)':<15}")
                print("-" * 70)
                for slip, days in overdue:
                    print(f"{slip.borrow_id:<15} | {slip.book_id:<10} | {slip.reader_id:<10} | {slip.due_date:<12} | {days:<15}")

        elif choice == "4":
            borrow_service.show_all_slips()
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
