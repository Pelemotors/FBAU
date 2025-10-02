חלקי ה־PRD הבאים: 1. 🎯 **רציונל ומטרות** 2. 🛠️ **תיאור פונקציונלי** 3. 📂 **מבנה פרויקט** 4. ⚙️ **טכנולוגיות נדרשות** 5. ⏰ **לוגיקת תזמון והרצה** 6. 🔐 **שיקולי אבטחה והרשאות** 7. 🧪 **שיטת בדיקות** 8. 🗂️ **קבצים ודוגמות ראשוניות**

🎯 חלק 1: רציונל ומטרות – מערכת אוטומטית לפרסום פוסטים לפייסבוק
🎯 המטרה המרכזית:

לפתח מערכת מקומית (Standalone) המאפשרת פרסום פוסטים לפייסבוק בצורה אוטומטית, מתוזמנת וגמישה, עם שליטה מלאה בידי המשתמש – ללא תלות ב־n8n וללא צורך באישורים מיוחדים מ־Meta.

✅ יעדים עיקריים:

פשטות שימוש – ממשק נוח שבו המשתמש יכול:

להזין טקסט ידני או להעלות קובץ.

להפיק פוסט בעזרת AI (Ollama).

לבחור קבוצות/דפים אליהם יפורסם הפוסט.

פרסום אוטומטי כאילו משתמש אנושי – שימוש ב־Puppeteer/Playwright לפתיחת דפדפן כרום:

התחברות עם המשתמש הקיים (באמצעות שם משתמש/סיסמה או cookies).

ניווט לקבוצות ולדפים.

הדבקה ופרסום הפוסט כאילו המשתמש עצמו עשה זאת.

ניהול גמיש של קבוצות יעד:

רשימת קישורים בקובץ CSV / טבלה פנימית.

אפשרות סינון (פוסט אחד רק לקבוצה מסוימת).

סימון הצלחה/כישלון בכל פרסום (log).

תזמון מלא של פוסטים:

פרסום מיידי או עתידי.

תזמון לפי שעה/תאריך.

חזרתיות (לדוגמה: כל יום שני ב־10:00).

בקרה ושקיפות:

הצגת "תצוגה מקדימה" לפני שליחה.

שמירה אוטומטית של טיוטות.

לוג מפורט (מתי נשלח, לאן נשלח, האם הצליח).

🧑‍💻 קהל יעד:

בעלי עסקים קטנים ובינוניים שמנהלים שיווק בפייסבוק.

מוכרי רכבים וסוחרים שרוצים לפרסם בקבוצות קניה/מכירה.

מנהלי קהילות שמעדיפים להפעיל כלי פנימי ולא להיות תלויים בצד שלישי.

משווקים עצמאיים שעובדים עם מספר מותגים/לקוחות.

🚫 למה לא להשתמש ב־API של פייסבוק או n8n?

API מוגבל – לא מאפשר פרסום בקבוצות (רק בדפים עסקיים/מודעות ממומנות).

סיבוכי הרשאות – נדרשים טוקנים, אישורים מאת Meta, ועמידה בתנאי פיתוח נוקשים.

n8n לא פותר את הבעיה – אין לו שליטה אמיתית על דפדפן/התחברות; בסוף עדיין נתקעים.

הפתרון שלנו – פועל כמו משתמש אנושי, ולכן עוקף מגבלות בצורה חוקית ומעשית.

🌟 היתרון המרכזי:

הכל מתבצע מקומית (ללא תלות בענן או צד ג').

שליטה מלאה בתוכן, בזמן ובקבוצות.

אוטומציה חכמה שחוסכת שעות עבודה.

מעולה — מציג כאן את **סעיף 2 במלואו** (פונקציונליות ותיאור מסכים), כולל ההשלמות לחיבור פייסבוק.
(לאחר אישורך נעבור לחלק 3: מבנה פרויקט).

---

# 🛠️ חלק 2: פונקציונליות ותיאור מסכים

## 2.1 סקירה תפעולית (מה המערכת עושה)

* יצירת פוסטים: ידני או בעזרת AI (Ollama).
* בחירת קבוצות יעד (קישורי קבוצות/דפים) לכל פוסט.
* תצוגה מקדימה ועריכה לפני שליחה.
* פרסום מיידי או מתוזמן (חד־פעמי/חוזר).
* ניהול סשן פייסבוק (Login/יבוא Cookies/בדיקת חיבור/ניתוק).
* מעקב מצב (לוג: הצלחות/כשלים/סיבות).
* ייבוא/ייצוא CSV לקבוצות.
* שמירת טיוטות.

---

## 2.2 מסכי מערכת (UI)

### 2.2.1 דשבורד (Dashboard)

**מטרה:** תמונת מצב + ניווט מהיר.

* אזורים:

  * כותרת עליונה: ניווט → “יצירת פוסט”, “ניהול קבוצות”, “תזמונים”, “לוג פרסומים”, “הגדרות”.
  * כרטיס “סטטוס פייסבוק”:

    * 🟢 מחובר | 🟡 דורש אימות | 🔴 לא מחובר
    * כפתורים: “התחבר/נהל חיבור”, “בדיקת חיבור”.
  * קיצורי דרך: “פוסט AI מהיר”, “פוסט ידני מהיר”.
  * תקציר אחרונים: 3 תזמונים קרובים, 5 לוגים אחרונים.
* פעולות:

  * מעבר מהיר ליצירת פוסט.
  * בדיקת חיבור לפייסבוק בלחיצה.

**ולידציות/הערות:**

* אם לא מחובר → הצגת קריאה לפעולה בולטת “התחבר כדי לפרסם”.
* RTL מלא; רספונסיבי.

---

### 2.2.2 יצירת פוסט חדש

**מצבי עבודה:**

1. ✨ **פוסט AI**

   * שדות:

     * Prompt (ברירת מחדל הניתנת לעריכה).
     * “צור טיוטה מ־AI” → ממלא עורך הטקסט.
   * תצוגה מקדימה: לפני שמירה/שליחה.
2. ✍️ **פוסט ידני**

   * שדות:

     * כותרת (אופציונלי).
     * גוף הפוסט (טקסט עשיר).
     * טעינת קובץ `.txt` (אופציונלי, ממלא את גוף הפוסט).
   * תצוגה מקדימה.

**שדות משותפים:**

* קבוצות יעד: רשימת צ’קבוקסים מסננת/מחפשת + “בחר הכול”.
* מדיה: העלאת תמונה/וידאו (אופציונלי).
* כפתורים: “שמור כטיוטה”, “פרסם עכשיו”, “תזמן פרסום”.

**ולידציות:**

* חובה: גוף הפוסט לא ריק.
* לפחות קבוצה אחת לפרסום מיידי/מתוזמן.
* אזהרה אם לא מחובר לפייסבוק בעת שליחה.

**הערות UX:**

* אזהרת כפילות: אם טקסט זהה פורסם ב־24 שעות האחרונות לאותה קבוצה → התראה “למחזר/לערוך?”.

---

### 2.2.3 ניהול קבוצות

**מטרה:** מאגר קבוצות/דפים לפרסום.

* טבלה:

  * עמודות: שם, URL, סטטוס אחרון (הצליח/נכשל/לא נבדק), תאריך עדכון אחרון, פעולות.
* פעולות:

  * “הוסף קבוצה” (שם+URL עם ולידציה).
  * “ייבוא CSV” / “ייצוא CSV”.
  * חיפוש/סינון.
  * מחיקה/עריכה.
  * “בדיקה לקבוצה” (מנסה לפתוח ולמצוא אזור כתיבה).

**ולידציות:**

* URL חייב להכיל facebook.com/… (קבוצות או דפים).
* שם נדרש (לזיהוי פנימי).

---

### 2.2.4 תזמון פרסומים

**מטרה:** ניהול תורים של פרסומים עתידיים.

* טבלה:

  * תאריך/שעה, סוג (AI/ידני), תקציר טקסט, קבוצות יעד (#), חזרתיות (ללא/יומי/שבועי/מותאם), סטטוס (ממתין/נשלח/נכשל), פעולות.
* פעולות:

  * “תזמן חדש” (גם מתוך יצירת פוסט).
  * עריכה/ביטול/שכפול תזמון.
  * הפעלת חזרתיות (CRON פשוט: יומי/שבועי/מותאם).

**הגדרות תזמון:**

* אזור זמן: Asia/Jerusalem (ברירת מחדל).
* Backoff במקרה Rate-limit (ראה 2.5.3).

---

### 2.2.5 לוג פרסומים

**מטרה:** שקיפות מלאה.

* טבלה כרונולוגית:

  * תאריך/שעה בפועל, קבוצה, תקציר טקסט, תוצאה (✔/❌), סיבת כשל (אם יש), קישור לפוסט (אם ניתן לחילוץ).
* פעולות:

  * סינון לפי טווח תאריכים/קבוצה/תוצאה.
  * ייצוא CSV.

---

### 2.2.6 חיבור לפייסבוק (Auth & Session)

**ניווט:** דשבורד → הגדרות → חיבורי רשתות → פייסבוק

**אלמנטים:**

* סטטוס: 🟢/🟡/🔴 + “עודכן לאחרונה: …”
* כפתורים:

  1. **התחבר דרך דפדפן** (Chromium גלוי עם `userDataDir` קבוע).
  2. **סיימתי התחברות** (שומר cookies+LS מוצפן).
  3. **ייבוא Cookies** (JSON EditThisCookie/Netscape).
  4. **ייצוא/גיבוי Session** (לקובץ מוצפן).
  5. **בדיקת חיבור** (טעינת FB וקבוצת בדיקה).
  6. **ניתוק וניקוי סשן** (מחיקת session.enc + אופציה למחיקת פרופיל דפדפן).

**הודעות מערכת (מיקרו־קופי):**

* “נדרש אימות דו־שלבי. פתחנו דפדפן — אנא השלם קוד.”
* “החיבור לא תקין — נדרש Login מחדש.”
* “Session נשמר/שוחזר בהצלחה.”

---

## 2.3 פלואוים מרכזיים

### 2.3.1 חיבור לפייסבוק — פלואו A (מומלץ)

1. המשתמש לוחץ “התחבר דרך דפדפן”.
2. נפתח Chromium גלוי עם פרופיל קבוע.
3. המשתמש מבצע login ידני (כולל 2FA).
4. חוזר למסך ולוחץ “סיימתי התחברות”.
5. המערכת שומרת cookies/LS מוצפנים, ומעדכנת סטטוס ל־🟢.

### 2.3.2 חיבור לפייסבוק — פלואו B (ייבוא Cookies)

1. המשתמש מייצא cookies מדפדפן כרום (תוסף).
2. “ייבוא Cookies” → בחירת קובץ JSON.
3. המערכת מאמתת/ממירה/שומרת מוצפן → סטטוס 🟢 אם תקין.

### 2.3.3 פרסום מיידי

1. יצירת פוסט (AI/ידני) + בחירת קבוצות.
2. “פרסם עכשיו”.
3. אם לא מחובר → התראה + קיצור למסך חיבור.
4. אם מחובר → פתיחת דפדפן headless, טעינת session, פוסט לכל קבוצה בתור:

   * ניווט, פתיחת Composer, הדבקת טקסט, העלאת מדיה (אם יש), “פרסם”.
   * לוג הצלחה/כשל לכל קבוצה.
5. הצגת תוצאות במסך + לוג.

### 2.3.4 תזמון פרסום

1. יצירת פוסט → “תזמן”.
2. בחירת תאריך/שעה/חזרתיות.
3. בשעה היעודה: ביצוע כמו “פרסום מיידי”.
4. במקרה Rate-limit/Checkpoint:

   * Backoff אוטומטי (ניסיון חוזר עד N פעמים).
   * רישום בלוג + התראה בדשבורד.

---

## 2.4 כללי ולידציה וחוויית משתמש

* **חובת שדות:**

  * גוף הפוסט (מלל).
  * לפחות קבוצה אחת לפרסום/תזמון.
* **אזהרות:**

  * כפילות תוכן (ב־24 שעות לאותה קבוצה).
  * לא מחובר לפייסבוק.
* **העלאות:**

  * מגבלת גודל מדיה (קובץ גדול → אזהרה).
* **RTL ונגישות:**

  * RTL מלא, טבלאות וכניסה במקלדת, ניגודיות תקינה.

---

## 2.5 התמודדות עם מקרי קצה

### 2.5.1 אימות דו־שלבי / Checkpoint

* זיהוי מסך אימות → עצירה בטוחה + פתיחת דפדפן גלוי.
* הצגת הודעה מודרכת להשלמת אימות.
* לאחר השלמה → “סיימתי” כדי לשמור session מעודכן.

### 2.5.2 סשן שפג תוקף

* ניסיון טעינה נכשל → הודעת “התחבר מחדש”.
* קיצור דרך לפתיחת דפדפן Login.

### 2.5.3 Rate-limit / הגבלות זמניות

* Backoff הדרגתי (למשל 2 דק’, 5 דק’, 10 דק’), עד N ניסיונות.
* סימון בלוג + סטטוס “נכשל” אם אזל הניסיון.

### 2.5.4 שינויים ב־UI של פייסבוק

* סלקטורים עמידים/איתור לפי טקסט/aria.
* אם לא נמצא Composer → ניסיון חלופי (Classic composer / מודל חדש).
* דיווח שגיאה מפורט בלוג (לניתוח ותיקון).

---

## 2.6 מיקרו־קופי (דוגמאות)

* כפתורים:

  * “צור טיוטה מ־AI”
  * “תצוגה מקדימה”
  * “שמור כטיוטה”
  * “פרסם עכשיו”
  * “תזמן פרסום”
  * “ייבוא CSV קבוצות”
  * “בדיקת חיבור”
  * “התחבר דרך דפדפן”
  * “סיימתי התחברות”
* התראות:

  * “הפוסט נשלח לקבוצה: {שם}”
  * “נכשל פרסום לקבוצה: {שם} — סיבה: {תקציר}”
  * “נדרש אימות דו־שלבי”
  * “החיבור תקין”

---

## 2.7 קריטריוני קבלה (Acceptance Criteria) עיקריים

* ניתן ליצור פוסט AI ולערוך אותו לפני שליחה.
* ניתן ליצור פוסט ידני/מ־TXT.
* ניתן לבחור קבוצות ולפרסם מיידית/לתזמן.
* סטטוס פייסבוק מוצג נכון; התחברות נשמרת בין ריצות.
* לכל קבוצה נרשמת תוצאה בלוג עם תאריך/שעה + תקציר סיבה בכישלון.
* ייבוא/ייצוא CSV לקבוצות עובד.
* זיהוי ואזהרת כפילות תוכן (לא חובה לחסום, רק להתריע).

---

מצוין ✅
עובר ל־**חלק 3: מבנה פרויקט (ארכיטקטורה, שכבות, ותיקיות)**.
(אציג כאן את כל המבנה המוצע + רכיבים, בלי קוד. לאחר אישורך נתקדם לחלק 4: טכנולוגיות נדרשות.)

---

# 📂 חלק 3: מבנה פרויקט (ארכיטקטורה ותיקיות)

## 3.1 ארכיטקטורה לוגית – סקירה מהירה

* **client/** – דאשבורד ריאקט לניהול פוסטים/קבוצות/תזמונים ולוגים.
* **server/** – API מקומי (Node.js + Express) שמנהל:

  * חיבור/סשן פייסבוק (Playwright/Puppeteer).
  * פרסום פוסטים (מיידי/מתוזמן) + לוגים.
  * יצירת פוסטים מ־AI (Ollama).
* **worker/** – רץ מתוזמן (node-cron) שמוציא לפועל תורים/תזמונים.
* **shared/** – טיפוסים/DTOs/קבועים משותפים ל־client+server.
* **data/** – מסד נתונים מקומי (SQLite) + מיגרציות (דרך Prisma).
* **.env** – קובץ משתני סביבה (עם placeholders) – יגיע בחלק 6.

> בחירה מודעת: **SQLite (לוקאלי)** לפשטות. ניתן להחליף ל־PostgreSQL בהמשך ללא שינוי לוגיקה (Prisma).

---

## 3.2 תרשים זרימה (טקסטואלי)

1. משתמש יוצר פוסט (AI/ידני) בדאשבורד → **client** שולח ל־**server** `/posts`.
2. המשתמש בוחר “פרסם עכשיו” או “תזמן”:

   * “פרסם עכשיו”: **server** מפעיל **publisherService** (פותח דפדפן עם session) → מפרסם לקבוצות → כותב **log**.
   * “תזמן”: **server** מוסיף רשומת **schedule** במסד; **worker** ירים אותן בזמן.
3. חיבור לפייסבוק:

   * **client** מפעיל `/auth/facebook/login/start` → נפתח דפדפן גלוי.
   * לאחר login ידני, **client** לוחץ “סיימתי” → `/auth/facebook/login/finish` שומר סשן מוצפן.
4. כל סטטוסים/לוגים נגישים במסכי הדאשבורד.

---

## 3.3 מבנה תיקיות מפורט

```
facebook-automation/
├─ client/                      # אפליקציית React (Vite) - RTL, Tailwind, shadcn
│  ├─ src/
│  │  ├─ pages/                # Dashboard, Posts, Groups, Schedules, Logs, Settings
│  │  ├─ components/           # UI components
│  │  ├─ hooks/                # useApi, useForm וכו'
│  │  ├─ lib/                  # api client, validators
│  │  ├─ store/                # Zustand/Context לניהול סטייט
│  │  ├─ routes.tsx
│  │  └─ main.tsx
│  └─ index.html
│
├─ server/                      # API מקומי + Playwright/Puppeteer
│  ├─ src/
│  │  ├─ app.ts                # אתחול Express, ראוטרים, אמצעי אבטחה
│  │  ├─ routes/
│  │  │  ├─ auth.routes.ts     # /auth/facebook/*
│  │  │  ├─ posts.routes.ts    # CRUD פוסטים, /publish-now
│  │  │  ├─ groups.routes.ts   # CRUD קבוצות (CSV import/export)
│  │  │  ├─ schedules.routes.ts# CRUD תזמונים
│  │  │  └─ logs.routes.ts     # קריאת לוגים
│  │  ├─ controllers/          # המרת בקשות → קריאות שירות
│  │  ├─ services/
│  │  │  ├─ sessionService.ts  # שמירת/שחזור session מוצפן (Keytar/ENV)
│  │  │  ├─ browserService.ts  # אתחול Playwright/Puppeteer + userDataDir
│  │  │  ├─ publisherService.ts# לוגיקת פרסום (ניווט, הדבקה, העלאת מדיה)
│  │  │  ├─ groupsService.ts   # ניהול קבוצות + בדיקות reachability
│  │  │  ├─ postsService.ts    # שמירת פוסטים/טיוטות/ולידציות כפילות
│  │  │  ├─ schedulesService.ts# שמירת תזמונים + אינטראקציה עם worker
│  │  │  └─ logsService.ts     # כתיבת/שליפת לוגים
│  │  ├─ integrations/
│  │  │  └─ ollamaClient.ts    # קריאה ל-Ollama (http://127.0.0.1:11434)
│  │  ├─ prisma/               # Prisma Client
│  │  │  └─ client.ts
│  │  ├─ utils/
│  │  │  ├─ crypto.ts          # הצפנה AES-256-GCM לקובצי session
│  │  │  ├─ selectors.ts       # סלקטורים/איתור קומפוזר בפייסבוק (גרסאות UI)
│  │  │  └─ backoff.ts         # ניהול ניסיונות חוזרים
│  │  └─ server.ts             # הפעלת השרת (PORT)
│  └─ package.json
│
├─ worker/                      # מתזמן ותורים
│  ├─ src/
│  │  ├─ index.ts              # node-cron: טעינת תזמונים מה-DB, הרצה בזמן
│  │  └─ jobRunner.ts          # מפעיל publisherService מול קבוצות + כתיבת לוג
│  └─ package.json
│
├─ shared/                      # טיפוסים וקבועים משותפים
│  ├─ src/
│  │  ├─ types.ts              # DTOs: Post, Group, Schedule, Log, AuthStatus
│  │  └─ constants.ts          # קבועים (e.g. MAX_MEDIA_MB, default prompt)
│  └─ package.json
│
├─ data/
│  ├─ prisma/
│  │  ├─ schema.prisma         # מודל DB (SQLite כברירת מחדל)
│  │  └─ migrations/           # יווצר אוטומטית ע"י Prisma
│  └─ storage/                 # session.enc, CSV imports/exports, media temp
│
├─ .env                         # יגיע בחלק 6 עם placeholders
├─ package.json                 # ניהול monorepo עם workspaces (npm)
└─ README.md
```

> הערה: `publisherService` מנתב לוגיקה של כתיבה לפייסבוק (איתור שדה “כתוב משהו…”, הדבקה, העלאת תמונה/וידאו, ולחיצה על “פרסם”), כולל ניהול מקרים מיוחדים (Composer חדש/ישן, מודל קופץ, הרשאות קבוצה).

---

## 3.4 מודל נתונים (Prisma – תיאור לוגי)

טבלאות מרכזיות (תיאור, לא הסכמה בפועל):

* **Post**

  * `id`, `title?`, `body`, `is_ai_generated`, `media_paths[]?`, `created_at`, `updated_at`
* **Group**

  * `id`, `name`, `url`, `last_status?` (success/failed/unknown), `last_checked_at?`
* **Schedule**

  * `id`, `post_id`, `groups[]` (רשימת groupIds), `run_at` (datetime),
    `repeat_rule?` (none/daily/weekly/cron), `status` (pending/running/done/failed), `last_run_at?`
* **Log**

  * `id`, `post_id?`, `group_id?`, `event` (publish_attempt/success/fail/auth_issue/etc),
    `message`, `created_at`, `meta_json?` (קישור לפוסט שפורסם, שגיאה, סלקטורים שנבחרו)
* **Connection**

  * `id`, `provider='facebook'`, `status`, `last_verified_at?`, `notes?`

---

## 3.5 שכבות שירות (Responsibilities)

* **sessionService**: שמירת/שחזור cookies/LS מוצפנים (Keytar כברירת מחדל, ENV כ־fallback).
* **browserService**: אתחול Chromium עם `userDataDir`, headless/headful, טעינת סשן.
* **publisherService**:

  * פתיחת URL קבוצת פייסבוק, איתור קומפוזר, הדבקת טקסט, העלאת מדיה, לחיצה על Post.
  * ניהול backoff ו־rate-limits, זיוי Checkpoint/2FA והחזרת קוד שגיאה ייעודי.
* **groupsService**: CRUD קבוצות, אימות URL, בדיקות reachability.
* **postsService**: CRUD פוסטים, בדיקות כפילות, שמירת טיוטות.
* **schedulesService**: CRUD תזמונים, תרגום repeat_rule ל־cron, אינטגרציה מול worker.
* **logsService**: כתיבת אירועים, שליפות עם פילטרים.

---

## 3.6 Workspaces ו־Scripts (npm)

בקובץ `package.json` הראשי (monorepo):

* workspaces: `["client", "server", "worker", "shared"]`
* סקריפטים כלליים:

  * `npm run dev` – מריץ client + server (concurrently) + worker במקביל.
  * `npm run build` – בניית client + קומפילציית TS ב־server/worker.
  * `npm run db:push` – `prisma db push`
  * `npm run db:migrate` – יצירת/הרצת מיגרציות
  * `npm run lint` / `npm run typecheck`

(נכתוב פקודות מדויקות בחלק 4/5 כשנפרט טכנולוגיות ותזמונים.)

---

## 3.7 אבני דרך (לפי מבנה)

1. שלד פרויקט (תיקיות + package.json + workspaces).
2. Prisma + סכימה בסיסית + DB SQLite.
3. שרת Express עם ראוטרי בסיס (בריאות/ברירת מחדל).
4. sessionService + browserService (בדיקת login flow).
5. מסכי client מינימליים: Dashboard, Facebook Connect, Groups.
6. publisherService בסיסי (פרסום טקסט לקבוצת דמו).
7. תזמון בסיסי (worker + node-cron) + לוגים.
8. הרחבות: תמונות/וידאו, CSV Import/Export, חזרתיות מתקדמת.

---

## 3.8 הרחבות עתידיות (לא ב־MVP)

* תמיכה מרובת חשבונות פייסבוק (multi-profile).
* פרופילי פוסטים (תבניות תוכן מוכנות).
* תגובות אוטומטיות לפוסט לאחר X דקות.
* זחילה/וולידציה של הרשאות קבוצה מראש (חיסכון שגיאות).
* תעדוף תורים/Rate Control לפי קבוצה.

---

מעולה. ממשיכים עם **מודלים מקומיים** ומתמקדים בתמיכה טובה בעברית.
להלן **חלק 4: טכנולוגיות נדרשות** (עם פקודות Copy-Paste). בסוף אבקש אישור להמשיך לחלק 5.

---

# ⚙️ חלק 4: טכנולוגיות נדרשות

## 4.1 תשתית כללית

* **Node.js**: גרסת LTS (מומלץ 20.x).
* **TypeScript**: בכל החבילות (server/worker/client/shared).
* **npm workspaces**: מונורפו: `client`, `server`, `worker`, `shared`.
* **OS Keychain**: `keytar` לשמירת מפתח הצפנה/סשן (Windows Credential Manager / macOS Keychain / libsecret בלינוקס).

**פקודות התקנה בסיסיות (שורש המונו־רפו):**

```bash
# יצירת תיקיית פרויקט
mkdir facebook-automation && cd facebook-automation

# קובץ package.json ראשי עם workspaces
npm init -y
npm pkg set "private"=true
npm pkg set "workspaces[]=@client" "workspaces[]=@server" "workspaces[]=@worker" "workspaces[]=@shared"
```

---

## 4.2 Backend (server/)

* **Express** – API מקומי.
* **Playwright** (מומלץ על פני Puppeteer ליציבות) – פתיחת Chromium עם `userDataDir`, headless/גלוי.
* **Prisma + SQLite** – DB מקומי קל.
* **Ollama Client** – HTTP ל־Ollama מקומי (`http://127.0.0.1:11434`).
* **אבטחה/כלים**: `keytar`, `dotenv`, `zod` (ולידציה), `pino`/`winston` (לוגים), `multer` (מדיה), `csv-parse` / `papaparse` (CSV).
* **Utilities**: `node-fetch`/`axios`, `cron-parser` (לקריאת חזרתיות מותאמת), backoff.

**התקנות (בתיקיית server):**

```bash
mkdir -p server && cd server && npm init -y

npm i express zod axios pino multer csv-parse dotenv keytar
npm i -D typescript ts-node @types/express @types/node @types/multer

# דפדפן
npm i -D playwright
npx playwright install chromium

# Prisma + SQLite
npm i prisma @prisma/client
npx prisma init --datasource-provider sqlite

# חבילות עזר
npm i cron-parser
```

---

## 4.3 Worker (worker/)

* **node-cron** או הרצה מתוזמנת ידנית עם cron parser + setInterval.
* ניגש לאותם services של ה־server (או מייצא מודולים משותפים).

**התקנות (בתיקיית worker):**

```bash
cd ../
mkdir -p worker && cd worker && npm init -y

npm i node-cron axios dotenv zod pino
npm i -D typescript ts-node @types/node
```

---

## 4.4 Shared (shared/)

* טיפוסים/DTOs/קבועים משותפים ל־client+server+worker.

**התקנות (בתיקיית shared):**

```bash
cd ../
mkdir -p shared && cd shared && npm init -y

npm i zod
npm i -D typescript @types/node
```

---

## 4.5 Frontend (client/)

* **React + Vite** (RTL), **TailwindCSS**, **shadcn/ui**, **Zustand** או Context.
* **react-hook-form + zod**: טפסים ולידציה.
* עיצוב RTL מלא.

**התקנות (בתיקיית client):**

```bash
cd ../
npm create vite@latest client -- --template react-ts
cd client
npm i zustand axios zod react-hook-form @hookform/resolvers
npm i -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
# (נגדיר tailwind בהמשך בשלב ה-UI)
```

---

## 4.6 Ollama – מודלים מומלצים לעברית (מקומיים)

נריץ על המחשב שלך. דוגמאות שידועות כבעלות תמיכה לא רעה בעברית:

* **aya:8b** – רב־לשוני, תומך עברית בצורה טובה יחסית.
* **qwen2.5:7b-instruct** – רב־לשוני, מפתיע לטובה בעברית.
* **gemma2:9b-instruct** – תמיכה בינונית בעברית, איכות ניסוח טובה.
* (אופציונלי) **llama3.1:8b-instruct** – סביר בעברית, לפעמים פחות יציב בטעמי ניסוח.

> בפועל ננסה 2-3 מודלים ונבחר לפי איכות הפוסטים שלך.

**פקודות Ollama:**

```bash
# בדיקת שרת (ברירת מחדל: 127.0.0.1:11434)
curl http://127.0.0.1:11434/api/tags

# הורדת מודלים
ollama pull aya:8b
ollama pull qwen2.5:7b-instruct
ollama pull gemma2:9b-instruct
# אופציונלי
ollama pull llama3.1:8b-instruct
```

**בדיקת עברית (דוגמה):**

```bash
curl http://127.0.0.1:11434/api/generate -d '{
  "model": "aya:8b",
  "prompt": "כתוב פוסט קצר בעברית לקבוצת פייסבוק של בעלי עסקים קטנים בנושא שימוש ב-AI ליצירת תוכן שיווקי, בסגנון חם ולא מכירתי."
}'
```

תנסה גם עם `qwen2.5:7b-instruct` ו־`gemma2:9b-instruct` ותשווה ניסוח.

---

## 4.7 קונפיגורציות חשובות

* **Playwright**:

  * `BROWSER_ENGINE=chromium`
  * `BROWSER_HEADLESS=true` (דיבוג: `false`)
  * `BROWSER_USER_DATA_DIR=.data/chrome-profile` (פרופיל קבוע)
* **הצפנה**:

  * `keytar` כברירת מחדל; אם אין → `FB_SESSION_KEY_SOURCE=env` (נזהיר).
* **Prisma/SQLite**:

  * קובץ DB מקומי: `data/prisma/dev.db` (ברירת מחדל).
* **לוגים**:

  * `pino`/`winston` עם רוטציות (אם נרצה), רמת `info` כברירת מחדל.

---

## 4.8 סיכומי בחירה

* בחרנו **Playwright** ליציבות בסילקטורים/דפדפן.
* **Ollama** כברירת מחדל — ללא עלויות/תלות חיצונית.
* **Prisma + SQLite** — פשטות למפתחים, מעבר קל ל־PostgreSQL בהמשך.
* **React + Vite + Tailwind + shadcn** — פיתוח UI מהיר, RTL נוח.
* **keytar** – אבטחת הסשן/מפתח הצפנה ברמת מערכת ההפעלה.

---

⏰ חלק 5: לוגיקת תזמון והרצה
5.1 עקרונות תזמון (Scheduling Principles)

אזור זמן: ברירת המחדל היא Asia/Jerusalem. כל תזמון נשמר ונרשם באזור זמן זה.

סוגי תזמון:

חד־פעמי (run_at תאריך־שעה מדויק)

חוזר (CRON / תבניות מובנות: יומי/שבועי)

הפרדת תורים:

תור פרסומים (Posts Queue)

תור בדיקות/תחזוקה (Health/Check Queue)

מניעת הצפות:

Spacing בין קבוצות: דיליי אקראי 10–40 שניות בין כל קבוצה.

Rate Control: מקסימום X קבוצות לדקה (ניתן להגדרה).

5.2 כללי בטיחות פרסום (Safety)

Random Delay בין פרסומים: 10–40 שניות (קונפיגורבילי).

Backoff חכם במקרה מגבלות/חסימה זמנית:

נסיון 1 → המתנה 2 דקות

נסיון 2 → המתנה 5 דקות

נסיון 3 → המתנה 10 דקות

יותר מ־3 כשלונות → סימון “נכשל” ללוג, ולעבור לקבוצה הבאה.

Idempotency: לכל (PostID, GroupID) נשמר “Fingerprint” של ניסיון פרסום כדי לא לפרסם כפול בטעות (חלון 24 שעות).

Window אקראי: היסט/ריכוך התחלה (Jitter) של 0–3 דקות בתחילת “בלוק” פרסום כדי להיראות אנושי.

5.3 זרימת עבודה של ה־Worker

טעינת תזמונים: ה־worker מריץ פולינג כל 30 שניות (ברירת מחדל) ומחפש תורים “Ready”.

בחירת משימות: לפי run_at <= now, סטטוס pending.

לנעול משימה: שינוי סטטוס ל־running עם locked_at + locked_by (שם ה־worker).

הכנה לפרסום:

בדיקת סטטוס החיבור לפייסבוק: אם “לא מחובר” → עצירה מדווחת לוג + מעבר למשימה הבאה.

בדיקת כפילות (לאותה קבוצה ב־24 שעות) → התראה בלוג והמשך רק אם הוגדר “לאשר כפילות”.

הרצה:

לכל Group בתור: לפתוח דפדפן עם session, לנווט, לבצע פרסום, לרשום תוצאה (✔/❌+סיבה), להמתין Random Delay.

סיום:

אם כל הקבוצות הצליחו → done.

אם היו כשלים חלקיים → done_with_errors.

אם הכל נכשל → failed.

חזרתיות:

אם קיימת repeat_rule → חשב next_run_at לפי CRON/תבנית ושחזר סטטוס ל־pending.

כתיבת last_run_at.

5.4 מצבי כשל ותיקון עצמי

Session Expired / Checkpoint: עצירה נקייה למשימה + לוג “נדרש Login”. המשימה מקבלת failed עם קוד סיבה AUTH_REQUIRED.

שינוי UI של פייסבוק: אם לא נמצא ה־Composer לאחר 2 אסטרטגיות חיפוש → failed עם UI_CHANGED.

מדיה גדולה מדי: סימון “נכשל” לקבוצה, המשך לקבוצה הבאה.

ריבוי כישלונות רצופים: אם 3 משימות רצופות נכשלו עקב AUTH_REQUIRED → השבתה זמנית של worker לפרסומים (health mode), הצגת באנר בדשבורד.

5.5 הגדרות תזמון (משתני סביבה)

הוסף ל־.env (תזכורת: תמלא placeholders ידנית בעת הצורך):

# Scheduling / Worker
SCHED_TIMEZONE=Asia/Jerusalem
SCHED_POLL_INTERVAL_MS=30000
SCHED_MAX_PARALLEL_JOBS=1

# Posting Pace
POST_GROUP_SPACING_MIN_MS=10000
POST_GROUP_SPACING_MAX_MS=40000
POST_GROUPS_PER_MINUTE=5

# Retry / Backoff
RETRY_MAX_ATTEMPTS=3
RETRY_DELAYS_MS=120000,300000,600000  # 2m,5m,10m

# Idempotency window (hours)
POST_DUP_WINDOW_HOURS=24

5.6 דוגמאות CRON (לתזמון חוזר)

כל יום ב־09:00: 0 9 * * *

כל שני ורביעי ב־18:30: 30 18 * * 1,3

כל שעה בשתי הדקות הראשונות: 0-2 * * * *

כל יום ראשון בתחילת החודש 10:00: 0 10 1 * 0

טמפלט JSON לתזמון (דוגמה לשליחת API מה־client ל־server):

{
  "postId": "post_123",
  "groupIds": ["grp_001", "grp_002", "grp_003"],
  "type": "recurring",
  "cron": "0 9 * * *",
  "timezone": "Asia/Jerusalem",
  "startAt": "2025-10-03T09:00:00+03:00",
  "maxRuns": null,
  "allowDuplicatesWithinWindow": false
}


חד־פעמי:

{
  "postId": "post_987",
  "groupIds": ["grp_010","grp_011"],
  "type": "one_time",
  "runAt": "2025-10-03T15:45:00+03:00",
  "timezone": "Asia/Jerusalem",
  "allowDuplicatesWithinWindow": false
}

5.7 Endpoints תזמון מוצעים (ב־server)

POST /schedules — יצירה (חד־פעמי/חוזר)

GET /schedules — רשימה עם פילטרים (status/type)

GET /schedules/:id — פרטים

PATCH /schedules/:id — עדכון (שעה/CRON/קבוצות/השהיה)

DELETE /schedules/:id — ביטול

POST /schedules/:id/run-now — הרצה מיידית (עוקף תזמון)

POST /schedules/validate-cron — ולידציה ל־CRON (מחזיר next 5 runs)

5.8 שדות מודל Schedule (תיאור לוגי)

id (uuid)

post_id (fk → Post)

group_ids (string[])

type (one_time | recurring)

לחד־פעמי: run_at (datetime, tz-aware)

לחוזר: cron (string), timezone (string), start_at (datetime), end_at? (datetime), max_runs? (int), runs_count (int)

status (pending | running | done | done_with_errors | failed | paused)

last_run_at? (datetime)

locked_at? (datetime), locked_by? (string)

meta_json? (object) – הגדרות ספציפיות (spacing override, groups per minute וכו’)

5.9 פקודות הרצה (Copy-Paste)

בהמשך נכתוב סקריפטים ב־package.json, לעת־עתה טמפלטים שמיים:

פיתוח (שרת + ווקר):

# טרמינל 1 (server)
cd server
npm run dev   # מפעיל Express + Playwright + Prisma client

# טרמינל 2 (worker)
cd worker
npm run dev   # מפעיל את מתזמן התורים (poll every SCHED_POLL_INTERVAL_MS)


בדיקת זמן ריצה (Asia/Jerusalem):

node -e "console.log(Intl.DateTimeFormat('he-IL',{timeZone:'Asia/Jerusalem',hour:'2-digit',minute:'2-digit'}).format(new Date()))"


בדיקת CRON לקבלת 5 תאריכים הבאים (דמה):

# פסאודו: בהמשך נוסיף endpoint
curl -X POST http://localhost:3001/schedules/validate-cron \
  -H "Content-Type: application/json" \
  -d '{"cron":"0 9 * * *","timezone":"Asia/Jerusalem"}'

5.10 תחזוקה ושגרות בריאות

Health Check פעם בשעה:

בדיקת Login לפייסבוק (headless ping לקבוצה לדוגמה).

בדיקת דיסק פנוי בתיקיות data/storage.

ניקוי לוגים ישנים מ־90 יום (קונפיגורבילי).

שחזור כשלי תזמון “תקועים”:

משימות running מעל 30 דקות → עוברות ל־failed עם סיבת Timeout.

Quiet Hours (אופציונלי): טווח שעות בו לא מפרסמים (למשל 23:00–06:30). פרסומים ש”נופלים” לשעה זו — נדחים אוטומטית לחלון הבא.

5.11 קריטריוני קבלה (תזמון והרצה)

ניתן להגדיר חד־פעמי/חוזר עם CRON תקין, ולקבל next runs בתצוגה.

Worker מושך משימות בזמן, נועל משימה ומחזיר סטטוס סופי.

Spacing אקראי מופעל בין קבוצות, עם שליטה בקונפיג.

Backoff עובד בשלושה שלבים ונרשם בלוג.

אין כפילות פרסום לאותה קבוצה בחלון 24 שעות (ברירת מחדל).

כשלי AUTH משביתים זמנית את ה־worker ומציגים התראה בדשבורד.
מעולה — מעדכן את **חלק 6: שיקולי אבטחה והרשאות** כך שהדפדפן **תמיד גלוי (Headful)** בזמן פעולה, כדי לאפשר פיקוח מלא מצד המשתמש. זה מחליף את הסעיף הקודם.

---

# 🔐 חלק 6: שיקולי אבטחה והרשאות (Always-Visible Browser)

## 6.1 מטרות אבטחה

* הגנה על **סשן פייסבוק** (cookies/LocalStorage) והפרדה מהרצת הדפדפן הראשי.
* שקיפות מלאה: **הדפדפן תמיד גלוי**, עם יכולת פיקוח, עצירה מיידית ואישור פעולות.
* מניעת שימוש עוין (קצבים, כפילויות, העלאות חריגות) ושמירה על פרטיות.

---

## 6.2 סיווג מידע

* **רגיש מאוד**: סשן פייסבוק (cookies/LS), מפתח הצפנה.
* **רגיש**: טקסטי פוסטים שלא פורסמו, תזמונים עתידיים, מדיה לפני פרסום.
* **רגיל**: רשימות קבוצות/לוגים ללא מזהים אישיים.

---

## 6.3 ניהול סודות וסשנים

* ברירת מחדל: **Keytar** (OS Keychain) לשמירת מפתח ההצפנה.
* קובץ סשן מוצפן: `data/storage/session.enc` בפורמט **AES-256-GCM** (IV וקוד אימות).
* Fallback (לא מומלץ): `FB_SESSION_KEY_SOURCE=env` → מוצג **אזהרת UI** מחמירה.
* הרשאות קבצים: `data/storage` ו־`data/prisma` בהרשאת משתמש בלבד.

**קריטריוני קבלה:**

* ללא Keytar → מוצגת אזהרה מחייבת אישור (Opt-in) לפני המשך.
* לא נרשמים סודות/קוקיז בלוגים.

---

## 6.4 תפקידי משתמש (לוקאלי)

* **Admin**: הכל, כולל ייבוא/ייצוא סשן.
* **Operator**: פרסום/תזמון/לוגים; **ללא** ייבוא/ייצוא סשן.
* **Viewer**: צפייה בלוגים/תזמונים בלבד.
  *(ניהול תפקידים–אופציונלי ל-MVP, מומלץ להמשך.)*

---

## 6.5 תקשורת ו־CORS

* ברירת מחדל מקומי. אם נפתח לרשת:

  * HTTPS מאחורי Reverse Proxy והגבלת IP.
  * CORS ממוקד ל־client בלבד.
  * שימוש ב־`helmet` ב-Express, כיבוי `X-Powered-By`.

---

## 6.6 מדיניות לוגים

* לעולם לא לשמור סודות/קוקיז/LS.
* רמות: `info` (שגרה), `warn` (אנומליות), `error` (חריגות).
* דיבאג (צילומי מסך/trace) **כבוי כברירת מחדל**; כאשר מופעל:

  * שמירה ל־`data/storage/debug` עם TTL (ברירת מחדל: 7 ימים).
  * מחיקה אוטומטית לאחר TTL.

---

## 6.7 הקשחת Playwright/Chromium — **עם חלון גלוי תמיד**

* **Always Headful**: `BROWSER_HEADLESS=false` בכל הרצה (Login/פרסום/בדיקות).

  * ניתן למזער חלון, אך הוא רץ גלוי וניתן לצפייה בכל עת.
* **פיקוח משתמש**:

  * **כפתור “Pause/Resume”** בחלון הראשי של האפליקציה (שולח פקודות ל־worker).
  * **Confirm Before Post (אופציונלי)**: תיבת דיאלוג לפני לחיצה על “פרסם” בכל קבוצה או פעם אחת לכל ריצה.
  * **Hotkey חירום** (למשל `Ctrl+Shift+.`) לעצירה מיידית של המשימה הנוכחית.
* **פרופיל מבודד**: שימוש ב־`userDataDir` יהודי לאפליקציה; אין נגיעה בפרופיל כרום הראשי.
* **הקשחת סביבה**:

  * חסימת הורדות/התראות/פופ-אפים לא נחוצים.
  * מספר לשוניות מצומצם; טיימאאוט ניווט 30–60 שניות.
  * גישה אתרתית: רק דומיינים חיוניים של פייסבוק.
* **זיהוי חריגות**:

  * Checkpoint/2FA → עצירה מודרכת + הנחיה במסך (המשתמש משלים ידנית).
  * שינוי UI (לא נמצא Composer) → דו״ח שגיאה מפורט בלוג.

---

## 6.8 הגבלת קצבים ו”אנושיות”

* **Delays אקראיים** בין קבוצות (10–40ש׳׳): נראות אנושית + הפחתת flags.
* **תקרת מהירות**: מקסימום קבוצות לדקה (ניתן להגדרה).
* **Backoff** הדרגתי בכשלים/Rate-limit (2/5/10 דק׳), עד N ניסיונות.
* **Quiet Hours** (אופציונלי): דחיית פרסומים לשעות מותרות.

---

## 6.9 ולידציה על קלטים ומדיה

* URL חייב להיות `facebook.com/...` (חסימת סכימות חשודות).
* העלאות: סיומות מותרות (jpg/png/mp4), גודל מרבי (ברירת מחדל: 15MB), מניעת path traversal.
* טקסט: אורך מקסימלי, ניקוי תווים חריגים, אזהרת כפילות 24 שעות לאותה קבוצה.

---

## 6.10 2FA / Checkpoints

* עם הופעת אימות: **הדפדפן כבר גלוי**; תוצג התראה באפליקציה “נדרש אימות דו-שלבי”.
* לאחר השלמה ידנית—לחיצה על “סיימתי התחברות” תשמור סשן חדש מוצפן ותחדש את הריצה.

---

## 6.11 הרשאות קבצים/תיקיות

* `data/storage/*`, `data/prisma/dev.db` — גישת משתמש יחיד (chmod 700/ACL).
* לוגים עם רוטציה/TTL (ברירת מחדל: 90 יום).
* תיקיית Debug נפרדת עם TTL קצר.

---

## 6.12 הגנות API (אם נפתח לרשת)

* Token מקומי בין client↔server ל־Endpoints רגישים (`/auth/*`, `/publish-now`, `/schedules/run-now`).
* Rate-Limit צד שרת לבקשות ניהוליות.
* CSRF רק אם client ו־server בדומיינים שונים.

---

## 6.13 עדכוני תלויות ואמינות

* שדרוג Playwright/Chromium מבוקר (נעילת גרסה, smoke tests לאחר שדרוג).
* עדכון מודלים ב-Ollama—בדיקות ניסוח בעברית לפני שימוש בפרודקשן.

---

## 6.14 תאימות ופרטיות

* מודלי AI מקומיים — ללא שליחה לצד ג׳.
* אם בעתיד יחובר API חיצוני—נעדכן את מדיניות הפרטיות והאבטחה.

---

## 6.15 משתני סביבה רלוונטיים (מעודכן)

```
# Sessions & Security
FB_SESSION_KEY_SOURCE=keytar
FB_SESSION_KEY=                    # ריק כשמשתמשים ב-keytar
SESSION_DIR=data/storage
SESSION_FILE=session.enc

# Browser (Always Visible)
BROWSER_ENGINE=chromium
BROWSER_HEADLESS=false             # ← תמיד גלוי
BROWSER_USER_DATA_DIR=.data/chrome-profile
NAVIGATION_TIMEOUT_MS=60000
BROWSER_START_MINIMIZED=false      # אופציונלי: הפעלה ממוזערת אך גלויה

# Logs & Debug
LOG_LEVEL=info
DEBUG_TRACES_ENABLED=false
DEBUG_TRACES_TTL_DAYS=7

# Media & Limits
MAX_MEDIA_MB=15
ALLOWED_MEDIA_EXT=jpg,png,mp4
```

---

## 6.16 Checklist אבטחה/שקיפות

* [ ] החלון גלוי בכל הרצה (אין Headless).
* [ ] Pause/Resume + Hotkey חירום פעילים.
* [ ] (אופציונלי) Confirm Before Post מאושר/כבוי לפי הגדרה.
* [ ] `session.enc` מוצפן; לא נרשמים סודות בלוגים.
* [ ] Delays/Rate-limit/Backoff פעילים.
* [ ] העלאות מסוננות כראוי; אין path traversal.
* [ ] Debug traces מוגבלים בזמן ובנפח.

---

## 6.17 קריטריוני קבלה (Security + Visibility)

* בכל פרסום/בדיקה/תזמון—הדפדפן נפתח **גלוי** ומציג את הפעולות.
* ניתן לעצור/להמשיך בזמן אמת מה-UI, ולעצור בחירום מיידית.
* אימותים/Checkpoints מטופלים ידנית בחלון הגלוי עם הנחיה ברורה.
* ללא Headless כלל; אין מצב פעולה ברקע ללא ידיעת המשתמש.

---

