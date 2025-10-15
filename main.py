from DataBook import DataBook
from DataReader import DataReader
from DataBorrowService import BorrowService

def main():
    data_book = DataBook()
    data_reader = DataReader()
    borrow_service = BorrowService()

    while True:
        print("\n========== MENU CHÍNH ==========")
        print("1. Quản lý sách")
        print("2. Quản lý độc giả")
        print("3. Quản lý mượn / trả sách")
        print("0. Thoát chương trình")
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == "1":
            menu_book(data_book)
        elif choice == "2":
            menu_reader(data_reader)
        elif choice == "3":
            menu_borrow(data_book, data_reader, borrow_service)
        elif choice == "0":
            print("📁 Dữ liệu đã được lưu lại. Tạm biệt!")
            data_book.save_to_csv()
            data_reader.save_to_file()
            break
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng nhập lại!")

# --- MENU QUẢN LÝ SÁCH ---
def menu_book(data):
    while True:
        print("\n===== MENU QUẢN LÝ SÁCH =====")
        print("1. Thêm sách mới")
        print("2. Sửa thông tin sách")
        print("3. Xóa sách")
        print("4. Tìm kiếm sách")
        print("5. Hiển thị toàn bộ sách")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == "1": data.add_book()
        elif choice == "2": data.update_book()
        elif choice == "3": data.delete_book()
        elif choice == "4": data.search_book()
        elif choice == "5": data.display_all()
        elif choice == "0": break
        else: print("❌ Lựa chọn không hợp lệ!")

# --- MENU QUẢN LÝ ĐỘC GIẢ ---
def menu_reader(data):
    while True:
        print("\n===== MENU QUẢN LÝ ĐỘC GIẢ =====")
        print("1. Thêm độc giả mới")
        print("2. Sửa thông tin độc giả")
        print("3. Xóa độc giả")
        print("4. Tìm kiếm độc giả")
        print("5. Hiển thị toàn bộ độc giả")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == "1": data.add_reader()
        elif choice == "2": rid = input("Nhập mã độc giả cần sửa: "); data.update_reader(rid)
        elif choice == "3": rid = input("Nhập mã độc giả cần xóa: "); data.delete_reader(rid)
        elif choice == "4": kw = input("Nhập từ khóa: "); data.search_reader(kw)
        elif choice == "5": data.display_all()
        elif choice == "0": break
        else: print("❌ Lựa chọn không hợp lệ!")

# --- MENU QUẢN LÝ MƯỢN/TRẢ ---
def menu_borrow(book_data, reader_data, borrow_service):
    while True:
        print("\n===== MENU MƯỢN / TRẢ SÁCH =====")
        print("1. Mượn sách")
        print("2. Trả sách")
        print("3. Kiểm tra sách quá hạn")
        print("4. Hiển thị danh sách phiếu mượn")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == "1":
            book_id = input("Nhập mã sách: ").strip()
            reader_id = input("Nhập mã độc giả: ").strip()
            print(borrow_service.borrow_book(book_data.books, reader_data.readers, book_id, reader_id))
        elif choice == "2":
            slip_id = input("Nhập mã phiếu mượn: ").strip()
            return_date = input("Nhập ngày trả (DD/MM/YYYY): ").strip()
            print(borrow_service.return_book(book_data.books, slip_id, return_date))
        elif choice == "3":
            overdue = borrow_service.check_overdue()
            if not overdue:
                print("✅ Không có phiếu mượn quá hạn.")
            else:
                print("⚠️ Danh sách phiếu mượn quá hạn:")
                for s in overdue:
                    s.display_info()
        elif choice == "4":
            borrow_service.show_all_slips()
        elif choice == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    main()
