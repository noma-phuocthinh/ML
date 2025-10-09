from datetime import datetime

def auto_update_date(canvas, text, delay=60000):
    """
    Cập nhật ngày hiện tại lên Canvas sau mỗi 1 phút
    :param canvas: Canvas chứa text
    :param text: text_item trên canvas
    :param delay: thời gian cập nhật, 60000=1 phút
    """
    # Lấy ngày hiện tại và định dạng
    current_date = datetime.now().strftime("%A, %B %d")
    # Cập nhật văn bản trên canvas
    canvas.itemconfig(text, text=current_date)
    # Lên lịch cập nhật mỗi 1 phút (60000ms)
    canvas.after(delay, auto_update_date, canvas, text, delay)

