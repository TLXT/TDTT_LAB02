# Bài Thực Hành Số 2: APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

**Môn học:** Tư Duy Tính Toán  
**Sinh viên thực hiện:** Trần Lê Xuân Tân  
**MSSV:** 24120136  
**Lớp:** 24CTT6  
**Khoa:** Công nghệ thông tin - Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM  

---

## 1. Giới thiệu ứng dụng
Dự án là một ứng dụng To-Do App (Quản lý công việc) nhỏ gọn, được thiết kế theo kiến trúc tách biệt hoàn toàn giữa Frontend và Backend. 

Ứng dụng đáp ứng đầy đủ các tiêu chí của bài thực hành:
- **Frontend:** Xây dựng bằng Streamlit, chịu trách nhiệm hiển thị giao diện và gửi request.
- **Backend:** Xây dựng bằng FastAPI, xử lý logic và thao tác với cơ sở dữ liệu.
- **Database & Authentication:** Tích hợp Firebase Authentication (Hỗ trợ đăng nhập Email/Password & Google Login) và lưu trữ dữ liệu Realtime với Firestore.
- **Tính năng chính:** Thêm công việc (chọn màu ưu tiên), hiển thị danh sách công việc, đánh dấu hoàn thành, xóa công việc và hiển thị thống kê.

---

## 2. Hướng dẫn cài đặt environment

Đảm bảo máy tính của bạn đã cài đặt sẵn Python (khuyến nghị phiên bản 3.10 trở lên).

**Bước 1: Clone repository về máy**
```bash
git clone <đường-dẫn-repository-của-bạn>
cd <tên-thư-mục-repository>
```

**Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)**
- Đối với Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- Đối với macOS/Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  
```

**Bước 3: Cài đặt các thư viện phụ thuộc**
```bash
pip install -r requirements.txt
```

**Bước 4: Cấu hình thông tin Firebase**
- Tạo file `secrets.toml` (hoặc `secrets_2.toml` tùy cấu hình) chứa thông tin cấp phép của Firebase (API Key, Service Account).
- *Lưu ý: File này đã được thêm vào `.gitignore` để bảo mật thông tin.*

---

## 3. Hướng dẫn chạy backend

Backend cần được chạy trước để sẵn sàng nhận request từ frontend. Đảm bảo bạn đang ở môi trường ảo `venv`.

**Bước 1:** Di chuyển vào thư mục backend
```bash
cd backend
```

**Bước 2:** Khởi chạy server Uvicorn
```bash
uvicorn app.main:app --reload
```
*Server Backend sẽ hoạt động tại: `http://127.0.0.1:8000`*

---

## 4. Hướng dẫn chạy frontend

Mở một cửa sổ Terminal/Command Prompt mới, kích hoạt lại môi trường ảo `venv` như ở phần cài đặt.

**Bước 1:** Đứng tại thư mục gốc của dự án (hoặc di chuyển vào thư mục chứa file app của frontend).

**Bước 2:** Khởi chạy giao diện Streamlit
```bash
streamlit run frontend/app.py 
```
*(Lưu ý: Điều chỉnh đường dẫn `frontend/app.py` cho khớp với cấu trúc thư mục thực tế).*

*Giao diện Frontend sẽ tự động mở trên trình duyệt tại: `http://localhost:8501`*

---

## 5. Video Demo

Video dưới đây trình bày chi tiết về:
- Giới thiệu ứng dụng.
- Thao tác khởi chạy backend và frontend.
- Đăng nhập bằng Firebase Authentication.
- Demo tính năng chính (CRUD tasks).
- Minh họa dữ liệu thay đổi thực tế trên Firebase Firestore.

👉 **[Bấm vào đây để xem Video Demo](#)** 
*(Lưu ý: Thay thế dấu # bằng đường dẫn URL tới video trên YouTube/Google Drive của bạn)*