"""
To-Do App Frontend
Streamlit application with Firebase Authentication
"""
import streamlit as st
from api_client import api_client
from datetime import datetime
import time
import requests
import re  


# Page configuration
st.set_page_config(
    page_title="To-Do App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #4285f4;
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 3em;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1em;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []


def sign_in_with_email_and_password(email, password):
    """Đăng nhập bằng Firebase REST API"""
    api_key = st.secrets["firebase_client"]["apiKey"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    response.raise_for_status() 
    return response.json() 

def create_user_with_email_and_password(email, password):
    """Đăng ký bằng Firebase REST API"""
    api_key = st.secrets["firebase_client"]["apiKey"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


# Login page
def login_page():
    """Display login page"""
    
    if "token" in st.query_params:
        token = st.query_params["token"]
        user_info = api_client.verify_token(token)
        
        if user_info:
            st.session_state.token = token
            st.session_state.user = user_info
            
            st.query_params.clear()
            st.success("Đăng nhập Google thành công! 🎉")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Phiên đăng nhập Google không hợp lệ hoặc đã hết hạn.")
            st.query_params.clear()

    st.markdown('<h1 class="main-header">📝 To-Do App</h1>', unsafe_allow_html=True)
    st.markdown("### Đăng nhập để bắt đầu quản lý công việc")
    
    tab1, tab2 = st.tabs(["Email/Password", "Đăng ký"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Mật khẩu")
            submit = st.form_submit_button("Đăng nhập", use_container_width=True)
            
            if submit:
                if email and password:
                    try:
                        user = sign_in_with_email_and_password(email, password)
                        st.session_state.user = user
                        st.session_state.token = user['idToken']
                        st.success("Đăng nhập thành công! 🎉")
                        time.sleep(1)
                        st.rerun()
                    except requests.exceptions.HTTPError as e:
                        error_data = e.response.json()
                        error_message = error_data.get("error", {}).get("message", "")
                        if "INVALID_LOGIN_CREDENTIALS" in error_message or "INVALID_EMAIL" in error_message:
                            st.error("Email hoặc mật khẩu không đúng")
                        else:
                            st.error(f"Lỗi đăng nhập: {error_message}")
                else:
                    st.warning("Vui lòng nhập đầy đủ email và mật khẩu.")
    
    with tab2:
        with st.form("register_form"):
            reg_email = st.text_input("Email", placeholder="your.email@example.com", key="reg_email")
            reg_password = st.text_input("Password", type="password", placeholder="Mật khẩu (ít nhất 6 ký tự)", key="reg_password")
            reg_password_confirm = st.text_input("Xác nhận Password", type="password", placeholder="Nhập lại mật khẩu", key="reg_password_confirm")
            register = st.form_submit_button("Đăng ký", use_container_width=True)
            
            if register:
                if reg_email and reg_password:
                    if reg_password != reg_password_confirm:
                        st.error("Mật khẩu xác nhận không khớp")
                    elif len(reg_password) < 6:
                        st.error("Mật khẩu phải có ít nhất 6 ký tự")
                    else:
                        try:
                            user = create_user_with_email_and_password(reg_email, reg_password)
                            st.success("Đăng ký thành công! Vui lòng đăng nhập ở tab bên cạnh.")
                        except requests.exceptions.HTTPError as e:
                            error_data = e.response.json()
                            error_message = error_data.get("error", {}).get("message", "")
                            if "EMAIL_EXISTS" in error_message:
                                st.error("Email đã được sử dụng")
                            else:
                                st.error(f"Lỗi đăng ký: {error_message}")
                else:
                    st.warning("Vui lòng nhập đầy đủ thông tin.")

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #5f6368; margin-bottom: 15px;'>Hoặc</div>", unsafe_allow_html=True)
    
    google_login_url = st.secrets.get("google-login", {}).get("google-url", "http://localhost:8000/auth/google/start")
    
    st.markdown(f'''
        <a href="{google_login_url}" target="_self" style="text-decoration: none;">
            <div style="background-color: #ffffff; color: #757575; border: 1px solid #dadce0; padding: 10px; border-radius: 4px; text-align: center; font-weight: 500; font-family: 'Google Sans', Roboto, Arial, sans-serif; box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3); cursor: pointer; transition: background-color 0.2s;">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 12px;">
                Đăng nhập bằng Google
            </div>
        </a>
    ''', unsafe_allow_html=True)


# Main app page
def main_app():
    """Display main application"""
    
    with st.sidebar:
        st.markdown("### 👤 Thông tin người dùng")
        user_email = st.session_state.user.get('email') or st.session_state.user.get('users', [{}])[0].get('email', 'Unknown')
        st.info(f"**Email:** {user_email}")
        
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.session_state.token = None
            st.session_state.tasks = []
            st.rerun()
        
        st.markdown("---")
        health = api_client.health_check()
        if health.get("status") == "healthy":
            st.success("✅ Backend: Hoạt động")
        else:
            st.error("❌ Backend: Lỗi kết nối")
    
    st.markdown('<h1 class="main-header">📝 To-Do App</h1>', unsafe_allow_html=True)
    
    token = st.session_state.token
    tasks_data = api_client.get_tasks(token)
    
    if tasks_data:
        tasks = tasks_data.get('tasks', [])
        st.session_state.tasks = tasks
    else:
        tasks = []
    
    stats = api_client.get_statistics(token)
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats.get('total', 0)}</div>
                <div class="stat-label">Tổng số công việc</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="stat-number">{stats.get('pending', 0)}</div>
                <div class="stat-label">Đang làm</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="stat-number">{stats.get('completed', 0)}</div>
                <div class="stat-label">Hoàn thành</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ➕ Thêm công việc mới")
    
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            task_title = st.text_input("Tiêu đề", placeholder="Nhập tiêu đề công việc...")
        with col2:
            # Danh sách 8 màu ưu tiên không chứa màu xanh lá
            PRIORITY_COLORS = {
                "🔴 Đỏ (Gấp)": "#FF5252",
                "🟠 Cam (Quan trọng)": "#FF9800",
                "🟡 Vàng (Lưu ý)": "#FFC107",
                "🔵 Xanh dương (Bình thường)": "#4facfe",
                "🩵 Xanh lơ (Thoải mái)": "#00BCD4",
                "🟣 Tím (Ý tưởng)": "#9C27B0",
                "💖 Hồng (Cá nhân)": "#E91E63",
                "⚪ Xám (Ưu tiên thấp)": "#9E9E9E"
            }
            selected_color_name = st.selectbox("🎨 Màu ưu tiên", list(PRIORITY_COLORS.keys()), index=3)
            task_color = PRIORITY_COLORS[selected_color_name]
        
        task_description = st.text_area("Mô tả (tùy chọn)", placeholder="Nhập mô tả chi tiết...")
        submit_task = st.form_submit_button("➕ Thêm công việc", use_container_width=True)
        
        if submit_task:
            if task_title:
                # Gắn mã màu ẩn vào phần đầu của description để lưu trữ
                full_desc = f"[COLOR:{task_color}]{task_description}"
                
                result = api_client.create_task(
                    token,
                    title=task_title,
                    description=full_desc
                )
                if result:
                    st.success("✅ Đã thêm công việc!")
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.warning("Vui lòng nhập tiêu đề công việc")
    
    st.markdown("---")
    
    col_title, col_btn = st.columns([0.85, 0.15])
    with col_title:
        st.markdown("### 📋 Danh sách công việc")
    with col_btn:
        if st.button("🔄 Làm mới", use_container_width=True):
            st.rerun()
    
    if not tasks:
        st.info("📭 Chưa có công việc nào. Hãy thêm công việc đầu tiên!")
    else:
        for task in tasks:
            task_id = task['id']
            title = task['title']
            raw_desc = task.get('description', '')
            status = task['status']
            created_at = task['created_at']
            
            # Tách lấy mã màu từ description
            color_match = re.search(r'\[COLOR:(#[0-9a-fA-F]{6})\]', raw_desc)
            if color_match:
                task_color = color_match.group(1)
                description = raw_desc.replace(color_match.group(0), '').strip()
            else:
                task_color = "#9E9E9E" # Màu xám mặc định
                description = raw_desc
            
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                date_str = dt.strftime('%d/%m/%Y %H:%M')
            except:
                date_str = created_at
            
            is_completed = status == 'completed'
            
            # Gán màu sắc (màu xanh lá nếu xong, màu đã chọn nếu đang làm)
            if is_completed:
                bg_color = "#34a85315" # Xanh lá kèm độ mờ
                border_color = "#34a853"
            else:
                bg_color = f"{task_color}15" # Mã màu kèm độ mờ
                border_color = task_color
                
            card_class = f"task-marker-{task_id}"
            
            # Khởi tạo cột luôn, KHÔNG DÙNG st.container() NỮA ĐỂ CHỐNG TRÀN MÀU
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            
            with col1:
                # Nhúng CSS trực tiếp vào HÀNG NGANG (stHorizontalBlock)
                st.markdown(f"""
                <style>
                    div[data-testid="stHorizontalBlock"]:has(.{card_class}) {{
                        background-color: {bg_color};
                        border-left: 6px solid {border_color};
                        padding: 15px 20px;
                        border-radius: 8px;
                        margin-bottom: 12px;
                        align-items: center; /* Căn giữa theo chiều dọc */
                        box-shadow: 0 2px 5px rgba(0,0,0,0.05); /* Đổ bóng nhẹ cho nổi bật */
                        transition: all 0.3s ease;
                    }}
                </style>
                <div class="{card_class}"></div>
                """, unsafe_allow_html=True)
                
                title_style = "text-decoration: line-through; color: #888;" if is_completed else "font-weight: bold; font-size: 1.15em;"
                st.markdown(f'<div style="{title_style}">{title}</div>', unsafe_allow_html=True)
                if description:
                    st.markdown(f'<div style="color: #999; font-size: 0.9em; margin-top: 5px;">{description}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color: #666; font-size: 0.8em; margin-top: 10px;">📅 {date_str}</div>', unsafe_allow_html=True)
            
            with col2:
                checked = st.checkbox(
                    "✅ Xong",
                    value=is_completed,
                    key=f"check_{task_id}"
                )
                if checked != is_completed:
                    new_status = "completed" if checked else "pending"
                    api_client.update_task(token, task_id, {"status": new_status})
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Xóa", key=f"delete_{task_id}", use_container_width=True):
                    if api_client.delete_task(token, task_id):
                        st.success("Đã xóa!")
                        time.sleep(0.5)
                        st.rerun()

# Main execution
def main():
    """Main application entry point"""
    init_session_state()
    
    if st.session_state.user is None:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()