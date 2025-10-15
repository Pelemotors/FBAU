from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime, timedelta
import threading
import time
from simple_facebook_bot import SimpleFacebookBot
from werkzeug.utils import secure_filename
import subprocess
import sys
import shutil

app = Flask(__name__)

# משתנה גלובלי לאחסון bot instance
login_bot = None

# הגדרות לפריסה ב-Vercel
if os.environ.get('VERCEL'):
    # ב-Vercel, נתיבי הקבצים שונים
    BASE_DIR = '/tmp'
else:
    # במחשב מקומי
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# נתיבים לקבצים
COOKIES_FILE = os.path.join(BASE_DIR, "sessions/facebook-cookie.json")
GROUPS_FILE = os.path.join(BASE_DIR, "data/groups.json")
POSTS_FILE = os.path.join(BASE_DIR, "data/posts.json")
MEDIA_FILE = os.path.join(BASE_DIR, "data/media.json")
SCHEDULE_FILE = os.path.join(BASE_DIR, "data/schedule.json")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

# צור תיקיות אם לא קיימות
os.makedirs(os.path.join(BASE_DIR, "sessions"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# הגדרות העלאת קבצים
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webm'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB מקסימום

def load_data(filename, default=[]):
    """טען נתונים מקובץ JSON"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except:
        return default

def save_data(filename, data):
    """שמור נתונים לקובץ JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def is_my_group(group_url):
    """בדוק אם הקבוצה שייכת למשתמש"""
    # טען קבוצות מהקובץ
    groups = load_data(GROUPS_FILE)
    
    for group in groups:
        if group.get('url') == group_url:
            return group.get('is_my_group', False)
    
    return False

def run_selector_explorer(group_url, group_name, post_text="", media_files=None):
    """הפעל את selector_explorer.py לקבוצות לא שלי"""
    try:
        print(f"🔍 מפעיל selector_explorer עבור {group_name}")
        
        # הפעל את הסקריפט
        cmd = [
            sys.executable, 
            "selector_explorer.py", 
            "--single-group", 
            group_url
        ]
        
        # הוסף טקסט אם יש
        if post_text:
            cmd.extend(["--text", post_text])
        
        # הוסף מדיה אם יש
        if media_files:
            for media_file in media_files:
                cmd.extend(["--media", media_file['path']])
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ selector_explorer הושלם בהצלחה עבור {group_name}")
            return True
        else:
            print(f"❌ שגיאה ב-selector_explorer עבור {group_name}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ שגיאה בהפעלת selector_explorer: {e}")
        return False

def run_simple_facebook_bot(group_url, post_text, media_files):
    """הפעל את simple_facebook_bot.py לקבוצות שלי"""
    try:
        print(f"🚀 מפעיל simple_facebook_bot עבור {group_url}")
        
        # הפעל את הבוט
        result = subprocess.run([
            sys.executable, 
            "simple_facebook_bot.py", 
            "--group", group_url,
            "--text", post_text,
            "--media", ",".join(media_files)
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ simple_facebook_bot הושלם בהצלחה")
            return True
        else:
            print(f"❌ שגיאה ב-simple_facebook_bot: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ שגיאה בהפעלת simple_facebook_bot: {e}")
        return False

def allowed_file(filename):
    """בדוק אם הקובץ מותר להעלאה"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """עמוד ראשי"""
    # בדוק אם יש cookies שמורים
    has_cookies = os.path.exists(COOKIES_FILE)
    
    # טען נתונים
    groups = load_data(GROUPS_FILE)
    posts = load_data(POSTS_FILE)
    
    # טען רק 5 קבוצות המדיה האחרונות
    media = load_data(MEDIA_FILE)
    media = sorted(media, key=lambda x: x.get('created', ''), reverse=True)[:5]
    
    # טען רק 15 הפעולות האחרונות להיסטוריה
    schedule = load_data(SCHEDULE_FILE)
    schedule = sorted(schedule, key=lambda x: x.get('created', ''), reverse=True)[:15]
    
    return render_template('index.html', 
                         has_cookies=has_cookies,
                         groups=groups,
                         posts=posts,
                         media=media,
                         schedule=schedule)

@app.route('/get_media_groups')
def get_media_groups():
    """קבל קבוצות מדיה עם פאגינציה"""
    try:
        # קבל פרמטרים
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        
        # טען נתונים
        media = load_data(MEDIA_FILE)
        
        # מיון לפי תאריך יצירה (החדשים ראשון)
        media = sorted(media, key=lambda x: x.get('created', ''), reverse=True)
        
        # חישוב פאגינציה
        total_items = len(media)
        total_pages = (total_items + per_page - 1) // per_page
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        # חתוך את הנתונים לעמוד הנוכחי
        page_data = media[start_index:end_index]
        
        return jsonify({
            'success': True,
            'data': page_data,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'per_page': per_page,
                'total_items': total_items,
                'has_prev': page > 1,
                'has_next': page < total_pages
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'שגיאה: {str(e)}'})

@app.route('/get_schedule_history')
def get_schedule_history():
    """קבל היסטוריית פרסומים עם פאגינציה ומיון"""
    try:
        # קבל פרמטרים
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 15))
        sort_by = request.args.get('sort_by', 'created')
        sort_order = request.args.get('sort_order', 'desc')
        
        # טען נתונים
        schedule = load_data(SCHEDULE_FILE)
        
        # מיון
        if sort_by == 'post':
            schedule = sorted(schedule, key=lambda x: x.get('post', {}).get('name', '') if x.get('post') else '', reverse=(sort_order == 'desc'))
        elif sort_by == 'groups':
            schedule = sorted(schedule, key=lambda x: len(x.get('groups', [])) if x.get('groups') else 0, reverse=(sort_order == 'desc'))
        elif sort_by == 'media':
            schedule = sorted(schedule, key=lambda x: len(x.get('media_files', [])) if x.get('media_files') else 0, reverse=(sort_order == 'desc'))
        elif sort_by == 'status':
            schedule = sorted(schedule, key=lambda x: x.get('status', ''), reverse=(sort_order == 'desc'))
        elif sort_by == 'created':
            schedule = sorted(schedule, key=lambda x: x.get('created', ''), reverse=(sort_order == 'desc'))
        else:
            schedule = sorted(schedule, key=lambda x: x.get('created', ''), reverse=True)
        
        # חישוב פאגינציה
        total_items = len(schedule)
        total_pages = (total_items + per_page - 1) // per_page
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        # חתוך את הנתונים לעמוד הנוכחי
        page_data = schedule[start_index:end_index]
        
        return jsonify({
            'success': True,
            'data': page_data,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'per_page': per_page,
                'total_items': total_items,
                'has_prev': page > 1,
                'has_next': page < total_pages
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'שגיאה: {str(e)}'})

@app.route('/login')
def login():
    """עמוד התחברות לפייסבוק"""
    return render_template('login.html')

# משתנה גלובלי לניהול התחברות
login_thread = None
login_bot = None
login_complete = False

# משתנה גלובלי לניהול פרסומים פעילים
active_publishing_tasks = {}

@app.route('/save_login', methods=['POST'])
def save_login():
    """שמור פרטי התחברות - פתרון עם כפתור אישור"""
    global login_thread, login_bot, login_complete
    
    try:
        print("🔄 מתחיל תהליך התחברות...")
        
        # מחק cookies קיימים אם יש
        if os.path.exists(COOKIES_FILE):
            os.remove(COOKIES_FILE)
            print("🗑️ מחקתי cookies קיימים")
        
        # צור תיקיית sessions אם לא קיימת
        os.makedirs("sessions", exist_ok=True)
        
        # איפוס משתנים
        login_complete = False
        
        # הפעל thread נפרד שימתין לאישור מהדף
        def wait_for_login():
            try:
                print("\n" + "="*60)
                print("🔐 ממתין לאישור התחברות...")
                print("📝 לאחר שהתחברת בפייסבוק, לחץ 'אישור התחברות' בדף")
                print("="*60)
                
                # פתח דפדפן חדש להתחברות
                from simple_facebook_bot import SimpleFacebookBot
                global login_bot
                login_bot = SimpleFacebookBot()
                
                # נווט לעמוד התחברות
                login_bot.page.goto("https://www.facebook.com/login")
                login_bot.page.wait_for_load_state('networkidle')
                
                print("✅ דפדפן נפתח להתחברות")
                print("🔔 המשתמש יכול להתחבר כעת בדפדפן")
                
                # המתן לאישור מהדף (לא מהטרמינל)
                while not login_complete:
                    time.sleep(1)
                
                # שמור cookies
                with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(login_bot.context.cookies(), f, indent=2, ensure_ascii=False)
                
                login_bot.close()
                login_bot = None
                
                print("✅ התחברות נשמרה בהצלחה!")
                print("🔄 הדשבורד יתעדכן אוטומטית")
                
            except Exception as e:
                print(f"❌ שגיאה בהתחברות: {e}")
        
        # הפעל את ה-thread ברקע
        login_thread = threading.Thread(target=wait_for_login, daemon=True)
        login_thread.start()
        
        return jsonify({
            "success": True, 
            "message": "דפדפן נפתח להתחברות. התחבר בפייסבוק ולחץ 'אישור התחברות'",
            "waiting_for_approval": True
        })
        
    except Exception as e:
        print(f"❌ שגיאה כללית בהתחברות: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})


@app.route('/approve_login', methods=['POST'])
def approve_login():
    """אשר התחברות מהדף"""
    global login_complete, login_bot
    
    try:
        if login_bot is None:
            return jsonify({"success": False, "message": "אין תהליך התחברות פעיל"})
        
        # סמן שההתחברות אושרה
        login_complete = True
        
        print("✅ המשתמש אישר את ההתחברות מהדף")
        
        return jsonify({"success": True, "message": "התחברות אושרה! ממתין לשמירת ה-cookies..."})
        
    except Exception as e:
        print(f"❌ שגיאה באישור התחברות: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/check_login_complete', methods=['GET'])
def check_login_complete():
    """בדוק אם ההתחברות הושלמה"""
    try:
        has_cookies = os.path.exists(COOKIES_FILE)
        if has_cookies:
            # בדוק אם הקובץ לא ריק
            with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
            
            if cookies_data and len(cookies_data) > 0:
                return jsonify({"success": True, "completed": True, "message": "התחברות הושלמה!"})
        
        return jsonify({"success": True, "completed": False, "message": "עדיין ממתין להשלמת ההתחברות"})
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/wait_for_login_confirmation', methods=['POST'])
def wait_for_login_confirmation():
    """המתן לאישור התחברות מהטרמינל"""
    global login_bot
    
    try:
        if not login_bot:
            return jsonify({"success": False, "message": "אין דפדפן פתוח להתחברות"})
        
        # הפעל thread נפרד שימתין לקלט מהטרמינל
        def wait_for_enter():
            try:
                print("\n" + "="*60)
                print("🔐 ממתין לאישור התחברות...")
                print("📝 לאחר שהתחברת בפייסבוק, לחץ Enter כאן בטרמינל")
                print("="*60)
                
                input()  # המתן ללחיצה על Enter
                
                # שמור cookies
                cookies = login_bot.context.cookies()
                save_data(COOKIES_FILE, cookies)
                login_bot.close()
                login_bot = None
                
                print("✅ התחברות נשמרה בהצלחה!")
                print("🔄 הדשבורד יתעדכן אוטומטית")
                
            except Exception as e:
                print(f"❌ שגיאה בהמתנה לאישור: {e}")
        
        # הפעל את ה-thread ברקע
        thread = threading.Thread(target=wait_for_enter, daemon=True)
        thread.start()
        
        return jsonify({
            "success": True, 
            "message": "ממתין לאישור בטרמינל... לחץ Enter בטרמינל לאחר ההתחברות",
            "waiting": True
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/confirm_login', methods=['POST'])
def confirm_login():
    """אשר התחברות לאחר שהמשתמש התחבר בדפדפן"""
    global login_bot
    
    try:
        if not login_bot:
            return jsonify({"success": False, "message": "אין דפדפן פתוח להתחברות"})
        
        # בדוק אם המשתמש התחבר - בדיקות מתקדמות יותר
        current_url = login_bot.page.url
        print(f"URL נוכחי: {current_url}")
        
        # בדוק אם יש cookies של התחברות
        cookies = login_bot.context.cookies()
        has_user_cookie = False
        has_session_cookie = False
        
        for cookie in cookies:
            if cookie.get('name') == 'c_user':
                has_user_cookie = True
                print(f"✅ נמצא cookie של משתמש: {cookie.get('value')}")
            elif cookie.get('name') == 'xs' or cookie.get('name') == 'datr':
                has_session_cookie = True
                print(f"✅ נמצא cookie של סשן: {cookie.get('name')}")
        
        # בדוק גם אם הדף לא בעמוד התחברות
        is_not_login_page = "login" not in current_url.lower() and "signup" not in current_url.lower()
        
        # בדוק אם יש אלמנטים שמצביעים על התחברות
        try:
            # חפש אלמנטים שמצביעים על התחברות (כמו תפריט המשתמש)
            user_elements = login_bot.page.query_selector_all('[data-testid="user-navigation-menu"], [aria-label*="חשבון"], [aria-label*="Account"], [data-click="profile_icon"]')
            has_user_elements = len(user_elements) > 0
            print(f"נמצאו אלמנטי משתמש: {len(user_elements)}")
        except:
            has_user_elements = False
        
        # אם יש cookies של משתמש או אלמנטי משתמש - המשתמש מחובר
        if has_user_cookie or (is_not_login_page and has_user_elements):
            # שמור cookies
            save_data(COOKIES_FILE, cookies)
            login_bot.close()
            login_bot = None
            
            print("✅ התחברות נשמרה בהצלחה!")
            return jsonify({"success": True, "message": "התחברות נשמרה בהצלחה!"})
        else:
            # אם אין cookies של משתמש, נסה בכל מקרה אם המשתמש אומר שהוא התחבר
            print("⚠️ לא נמצאו cookies של משתמש, אבל נשמור בכל מקרה")
            
            # שמור cookies בכל מקרה (לפעמים זה עובד גם בלי זיהוי מושלם)
            save_data(COOKIES_FILE, cookies)
            login_bot.close()
            login_bot = None
            
            print("✅ התחברות נשמרה (בהנחה שהמשתמש התחבר)")
            return jsonify({"success": True, "message": "התחברות נשמרה בהצלחה!"})
        
    except Exception as e:
        print(f"❌ שגיאה באישור התחברות: {e}")
        
        # גם במקרה של שגיאה, נסה לשמור את ה-cookies הקיימים
        try:
            if login_bot:
                cookies = login_bot.context.cookies()
                save_data(COOKIES_FILE, cookies)
                login_bot.close()
                login_bot = None
                print("✅ התחברות נשמרה למרות השגיאה")
                return jsonify({"success": True, "message": "התחברות נשמרה בהצלחה!"})
        except:
            pass
            
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/check_login_status', methods=['POST'])
def check_login_status():
    """בדוק סטטוס התחברות בדפדפן הפתוח"""
    global login_bot
    
    try:
        if not login_bot:
            return jsonify({"success": False, "message": "אין דפדפן פתוח להתחברות"})
        
        # קבל מידע על המצב הנוכחי
        current_url = login_bot.page.url
        cookies = login_bot.context.cookies()
        
        # בדוק cookies
        cookie_info = []
        has_user_cookie = False
        
        for cookie in cookies:
            if cookie.get('name') == 'c_user':
                has_user_cookie = True
            cookie_info.append({
                'name': cookie.get('name'),
                'domain': cookie.get('domain'),
                'path': cookie.get('path')
            })
        
        # בדוק אלמנטי משתמש
        try:
            user_elements = login_bot.page.query_selector_all('[data-testid="user-navigation-menu"], [aria-label*="חשבון"], [aria-label*="Account"]')
            user_elements_count = len(user_elements)
        except:
            user_elements_count = 0
        
        return jsonify({
            "success": True,
            "current_url": current_url,
            "has_user_cookie": has_user_cookie,
            "user_elements_count": user_elements_count,
            "cookies_count": len(cookies),
            "cookie_info": cookie_info[:5],  # רק 5 הראשונים
            "message": f"URL: {current_url}, Cookies: {len(cookies)}, User Elements: {user_elements_count}"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/cancel_login', methods=['POST'])
def cancel_login():
    """בטל תהליך התחברות"""
    global login_bot
    
    try:
        if login_bot:
            login_bot.close()
            login_bot = None
            print("❌ תהליך התחברות בוטל")
        
        return jsonify({"success": True, "message": "תהליך התחברות בוטל"})
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/disconnect_user', methods=['POST'])
def disconnect_user():
    """נתק משתמש נוכחי"""
    try:
        # מחק את קובץ ה-cookies
        if os.path.exists(COOKIES_FILE):
            os.remove(COOKIES_FILE)
            print("✅ קובץ cookies נמחק - משתמש נותק")
            return jsonify({"success": True, "message": "המשתמש נותק בהצלחה"})
        else:
            return jsonify({"success": False, "message": "אין משתמש מחובר"})
    except Exception as e:
        print(f"❌ שגיאה בניתוק משתמש: {e}")
        return jsonify({"success": False, "message": f"שגיאה בניתוק: {str(e)}"})

@app.route('/connect_new_user', methods=['POST'])
def connect_new_user():
    """התחבר עם משתמש חדש"""
    try:
        print("🔄 מתחיל תהליך התחברות עם משתמש חדש...")
        
        # מחק cookies קיימים אם יש
        if os.path.exists(COOKIES_FILE):
            os.remove(COOKIES_FILE)
            print("🗑️ מחקתי cookies קיימים")
        
        # צור תיקיית sessions אם לא קיימת
        os.makedirs("sessions", exist_ok=True)
        
        # הפעל את הסקריפט ליצירת cookies חדשים
        result = subprocess.run([
            sys.executable, 
            "simple_facebook_bot.py", 
            "--login-only"
        ], capture_output=True, text=True, encoding='utf-8', timeout=300)
        
        if result.returncode == 0:
            print("✅ התחברות עם משתמש חדש הושלמה")
            return jsonify({"success": True, "message": "התחברות עם משתמש חדש הושלמה בהצלחה!"})
        else:
            print(f"❌ שגיאה בהתחברות: {result.stderr}")
            return jsonify({"success": False, "message": f"שגיאה בהתחברות: {result.stderr}"})
            
    except subprocess.TimeoutExpired:
        print("⏰ פג הזמן להתחברות")
        return jsonify({"success": False, "message": "פג הזמן להתחברות. נסה שוב."})
    except Exception as e:
        print(f"❌ שגיאה כללית בהתחברות: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/list_sessions', methods=['GET'])
def list_sessions():
    """רשום את כל הסשנים השמורים"""
    try:
        sessions_dir = "sessions"
        if not os.path.exists(sessions_dir):
            return jsonify({"success": True, "sessions": []})
        
        sessions = []
        for filename in os.listdir(sessions_dir):
            if filename.endswith('.json') and filename != 'facebook-cookie.json':
                filepath = os.path.join(sessions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        cookies_data = json.load(f)
                    
                    # חפש מידע על המשתמש
                    username = "לא ידוע"
                    user_id = None
                    for cookie in cookies_data:
                        if cookie.get('name') == 'c_user':
                            user_id = cookie.get('value', 'לא ידוע')
                            username = f"משתמש ID: {user_id}"
                            break
                    
                    # קבל תאריך יצירה
                    created_time = datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                    
                    sessions.append({
                        "filename": filename,
                        "username": username,
                        "user_id": user_id,
                        "created": created_time,
                        "is_current": filename == "facebook-cookie.json"
                    })
                except Exception as e:
                    print(f"שגיאה בטעינת {filename}: {e}")
        
        return jsonify({"success": True, "sessions": sessions})
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/switch_session', methods=['POST'])
def switch_session():
    """החלף לסשן אחר"""
    try:
        data = request.json
        session_filename = data.get('filename')
        
        if not session_filename:
            return jsonify({"success": False, "message": "לא נבחר סשן"})
        
        sessions_dir = "sessions"
        source_file = os.path.join(sessions_dir, session_filename)
        target_file = os.path.join(sessions_dir, "facebook-cookie.json")
        
        if not os.path.exists(source_file):
            return jsonify({"success": False, "message": "קובץ הסשן לא נמצא"})
        
        # העתק את הסשן הנבחר לסשן הפעיל
        shutil.copy2(source_file, target_file)
        
        print(f"✅ הוחלף לסשן: {session_filename}")
        return jsonify({"success": True, "message": f"הוחלף לסשן: {session_filename}"})
        
    except Exception as e:
        print(f"❌ שגיאה בהחלפת סשן: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/save_current_session', methods=['POST'])
def save_current_session():
    """שמור את הסשן הנוכחי עם שם מותאם אישית"""
    try:
        data = request.json
        session_name = data.get('name', '').strip()
        
        if not session_name:
            return jsonify({"success": False, "message": "יש להזין שם לסשן"})
        
        if not os.path.exists(COOKIES_FILE):
            return jsonify({"success": False, "message": "אין סשן פעיל לשמירה"})
        
        # צור שם קובץ בטוח
        safe_name = "".join(c for c in session_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        if not safe_name:
            safe_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        target_filename = f"{safe_name}.json"
        target_filepath = os.path.join("sessions", target_filename)
        
        # העתק את הסשן הנוכחי
        shutil.copy2(COOKIES_FILE, target_filepath)
        
        print(f"✅ סשן נשמר: {target_filename}")
        return jsonify({"success": True, "message": f"הסשן '{session_name}' נשמר בהצלחה!"})
        
    except Exception as e:
        print(f"❌ שגיאה בשמירת סשן: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/get_user_status', methods=['GET'])
def get_user_status():
    """קבל סטטוס המשתמש הנוכחי"""
    try:
        has_cookies = os.path.exists(COOKIES_FILE)
        
        if has_cookies:
            # נסה לזהות איזה משתמש מחובר
            try:
                with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                    cookies_data = json.load(f)
                
                # חפש שם משתמש ב-cookies
                username = "לא ידוע"
                user_id = None
                for cookie in cookies_data:
                    if cookie.get('name') == 'c_user':
                        user_id = cookie.get('value', 'לא ידוע')
                        username = f"משתמש ID: {user_id}"
                        break
                
                return jsonify({
                    "connected": True, 
                    "username": username,
                    "user_id": user_id,
                    "message": "משתמש מחובר"
                })
            except:
                return jsonify({
                    "connected": True, 
                    "username": "משתמש מחובר",
                    "user_id": None,
                    "message": "משתמש מחובר"
                })
        else:
            return jsonify({
                "connected": False, 
                "username": None,
                "user_id": None,
                "message": "אין משתמש מחובר"
            })
            
    except Exception as e:
        return jsonify({
            "connected": False, 
            "username": None,
            "user_id": None,
            "message": f"שגיאה: {str(e)}"
        })

@app.route('/add_group', methods=['POST'])
def add_group():
    """הוסף קבוצה חדשה"""
    data = request.json
    group_url = data.get('url', '').strip()
    group_name = data.get('name', '').strip()
    is_my_group = data.get('is_my_group', False)  # שדה חדש
    
    if not group_url:
        return jsonify({"success": False, "message": "יש להזין URL של הקבוצה"})
    
    if not group_name:
        group_name = f"קבוצה {datetime.now().strftime('%H:%M')}"
    
    # טען קבוצות קיימות
    groups = load_data(GROUPS_FILE)
    
    # בדוק אם הקבוצה כבר קיימת
    for group in groups:
        if group.get('url') == group_url:
            return jsonify({"success": False, "message": "הקבוצה כבר קיימת"})
    
    # הוסף קבוצה חדשה
    new_group = {
        "id": len(groups) + 1,
        "name": group_name,
        "url": group_url,
        "is_my_group": is_my_group,
        "active": True,
        "created": datetime.now().isoformat()
    }
    
    groups.append(new_group)
    
    if save_data(GROUPS_FILE, groups):
        group_type = "שלי" if is_my_group else "חיצונית"
        return jsonify({"success": True, "message": f"הקבוצה '{group_name}' נוספה בהצלחה כקבוצה {group_type}!"})
    else:
        return jsonify({"success": False, "message": "שגיאה בשמירת הקבוצה"})

@app.route('/update_group/<int:group_id>', methods=['POST'])
def update_group(group_id):
    """עדכן פרטי קבוצה"""
    data = request.json
    is_my_group = data.get('is_my_group', False)
    
    # טען קבוצות קיימות
    groups = load_data(GROUPS_FILE)
    
    # מצא את הקבוצה ועדכן אותה
    for group in groups:
        if group.get('id') == group_id:
            group['is_my_group'] = is_my_group
            group['updated'] = datetime.now().isoformat()
            
            if save_data(GROUPS_FILE, groups):
                group_type = "שלי" if is_my_group else "חיצונית"
                return jsonify({"success": True, "message": f"הקבוצה עודכנה ל-{group_type}!"})
            else:
                return jsonify({"success": False, "message": "שגיאה בשמירת השינויים"})
    
    return jsonify({"success": False, "message": "קבוצה לא נמצאה"})

@app.route('/edit_post', methods=['POST'])
def edit_post():
    """ערוך פוסט קיים"""
    data = request.json
    post_id = data.get('post_id')
    post_name = data.get('name', '').strip()
    post_text = data.get('text', '').strip()
    
    if not post_id:
        return jsonify({"success": False, "message": "לא נמסר מזהה פוסט"})
    
    if not post_name or not post_text:
        return jsonify({"success": False, "message": "יש למלא את כל השדות"})
    
    # טען פוסטים קיימים
    posts = load_data(POSTS_FILE)
    
    # מצא את הפוסט ועדכן אותו
    for post in posts:
        if post.get('id') == post_id:
            post['name'] = post_name
            post['text'] = post_text
            post['updated'] = datetime.now().isoformat()
            
            if save_data(POSTS_FILE, posts):
                return jsonify({"success": True, "message": "הפוסט עודכן בהצלחה!"})
            else:
                return jsonify({"success": False, "message": "שגיאה בשמירת השינויים"})
    
    return jsonify({"success": False, "message": "פוסט לא נמצא"})

@app.route('/edit_group', methods=['POST'])
def edit_group():
    """ערוך קבוצה קיימת"""
    data = request.json
    group_id = data.get('group_id')
    group_name = data.get('name', '').strip()
    group_url = data.get('url', '').strip()
    is_my_group = data.get('is_my_group', False)
    
    if not group_id:
        return jsonify({"success": False, "message": "לא נמסר מזהה קבוצה"})
    
    if not group_name or not group_url:
        return jsonify({"success": False, "message": "יש למלא את כל השדות"})
    
    # טען קבוצות קיימות
    groups = load_data(GROUPS_FILE)
    
    # בדוק אם URL כבר קיים בקבוצה אחרת
    for group in groups:
        if group.get('id') != group_id and group.get('url') == group_url:
            return jsonify({"success": False, "message": "URL זה כבר קיים בקבוצה אחרת"})
    
    # מצא את הקבוצה ועדכן אותה
    for group in groups:
        if group.get('id') == group_id:
            group['name'] = group_name
            group['url'] = group_url
            group['is_my_group'] = is_my_group
            group['updated'] = datetime.now().isoformat()
            
            if save_data(GROUPS_FILE, groups):
                group_type = "שלי" if is_my_group else "חיצונית"
                return jsonify({"success": True, "message": f"הקבוצה עודכנה בהצלחה כקבוצה {group_type}!"})
            else:
                return jsonify({"success": False, "message": "שגיאה בשמירת השינויים"})
    
    return jsonify({"success": False, "message": "קבוצה לא נמצאה"})

@app.route('/add_post', methods=['POST'])
def add_post():
    """הוסף פוסט חדש"""
    data = request.json
    post_text = data.get('text', '').strip()
    post_name = data.get('name', '').strip()
    
    if not post_text:
        return jsonify({"success": False, "message": "יש להזין תוכן לפוסט"})
    
    if not post_name:
        post_name = f"פוסט {datetime.now().strftime('%H:%M')}"
    
    # טען פוסטים קיימים
    posts = load_data(POSTS_FILE)
    
    # הוסף פוסט חדש
    new_post = {
        "id": len(posts) + 1,
        "name": post_name,
        "text": post_text,
        "created": datetime.now().isoformat()
    }
    
    posts.append(new_post)
    
    if save_data(POSTS_FILE, posts):
        return jsonify({"success": True, "message": "הפוסט נוסף בהצלחה!"})
    else:
        return jsonify({"success": False, "message": "שגיאה בשמירת הפוסט"})

@app.route('/upload_media', methods=['POST'])
def upload_media():
    """העלה קבצי מדיה"""
    try:
        if 'files' not in request.files:
            return jsonify({"success": False, "message": "לא נבחרו קבצים"})
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({"success": False, "message": "לא נבחרו קבצים"})
        
        uploaded_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # שמור את הקובץ
                original_filename = file.filename
                # הוסף timestamp לשם הקובץ כדי למנוע התנגשויות
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(original_filename)
                
                # נקה את השם אבל שמור את הסיומת
                clean_name = secure_filename(name)
                if not clean_name:  # אם השם ריק אחרי הניקוי
                    clean_name = "file"
                
                filename = f"{clean_name}_{timestamp}{ext}"
                
                file_path = os.path.join(UPLOADS_DIR, filename)
                file.save(file_path)
                
                uploaded_files.append({
                    "name": file.filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path)
                })
            else:
                return jsonify({"success": False, "message": f"קובץ {file.filename} לא נתמך. קבצים נתמכים: {', '.join(ALLOWED_EXTENSIONS)}"})
        
        return jsonify({
            "success": True, 
            "message": f"הועלו {len(uploaded_files)} קבצים בהצלחה!",
            "files": uploaded_files
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה בהעלאת קבצים: {str(e)}"})

@app.route('/add_media_group', methods=['POST'])
def add_media_group():
    """הוסף קבוצת מדיה (נתיבים מקומיים)"""
    try:
        data = request.json
        print(f"📥 נתונים התקבלו: {data}")
        
        title = data.get('title', '').strip()
        files = data.get('files', [])
        
        print(f"📝 כותרת: {title}")
        print(f"📁 קבצים: {files}")
        
        if not title:
            return jsonify({"success": False, "message": "יש להזין כותרת לקבוצת המדיה"})
        
        if not files or len(files) == 0:
            return jsonify({"success": False, "message": "יש לבחור לפחות קובץ אחד"})
        
        # טען מדיה קיימת
        media = load_data(MEDIA_FILE)
        
        # בדוק אם הכותרת כבר קיימת
        for item in media:
            if item.get('title') == title:
                return jsonify({"success": False, "message": "קבוצת מדיה עם כותרת זו כבר קיימת"})
        
        # הוסף קבוצת מדיה חדשה
        new_media_group = {
            "id": len(media) + 1,
            "title": title,
            "files": files,
            "created": datetime.now().isoformat()
        }
        
        media.append(new_media_group)
        
        if save_data(MEDIA_FILE, media):
            print(f"✅ קבוצת המדיה '{title}' נשמרה בהצלחה")
            return jsonify({"success": True, "message": f"קבוצת המדיה '{title}' נוספה בהצלחה עם {len(files)} קבצים!"})
        else:
            print("❌ שגיאה בשמירת קבוצת המדיה")
            return jsonify({"success": False, "message": "שגיאה בשמירת קבוצת המדיה"})
    
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/schedule_post', methods=['POST'])
def schedule_post():
    """תזמן פוסט"""
    data = request.json
    group_ids = data.get('groups', [])
    post_id = data.get('post_id')
    media_id = data.get('media_id')
    schedule_time = data.get('schedule_time')
    
    if not group_ids:
        return jsonify({"success": False, "message": "יש לבחור לפחות קבוצה אחת"})
    
    if not post_id and not media_id:
        return jsonify({"success": False, "message": "יש לבחור פוסט או מדיה"})
    
    # טען נתונים
    groups = load_data(GROUPS_FILE)
    posts = load_data(POSTS_FILE)
    media = load_data(MEDIA_FILE)
    
    # מצא את הפוסט (אם נבחר)
    post = None
    if post_id:
        post = next((p for p in posts if p['id'] == post_id), None)
        if not post:
            return jsonify({"success": False, "message": "פוסט לא נמצא"})
    
    # מצא את קבוצת המדיה (אם נבחרה)
    media_files = []
    if media_id:
        media_item = next((m for m in media if m['id'] == media_id), None)
        if media_item and media_item.get('files'):
            media_files = media_item['files']
    
    # מצא את הקבוצות
    selected_groups = [g for g in groups if g['id'] in group_ids]
    
    if not selected_groups:
        return jsonify({"success": False, "message": "קבוצות לא נמצאו"})
    
    # טען תזמונים קיימים
    schedule = load_data(SCHEDULE_FILE)
    
    # הוסף תזמון חדש
    new_schedule = {
        "id": len(schedule) + 1,
        "post": post,
        "groups": selected_groups,
        "media_files": media_files,
        "schedule_time": schedule_time,
        "status": "scheduled",
        "created": datetime.now().isoformat()
    }
    
    schedule.append(new_schedule)
    
    if save_data(SCHEDULE_FILE, schedule):
        # הפעל תזמון אם זה מיידי
        if not schedule_time or schedule_time == "now":
            thread = threading.Thread(target=run_scheduled_post, args=(new_schedule,))
            thread.start()
        
        return jsonify({"success": True, "message": "הפוסט תוזמן בהצלחה!", "schedule_id": new_schedule['id']})
    else:
        return jsonify({"success": False, "message": "שגיאה בשמירת התזמון"})

def update_schedule_status(schedule_id, status, successful_count=0, failed_count=0, error_message=''):
    """עדכן סטטוס של תזמון"""
    try:
        schedule = load_data(SCHEDULE_FILE)
        for item in schedule:
            if item['id'] == schedule_id:
                item['status'] = status
                if status == 'completed':
                    item['completed_at'] = datetime.now().isoformat()
                    item['successful_groups'] = successful_count
                    item['failed_groups'] = failed_count
                elif status == 'failed':
                    item['error_message'] = error_message
                    item['failed_at'] = datetime.now().isoformat()
                elif status == 'in_progress':
                    item['started_at'] = datetime.now().isoformat()
                break
        save_data(SCHEDULE_FILE, schedule)
    except Exception as e:
        print(f"שגיאה בעדכון סטטוס תזמון: {e}")

def update_group_status(schedule_id, group_name, status, error_message='', post_url=''):
    """עדכן סטטוס של קבוצה בתזמון"""
    try:
        schedule = load_data(SCHEDULE_FILE)
        for item in schedule:
            if item['id'] == schedule_id:
                if 'group_statuses' not in item:
                    item['group_statuses'] = {}
                
                item['group_statuses'][group_name] = {
                    'status': status,
                    'updated_at': datetime.now().isoformat(),
                    'error_message': error_message,
                    'post_url': post_url
                }
                
                # הוסף לוג מפורט (רק אם זה לא 'in_progress' - כדי למנוע כפילות)
                if 'logs' not in item:
                    item['logs'] = []
                
                # הוסף לוג רק למצבים סופיים
                if status in ['success', 'failed']:
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'type': status,
                        'message': f"{'✅' if status == 'success' else '❌'} {group_name}: {error_message if error_message else 'הושלם'}"
                    }
                    item['logs'].append(log_entry)
                    
                    # שמור URL אם זה הצלחה
                    if status == 'success' and post_url:
                        if 'successful_posts' not in item:
                            item['successful_posts'] = []
                        item['successful_posts'].append({
                            'group_name': group_name,
                            'url': post_url,
                            'timestamp': datetime.now().isoformat()
                        })
                
                break
        save_data(SCHEDULE_FILE, schedule)
    except Exception as e:
        print(f"שגיאה בעדכון סטטוס קבוצה: {e}")

def run_scheduled_post(schedule_item):
    """הרץ פוסט מתוזמן עם זיהוי סוג הקבוצה"""
    global active_publishing_tasks
    
    schedule_id = schedule_item['id']
    
    try:
        post = schedule_item['post']
        groups = schedule_item['groups']
        media_files = schedule_item.get('media_files', [])
        
        # הוסף לרשימת המשימות הפעילות
        active_publishing_tasks[schedule_id] = {
            'should_stop': False,
            'started_at': datetime.now()
        }
        
        # עדכן סטטוס ל"בתהליך"
        update_schedule_status(schedule_id, 'in_progress')
        
        if post:
            print(f"מתחיל פרסום פוסט: {post['name']}")
        else:
            print("מתחיל פרסום מדיה בלבד")
        if media_files:
            print(f"עם {len(media_files)} קבצי מדיה")
        
        successful_groups = 0
        failed_groups = 0
        
        # בדוק אם יש קבוצות "שלי" - צור בוט אחד לכולן
        my_groups = [g for g in groups if is_my_group(g['url'])]
        bot = None
        if my_groups:
            print(f"🏠 מצאתי {len(my_groups)} קבוצות שלי - יוצר בוט...")
            bot = SimpleFacebookBot()
        
        try:
            for group in groups:
                # בדוק אם הפרסום צריך להיעצר
                if active_publishing_tasks.get(schedule_id, {}).get('should_stop', False):
                    print(f"🛑 הפרסום נעצר על ידי המשתמש")
                    update_schedule_status(schedule_id, 'stopped', successful_groups, failed_groups)
                    break
                
                try:
                    group_url = group['url']
                    group_name = group['name']
                    
                    print(f"מפרסם בקבוצה: {group_name}")
                    print(f"URL: {group_url}")
                    
                    # בדוק אם הקבוצה של המשתמש
                    if is_my_group(group_url):
                        print("🏠 זו קבוצה שלי - משתמש ב-simple_facebook_bot")
                        
                        post_text = post['text'] if post else ""
                        
                        # העבר את כל קבצי המדיה
                        if media_files:
                            print(f"📁 מעלה {len(media_files)} קבצי מדיה...")
                            success = bot.post_to_group_with_multiple_media(
                                group_url=group_url,
                                text=post_text,
                                media_files=media_files
                            )
                        else:
                            success = bot.post_to_group(
                                group_url=group_url,
                                text=post_text,
                                image_path=None
                            )
                        
                    else:
                        print("🔍 זו קבוצה לא שלי - משתמש ב-selector_explorer")
                        
                        # השתמש ב-selector_explorer
                        post_text = post['text'] if post else ""
                        success = run_selector_explorer(group_url, group_name, post_text, media_files)
                    
                    if success:
                        print(f"✅ פורסם בהצלחה בקבוצה: {group_name}")
                        successful_groups += 1
                        # קבל את ה-URL של הקבוצה כ-URL של הפוסט (מכיוון שאין דרך לדעת את ה-URL המדויק של הפוסט)
                        update_group_status(schedule_id, group_name, 'success', '', group_url)
                    else:
                        print(f"❌ נכשל פרסום בקבוצה: {group_name}")
                        failed_groups += 1
                        update_group_status(schedule_id, group_name, 'failed', 'שגיאה לא ידועה')
                        
                except Exception as e:
                    print(f"❌ שגיאה בקבוצה {group['name']}: {e}")
                    failed_groups += 1
                    update_group_status(schedule_id, group['name'], 'failed', str(e))
        
        finally:
            # סגור את הבוט אם נוצר
            if bot:
                print("🔒 סוגר את הדפדפן...")
                bot.close()
        
        # עדכן סטטוס סופי רק אם לא נעצר
        if not active_publishing_tasks.get(schedule_id, {}).get('should_stop', False):
            update_schedule_status(schedule_id, 'completed', successful_groups, failed_groups)
            print(f"פרסום הושלם! הצלחות: {successful_groups}, כישלונות: {failed_groups}")
        
    except Exception as e:
        print(f"שגיאה כללית בפרסום: {e}")
        update_schedule_status(schedule_item['id'], 'failed', 0, len(groups), str(e))
    
    finally:
        # הסר מהרשימת המשימות הפעילות
        if schedule_id in active_publishing_tasks:
            del active_publishing_tasks[schedule_id]

@app.route('/republish_item/<int:item_id>', methods=['POST'])
def republish_item(item_id):
    """פרסם מחדש פריט מההיסטוריה"""
    try:
        # טען תזמונים
        schedule = load_data(SCHEDULE_FILE)
        
        # מצא את הפריט
        original_item = None
        for item in schedule:
            if item.get('id') == item_id:
                original_item = item
                break
        
        if not original_item:
            return jsonify({"success": False, "message": "פריט לא נמצא"})
        
        # צור פריט חדש עם אותם נתונים
        new_schedule = {
            "id": len(schedule) + 1,
            "post": original_item.get('post'),
            "groups": original_item.get('groups', []),
            "media_files": original_item.get('media_files', []),
            "schedule_time": "now",
            "status": "scheduled",
            "created": datetime.now().isoformat()
        }
        
        # הוסף לתזמונים
        schedule.append(new_schedule)
        
        if save_data(SCHEDULE_FILE, schedule):
            # הפעל תזמון מיידי
            thread = threading.Thread(target=run_scheduled_post, args=(new_schedule,))
            thread.start()
            
            return jsonify({"success": True, "message": "הפרסום תוזמן מחדש בהצלחה!"})
        else:
            return jsonify({"success": False, "message": "שגיאה בשמירת התזמון"})
            
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/get_publishing_logs/<int:schedule_id>')
def get_publishing_logs(schedule_id):
    """קבל לוגים של פרסום מסוים"""
    try:
        # טען תזמונים
        schedule = load_data(SCHEDULE_FILE)
        
        # מצא את התזמון
        schedule_item = None
        for item in schedule:
            if item.get('id') == schedule_id:
                schedule_item = item
                break
        
        if not schedule_item:
            return jsonify({"success": False, "message": "תזמון לא נמצא"})
        
        logs = []
        status = schedule_item.get('status', 'unknown')
        
        # הוסף לוג התחלה
        if status in ['scheduled', 'in_progress']:
            logs.append({
                "type": "info",
                "message": f"🚀 מתחיל פרסום #{schedule_id}",
                "timestamp": schedule_item.get('created', datetime.now().isoformat())
            })
        
        # הוסף לוגים לפי סטטוס
        if status == 'in_progress':
            logs.append({
                "type": "progress",
                "message": "⏳ פרסום בתהליך...",
                "timestamp": schedule_item.get('started_at', datetime.now().isoformat())
            })
            
        elif status == 'completed':
            logs.append({
                "type": "success",
                "message": "✅ פרסום הושלם בהצלחה!",
                "timestamp": schedule_item.get('completed_at', datetime.now().isoformat())
            })
            
            # הוסף פרטים על תוצאות
            successful = schedule_item.get('successful_groups', 0)
            failed = schedule_item.get('failed_groups', 0)
            
            if successful > 0:
                logs.append({
                    "type": "success",
                    "message": f"📊 {successful} קבוצות פורסמו בהצלחה",
                    "timestamp": schedule_item.get('completed_at', datetime.now().isoformat())
                })
            
            if failed > 0:
                logs.append({
                    "type": "error",
                    "message": f"❌ {failed} קבוצות נכשלו",
                    "timestamp": schedule_item.get('completed_at', datetime.now().isoformat())
                })
                
        elif status == 'stopped':
            logs.append({
                "type": "warning",
                "message": "🛑 הפרסום נעצר על ידי המשתמש",
                "timestamp": schedule_item.get('stopped_at', datetime.now().isoformat())
            })
            
        elif status == 'failed':
            logs.append({
                "type": "error",
                "message": f"❌ פרסום נכשל: {schedule_item.get('error_message', 'שגיאה לא ידועה')}",
                "timestamp": schedule_item.get('failed_at', datetime.now().isoformat())
            })
        
        # הוסף לוגים מפורטים אם יש (כבר כוללים את כל המידע)
        detailed_logs = schedule_item.get('logs', [])
        
        # אם הפרסום הושלם, נסנן לוגים כפולים ונעדכן את התוצאות
        if status == 'completed':
            # קבל רשימת קבוצות שהצליחו ונכשלו
            group_statuses = schedule_item.get('group_statuses', {})
            successful_groups = []
            failed_groups = []
            
            for group_name, group_status in group_statuses.items():
                if group_status.get('status') == 'success':
                    successful_groups.append(group_name)
                elif group_status.get('status') == 'failed':
                    failed_groups.append(group_name)
            
            # הוסף לוגים מעודכנים לכל קבוצה
            for group_name in successful_groups:
                logs.append({
                    "type": "success",
                    "message": f"✅ {group_name}: הושלם",
                    "timestamp": datetime.now().isoformat()
                })
            
            for group_name in failed_groups:
                logs.append({
                    "type": "error",
                    "message": f"❌ {group_name}: שגיאה לא ידועה",
                    "timestamp": datetime.now().isoformat()
                })
        else:
            # אם הפרסום עדיין בתהליך, הצג את הלוגים המקוריים
            for log_entry in detailed_logs:
                logs.append({
                    "type": log_entry.get('type', 'info'),
                    "message": log_entry.get('message', ''),
                    "timestamp": log_entry.get('timestamp', datetime.now().isoformat())
                })
        
        # מיין לוגים לפי זמן
        logs.sort(key=lambda x: x.get('timestamp', ''))
        
        completed = status in ['completed', 'stopped', 'failed']
        
        # קבל רשימת קישורים מוצלחים
        successful_posts = schedule_item.get('successful_posts', [])
        
        return jsonify({
            "success": True,
            "logs": logs,
            "completed": completed,
            "status": status,
            "successful_posts": successful_posts
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/stop_publishing/<int:schedule_id>', methods=['POST'])
def stop_publishing(schedule_id):
    """עצור פרסום פעיל"""
    try:
        global active_publishing_tasks
        
        # בדוק אם יש פרסום פעיל עם המזהה הזה
        if schedule_id in active_publishing_tasks:
            # סמן שהפרסום צריך להיעצר
            active_publishing_tasks[schedule_id]['should_stop'] = True
            
            # עדכן סטטוס בקובץ
            schedule = load_data(SCHEDULE_FILE)
            for item in schedule:
                if item['id'] == schedule_id:
                    item['status'] = 'stopped'
                    item['stopped_at'] = datetime.now().isoformat()
                    break
            save_data(SCHEDULE_FILE, schedule)
            
            print(f"🛑 פרסום #{schedule_id} סומן לעצירה")
            return jsonify({"success": True, "message": "הפרסום סומן לעצירה"})
        else:
            # בדוק אם הפרסום כבר הושלם או לא קיים
            schedule = load_data(SCHEDULE_FILE)
            for item in schedule:
                if item['id'] == schedule_id:
                    if item.get('status') in ['completed', 'failed']:
                        return jsonify({"success": False, "message": "הפרסום כבר הושלם או נכשל"})
                    else:
                        # עדכן סטטוס בכל מקרה
                        item['status'] = 'stopped'
                        item['stopped_at'] = datetime.now().isoformat()
                        save_data(SCHEDULE_FILE, schedule)
                        return jsonify({"success": True, "message": "הפרסום נעצר"})
            
            return jsonify({"success": False, "message": "פרסום לא נמצא"})
            
    except Exception as e:
        print(f"❌ שגיאה בעצירת פרסום: {e}")
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

@app.route('/delete_item/<item_type>/<int:item_id>', methods=['DELETE'])
def delete_item(item_type, item_id):
    """מחק פריט"""
    try:
        if item_type == 'group':
            filename = GROUPS_FILE
        elif item_type == 'post':
            filename = POSTS_FILE
        elif item_type == 'media':
            filename = MEDIA_FILE
        elif item_type == 'schedule':
            filename = SCHEDULE_FILE
        else:
            return jsonify({"success": False, "message": "סוג פריט לא תקין"})
        
        # טען נתונים
        data = load_data(filename)
        
        # מחק פריט
        original_length = len(data)
        data = [item for item in data if item.get('id') != item_id]
        
        if len(data) == original_length:
            return jsonify({"success": False, "message": "פריט לא נמצא"})
        
        if save_data(filename, data):
            return jsonify({"success": True, "message": "הפריט נמחק בהצלחה!"})
        else:
            return jsonify({"success": False, "message": "שגיאה במחיקת הפריט"})
            
    except Exception as e:
        return jsonify({"success": False, "message": f"שגיאה: {str(e)}"})

# Handler ל-Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 מתחיל דשבורד פייסבוק על פורט {port}...")
    print("📱 הדשבורד זמין!")
    app.run(debug=False, host='0.0.0.0', port=port)
