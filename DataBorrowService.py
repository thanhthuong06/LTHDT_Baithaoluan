import csv
from datetime import datetime, timedelta
from Lop_doi_tuong import BorrowSlip, Book, Reader, Staff

class BorrowService:
    def __init__(self, filename="borrow_data.csv"):
        self.borrow_slips = []
        self.filename = filename
        self.load_from_csv()

    # ===============================
    # NẠP DỮ LIỆU TỪ CSV
    # ===============================
    def load_from_csv(self):
        try:
            with open(self.filename, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    slip = BorrowSlip(
                        borrow_id=row["borrow_id"],
                        book_id=row["book_id"],
                        reader_id=row["reader_id"],
                        borrow_date=row["borrow_date"],
                        due_date=row["due_date"],
                        return_date=row["return_date"],
                        quantity=int(row["quantity"]),
                        lender_id=row["lender_id"],
                        receiver_id=row["receiver_id"]
                    )
                    self.borrow_slips.append(slip)
        except FileNotFoundError:
            print("Chưa có file dữ liệu phiếu mượn, sẽ tạo mới khi lưu.")

    # ===============================
    # LƯU DỮ LIỆU RA CSV
    # ===============================
    def save_to_csv(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "borrow_id","book_id","reader_id",
                "borrow_date","due_date","return_date",
                "quantity","lender_id","receiver_id"
            ])
            for s in self.borrow_slips:
                writer.writerow([
                    s.borrow_id, s.book_id, s.reader_id,
                    s.borrow_date, s.due_date, s.return_date,
                    s.quantity, s.lender_id, s.receiver_id
                ])

    # ===============================
    # HÀM MƯỢN SÁCH
    # ===============================
    def borrow_book(self, book_list, reader_list, staff_list, book_id, reader_id, lender_id, quantity=1):
        book = next((b for b in book_list if b.book_id == book_id), None)
        reader = next((r for r in reader_list if r.reader_id == reader_id), None)
        lender = next((s for s in staff_list if s.staff_id == lender_id), None)

        if not book:
            return "Mã sách không tồn tại!"
        if not reader:
            return "Mã độc giả không tồn tại!"
        if not lender:
            return "Mã nhân viên cho mượn không tồn tại!"
        if book.quantity == 0:
            return f"Sách '{book.title}' đã hết!"
        if quantity > book.quantity:
            return f"Chỉ còn {book.quantity} quyển sách '{book.title}'."

        today = datetime.now()
        due_date = today + timedelta(days=60)
        slip_id = f"P{today.strftime('%Y%m%d')}_{len(self.borrow_slips)+1:04d}"

        slip = BorrowSlip(
            borrow_id=slip_id,
            book_id=book.book_id,
            reader_id=reader.reader_id,
            borrow_date=today.strftime("%d/%m/%Y"),
            due_date=due_date.strftime("%d/%m/%Y"),
            return_date="",
            quantity=quantity,
            lender_id=lender.staff_id,
            receiver_id=""
        )

        self.borrow_slips.append(slip)

        # Cập nhật số lượng sách
        book.quantity -= quantity
        book.status = "Đã mượn" if book.quantity == 0 else "Còn"

        # Cập nhật thông tin Reader
        reader.borrowed_books += quantity
        reader.borrowed_books_list.extend([book.book_id]*quantity)

        self.save_to_csv()

        return (f"Phiếu mượn: {slip_id}\n"
                f"Độc giả {reader.full_name} đã mượn {quantity} quyển sách '{book.title}'.\n"
                f"Người cho mượn: {lender.full_name} ({lender.staff_id})\n"
                f"Hạn trả dự kiến: {due_date.strftime('%d/%m/%Y')}\n"
                f"Còn lại: {book.quantity} quyển.")

    # ===============================
    # HÀM TRẢ SÁCH
    # ===============================
    def return_book(self, book_list, reader_list, staff_list, slip_id, return_date_str, receiver_id):
        slip = next((s for s in self.borrow_slips if s.borrow_id == slip_id), None)
        if not slip:
            return "Không tìm thấy phiếu mượn."

        book = next((b for b in book_list if b.book_id == slip.book_id), None)
        if not book:
            return "Không tìm thấy thông tin sách."

        receiver = next((s for s in staff_list if s.staff_id == receiver_id), None)
        if not receiver:
            return "Mã nhân viên nhận trả không tồn tại!"

        try:
            return_date = datetime.strptime(return_date_str, "%d/%m/%Y")
            borrow_date = datetime.strptime(slip.borrow_date, "%d/%m/%Y")
            if return_date <= borrow_date:
                return "Ngày trả phải sau ngày mượn."
        except ValueError:
            return "Sai định dạng ngày (dd/mm/yyyy)."

        slip.return_date = return_date_str
        slip.receiver_id = receiver.staff_id

        # Cập nhật số lượng sách
        book.quantity += slip.quantity
        book.status = "Còn"

        # Cập nhật danh sách sách mượn của Reader
        reader = next((r for r in reader_list if r.reader_id == slip.reader_id), None)
        if reader:
            reader.borrowed_books -= slip.quantity
            for _ in range(slip.quantity):
                if slip.book_id in reader.borrowed_books_list:
                    reader.borrowed_books_list.remove(slip.book_id)

        self.save_to_csv()

        return (f"Trả sách '{book.title}' thành công.\n"
                f"Người nhận trả: {receiver.full_name} ({receiver.staff_id})\n"
                f"Hiện còn {book.quantity} quyển.")

    # ===============================
    # KIỂM TRA QUÁ HẠN
    # ===============================
    def check_overdue(self):
        overdue_list = []
        for slip in self.borrow_slips:
            if slip.return_date:  # Nếu đã có ngày trả
                actual_return = datetime.strptime(slip.return_date, "%d/%m/%Y")
                due_date = datetime.strptime(slip.due_date, "%d/%m/%Y")
                if actual_return > due_date:
                    overdue_days = (actual_return - due_date).days
                    overdue_list.append((slip, overdue_days))
        return overdue_list


    # ===============================
    # HIỂN THỊ TẤT CẢ PHIẾU MƯỢN
    # ===============================
    def show_all_slips(self):
        if not self.borrow_slips:
            print("Chưa có phiếu mượn nào.")
            return

        print("\n===== DANH SÁCH PHIẾU MƯỢN =====")
        print(f"{'Mã phiếu':<15} | {'Mã sách':<8} | {'Mã độc giả':<10} | {'SL':<3} | {'Ngày mượn':<12} | {'Hạn trả':<12} | {'Ngày trả':<12} | {'Cho mượn(ID)':<20} | {'Nhận trả(ID)':<20}")
        print("-"*140)
        for s in self.borrow_slips:
            print(f"{s.borrow_id:<15} | {s.book_id:<8} | {s.reader_id:<10} | {s.quantity:<3} | "
                  f"{s.borrow_date:<12} | {s.due_date:<12} | {s.return_date or '-':<12} | "
                  f"{s.lender_id:<20} | {s.receiver_id or '-':<20}")
