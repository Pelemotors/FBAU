from playwright.sync_api import sync_playwright
import json
import os
import sys
from datetime import datetime

# תיקון בעיית קידוד UTF-8
if sys.platform == "win32":
    os.system("chcp 65001")
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class SelectorExplorer:
    def __init__(self):
        print("🔍 SelectorExplorer הופעל")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        # רשימת קבצי מדיה לבדיקה
        self.test_files = [
            "C:\\Users\\chen elzam\\Downloads\\556175307_10234337950623471_102273060015623959_n.jpg",
            "C:\\Users\\chen elzam\\Downloads\\ChatGPT Image Sep 24, 2025, 04_04_43 PM.png"
        ]
    
    def load_cookies(self):
        """טעינת cookies"""
        cookie_file = "sessions/facebook-cookie.json"
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
                self.context.add_cookies(cookies)
                print("✅ Cookies נטענו")
                return True
        print("❌ לא נמצאו cookies")
        return False
    
    def explore_group_selectors(self, group_url, group_name):
        """חקור סלקטורים בקבוצה"""
        print(f"\n{'='*60}")
        print(f"🔍 חוקר קבוצה: {group_name}")
        print(f"📍 URL: {group_url}")
        print(f"{'='*60}")
        
        try:
            # טען cookies
            if not self.load_cookies():
                print("❌ לא ניתן לטעון cookies")
                return None
            
            # נכנס לקבוצה
            print(f"📍 נכנס לקבוצה...")
            self.page.goto(group_url)
            self.page.wait_for_load_state('networkidle')
            
            # המתן קצת
            self.page.wait_for_timeout(3000)
            
            selectors_data = {
                "group_name": group_name,
                "group_url": group_url,
                "timestamp": datetime.now().isoformat(),
                "composer_selectors": [],
                "media_selectors": [],
                "publish_selectors": [],
                "text_selectors": []
            }
            
            # 1. חפש סלקטורים לקומפוזר
            print("📝 מחפש סלקטורי קומפוזר...")
            composer_selectors = self.find_composer_selectors()
            selectors_data["composer_selectors"] = composer_selectors
            
            # 2. פתח קומפוזר אם נמצא
            if composer_selectors:
                print("🚀 מנסה לפתוח קומפוזר...")
                if self.try_open_composer(composer_selectors[0]):
                    print("✅ קומפוזר נפתח בהצלחה!")
                    
                    # המתן שהקומפוזר ייפתח
                    self.page.wait_for_timeout(3000)
                    
                    # 3. חפש סלקטורים בתוך הקומפוזר
                    print("🔍 מחפש סלקטורים בקומפוזר...")
                    
                    # סלקטורי טקסט
                    text_selectors = self.find_text_selectors()
                    selectors_data["text_selectors"] = text_selectors
                    
                    # בדוק סלקטורי טקסט
                    if text_selectors:
                        print("\n📝 בודק סלקטורי טקסט...")
                        working_text = self.test_text_selectors(text_selectors)
                        selectors_data["working_text_selectors"] = working_text
                    
                    # סלקטורי מדיה
                    media_selectors = self.find_media_selectors()
                    selectors_data["media_selectors"] = media_selectors
                    
                    # בדוק סלקטורי מדיה
                    if media_selectors:
                        print("\n📷 בודק סלקטורי מדיה...")
                        working_media = self.test_media_selectors(media_selectors)
                        selectors_data["working_media_selectors"] = working_media
                    
                    # סלקטורי פרסום
                    publish_selectors = self.find_publish_selectors()
                    selectors_data["publish_selectors"] = publish_selectors
                    
                    # בדוק סלקטורי פרסום
                    if publish_selectors:
                        print("\n🚀 בודק סלקטורי פרסום...")
                        working_publish = self.test_publish_selectors(publish_selectors)
                        selectors_data["working_publish_selectors"] = working_publish
                    
                    print("✅ סריקה הושלמה!")
                else:
                    print("❌ לא הצליח לפתוח קומפוזר")
            else:
                print("❌ לא נמצאו סלקטורי קומפוזר")
            
            return selectors_data
            
        except Exception as e:
            print(f"❌ שגיאה בחקירת הקבוצה: {e}")
            return None
    
    def find_composer_selectors(self):
        """חפש סלקטורים לקומפוזר"""
        selectors = []
        
        # סלקטור 1: "כאן כותבים…"
        try:
            elements = self.page.query_selector_all("text='כאן כותבים…'")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "text_content",
                        "selector": f"text='כאן כותבים…'",
                        "index": i,
                        "found": True,
                        "description": "כאן כותבים…"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור 'כאן כותבים…': {e}")
        
        # סלקטור 2: "כתוב משהו..."
        try:
            elements = self.page.query_selector_all("text='כתוב משהו...'")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "text_content",
                        "selector": f"text='כתוב משהו...'",
                        "index": i,
                        "found": True,
                        "description": "כתוב משהו..."
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור 'כתוב משהו...': {e}")
        
        # סלקטור 3: textarea עם placeholder
        try:
            elements = self.page.query_selector_all("textarea[placeholder*='כתוב']")
            if elements:
                for i, element in enumerate(elements):
                    placeholder = element.get_attribute("placeholder")
                    selectors.append({
                        "type": "textarea_placeholder",
                        "selector": f"textarea[placeholder*='כתוב']",
                        "index": i,
                        "found": True,
                        "placeholder": placeholder,
                        "description": f"textarea עם placeholder: {placeholder}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור textarea: {e}")
        
        # סלקטור 4: div עם contenteditable
        try:
            elements = self.page.query_selector_all("div[contenteditable='true']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "contenteditable",
                        "selector": f"div[contenteditable='true']",
                        "index": i,
                        "found": True,
                        "description": "div עם contenteditable"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור contenteditable: {e}")
        
        # סלקטור 5: כפתורי פרסום
        try:
            elements = self.page.query_selector_all("[aria-label*='פרסם'], [aria-label*='Create'], [data-testid*='create']")
            if elements:
                for i, element in enumerate(elements):
                    aria_label = element.get_attribute("aria-label")
                    data_testid = element.get_attribute("data-testid")
                    selectors.append({
                        "type": "button",
                        "selector": f"[aria-label*='פרסם'], [aria-label*='Create'], [data-testid*='create']",
                        "index": i,
                        "found": True,
                        "aria_label": aria_label,
                        "data_testid": data_testid,
                        "description": f"כפתור: {aria_label or data_testid}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור כפתורים: {e}")
        
        print(f"📊 נמצאו {len(selectors)} סלקטורי קומפוזר")
        return selectors
    
    def try_open_composer(self, selector_info):
        """נסה לפתוח קומפוזר עם סלקטור נתון"""
        try:
            if selector_info["type"] == "text_content":
                elements = self.page.query_selector_all(selector_info["selector"])
                if elements and selector_info["index"] < len(elements):
                    elements[selector_info["index"]].click()
                    return True
            elif selector_info["type"] == "textarea_placeholder":
                elements = self.page.query_selector_all(selector_info["selector"])
                if elements and selector_info["index"] < len(elements):
                    elements[selector_info["index"]].click()
                    return True
            elif selector_info["type"] == "contenteditable":
                elements = self.page.query_selector_all(selector_info["selector"])
                if elements and selector_info["index"] < len(elements):
                    elements[selector_info["index"]].click()
                    return True
            elif selector_info["type"] == "button":
                elements = self.page.query_selector_all(selector_info["selector"])
                if elements and selector_info["index"] < len(elements):
                    elements[selector_info["index"]].click()
                    return True
        except Exception as e:
            print(f"❌ שגיאה בפתיחת קומפוזר: {e}")
        return False
    
    def find_text_selectors(self):
        """חפש סלקטורים לכתיבת טקסט"""
        selectors = []
        
        # סלקטור 1: div עם contenteditable בתוך dialog
        try:
            elements = self.page.query_selector_all("//div[@role='dialog']//div[@contenteditable='true']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "xpath_contenteditable",
                        "selector": "//div[@role='dialog']//div[@contenteditable='true']",
                        "index": i,
                        "found": True,
                        "description": "div contenteditable בתוך dialog"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור טקסט 1: {e}")
        
        # סלקטור 2: div עם contenteditable כללי
        try:
            elements = self.page.query_selector_all("div[contenteditable='true']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "contenteditable_general",
                        "selector": "div[contenteditable='true']",
                        "index": i,
                        "found": True,
                        "description": "div contenteditable כללי"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור טקסט 2: {e}")
        
        print(f"📝 נמצאו {len(selectors)} סלקטורי טקסט")
        return selectors
    
    def find_media_selectors(self):
        """חפש סלקטורים להעלאת מדיה"""
        selectors = []
        
        # סלקטור 1: "תמונה או סרטון" בעברית - בתוך toolbar
        try:
            elements = self.page.query_selector_all("#toolbarLabel [aria-label='תמונה או סרטון']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "toolbar_aria_label_hebrew",
                        "selector": "#toolbarLabel [aria-label='תמונה או סרטון']",
                        "index": i,
                        "found": True,
                        "description": "תמונה או סרטון בתוך toolbar (עברית)"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה toolbar: {e}")
        
        # סלקטור 2: "תמונה או סרטון" כללי
        try:
            elements = self.page.query_selector_all("[aria-label='תמונה או סרטון']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "aria_label_hebrew",
                        "selector": "[aria-label='תמונה או סרטון']",
                        "index": i,
                        "found": True,
                        "description": "תמונה או סרטון (עברית)"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה 1: {e}")
        
        # סלקטור 3: "Photo/Video" באנגלית
        try:
            elements = self.page.query_selector_all("[aria-label='Photo/Video']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "aria_label_english",
                        "selector": "[aria-label='Photo/Video']",
                        "index": i,
                        "found": True,
                        "description": "Photo/Video (אנגלית)"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה 2: {e}")
        
        # סלקטור 4: input file עם accept ספציפי (לפי המבנה שנתת)
        try:
            elements = self.page.query_selector_all("input[accept*='image'][accept*='video']")
            if elements:
                for i, element in enumerate(elements):
                    accept = element.get_attribute("accept")
                    multiple = element.get_attribute("multiple")
                    selectors.append({
                        "type": "file_input_multiple",
                        "selector": "input[accept*='image'][accept*='video']",
                        "index": i,
                        "found": True,
                        "accept": accept,
                        "multiple": multiple,
                        "description": f"input file עם accept: {accept}, multiple: {multiple}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה 3: {e}")
        
        # סלקטור 5: input file ספציפי בתוך toolbar (לפי המבנה שנתת)
        try:
            elements = self.page.query_selector_all("div.xr9ek0c input[type='file']")
            if elements:
                for i, element in enumerate(elements):
                    accept = element.get_attribute("accept")
                    multiple = element.get_attribute("multiple")
                    selectors.append({
                        "type": "toolbar_file_input",
                        "selector": "div.xr9ek0c input[type='file']",
                        "index": i,
                        "found": True,
                        "accept": accept,
                        "multiple": multiple,
                        "description": f"input file בתוך toolbar: {accept}, multiple: {multiple}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה 4: {e}")
        
        # סלקטור 6: input file עם multiple (לפי המבנה שנתת)
        try:
            elements = self.page.query_selector_all("input[type='file'][multiple]")
            if elements:
                for i, element in enumerate(elements):
                    accept = element.get_attribute("accept")
                    selectors.append({
                        "type": "file_input_multiple_direct",
                        "selector": "input[type='file'][multiple]",
                        "index": i,
                        "found": True,
                        "accept": accept,
                        "description": f"input file עם multiple: {accept}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור מדיה 5: {e}")
        
        print(f"📷 נמצאו {len(selectors)} סלקטורי מדיה")
        return selectors
    
    def find_publish_selectors(self):
        """חפש סלקטורים לפרסום"""
        selectors = []
        
        # סלקטור 1: "פרסם" בעברית
        try:
            elements = self.page.query_selector_all("//div[@role='dialog']//div[@aria-label='פרסם']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "aria_label_hebrew",
                        "selector": "//div[@role='dialog']//div[@aria-label='פרסם']",
                        "index": i,
                        "found": True,
                        "description": "פרסם (עברית)"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 1: {e}")
        
        # סלקטור 2: "Post" באנגלית
        try:
            elements = self.page.query_selector_all("//div[@role='dialog']//div[@aria-label='Post']")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "aria_label_english",
                        "selector": "//div[@role='dialog']//div[@aria-label='Post']",
                        "index": i,
                        "found": True,
                        "description": "Post (אנגלית)"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 2: {e}")
        
        # סלקטור 3: כפתור עם טקסט "פרסם" (לפי המבנה שנתת)
        try:
            elements = self.page.query_selector_all("//button[contains(text(), 'פרסם')]")
            if elements:
                for i, element in enumerate(elements):
                    text = element.text_content()
                    selectors.append({
                        "type": "button_text_hebrew",
                        "selector": "//button[contains(text(), 'פרסם')]",
                        "index": i,
                        "found": True,
                        "text": text,
                        "description": f"כפתור עם טקסט: {text}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 3: {e}")
        
        # סלקטור 4: כפתור פרסום לפי המבנה הספציפי שנתת
        try:
            # חיפוש לפי המבנה המדויק: span עם טקסט "פרסם" בתוך div עם role="button"
            elements = self.page.query_selector_all("span:has-text('פרסם')")
            if elements:
                for i, element in enumerate(elements):
                    # בדוק אם האלמנט נמצא בתוך כפתור
                    parent_button = element.query_selector("xpath=ancestor::div[@role='button']")
                    if parent_button:
                        selectors.append({
                            "type": "publish_button_structure",
                            "selector": "span:has-text('פרסם')",
                            "index": i,
                            "found": True,
                            "text": element.text_content(),
                            "description": "כפתור פרסום לפי מבנה ספציפי"
                        })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 4: {e}")
        
        # סלקטור 5: חיפוש לפי המבנה המדויק של div עם role="button"
        try:
            elements = self.page.query_selector_all("div[role='button']:has(span:has-text('פרסם'))")
            if elements:
                for i, element in enumerate(elements):
                    selectors.append({
                        "type": "publish_button_role",
                        "selector": "div[role='button']:has(span:has-text('פרסם'))",
                        "index": i,
                        "found": True,
                        "description": "div עם role=button המכיל 'פרסם'"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 5: {e}")
        
        # סלקטור 4: כפתור עם טקסט "Post"
        try:
            elements = self.page.query_selector_all("//button[contains(text(), 'Post')]")
            if elements:
                for i, element in enumerate(elements):
                    text = element.text_content()
                    selectors.append({
                        "type": "button_text_english",
                        "selector": "//button[contains(text(), 'Post')]",
                        "index": i,
                        "found": True,
                        "text": text,
                        "description": f"כפתור עם טקסט: {text}"
                    })
        except Exception as e:
            print(f"⚠️ שגיאה בסלקטור פרסום 4: {e}")
        
        print(f"🚀 נמצאו {len(selectors)} סלקטורי פרסום")
        return selectors
    
    def test_text_selectors(self, selectors):
        """בדוק סלקטורי טקסט"""
        working_selectors = []
        
        for selector in selectors:
            print(f"\n📝 בודק: {selector['description']}")
            print(f"   סלקטור: {selector['selector']}")
            
            try:
                # נסה למצוא את האלמנט
                if selector['type'] == 'xpath_contenteditable':
                    element = self.page.query_selector(f"xpath={selector['selector']}")
                else:
                    element = self.page.query_selector(selector['selector'])
                
                if element:
                    # נסה ללחוץ עליו
                    element.click()
                    self.page.wait_for_timeout(1000)
                    
                    # נסה לכתוב טקסט
                    test_text = "טקסט בדיקה"
                    element.fill(test_text)
                    self.page.wait_for_timeout(1000)
                    
                    # שאל את המשתמש
                    response = input(f"   ✅ האם הסלקטור עבד? (Y/N/S): ").strip().upper()
                    
                    if response == 'Y':
                        selector['working'] = True
                        working_selectors.append(selector)
                        print("   ✅ סלקטור עובד!")
                    elif response == 'N':
                        selector['working'] = False
                        print("   ❌ סלקטור לא עובד")
                    elif response == 'S':
                        print("   ⏭️ דילגת על הסלקטור")
                    else:
                        print("   ⚠️ תשובה לא מובנת, דילגתי")
                    
                    # נקה את הטקסט
                    try:
                        element.clear()
                    except:
                        pass
                else:
                    print("   ❌ לא נמצא האלמנט")
                    selector['working'] = False
                    
            except Exception as e:
                print(f"   ❌ שגיאה: {e}")
                selector['working'] = False
        
        return working_selectors
    
    def test_media_selectors(self, selectors):
        """בדוק סלקטורי מדיה"""
        working_selectors = []
        
        for selector in selectors:
            print(f"\n📷 בודק: {selector['description']}")
            print(f"   סלקטור: {selector['selector']}")
            
            try:
                # נסה למצוא את האלמנט
                if selector['type'] == 'toolbar_aria_label_hebrew':
                    element = self.page.query_selector(selector['selector'])
                elif selector['type'] == 'aria_label_hebrew':
                    element = self.page.query_selector(selector['selector'])
                elif selector['type'] == 'aria_label_english':
                    element = self.page.query_selector(selector['selector'])
                elif selector['type'] == 'file_input_multiple':
                    element = self.page.query_selector(selector['selector'])
                else:
                    element = self.page.query_selector(selector['selector'])
                
                if element:
                    # נסה ללחוץ עליו
                    if selector['type'] == 'file_input_multiple':
                        # עבור input file, רק בדוק אם הוא קיים
                        print("   📁 נמצא input file עם multiple")
                        response = input(f"   ✅ האם הסלקטור עובד? (Y/N/S): ").strip().upper()
                    else:
                        # עבור כפתורים אחרים, נסה ללחוץ ולהעלות קובץ
                        try:
                            print("   🖱️ לוחץ על כפתור...")
                            with self.page.expect_file_chooser(timeout=5000) as file_chooser_info:
                                element.click()
                            file_chooser = file_chooser_info.value
                            print("   📁 FileChooser נפתח!")
                            
                            # נסה להעלות קובץ אמיתי
                            test_file = None
                            for file_path in self.test_files:
                                if os.path.exists(file_path):
                                    test_file = file_path
                                    break
                            
                            if test_file:
                                print(f"   📷 מעלה קובץ: {os.path.basename(test_file)}")
                                file_chooser.set_files([test_file])
                                self.page.wait_for_timeout(2000)
                                print("   ✅ קובץ הועלה!")
                                
                                # שאל את המשתמש אם זה עבד
                                response = input(f"   ✅ האם הקובץ הועלה בהצלחה? (Y/N/S): ").strip().upper()
                                
                                if response == 'Y':
                                    print("   ✅ הקובץ הועלה בהצלחה - משאיר אותו!")
                            else:
                                print("   ⚠️ לא נמצא קובץ לבדיקה")
                                file_chooser.cancel()
                                response = input(f"   ✅ האם הסלקטור עבד? (Y/N/S): ").strip().upper()
                                
                        except Exception as e:
                            print(f"   ❌ FileChooser לא נפתח: {e}")
                            response = input(f"   ❌ האם הסלקטור עבד? (Y/N/S): ").strip().upper()
                    
                    if response == 'Y':
                        selector['working'] = True
                        working_selectors.append(selector)
                        print("   ✅ סלקטור עובד!")
                    elif response == 'N':
                        selector['working'] = False
                        print("   ❌ סלקטור לא עובד")
                    elif response == 'S':
                        print("   ⏭️ דילגת על הסלקטור")
                    else:
                        print("   ⚠️ תשובה לא מובנת, דילגתי")
                else:
                    print("   ❌ לא נמצא האלמנט")
                    selector['working'] = False
                    
            except Exception as e:
                print(f"   ❌ שגיאה: {e}")
                selector['working'] = False
        
        return working_selectors
    
    def test_publish_selectors(self, selectors):
        """בדוק סלקטורי פרסום"""
        print(f"\n🚀 בודק {len(selectors)} סלקטורי פרסום...")
        print("⚠️ חשוב: כפתור הפרסום מופיע רק לאחר כתיבת טקסט או העלאת מדיה!")
        print("💡 אם לא רואה כפתור פרסום, זה תקין - צריך לכתוב טקסט או להעלות מדיה קודם")
        
        working_selectors = []
        
        for selector in selectors:
            print(f"\n🚀 בודק: {selector['description']}")
            print(f"   סלקטור: {selector['selector']}")
            
            try:
                # נסה למצוא את האלמנט
                if selector['type'] == 'aria_label_hebrew':
                    element = self.page.query_selector(f"xpath={selector['selector']}")
                elif selector['type'] == 'aria_label_english':
                    element = self.page.query_selector(f"xpath={selector['selector']}")
                elif selector['type'] == 'button_text_hebrew':
                    element = self.page.query_selector(f"xpath={selector['selector']}")
                elif selector['type'] == 'button_text_english':
                    element = self.page.query_selector(f"xpath={selector['selector']}")
                elif selector['type'] == 'publish_button_structure':
                    element = self.page.query_selector(selector['selector'])
                elif selector['type'] == 'publish_button_role':
                    element = self.page.query_selector(selector['selector'])
                else:
                    element = self.page.query_selector(selector['selector'])
                
                if element:
                    # בדוק אם הכפתור זמין
                    is_enabled = element.is_enabled()
                    is_visible = element.is_visible()
                    
                    print(f"   👁️ נראה: {is_visible}, 🟢 זמין: {is_enabled}")
                    
                    if is_visible and is_enabled:
                        response = input(f"   ✅ האם הסלקטור עובד? (Y/N/S): ").strip().upper()
                        
                        if response == 'Y':
                            selector['working'] = True
                            working_selectors.append(selector)
                            print("   ✅ סלקטור עובד!")
                        elif response == 'N':
                            selector['working'] = False
                            print("   ❌ סלקטור לא עובד")
                        elif response == 'S':
                            print("   ⏭️ דילגת על הסלקטור")
                        else:
                            print("   ⚠️ תשובה לא מובנת, דילגתי")
                    else:
                        print("   ❌ כפתור לא זמין או לא נראה")
                        selector['working'] = False
                else:
                    print("   ❌ לא נמצא האלמנט")
                    selector['working'] = False
                    
            except Exception as e:
                print(f"   ❌ שגיאה: {e}")
                selector['working'] = False
        
        return working_selectors
    
    def test_full_posting_process(self, group_url=None, post_text="", media_files=None):
        """תהליך פרסום מלא עם סלקטורים ידועים"""
        print("\n🚀 מתחיל תהליך פרסום מלא...")
        
        # אם לא נשלח טקסט, לא נכתוב טקסט
        if post_text:
            print(f"📝 טקסט לפוסט: {post_text}")
        else:
            print("📝 ללא טקסט (רק מדיה)")
            
        # אם יש קבצי מדיה
        if media_files:
            print(f"📁 {len(media_files)} קבצי מדיה")
        else:
            print("📁 ללא מדיה")
        
        try:
            # 0. נכנס לקבוצה (אם ניתנה URL)
            if group_url:
                print(f"\n0️⃣ נכנס לקבוצה: {group_url}")
                try:
                    # טעינת cookies
                    print("🍪 בודק cookies...")
                    if not self.load_cookies():
                        print("❌ לא הצלחתי לטעון cookies")
                        return False
                    print("✅ Cookies נטענו בהצלחה")
                    
                    # כניסה לקבוצה
                    print("🌐 נכנס לקבוצה...")
                    self.page.goto(group_url)
                    print("⏳ ממתין לטעינת הדף...")
                    self.page.wait_for_load_state('networkidle')
                    print("✅ נכנסתי לקבוצה!")
                    print("⏳ ממתין 2 שניות...")
                    self.page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"❌ שגיאה בכניסה לקבוצה: {e}")
                    return False
            
            # 1. פתח קומפוזר (סלקטור ידוע)
            print("\n1️⃣ פותח קומפוזר...")
            try:
                print("🔍 מחפש כפתור קומפוזר...")
                composer_button = self.page.wait_for_selector("text='כאן כותבים…'", timeout=10000)
                if composer_button:
                    print("🖱️ לוחץ על כפתור קומפוזר...")
                    composer_button.click()
                    print("✅ קומפוזר נפתח!")
                    print("⏳ ממתין 3 שניות לקומפוזר להיפתח...")
                    self.page.wait_for_timeout(3000)
                else:
                    print("❌ לא מצאתי כפתור קומפוזר - ייתכן שהקבוצה מגבילה פרסום")
                    return False
            except Exception as e:
                print(f"❌ שגיאה בפתיחת קומפוזר: {e}")
                return False
            
            # 2. כתוב טקסט בדיקה (סלקטור ידוע)
            # כתוב טקסט רק אם יש טקסט
            if post_text:
                print("\n2️⃣ כותב טקסט...")
                try:
                    print("🔍 מחפש שדה טקסט...")
                    text_field = self.page.wait_for_selector("//div[@role='dialog']//div[@contenteditable='true']", timeout=10000)
                    if text_field:
                        print("🖱️ לוחץ על שדה הטקסט...")
                        text_field.click()
                        print("✍️ כותב טקסט...")
                        text_field.fill(post_text)
                        print("✅ טקסט נכתב!")
                        print("⏳ ממתין 2 שניות...")
                        self.page.wait_for_timeout(2000)
                    else:
                        print("❌ לא מצאתי שדה טקסט - ייתכן שהקומפוזר לא נפתח")
                        return False
                except Exception as e:
                    print(f"❌ שגיאה בכתיבת טקסט: {e}")
                    return False
            else:
                print("\n2️⃣ מדלג על כתיבת טקסט (ללא טקסט)")
            
            # 3. העלה מדיה (אם יש)
            if media_files:
                print("\n3️⃣ מעלה מדיה...")
                uploaded_count = 0
                
                for i, media_file in enumerate(media_files):
                    media_path = media_file['path']
                    print(f"📎 מעלה קובץ {i+1}/{len(media_files)}: {os.path.basename(media_path)}")
                    print(f"   📍 נתיב מלא: {media_path}")
                    print(f"   📏 גודל קובץ: {os.path.getsize(media_path) if os.path.exists(media_path) else 'לא קיים'} bytes")
                    
                    if os.path.exists(media_path):
                        try:
                            print(f"🔍 מחפש כפתור מדיה עבור קובץ {i+1}...")
                            media_button = self.page.wait_for_selector("[aria-label='תמונה או סרטון']", timeout=5000)
                            if media_button:
                                print(f"✅ מצאתי כפתור מדיה")
                                print(f"🖱️ לוחץ על כפתור מדיה...")
                                with self.page.expect_file_chooser(timeout=10000) as file_chooser_info:
                                    media_button.click()
                                file_chooser = file_chooser_info.value
                                print(f"📁 FileChooser נפתח")
                                
                                print(f"📤 מעלה קובץ...")
                                file_chooser.set_files(media_path)
                                print(f"✅ העלה קובץ: {os.path.basename(media_path)}")
                                uploaded_count += 1
                                
                                # המתן שהקובץ יועלה
                                print(f"⏳ ממתין 3 שניות להעלאה...")
                                self.page.wait_for_timeout(3000)
                                
                                # בדוק שהקובץ הועלה
                                try:
                                    print(f"🔍 בודק אם הקובץ הועלה...")
                                    self.page.wait_for_selector("img[src*='blob:']", timeout=2000)
                                    print(f"✅ אישור: קובץ {os.path.basename(media_path)} הועלה בהצלחה")
                                except:
                                    print(f"⚠️ לא ניתן לאשר העלאת קובץ {os.path.basename(media_path)}")
                            else:
                                print(f"❌ לא מצאתי כפתור מדיה - ייתכן שהקומפוזר לא נפתח")
                        except Exception as e:
                            print(f"❌ שגיאה בהעלאת קובץ {os.path.basename(media_path)}: {e}")
                    else:
                        print(f"⚠️ קובץ לא קיים: {media_path}")
                
                print(f"📊 סה״כ הועלו {uploaded_count} מתוך {len(media_files)} קבצים")
               
                # בדוק אם יש מגבלה על מספר קבצים
                if uploaded_count < len(media_files):
                    print(f"⚠️ רק {uploaded_count} מתוך {len(media_files)} קבצים הועלו - ייתכן שיש מגבלה")
                    print("💡 פייסבוק עלול להגביל מספר קבצים בפוסט אחד")
            else:
                print("\n3️⃣ מדלג על העלאת מדיה (ללא מדיה)")
            
            # 4. לחץ על פרסום
            print("\n4️⃣ מחפש כפתור פרסום...")
            try:
                # המתן קצת כדי שכפתור הפרסום יופיע
                self.page.wait_for_timeout(3000)
                
                # נסה סלקטורים שונים לכפתור פרסום (הסלקטור שעובד מ-simple_facebook_bot)
                publish_selectors = [
                    "xpath=//div[@role='dialog']//div[@aria-label='פרסם']",
                    "span:has-text('פרסם')",
                    "div[role='button']:has(span:has-text('פרסם'))",
                    "[data-testid='post-button']",
                    "button:has-text('פרסם')",
                    "div:has-text('פרסם')"
                ]
                
                print(f"🔍 מנסה {len(publish_selectors)} סלקטורים שונים לכפתור פרסום...")
                publish_button = None
                for i, selector in enumerate(publish_selectors):
                    try:
                        print(f"   {i+1}. בודק סלקטור: {selector}")
                        publish_button = self.page.wait_for_selector(selector, timeout=3000)
                        if publish_button and publish_button.is_visible():
                            print(f"✅ מצאתי כפתור פרסום עם סלקטור: {selector}")
                            break
                        else:
                            print(f"   ❌ לא נמצא או לא נראה עם סלקטור זה")
                    except Exception as e:
                        print(f"   ❌ שגיאה עם סלקטור זה: {e}")
                        continue
                
                if publish_button:
                    print("🖱️ לוחץ על כפתור פרסום...")
                    publish_button.click()
                    print("✅ לחצתי על פרסום!")
                    
                    # המתן שהפוסט יתפרסם
                    print("⏳ ממתין 5 שניות לפרסום...")
                    self.page.wait_for_timeout(5000)
                    print("🎉 תהליך הפרסום הושלם!")
                    return True
                else:
                    print("❌ לא מצאתי כפתור פרסום פעיל")
                    print("💡 ייתכן שהקבוצה דורשת אישור מנהל לפני פרסום")
                    # הדפס את כל הכפתורים הזמינים
                    buttons = self.page.query_selector_all("button, div[role='button']")
                    print(f"🔍 נמצאו {len(buttons)} כפתורים בדף")
                    return False
                    
            except Exception as e:
                print(f"❌ שגיאה בפרסום: {e}")
                return False
                
        except Exception as e:
            print(f"❌ שגיאה כללית בתהליך: {e}")
            return False

    def close(self):
        """סגור את הדפדפן"""
        try:
            self.browser.close()
            self.playwright.stop()
            print("🔒 דפדפן נסגר")
        except:
            pass

def main():
    """פונקציה ראשית - תהליך פרסום מלא"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Facebook Group Posting Bot')
    parser.add_argument('--single-group', help='URL של קבוצה יחידה לפרסום')
    parser.add_argument('--text', help='טקסט לפוסט')
    parser.add_argument('--media', action='append', help='נתיב לקובץ מדיה (ניתן לחזור על הפרמטר)')
    
    args = parser.parse_args()
    
    # אם נשלחו פרמטרים מהדשבורד
    if args.single_group:
        print(f"🚀 מתחיל פרסום לקבוצה: {args.single_group}")
        
        # הכן קבצי מדיה
        media_files = []
        if args.media:
            for media_path in args.media:
                media_files.append({'path': media_path, 'name': os.path.basename(media_path)})
        
        # הפעל פרסום
        explorer = SelectorExplorer()
        try:
            success = explorer.test_full_posting_process(
                group_url=args.single_group,
                post_text=args.text or "",
                media_files=media_files
            )
            
            if success:
                print("✅ פרסום הושלם בהצלחה!")
                sys.exit(0)
            else:
                print("❌ פרסום נכשל")
                sys.exit(1)
        finally:
            explorer.close()
        return
    
    # אם לא נשלחו פרמטרים, רץ במצב רגיל
    print("🚀 מתחיל תהליך פרסום מלא בקבוצות פייסבוק...")
    print("📋 הסקריפט ישתמש בסלקטורים הידועים כעובדים:")
    print("   📝 קומפוזר: 'כאן כותבים…'")
    print("   ✍️ טקסט: //div[@role='dialog']//div[@contenteditable='true']")
    print("   📷 מדיה: [aria-label='תמונה או סרטון']")
    print("   🚀 פרסום: span עם טקסט 'פרסם'")
    print("\n📁 הסקריפט יעלה קבצים אמיתיים:")
    print("   🖼️ 556175307_10234337950623471_102273060015623959_n.jpg")
    print("   🖼️ ChatGPT Image Sep 24, 2025, 04_04_43 PM.png")
    print("="*60)
    
    # רשימת קבוצות לפרסום
    groups = [
        ("https://www.facebook.com/groups/persum.israel/", "פרסום ישראל"),
        ("https://www.facebook.com/groups/3347199695494901", "קבוצה 1"),
        ("https://www.facebook.com/groups/1920854911477422", "קבוצה 2"),
        ("https://www.facebook.com/groups/645409222247058", "קבוצה 3")
    ]
    
    explorer = SelectorExplorer()
    
    try:
        for group_url, group_name in groups:
            print(f"\n🚀 מתחיל פרסום ב{group_name}...")
            print(f"📍 URL: {group_url}")
            
            # עבור ישר לתהליך פרסום מלא
            success = explorer.test_full_posting_process(group_url, "", [])
            
            if success:
                print(f"✅ פרסום ב{group_name} הושלם בהצלחה!")
            else:
                print(f"❌ פרסום ב{group_name} נכשל")
            
            # שאל האם להמשיך לקבוצה הבאה
            print(f"\n{'='*60}")
            print("🤔 מה ברצונך לעשות?")
            print("1️⃣ להמשיך לקבוצה הבאה")
            print("2️⃣ לעצור כאן")
            choice = input("\nבחר אפשרות (1/2): ").strip()
            
            if choice == "2":
                print("\n🛑 עוצר כאן...")
                break
            else:
                print("\n➡️ ממשיך לקבוצה הבאה...")
        
    except KeyboardInterrupt:
        print("\n⏹️ התהליך הופסק על ידי המשתמש")
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
    finally:
        explorer.close()
        input("\n🔒 לחץ Enter לסגירה...")

if __name__ == "__main__":
    main()
