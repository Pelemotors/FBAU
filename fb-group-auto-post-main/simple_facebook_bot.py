from playwright.sync_api import sync_playwright
import json
import os
import sys

# תיקון בעיית קידוד UTF-8
if sys.platform == "win32":
    os.system("chcp 65001")
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# הגדרות לפריסה ב-Vercel
if os.environ.get('VERCEL'):
    # ב-Vercel, נתיבי הקבצים שונים
    BASE_DIR = '/tmp'
else:
    # במחשב מקומי
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SimpleFacebookBot:
    def __init__(self):
        print("🤖 SimpleFacebookBot הופעל")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
    
    def load_cookies(self):
        """טעינת cookies"""
        cookie_file = os.path.join(BASE_DIR, "sessions/facebook-cookie.json")
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
                self.context.add_cookies(cookies)
                print("✅ Cookies נטענו")
                return True
        print("❌ לא נמצאו cookies")
        return False
    
    def post_to_group(self, group_url, text, image_path):
        """פרסם פוסט בקבוצה"""
        try:
            print("🚀 מתחיל פרסום פוסט...")
            
            # טען cookies
            if not self.load_cookies():
                return False
            
            # נכנס לקבוצה
            print(f"📍 נכנס לקבוצה: {group_url}")
            self.page.goto(group_url)
            self.page.wait_for_load_state('networkidle')
            
            # פתח קומפוזר - לחץ על "כאן כותבים…"
            print("📝 פותח קומפוזר...")
            composer_elements = self.page.query_selector_all("text='כאן כותבים…'")
            if composer_elements:
                composer_elements[0].click()
                print("✅ לחץ על קומפוזר")
                self.page.wait_for_timeout(3000)
            else:
                print("❌ לא נמצא קומפוזר")
                return False
            
            # המתן שהקומפוזר ייפתח
            self.page.wait_for_timeout(3000)
            
            # כתוב טקסט
            print(f"✍️ כותב טקסט: {text}")
            try:
                text_field = self.page.wait_for_selector("//div[@role='dialog']//div[@contenteditable='true']", timeout=10000)
                text_field.click()  # לחץ על השדה לפני כתיבה
                self.page.wait_for_timeout(1000)
                text_field.fill(text)
                print("✅ כתב טקסט")
                self.page.wait_for_timeout(1000)
            except Exception as e:
                print(f"❌ שגיאה בכתיבת טקסט: {e}")
                # נסה שוב עם סלקטור אחר
                try:
                    text_field = self.page.query_selector("div[contenteditable='true']")
                    if text_field:
                        text_field.click()
                        self.page.wait_for_timeout(1000)
                        text_field.fill(text)
                        print("✅ כתב טקסט (ניסיון שני)")
                        self.page.wait_for_timeout(1000)
                    else:
                        print("❌ לא נמצא שדה טקסט")
                except Exception as e2:
                    print(f"❌ שגיאה בכתיבת טקסט (ניסיון שני): {e2}")
            
            # העלה תמונה
            if image_path and os.path.exists(image_path):
                print(f"📷 מעלה תמונה: {os.path.basename(image_path)}")
                
                # לחץ על כפתור "תמונה או סרטון"
                media_button = self.page.query_selector("[aria-label='תמונה או סרטון']")
                if media_button:
                    with self.page.expect_file_chooser(timeout=3000) as file_chooser_info:
                        media_button.click()
                    
                    file_chooser = file_chooser_info.value
                    file_chooser.set_files([image_path])
                    print("✅ העלה תמונה")
                    self.page.wait_for_timeout(3000)
                else:
                    print("❌ לא נמצא כפתור העלאת מדיה")
            else:
                print("⚠️ נתיב תמונה לא תקין")
            
            # פרסם את הפוסט - לחץ על "פרסם"
            print("🚀 מפרסם את הפוסט...")
            try:
                # נסה כמה סלקטורים לכפתור הפרסום
                publish_button = None
                
                # סלקטור 1: xpath המקורי
                try:
                    publish_button = self.page.wait_for_selector("xpath=//div[@role='dialog']//div[@aria-label='פרסם']", timeout=5000)
                    print("✅ נמצא כפתור פרסום (xpath)")
                except:
                    pass
                
                # סלקטור 2: span עם טקסט "פרסם"
                if not publish_button:
                    try:
                        publish_button = self.page.wait_for_selector("span:has-text('פרסם')", timeout=5000)
                        print("✅ נמצא כפתור פרסום (span)")
                    except:
                        pass
                
                # סלקטור 3: div עם aria-label="פרסם"
                if not publish_button:
                    try:
                        publish_button = self.page.wait_for_selector("div[aria-label='פרסם']", timeout=5000)
                        print("✅ נמצא כפתור פרסום (aria-label)")
                    except:
                        pass
                
                if publish_button:
                    print(f"📍 מיקום כפתור: {publish_button.bounding_box()}")
                    publish_button.click()
                    print("✅ לחץ על פרסם")
                    
                    # המתן זמן לפרסום
                    print("⏳ ממתין לפרסום...")
                    self.page.wait_for_timeout(5000)
                    
                    # בדוק שהקומפוזר נסגר
                    try:
                        composer = self.page.query_selector("div[role='dialog']")
                        if not composer:
                            print("✅ הקומפוזר נסגר - הפרסום הצליח")
                            print("🎉 הפוסט פורסם בהצלחה!")
                            return True
                        else:
                            print("❌ הקומפוזר עדיין פתוח - הפרסום נכשל")
                            return False
                    except:
                        print("⚠️ לא ניתן לבדוק סטטוס הקומפוזר")
                        return False
                else:
                    print("❌ לא נמצא כפתור פרסום")
                    print("🔍 מחפש אלמנטים זמינים...")
                    
                    # הדפס את כל הכפתורים הזמינים
                    buttons = self.page.query_selector_all("button")
                    print(f"📋 נמצאו {len(buttons)} כפתורים:")
                    for i, btn in enumerate(buttons[:10]):  # רק 10 הראשונים
                        try:
                            text = btn.inner_text()[:50] if btn.inner_text() else "ללא טקסט"
                            print(f"  {i+1}. {text}")
                        except:
                            print(f"  {i+1}. לא ניתן לקרוא טקסט")
                    
                    return False
            except Exception as e:
                print(f"❌ שגיאה בלחיצה על פרסם: {e}")
                return False
                
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            return False
    
    def post_to_group_with_multiple_media(self, group_url, text, media_files):
        """פרסם פוסט בקבוצה עם מספר קבצי מדיה"""
        try:
            print("🚀 מתחיל פרסום פוסט עם מספר קבצי מדיה...")
            
            # טען cookies
            if not self.load_cookies():
                return False
            
            # נכנס לקבוצה
            print(f"📍 נכנס לקבוצה: {group_url}")
            self.page.goto(group_url)
            self.page.wait_for_load_state('networkidle')
            
            # פתח קומפוזר - לחץ על "כאן כותבים…"
            print("📝 פותח קומפוזר...")
            composer_elements = self.page.query_selector_all("text='כאן כותבים…'")
            if composer_elements:
                composer_elements[0].click()
                print("✅ לחץ על קומפוזר")
                self.page.wait_for_timeout(3000)
            else:
                print("❌ לא נמצא קומפוזר")
                return False
            
            # המתן שהקומפוזר ייפתח
            self.page.wait_for_timeout(3000)
            
            # כתוב טקסט (אם יש)
            if text:
                print(f"✍️ כותב טקסט: {text}")
                try:
                    text_field = self.page.wait_for_selector("//div[@role='dialog']//div[@contenteditable='true']", timeout=10000)
                    text_field.click()
                    self.page.wait_for_timeout(1000)
                    text_field.fill(text)
                    print("✅ כתב טקסט")
                    self.page.wait_for_timeout(1000)
                except Exception as e:
                    print(f"❌ שגיאה בכתיבת טקסט: {e}")
            
            # העלה קבצי מדיה
            print(f"📁 מעלה {len(media_files)} קבצי מדיה...")
            uploaded_count = 0
            
            for i, media_file in enumerate(media_files):
                media_path = media_file['path']
                print(f"📎 מעלה קובץ {i+1}/{len(media_files)}: {os.path.basename(media_path)}")
                print(f"   📍 נתיב מלא: {media_path}")
                print(f"   📏 גודל קובץ: {os.path.getsize(media_path) if os.path.exists(media_path) else 'לא קיים'} bytes")
                
                if os.path.exists(media_path):
                    try:
                        # לחץ על כפתור הוספת מדיה
                        media_button = self.page.wait_for_selector("[aria-label='תמונה או סרטון']", timeout=5000)
                        if media_button:
                            media_button.click()
                            print(f"✅ לחץ על כפתור מדיה")
                            self.page.wait_for_timeout(1500)
                            
                            # המתן ל-FileChooser
                            with self.page.expect_file_chooser() as fc_info:
                                # לחץ שוב על כפתור המדיה אם צריך
                                media_button.click()
                            file_chooser = fc_info.value
                            
                            # העלה את הקובץ
                            file_chooser.set_files(media_path)
                            print(f"✅ העלה קובץ: {os.path.basename(media_path)}")
                            uploaded_count += 1
                            
                            # המתן שהקובץ יועלה לפני המעבר לקובץ הבא
                            self.page.wait_for_timeout(3000)
                            
                            # בדוק שהקובץ הועלה (חפש thumbnail או preview)
                            try:
                                # חפש אלמנט שמצביע על שהקובץ הועלה
                                self.page.wait_for_selector("img[src*='blob:']", timeout=3000)
                                print(f"✅ אישור: קובץ {os.path.basename(media_path)} הועלה בהצלחה")
                            except:
                                print(f"⚠️ לא ניתן לאשר העלאת קובץ {os.path.basename(media_path)} - ייתכן שהקובץ הועלה אבל לא נוצר preview")
                        else:
                            print(f"❌ לא נמצא כפתור מדיה")
                    except Exception as e:
                        print(f"❌ שגיאה בהעלאת קובץ {os.path.basename(media_path)}: {e}")
                else:
                    print(f"⚠️ קובץ לא קיים: {media_path}")
            
            print(f"📊 סה״כ הועלו {uploaded_count} מתוך {len(media_files)} קבצים")
            
            # בדוק אם יש מגבלה על מספר קבצים
            if uploaded_count < len(media_files):
                print(f"⚠️ רק {uploaded_count} מתוך {len(media_files)} קבצים הועלו - ייתכן שיש מגבלה")
                print("💡 פייסבוק עלול להגביל מספר קבצים בפוסט אחד")
            
            # פרסם את הפוסט
            print("🚀 מפרסם את הפוסט...")
            try:
                # נסה כמה סלקטורים לכפתור הפרסום
                publish_button = None
                
                # סלקטור 1: span עם טקסט "פרסם"
                try:
                    publish_button = self.page.wait_for_selector("span:has-text('פרסם')", timeout=5000)
                    print("✅ נמצא כפתור פרסום (סלקטור 1)")
                except:
                    pass
                
                # סלקטור 2: div עם aria-label="פרסם"
                if not publish_button:
                    try:
                        publish_button = self.page.wait_for_selector("div[aria-label='פרסם']", timeout=5000)
                        print("✅ נמצא כפתור פרסום (סלקטור 2)")
                    except:
                        pass
                
                # סלקטור 3: לחפש בכלל כפתורים עם "פרסם"
                if not publish_button:
                    try:
                        publish_button = self.page.query_selector("button:has-text('פרסם')")
                        if publish_button:
                            print("✅ נמצא כפתור פרסום (סלקטור 3)")
                    except:
                        pass
                
                if publish_button:
                    print(f"📍 מיקום כפתור: {publish_button.bounding_box()}")
                    publish_button.click()
                    print("✅ לחץ על פרסם")
                    
                    # המתן זמן לפרסום
                    print("⏳ ממתין לפרסום...")
                    self.page.wait_for_timeout(5000)
                    
                    # בדוק שהקומפוזר נסגר
                    try:
                        composer = self.page.query_selector("div[role='dialog']")
                        if not composer:
                            print("✅ הקומפוזר נסגר - הפרסום הצליח")
                            print("🎉 הפוסט פורסם בהצלחה!")
                            return True
                        else:
                            print("❌ הקומפוזר עדיין פתוח - הפרסום נכשל")
                            return False
                    except:
                        print("⚠️ לא ניתן לבדוק סטטוס הקומפוזר")
                        return False
                else:
                    print("❌ לא נמצא כפתור פרסום")
                    print("🔍 מחפש אלמנטים זמינים...")
                    
                    # הדפס את כל הכפתורים הזמינים
                    buttons = self.page.query_selector_all("button")
                    print(f"📋 נמצאו {len(buttons)} כפתורים:")
                    for i, btn in enumerate(buttons[:10]):  # רק 10 הראשונים
                        try:
                            text = btn.inner_text()[:50] if btn.inner_text() else "ללא טקסט"
                            print(f"  {i+1}. {text}")
                        except:
                            print(f"  {i+1}. לא ניתן לקרוא טקסט")
                    
                    return False
            except Exception as e:
                print(f"❌ שגיאה בלחיצה על פרסם: {e}")
                return False
        except Exception as e:
            print(f"❌ שגיאה כללית: {e}")
            return False
    
    def close(self):
        """סגירת הדפדפן"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

def main():
    import sys
    
    # בדוק ארגומנטים
    if len(sys.argv) > 1 and sys.argv[1] == "--login-only":
        print("🔐 מצב התחברות בלבד...")
        bot = SimpleFacebookBot()
        try:
            # נווט לעמוד התחברות
            bot.page.goto("https://www.facebook.com/login")
            bot.page.wait_for_load_state('networkidle')
            
            print("✅ דפדפן נפתח להתחברות")
            print("אנא התחבר לפייסבוק בדפדפן")
            input("לחץ Enter אחרי שהתחברת...")
            
            # שמור cookies
            cookies = bot.context.cookies()
            
            # צור תיקיית sessions אם לא קיימת
            import os
            os.makedirs("sessions", exist_ok=True)
            
            with open("sessions/facebook-cookie.json", 'w', encoding='utf-8') as f:
                import json
                json.dump(cookies, f, indent=2, ensure_ascii=False)
            
            print("✅ התחברות נשמרה בהצלחה!")
            
        except Exception as e:
            print(f"❌ שגיאה בהתחברות: {e}")
        finally:
            bot.close()
        return
    
    print("🤖 Simple Facebook Bot מתחיל...")
    bot = SimpleFacebookBot()
    
    try:
        # הגדרות
        group_url = "https://www.facebook.com/groups/1229294725669511"
        post_text = "זה פוסט לדוגמה"
        image_path = r"C:\Users\chen elzam\Downloads\בניית לוגו פלא מוטורס (1).png"
        
        # פרסם פוסט
        success = bot.post_to_group(group_url, post_text, image_path)
        
        if success:
            print("\n" + "="*50)
            print("🎉 הפוסט פורסם בהצלחה!")
            print("הדפדפן נשאר פתוח לבדיקה")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("❌ פרסום הפוסט נכשל")
            print("="*50)
        
        input("\nלחץ Enter כדי לסגור...")
        
    except Exception as e:
        print(f"שגיאה: {e}")
    finally:
        if bot:
            bot.close()

if __name__ == "__main__":
    main()
