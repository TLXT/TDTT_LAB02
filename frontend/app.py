"""
LetsLockin Frontend
Streamlit application with Firebase Authentication
"""
import streamlit as st
from api_client import api_client
from datetime import datetime, date, timedelta, timezone
import time
import requests
import re  


# Page configuration
st.set_page_config(
    page_title="LetsLockin",
    page_icon="🎯",
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

    st.markdown('<h1 class="main-header">🎯 LetsLockin</h1>', unsafe_allow_html=True)
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
    
    # Tính toán chính xác Giờ Việt Nam (UTC+7)
    vn_now = datetime.now(timezone.utc) + timedelta(hours=7)
    
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
    
    st.markdown('<h1 class="main-header">🎯 LetsLockin</h1>', unsafe_allow_html=True)
    
    token = st.session_state.token
    tasks_data = api_client.get_tasks(token)
    raw_tasks = tasks_data.get('tasks', []) if tasks_data else []
    
    # --- BỘ LỌC NGÀY (ĐÃ CHỈNH LẠI CỘT CHO GỌN) ---
    # Thêm một cột trống (spacer) ở cuối để đẩy các nội dung gọn về bên trái
    col_filter_label, col_filter_mode, col_filter_date, spacer = st.columns([0.12, 0.20, 0.20, 0.48])
    with col_filter_label:
        st.markdown("<h4 style='margin-top: 5px;'>📅 Xem theo:</h4>", unsafe_allow_html=True)
    with col_filter_mode:
        view_mode = st.radio("Chế độ xem", ["Ngày cụ thể", "Tất cả"], horizontal=True, label_visibility="collapsed")
    with col_filter_date:
        if view_mode == "Ngày cụ thể":
            # Sử dụng ngày VN hiện tại làm mặc định
            selected_date = st.date_input("Chọn ngày", vn_now.date(), label_visibility="collapsed")
            selected_date_str = selected_date.strftime('%Y-%m-%d')
        else:
            selected_date_str = None

    # --- XỬ LÝ VÀ LỌC DỮ LIỆU ---
    processed_tasks = []
    for task in raw_tasks:
        raw_desc = task.get('description', '')
        created_at_raw = task.get('created_at', '')
        
        # Xử lý thời gian tạo từ UTC sang Múi giờ Việt Nam
        try:
            dt = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
            if dt.tzinfo is not None:
                dt_vn = dt.astimezone(timezone(timedelta(hours=7)))
            else:
                dt_vn = dt + timedelta(hours=7)
            created_time_str = dt_vn.strftime('%H:%M - %d/%m/%Y')
        except Exception:
            created_time_str = created_at_raw
            
        task['created_time_str'] = created_time_str
        
        # Bóc tách Ngày làm việc 
        date_match = re.search(r'\[DATE:(\d{4}-\d{2}-\d{2})\]', raw_desc)
        if date_match:
            task_date_str = date_match.group(1)
            raw_desc = raw_desc.replace(date_match.group(0), '')
        else:
            # Fallback ngày tạo theo giờ VN
            try:
                dt_fallback = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                if dt_fallback.tzinfo is not None:
                    dt_fallback = dt_fallback.astimezone(timezone(timedelta(hours=7)))
                else:
                    dt_fallback = dt_fallback + timedelta(hours=7)
                task_date_str = dt_fallback.strftime('%Y-%m-%d')
            except:
                task_date_str = vn_now.strftime('%Y-%m-%d')
                
        # Bóc tách Mã màu 
        color_match = re.search(r'\[COLOR:(#[0-9a-fA-F]{6})\]', raw_desc)
        if color_match:
            task_color = color_match.group(1)
            clean_desc = raw_desc.replace(color_match.group(0), '').strip()
        else:
            task_color = "#9E9E9E"
            clean_desc = raw_desc.strip()
            
        task['parsed_date'] = task_date_str
        task['parsed_color'] = task_color
        task['clean_desc'] = clean_desc
        
        # Áp dụng bộ lọc
        if selected_date_str and task_date_str != selected_date_str:
            continue
            
        processed_tasks.append(task)

    # --- THỐNG KÊ (Tính toán dựa trên danh sách đã lọc) ---
    total_tasks = len(processed_tasks)
    completed_tasks = sum(1 for t in processed_tasks if t['status'] == 'completed')
    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_tasks}</div>
            <div class="stat-label">Tổng số công việc</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-number">{pending_tasks}</div>
            <div class="stat-label">Đang làm</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-number">{completed_tasks}</div>
            <div class="stat-label">Hoàn thành</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ➕ Thêm công việc mới")
    
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            task_title = st.text_input("Tiêu đề", placeholder="Nhập tiêu đề công việc...")
        with col2:
            # Gợi ý mặc định là ngày VN đang xem
            default_date = selected_date if view_mode == "Ngày cụ thể" else vn_now.date()
            task_date = st.date_input("📅 Ngày thực hiện", default_date)
        with col3:
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
                full_desc = f"[DATE:{task_date.strftime('%Y-%m-%d')}][COLOR:{task_color}]{task_description}"
                
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
        title_suffix = f" ngày {selected_date.strftime('%d/%m/%Y')}" if view_mode == "Ngày cụ thể" else " (Tất cả)"
        st.markdown(f"### 📋 Danh sách công việc{title_suffix}")
    with col_btn:
        if st.button("🔄 Làm mới", use_container_width=True):
            st.rerun()
    
    if not processed_tasks:
        st.info("📭 Không có công việc nào trong danh sách này!")
    else:
        for task in processed_tasks:
            task_id = task['id']
            title = task['title']
            description = task['clean_desc']
            task_color = task['parsed_color']
            task_date_str = task['parsed_date']
            status = task['status']
            created_time_str = task['created_time_str']
            
            # Format lại ngày để hiển thị
            try:
                dt = datetime.strptime(task_date_str, '%Y-%m-%d')
                display_date = dt.strftime('%d/%m/%Y')
            except:
                display_date = task_date_str
            
            is_completed = status == 'completed'
            
            if is_completed:
                bg_color = "#34a85315" 
                border_color = "#34a853"
            else:
                bg_color = f"{task_color}15"
                border_color = task_color
                
            card_class = f"task-marker-{task_id}"
            
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            
            with col1:
                st.markdown(f"""
                <style>
                    div[data-testid="stHorizontalBlock"]:has(.{card_class}) {{
                        background-color: {bg_color};
                        border-left: 6px solid {border_color};
                        padding: 15px 20px;
                        border-radius: 8px;
                        margin-bottom: 12px;
                        align-items: center; 
                        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                        transition: all 0.3s ease;
                    }}
                </style>
                <div class="{card_class}"></div>
                """, unsafe_allow_html=True)
                
                title_style = "text-decoration: line-through; color: #888;" if is_completed else "font-weight: bold; font-size: 1.15em;"
                st.markdown(f'<div style="{title_style}">{title}</div>', unsafe_allow_html=True)
                if description:
                    st.markdown(f'<div style="color: #999; font-size: 0.9em; margin-top: 5px;">{description}</div>', unsafe_allow_html=True)
                
                # Hiển thị song song Ngày hẹn và Giờ tạo
                st.markdown(f'''
                    <div style="color: #666; font-size: 0.85em; margin-top: 10px; display: flex; gap: 20px;">
                        <span style="font-weight: 500;">⏳ Lịch hẹn: {display_date}</span>
                        <span>🕒 Tạo lúc: {created_time_str}</span>
                    </div>
                ''', unsafe_allow_html=True)
            
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