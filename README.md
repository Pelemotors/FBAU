# פייסבוק אוטומציה - Facebook Automation

מערכת אוטומטית לפרסום פוסטים לפייסבוק עם תזמון וניהול קבוצות.

## 🎯 מטרות הפרויקט

- פרסום אוטומטי לפייסבוק כאילו משתמש אנושי
- תזמון פוסטים (חד-פעמי וחוזר)
- ניהול קבוצות ודפים
- יצירת פוסטים עם AI (Ollama)
- שקיפות מלאה - הדפדפן תמיד גלוי
- שליטה מקומית מלאה ללא תלות בצד שלישי

## 🏗️ מבנה הפרויקט

```
facebook-automation/
├── client/          # React + Vite (RTL, Tailwind)
├── server/          # Express API + Playwright
├── worker/          # Scheduler (node-cron)
├── shared/          # Types & Constants
└── data/            # Database & Storage
```

## 🚀 התקנה והפעלה

### דרישות מוקדמות

- Node.js 20.x או חדש יותר
- npm או yarn
- Ollama (לפוסטים עם AI)

### התקנה

```bash
# שכפול הפרויקט
git clone <repository-url>
cd facebook-automation

# התקנת תלויות
npm install

# בניית כל החבילות
npm run build
```

### הפעלה

```bash
# הפעלת כל השירותים במקביל
npm run dev

# או הפעלה נפרדת:
npm run dev:client    # http://localhost:5173
npm run dev:server    # http://localhost:3001
npm run dev:worker    # Worker process
```

## 📋 סקריפטים זמינים

### סקריפטים כלליים
- `npm run dev` - הפעלת כל השירותים במקביל
- `npm run build` - בניית כל החבילות
- `npm run lint` - בדיקת קוד
- `npm run typecheck` - בדיקת טיפוסים

### סקריפטים נפרדים
- `npm run dev:client` - הפעלת Client
- `npm run dev:server` - הפעלת Server
- `npm run dev:worker` - הפעלת Worker
- `npm run build:client` - בניית Client
- `npm run build:server` - בניית Server
- `npm run build:worker` - בניית Worker

## 🔧 הגדרות

### משתני סביבה

צור קובץ `.env` בשורש הפרויקט:

```env
# Server
PORT=3001
NODE_ENV=development

# Database
DATABASE_URL=file:./data/prisma/dev.db

# Scheduling
SCHED_TIMEZONE=Asia/Jerusalem
SCHED_POLL_INTERVAL_MS=30000

# Browser
BROWSER_HEADLESS=false
BROWSER_USER_DATA_DIR=.data/chrome-profile

# Security
FB_SESSION_KEY_SOURCE=keytar
SESSION_DIR=data/storage

# AI (Ollama)
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=aya:8b
```

### התקנת Ollama

```bash
# הורדת Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# הורדת מודל לעברית
ollama pull aya:8b
ollama pull qwen2.5:7b-instruct
```

## 🎨 תכונות

### Client (React + Vite)
- ✅ ממשק RTL מלא
- ✅ Tailwind CSS לעיצוב
- ✅ ניווט בין עמודים
- ✅ ניהול מצב עם Zustand
- 🔄 יצירת פוסטים (AI/ידני)
- 🔄 ניהול קבוצות
- 🔄 תזמון פרסומים
- 🔄 לוגים ודוחות

### Server (Express + TypeScript)
- ✅ API בסיסי
- ✅ Health checks
- ✅ CORS מוגדר
- ✅ Middleware אבטחה
- 🔄 חיבור לפייסבוק
- 🔄 פרסום אוטומטי
- 🔄 ניהול סשן
- 🔄 אינטגרציה עם Ollama

### Worker (Scheduler)
- ✅ Heartbeat בסיסי
- ✅ תמיכה ב-cron
- 🔄 ביצוע תזמונים
- 🔄 ניהול תורים
- 🔄 Backoff ו-Retry

### Shared (Types & Constants)
- ✅ טיפוסים מלאים
- ✅ ולידציה עם Zod
- ✅ קבועים מוגדרים
- ✅ הודעות שגיאה בעברית

## 🔐 אבטחה ושקיפות

- **דפדפן תמיד גלוי** - אין מצב Headless
- **סשן מוצפן** - שמירה מאובטחת של cookies
- **פיקוח מלא** - אפשרות לעצור/להמשיך בכל עת
- **לוגים מפורטים** - מעקב אחר כל פעולה
- **הגבלות קצב** - מניעת חסימה

## 🛠️ פיתוח

### מבנה קבצים

```
client/src/
├── pages/           # עמודים ראשיים
├── components/      # קומפוננטות UI
├── hooks/           # Custom hooks
├── store/           # ניהול מצב
└── lib/             # ספריות עזר

server/src/
├── routes/          # API endpoints
├── controllers/     # לוגיקה עסקית
├── services/        # שירותים
├── utils/           # עזרים
└── prisma/          # מסד נתונים

worker/src/
├── index.ts         # נקודת כניסה
└── jobRunner.ts     # ביצוע משימות

shared/src/
├── types.ts         # טיפוסים
└── constants.ts     # קבועים
```

### כללי פיתוח

1. **TypeScript** - חובה בכל החבילות
2. **Zod** - ולידציה של נתונים
3. **RTL** - תמיכה מלאה בעברית
4. **Error Handling** - טיפול בשגיאות בכל רמה
5. **Logging** - לוגים מפורטים לכל פעולה

## 📊 סטטוס פיתוח

- [x] שלד פרויקט (Monorepo)
- [x] Client בסיסי (React + Vite)
- [x] Server בסיסי (Express)
- [x] Worker בסיסי (Scheduler)
- [x] Shared types & constants
- [ ] חיבור לפייסבוק
- [ ] פרסום אוטומטי
- [ ] ניהול קבוצות
- [ ] תזמון מתקדם
- [ ] אינטגרציה עם AI

## 🤝 תרומה

1. Fork הפרויקט
2. צור branch חדש (`git checkout -b feature/amazing-feature`)
3. Commit השינויים (`git commit -m 'Add amazing feature'`)
4. Push ל-branch (`git push origin feature/amazing-feature`)
5. פתח Pull Request

## 📄 רישיון

ISC License - ראה קובץ [LICENSE](LICENSE) לפרטים.

## 🆘 תמיכה

אם נתקלת בבעיה או יש לך שאלה:

1. בדוק את ה-[Issues](../../issues) הקיימים
2. צור Issue חדש עם פרטים מלאים
3. צור קשר דרך [Discussions](../../discussions)

---

**הערה חשובה**: המערכת פועלת כאילו משתמש אנושי ומכבדת את תנאי השימוש של פייסבוק. השתמשו באחריות.
