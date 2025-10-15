from datetime import datetime,timedelta
from Lop import BorrowSlip  

class BorrowService:
    def __init__(self):
        # Danh sách các phiếu mượn đang quản lý
        self.borrow_slips = []

    # -----------------------------
    # HÀM MƯỢN SÁCH
    # -----------------------------
    def borrow_book(self, book_list, reader_list, book_id, reader_id):
        """
        Xử lý nghiệp vụ mượn sách:
        - Kiểm tra mã sách và độc giả có tồn tại không.
        - Kiểm tra tình trạng sách có 'Còn' hay không.
        - Tạo phiếu mượn và cập nhật tình trạng sách.
        """
        # Tìm sách và độc giả tương ứng
        book = next((b for b in book_list if b.book_id == book_id), None)
        reader = next((r for r in reader_list if r.reader_id == reader_id), None)

        if not book:
            return " Mã sách không tồn tại!"
        if not reader:
            return " Mã độc giả không tồn tại!"
        if book.status != "Còn":
            return f" Sách '{book.title}' hiện đang {book.status}!"

        # Tạo phiếu mượn (BorrowSlip)
        today = datetime.now().strftime("%d/%m/%Y")
        # Ngày trả dự kiến là sau 7 ngày
        return_date = (datetime.now().replace() + 
                       timedelta(days=7)).strftime("%d/%m/%Y")
        slip_id = f"P{datetime.now().strftime('%Y%m%d')}_{len(self.borrow_slips)+1:04d}"

        slip = BorrowSlip(slip_id, book.book_id, reader.reader_id, today, return_date)
        self.borrow_slips.append(slip)

        # Cập nhật tình trạng sách
        book.status = "Đã mượn"

        return f" Độc giả {reader.full_name} đã mượn sách '{book.title}' (Mã phiếu: {slip_id}) thành công."

    # -----------------------------
    # HÀM TRẢ SÁCH
    # -----------------------------
    def return_book(self, book_list, slip_id, return_date_str):
        slip = next((s for s in self.borrow_slips if s.borrow_id == slip_id), None)
        if not slip:
            return " Không tìm thấy phiếu mượn."

        book = next((b for b in book_list if b.book_id == slip.book_id), None)
        if not book:
            return " Không tìm thấy thông tin sách."

        try:
            return_date = datetime.strptime(return_date_str, "%d/%m/%Y")
            borrow_date = datetime.strptime(slip.borrow_date, "%d/%m/%Y")
            if return_date <= borrow_date:
                return " Ngày trả phải lớn hơn ngày mượn."
        except:
            return " Ngày trả sai định dạng (DD/MM/YYYY)."

        slip.return_date = return_date_str
        book.status = "Còn"

        return f" Sách '{book.title}' đã được trả thành công."


    # -----------------------------
    # HÀM KIỂM TRA QUÁ HẠN
    # -----------------------------
    def check_overdue(self):
        """
        Kiểm tra các phiếu mượn quá hạn trong hệ thống.
        """
        today = datetime.now()
        overdue_list = []
        for slip in self.borrow_slips:
            if slip.return_date == "":  # chưa trả
                try:
                    borrow_date = datetime.strptime(slip.borrow_date, "%d/%m/%Y")
                    due_date = borrow_date + timedelta(days=7)
                    if today > due_date:
                        overdue_list.append(slip)
                except:
                    pass
        return overdue_list


    # -----------------------------
    # 4️⃣ HÀM HIỂN THỊ DANH SÁCH PHIẾU
    # -----------------------------
    def show_all_slips(self):
        """
        Hiển thị toàn bộ danh sách phiếu mượn hiện có.
        """
        if not self.borrow_slips:
            print("📭 Chưa có phiếu mượn nào.")
            return
        print("\n===== DANH SÁCH PHIẾU MƯỢN =====")
        for slip in self.borrow_slips:
            slip.display_info()