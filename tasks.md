1.0 יצירת מונורפו עם npm workspaces

מטרה: לייצר שלד בסיסי של הפרויקט עם Workspaces ל־client, server, worker, shared.

1.1 אתחול תיקיית הפרויקט

תוצר: תיקייה facebook-automation/ עם package.json ראשי מאותחל.

קריטריוני קבלה: npm init -y הושלם; הקובץ נוצר.

1.2 הגדרת Workspaces

תוצר: עדכון package.json ראשי עם:

"private": true

"workspaces": ["client","server","worker","shared"]

קריטריוני קבלה: npm -w server -v ו־npm -w client -v לא זורקות שגיאה.

1.3 יצירת תיקיות בסיס

תוצר: תיקיות ריקות: client/, server/, worker/, shared/.

קריטריוני קבלה: dir (Windows) או ls (Linux/Mac) מציג את 4 התיקיות.

1.4 סקריפטים ראשיים לניהול ריבוי חבילות

תוצר: ב־package.json ראשי סקריפטים:

dev, dev:server, dev:worker, dev:client

build, build:server, build:worker, build:client

(אופציונלי) lint, typecheck

קריטריוני קבלה: npm run build:client לא זורק שגיאה כשיתווספו סקריפטים בתתי־חבילות.

1.5 התקנת עזרה לריבוי סקריפטים

תוצר: npm-run-all מותקן ב־root (devDependencies).

קריטריוני קבלה: npm run dev יריץ מקבץ ברגע שתתי־החבילות יוגדרו.

2.0 אתחול פרויקט Client (React + Vite, RTL, Tailwind מוכנים)

מטרה: ליצור שלד UI ניהולי בסיסי לדשבורד.

2.1 יצירת פרויקט Vite (React TS)

תוצר: פרויקט client/ עם vite + TypeScript.

קריטריוני קבלה: npm --workspace client run dev מעלה שרת פיתוח ברירת מחדל.

2.2 התקנות בסיס ל־UI

תוצר: מותקנים tailwindcss, postcss, autoprefixer, zustand, axios, zod, react-hook-form, @hookform/resolvers.

קריטריוני קבלה: client/package.json מציג תלויות, והבילד עובר.

2.3 קונפיגורציית Tailwind + RTL

תוצר: קבצי tailwind.config.{js,ts} + postcss.config.{js,ts} + עדכון index.html/main.tsx ל־RTL.

קריטריוני קבלה: מחלקות Tailwind פועלות; dir="rtl" מיושם; הטקסט מיושר לימין.

2.4 שלד עמודים/ראוטינג

תוצר: קבצי בסיס:

client/src/pages/{Dashboard.tsx, Posts.tsx, Groups.tsx, Schedules.tsx, Logs.tsx, Settings.tsx}

client/src/routes.tsx + client/src/main.tsx

קריטריוני קבלה: ניווט עובד בין עמודים (ללא תוכן מלא עדיין).

2.5 קומפוננטות בסיס + Store

תוצר: תקיות components/, hooks/, store/, lib/ עם קבצים ריקים/מינימליים:

useApi.ts, useAuthStatus.ts

store/appStore.ts

קריטריוני קבלה: האפליקציה נבנית בהצלחה עם יצוא ברירת מחדל לקומפוננטות.

3.0 אתחול פרויקט Server (Express + TS)

מטרה: שרת API בסיסי לפי PRD.

3.1 יצירת פרויקט Node + TS

תוצר: server/package.json, tsconfig.json, מבנה src/.

קריטריוני קבלה: npm --workspace server run dev מריץ ts-node ללא שגיאות.

3.2 התקנות תשתית

תוצר: מותקנים express, zod, axios, dotenv, pino, helmet, multer, csv-parse, keytar.

קריטריוני קבלה: שרת עולה; /health מחזיר 200.

3.3 קובץ אפליקציה בסיסי

תוצר: server/src/app.ts עם Middlewares, CORS (ל־client), ראוטר /health.

קריטריוני קבלה: קריאה ל־GET /health מחזירה {status:'ok'}.

3.4 נקודת כניסה

תוצר: server/src/server.ts שמאזין על PORT (ברירת מחדל 3001).

קריטריוני קבלה: node מריץ ומדפיס “listening on :3001”.

4.0 אתחול פרויקט Worker (node-cron / poller)

מטרה: תהליך עצמאי לתזמון.

4.1 יצירת פרויקט TS

תוצר: worker/package.json, tsconfig.json, src/.

קריטריוני קבלה: npm --workspace worker run dev מריץ index.ts.

4.2 שלד קבצים

תוצר: worker/src/index.ts (polling כל 30 שניות – יתחבר בהמשך ל־DB), worker/src/jobRunner.ts (שלד).

קריטריוני קבלה: לוג “worker started” מופיע.

5.0 חבילה משותפת Shared (DTOs/Types/Constants)

מטרה: להחזיק טיפוסים משותפים.

5.1 יצירת חבילה

תוצר: shared/package.json, tsconfig.json, src/{types.ts, constants.ts}.

קריטריוני קבלה: ניתן לייבא shared מה־server וה־client (בהמשך).

6.0 קובץ README ראשי ותיעוד ראשוני

מטרה: תיעוד בסיס למפתחים.

6.1 יצירת README

תוצר: README.md בשורש מסביר מבנה, סקריפטים, איך להריץ dev.

קריטריוני קבלה: כולל הוראות קצרות להפעלה.

7.0 הכנת סביבת ENV (שלב 1 – placeholders בלבד)

מטרה: להכין .env בשורש וב־packages לפי ה-PRD (נמלא בהמשך).

7.1 יצירת .env.example בשורש

תוצר: .env.example עם:

SCHED_*, BROWSER_*, LOG_LEVEL, SESSION_DIR, SESSION_FILE, FB_SESSION_KEY_SOURCE

קריטריוני קבלה: קיים קובץ דוגמה עם placeholders ברורים.

7.2 חיבור טעינת ENV ב־server/worker

תוצר: dotenv.config() בקבצי הכניסה של server/worker.

קריטריוני קבלה: משתנים נקראים בהצלחה (לוג בדיקה).

8.0 סקריפטים להפעלה מקבילית ולבדיקות Smoke

מטרה: להבטיח שכל החבילות עולות יחד (גם אם הן עדיין “ריקות”).

8.1 הוספת סקריפטים בכל חבילה

תוצר:

client: dev שמריץ Vite, build שמריץ vite build.

server: dev עם ts-node-dev/nodemon, build עם tsc.

worker: dev עם ts-node-dev/nodemon, build עם tsc.

קריטריוני קבלה: npm run dev מהשורש מפעיל 3 תהליכים (client/server/worker) ללא שגיאת בנייה.

8.2 Smoke Test ראשוני

תוצר: גישה ל־http://localhost:<client_port> (Vite), http://localhost:3001/health (server).

קריטריוני קבלה: שניהם מגיבים; worker מדפיס heartbeat.

9.0 תבנית מבנה תיקיות מוסכמת (Skeleton)

מטרה: להבטיח עקביות עם ה־PRD.

9.1 אימוץ המבנה המוגדר ב־PRD

תוצר: יצירת התיקיות/קבצים הריקים לפי סכמת ה־PRD:

server/src/{routes,controllers,services,integrations,prisma,utils}

client/src/{pages,components,hooks,lib,store}

worker/src/{jobRunner.ts}

shared/src/{types.ts,constants.ts}

קריטריוני קבלה: המבנה קיים; קבצים מכילים הערת TODO תואמת.

10.0 בקרת גרסאות (Git)

מטרה: להכין ריפו נקי ל־GitHub/Vercel בעתיד (לפי ה־PRD).

10.1 אתחול Git + .gitignore

תוצר: git init + יצירת .gitignore (node, dist, .env, data/prisma/dev.db, data/storage).

קריטריוני קבלה: git status נקי אחרי ה־commit.

10.2 Commit ראשון

תוצר: feat: scaffold monorepo & skeleton ב־main.

קריטריוני קבלה: היסטוריית commit עם הודעה אחת לפחות.

סיכום תוצרים לשלב 1

מונורפו מוכן עם 4 חבילות.

סקריפטים שמריצים את שלושת התהליכים במקביל.

שלדי קבצים/תיקיות תואמים PRD.

README בסיסי ותבנית .env.example.

Git מאותחל עם .gitignore מתאים.

שלב 2 — DB & Prisma
🎯 מטרות השלב

להגדיר מודל נתונים תואם־PRD שמכסה Posts, Groups, Schedules, Logs, ו־Connection.

להחליט על מנוע DB (מקומי ל־MVP, אפשרות מעבר בהמשך בלי שינויי לוגיקה).

לקבוע שמות, אינדקסים, יחסים וכללי מחיקה/עדכון.

להכין תוכנית seed (דמו) ובדיקות קבלה.

2.1 בחירת מנוע וארגון הקבצים

מומלץ ל־MVP: SQLite מקומי (קל, מהיר, בלי התקנות שרת).
תכנון קדימה: שמרו על טיפוסים ניטרליים (DateTime/JSON/String) כדי לאפשר מעבר ל־PostgreSQL בהמשך ללא שינויים גדולים.

החלטות ארגון:

מיקום DB מקומי: data/prisma/dev.db.

מיגרציות משויכות לפרויקט ה־server (שם יישב Prisma).

שמרו את CRUD ליישויות תחת server (services + controllers), ואת הטיפוסים המשותפים ב־shared.

2.2 ישויות, שדות וכללים (תכנון לוגי, ללא סכמה קוד)

להלן תכנון לוגי שממפה ישירות לצרכי ה־PRD:

A) Post

שדות חיוניים:
id (uuid), title? (string, קצר), body (string, ארוך),
is_ai_generated (boolean),
media_paths (string[]) או טבלת משנה MediaAsset (ראו סעיף הרחבה),
created_at (DateTime, default now), updated_at (DateTime, auto-update).

אינדקסים/כללים:
אינדקס על created_at.
רצוי מנגנון “fingerprint” למניעת כפילות: hash של (body + trimmed media names).

ולידציות עסקיות:
גוף פוסט לא ריק; אורך מרבי לגוף (למשל 10–20k תווים).
אם is_ai_generated=true – שמרו זאת למעקב.

B) Group

שדות:
id (uuid), name (string), url (string),
last_status (enum: success/failed/unknown),
last_checked_at (DateTime?).

כללים:
URL חייב להיות facebook.com/....
אינדקס ייחודי על url (מונע כפילות).

ולידציות עסקיות:
לשקול שמירה נקייה של ה־URL (ללא פרמטרים זמניים, אם אפשר).

C) Schedule

שדות:
id (uuid), post_id (fk → Post),
group_ids (string[] of uuids) או טבלת קשר Many-to-Many (מומלץ לטווח ארוך),
type (enum: one_time | recurring),
חד־פעמי: run_at (DateTime, tz-aware),
חוזר: cron (string), timezone (string), start_at (DateTime), end_at? (DateTime),
max_runs? (int), runs_count (int, default 0),
status (enum: pending|running|done|done_with_errors|failed|paused),
last_run_at? (DateTime),
locked_at? (DateTime), locked_by? (string),
meta_json? (Json).

כללים:
אינדקס על status, run_at, cron.
כש־type=one_time, run_at חובה. כש־type=recurring, cron ו־timezone חובה.
מנגנון נעילה (locked_at/locked_by) להגנה מ־double-run.

התנהגות מחיקות:
מחיקת Post לא מוחקת Schedule (מנע orphan באמצעות בדיקות אפליקטיביות או onDelete=Restrict).

D) Log

שדות:
id (uuid), post_id?, group_id?,
event (enum: publish_attempt|success|fail|auth_issue|ui_changed|rate_limited|duplicate_skipped|worker_start|worker_stop…),
message (string, קצר יחסית),
created_at (DateTime),
meta_json? (Json) – מקום לשגיאה גולמית, לינק לפוסט, סלקטורים שבחרנו בפועל, זמני פעולה.

אינדקסים:
על created_at + קומפוזיט על (event, created_at) לסינונים מהירים.

E) Connection

שדות:
id (uuid), provider (constant='facebook'),
status (enum: connected | needs_reauth | disconnected),
last_verified_at? (DateTime),
notes? (string).

הערה:
נתוני הסשן עצמם לא ב־DB: נשמרים מוצפנים בקבצים (ראה PRD חלק אבטחה). הטבלה משקפת סטטוס בלבד לממשק.

💡 הרחבה מומלצת (לא חובה ל־MVP):
MediaAsset כטבלת משנה: id, post_id, type (image|video), path, size_kb, hash.
זה יעזור בעתיד לניהול מדיה, בדיקות גודל, ומניעת כפילויות.

2.3 יחסים וקסקדות

Post (1) — (N) Schedule: מחיקת Post אסורה אם יש Schedule פעיל. השתמשו ב־Restrict.

Post (1) — (N) Log (אופציונלי): מחיקת Post לא מוחקת לוגים היסטוריים (לוגים נשארים לתחקור).

Group (1) — (N) Log: כנ״ל.

Schedule — Group: עדיף טבלת קשר ScheduleGroup עם שדות schedule_id, group_id, order_index. זה גמיש יותר מ־array של UUIDs.

Connection: אין FK; ישות סטטוס־ממשק.

המלצה עסקית:
קבעו כלל “Idempotency Window” של 24 שעות ברמת אפליקציה (PRD) כדי למנוע כפילות פרסום – שמרו hash ניסיון (Post+Group+תאריך) בטבלת עזר או ב־Log עם event=duplicate_skipped.

2.4 אינדקסים והאצות מוצעות

Group.url – ייחודי.

Schedule.status, Schedule.run_at, Schedule.cron – לסינון worker.

Log.created_at, (Log.event, Log.created_at) – לשאילתות בדוחות.

Post.created_at – לארכיונים ותצוגות.

2.5 מדיניות זמן ואזור זמן

TZ ברירת מחדל: Asia/Jerusalem.

שדות זמן: שמרו UTC ב־DB, והציגו/פרשו ל־Asia/Jerusalem ב־UI וב־worker.

Recurring: שמרו גם timezone על כל Schedule חוזר (PRD).

2.6 Strategy ל־Seed (נתוני דמו)

מטרה: אפשרות להריץ תסריט מלא מקצה לקצה בסביבה ריקה.

תכולה מינימלית:

Group דמו אחת (URL לקבוצת בדיקה פנימית/placeholder).

Post דמו אחד (is_ai_generated=false, גוף קצר).

Schedule חד־פעמי דמה לעוד 48 שעות עם הקבוצה הנ״ל (סטטוס pending).

Connection סטטוס disconnected.

כלל בטיחות: אל תכניסו URL אמיתי ללא אישור. עדיף placeholder כדי למנוע פרסום שגוי.

2.7 משתני סביבה (תוספות רלוונטיות לשלב DB)

DATABASE_URL – מסלול לקובץ SQLite המקומי.

SCHED_TIMEZONE – ברירת מחדל לאזור זמן (תואם PRD).

תזכורת: קובץ .env.example רק עם placeholders; .env אמיתי לא נכנס ל־git.

2.8 קריטריוני קבלה (שלב DB & Prisma)

קיימת סכמת DB מלאה שמכסה את כל הישויות לעיל.

מיגרציה ראשונה נוצרת ומריצה בהצלחה (DB קיים).

בדיקת יחסים ואינדקסים עוברת (שאילתות דמה מצד השרת).

תסריט seed מריץ ומייצר:

Group דמו

Post דמו

Schedule דמו (pending, one_time)

Connection במצב disconnected

אפשר להציג בממשק (בשלב 3) את הרשימות הריקות/דמו ללא שגיאות.

2.9 מדיניות שמות וסוגים (סטנדרטיזציה)

שמות טבלאות ביחיד באנגלית PascalCase או snake_case אחיד (בחרו סגנון אחד ושמרו עליו).

שמות שדות באנגלית ב־snake_case, טיפוסים בסיסיים: string, boolean, DateTime, Json, enum.

enums באנגלית באותיות קטנות/גדולות עקביות (למשל: publish_attempt, success… או CamelCase — רק לא לערבב).

2.10 בדיקות ידניות (Smoke, ללא קוד)

בצעו את הבדיקות הבאות, ידנית:

יצירת Post דמו → נשמר עם timestamps.

יצירת Group עם URL ייחודי → ניסיון יצירת כפילות נכשל (לפי הכלל שהגדרתם).

יצירת Schedule חד־פעמי שמצביע ל־Post + Group → סטטוס pending ונראה ב־DB.

שינוי סטטוס Schedule ל־running וכתיבת Log publish_attempt → נשמרים תקין.

יצירת Connection במצב connected → עדכון last_verified_at עובד.

2.11 טעויות נפוצות שכדאי להימנע מהן

שמירת group_ids כ־string אחד (CSV) במקום מבנה נתונים/טבלת קשר. עדיף טבלת קשר.

שכחת אינדקס על Schedule.run_at → worker יתעכב על סריקות.

מחיקת Post שמקושר ל־Schedule פעיל → צריכה להיחסם ברמת אפליקציה/DB.

טיפול חלקי ב־timezone ל־recurring → יוצר זמני ריצה לא נכונים בקיץ/חורף.

שמירת סודות/קוקיז ב־DB. הסשן עצמו חייב להיות מוצפן בקובץ (כפי שהוגדר באבטחה).

2.12 הרחבות עתידיות (תכננו מראש)

ScheduleGroup (Many-to-Many) עם order_index ודגלים לקבוצה (למשל allow_duplicate_within_window).

PostingPolicy לטיוב rate-control לכל קבוצה/משתמש.

MediaAsset לטיפול מדיה ברזולוציה גבוהה/וידאו כבד.

Audit לטבלאות ניהול (מי מחק/ערך).
שלב 3 — שרת Express (API)
🎯 מטרות השלב

להרים API מקומי מאורגן (Node.js + Express) שישמש שכבת תווך ל־Client, ל־Worker, ולדפדפן האוטומטי.

ליישם נקודות קצה מינימליות ל־Posts/Groups/Schedules/Logs וחיבור לפייסבוק (Auth/Session).

לעמוד בעקרונות הארכיטקטורה, התזמון והשקיפות שנקבעו ב־PRD.

3.1 מבנה תיקיות מומלץ (Server)

routes/ — הגדרת Endpoints “דקים”.

controllers/ — לוגיקה אפליקטיבית לכל מודול (posts, groups, schedules, logs, auth).

services/ — גישה ל־DB (Prisma), אינטגרציות (publisher/session/ollama), ותשתיות (logs/backoff/selectors/crypto).

prisma/ — אתחול Prisma Client.

utils/ — עזרי אבטחה, אימות, parse, ולידציות.
מבנה זה תואם את חלוקת הרכיבים שב־PRD (כולל קבצי עזר לבק־אוף, סלקטורים, הצפנה, ועוד).

3.2 Middleware חיוניים (המלצות)

אבטחה בסיסית: helmet, cors (מוגבל ל־client המקומי), express-rate-limit לנתיבים רגישים (Auth/Publish/Run-Now). תיאום עם מדיניות ההגנות ב־PRD.

לוגים: pino/winston ברמת info + רוטציה; שמירה מדורגת של תקלות (TTL).

Body limits & uploads: מגבלת גודל, סינון סיומות (jpg/png/mp4), מניעת path traversal — בהתאם להגבלות PRD.

ולידציה שיטתית: Zod/Yup לכל Request (כולל URL שחייב להכיל facebook.com/... לקבוצות).

Error Handler אחיד: החזרת JSON עקבי, מיפוי קודי שגיאה, הסתרת פרטים רגישים.

3.3 מודולי Service מרכזיים

prismaService – חיבור יחיד ל־DB + פונקציות CRUD.

sessionService – ניהול/הצפנת קובץ session.enc + סטטוס בטבלת Connection (DB). “סודות” לא יישמרו ב־DB עצמו.

browserService (Playwright) – אתחול דפדפן גלוי בלבד עם userDataDir קבוע לפיקוח מלא (אין Headless).

publisherService – פרסום לקבוצות: איתור קומפוזר עמיד לשינויים (סלקטורים/aria), העלאת מדיה, לוג תוצאות לכל קבוצה, Respect ל־Rate/Backoff/Spacing.

backoffService – ניהול ניסיונות חוזרים (2/5/10 דק׳) ותעוד בלוג.

logsService – כתיבת לוגים תקנית (attempt/success/fail/auth_issue/ui_changed/duplicate_skipped וכו׳), שליפות עם פילטרים וייצוא.

3.4 נקודות קצה (API) – רשימת מינימום

דגשים: החזרי JSON עקביים, ולידציה לפני DB/הרצה, לוגים משמעותיים, ושגיאות נהירות.

A) בריאות וחיבור

GET /health — בדיקת חיים (גרסה, זמן ריצה).

GET /auth/facebook/status — סטטוס Connection (🟢/🟡/🔴) + last_verified_at.

POST /auth/facebook/login/start — פתיחת דפדפן גלוי לחלון התחברות.

POST /auth/facebook/login/finish — שמירת סשן מוצפן + עדכון Connection.

POST /auth/facebook/check — טעינת FB/קבוצת בדיקה; עדכון סטטוס.

POST /auth/facebook/disconnect — מחיקת session.enc + ניקוי סטטוס.

B) Posts

GET /posts / GET /posts/:id — שליפה/פריט.

POST /posts — יצירה (AI/ידני; שמירת גוף, מדיה, דגל is_ai_generated).

PUT /posts/:id — עדכון; DELETE /posts/:id — מחיקה (חסימה אם יש Schedule פעיל).

POST /posts/:id/publish-now — פרסום מיידי לקבוצות נבחרות + כתיבת לוג לכל קבוצה.

C) Groups

GET /groups / POST /groups / PUT /groups/:id / DELETE /groups/:id — ניהול מלא.

POST /groups/import / GET /groups/export — CSV.

ולידציה: name חובה; url חייב להכיל facebook.com/….

D) Schedules

GET /schedules / POST /schedules / PUT /schedules/:id / DELETE /schedules/:id — חד־פעמי/חוזר.

שדות עיקריים: post_id, groups[]/M2M, type (one_time|recurring), run_at או cron+timezone.

POST /schedules/:id/run-now — דריסה ידנית (מוגן/מדורג).

כיבוד אזור הזמן Asia/Jerusalem וחוקי Backoff/Jitter/Spacing.

E) Logs

GET /logs — שליפות עם פילטרים (טווח תאריכים/קבוצה/תוצאה), כולל ייצוא CSV.

3.5 כללי עסק/אבטחה ב־API (מפתחי על)

דפדפן תמיד גלוי: כל הפעלות (בדיקה/פרסום/תזמון) פותחות חלון נראה; אין Headless.

Idempotency 24h: מניעת פרסום כפול לאותה קבוצה בחלון זמן — בדיקה לפני פרסום/ריצה.

Backoff + Spacing: ניסיונות חוזרים מדורגים ודיליי אקראי בין קבוצות.

סלקטורים עמידים: נפילות UI בפייסבוק → זיהוי חלופות, לוג מפורט והמשך זהיר.

ניהול Session מאובטח: cookies/LS בקובץ מוצפן; DB שומר רק סטטוס/מטא.

ולידציות קלטים: URL של קבוצות, מגבלות מדיה, וטקסט (אורך/ניקוי/התראה על כפילות).

3.6 קונטרקטי בקשות/תגובות (הכוונה ללא קוד)

POST /posts — קלט: title?, body, is_ai_generated, media[]?. פלט: פרטי Post + id.

POST /groups — קלט: name, url. פלט: פרטי Group + id. (החלה של ולידציות PRD ל־URL).

POST /schedules — קלט: post_id, groups[]/group_ids[], type, run_at או cron+timezone. פלט: פרטי Schedule.

POST /posts/:id/publish-now — קלט: group_ids[]. פלט: סיכום per-group (✔/❌ + תקציר סיבה), לינק לפוסט אם זמין.

GET /logs — פרמ׳ שאילתה: from, to, group_id, status|event. פלט: מערך רשומות.

טיפ: הגדירו לכל Endpoint “שדות חובה/אופציונליים”, וקונבנציית שגיאות (code, message, details) עקבית.

3.7 תרחישי בדיקת Smoke (ידני, ללא קוד)

/health מחזיר 200.

POST /auth/facebook/login/start — נפתח דפדפן גלוי.

POST /auth/facebook/login/finish — נוצר session.enc מוצפן + Connection מתעדכן ל־🟢.

יצירת Group עם URL חוקי; ניסיון כפילות נכשל.

יצירת Post → publish-now עם קבוצה אחת: נרשמים לוגי ניסיון/הצלחה/כשל לפי תוצאה.

יצירת Schedule one_time לעוד שעה → שינוי סטטוס ל־pending ונראות ב־GET /schedules.

ריצת run-now לסידור הנ״ל → פרסום בפועל, Spacing/Backoff מופעלים; כתיבת לוג; עדכון סטטוס.

3.8 קריטריוני קבלה (שלב שרת)

כל ה־Endpoints שלעיל קיימים ופועלים עם ולידציה ושגיאות נהירות.

דפדפן נפתח תמיד גלוי בכל פעולה רלוונטית; אין מצב Headless.

ניהול Session בטוח (קובץ מוצפן; DB מכיל סטטוס בלבד).

לוגים נרשמים בהתאם ל־PRD (סינון/ייצוא).

עמידה ב־Backoff/Spacing/Idempotency 24h.

3.9 משתני סביבה (Server, הרחבה)

PORT (ברירת מחדל 3001).

DATABASE_URL (SQLite לוקאלי).

SCHED_TIMEZONE=Asia/Jerusalem.

SESSION_DIR, SESSION_FILE, FB_SESSION_KEY_SOURCE (מפתח/מקור להצפנה—בהתאם לאבטחה).

3.10 הערות יישום חשובות

הפרדת חששות: routes “דקים” → controllers → services → utils. מקל על בדיקות והחלפות.

חסינות לשינויים ב־UI: שמרו שכבה ייעודית ל־selectors/strategies כדי להחליף במהירות.

תיעוד API: החזיקו מסמך/Swagger קל־משקל לעקביות מול ה־Client.

רמות לוג: info כברירת מחדל; debug רק זמנית (עם TTL/רוטציה).
שלב 4 — Client (UI/UX)
🎯 מטרות

לבנות דאשבורד ניהולי נוח, RTL מלא, שמכסה: סטטוס חיבור לפייסבוק, יצירת פוסטים (AI/ידני), ניהול קבוצות, תזמונים ולוגים.

להבטיח זרימות עבודה חלקות: “יצירת פוסט → תצוגה מקדימה → בחירת קבוצות → פרסום עכשיו/תזמון → תוצאות בלוג”.

שקיפות מלאה: חיווי סטטוס ותוצאות לכל פעולה, התאמה לאבטחה (דפדפן תמיד גלוי), ואזהרות כפילות.

4.1 ארכיטקטורה Frontend (ללא קוד)

Pages (routes): Dashboard, Posts, Groups, Schedules, Logs, Settings (תתי־טאב: Facebook Connect, General).

State Mgmt: Zustand/Context לסטטוס חיבור, סטטוס ריצות, בחירת קבוצות, טיוטות.

Forms: react-hook-form + zod לוולידציות סדורות (שדות חובה, URL חוקי, אורך טקסט, מגבלות מדיה).

API Client: שכבה אחת מרוכזת (axios) עם Interceptors לשגיאות/טוקן.

Design System: Tailwind + shadcn (כפתורים, קארדים, טבלאות, דיאלוגים).

i18n/RTL: dir="rtl", יישור לימין, תאריכים בפורמט מקומי (Asia/Jerusalem).

4.2 מסכים ותכולה
4.2.1 Dashboard

מטרה: תמונת מצב + קיצורי דרך.

כרטיס “סטטוס פייסבוק”: 🟢 מחובר / 🟡 דרוש אימות / 🔴 לא מחובר; כפתורים: “התחבר/נהל חיבור”, “בדיקת חיבור”.

“תזמונים קרובים” (3 רשומות), “לוגים אחרונים” (5 רשומות).

קיצורי דרך: “פוסט AI מהיר”, “פוסט ידני מהיר”.
ולידציות/חיווי:

אם 🔴 לא מחובר → באנר פעולה מהיר “להתחברות”.

4.2.2 Posts

טאבים:

פוסט AI

Prompt בסיסי (ניתן לעריכה) → “צור טיוטה מ־AI” → ממלא שדה תוכן.

תצוגה מקדימה.

פוסט ידני

שדות: כותרת (אופציונלי), גוף הפוסט (Rich Text מינימלי), טעינת קובץ טקסט (אופציונלי, ממלא את הגוף).
משותף לשני המצבים:

בחירת קבוצות: סיידבר/מודל עם רשימת קבוצות + חיפוש/סינון + “בחר הכול”.

מדיה: העלאת תמונה/וידאו (בדיקת גודל/סיומת).

כפתורים: “שמור כטיוטה”, “תצוגה מקדימה”, “פרסם עכשיו”, “תזמן פרסום”.
ולידציות UX:

גוף פוסט חובה; אזהרת כפילות אם תוכן זהה פורסם באותה קבוצה ב־24 שעות.

אם אין חיבור לפייסבוק בשעת “פרסם עכשיו”/“תזמן” → דיאלוג הכוונה למסך חיבור.

4.2.3 Groups

טבלה: שם, URL, סטטוס אחרון, עודכן לאחרונה, פעולות.

פעולות: הוספה/עריכה/מחיקה; ייבוא CSV / ייצוא CSV; בדיקת קבוצה (בדיקת reachability).
ולידציה:

name חובה; url חייב להכיל facebook.com/… (שגיאת טופס ברורה).

4.2.4 Schedules

טבלה: תאריך/שעה, סוג (AI/ידני), תקציר טקסט, #קבוצות, חזרתיות (ללא/יומי/שבועי/מותאם), סטטוס (pending/running/done/failed), פעולות.

יצירת/עריכת תזמון:

חד־פעמי: בחירת תאריך/שעה (TZ: Asia/Jerusalem).

חוזר: cron / בחירה מודרכת (Daily/Weekly/Custom) + timezone.

פעולות: עריכה/ביטול/שכפול/Run-Now.
UX בטיחות:

Jitter והשהיה אקראית מוצגות כמדיניות; Tooltip מסביר.

4.2.5 Logs

טבלת כרונולוגיה: תאריך/שעה, קבוצה, תקציר, ✔/❌, סיבת כשל, קישור לפוסט אם זמין.

פילטרים: טווח תאריכים, קבוצה, אירוע/סטטוס.

כפתור ייצוא CSV.

4.2.6 Settings → Facebook Connect

כרטיס סטטוס: 🟢/🟡/🔴 + “עודכן לאחרונה”.

כפתורים:

“התחבר דרך דפדפן” — פותח חלון גלוי.

“סיימתי התחברות” — שומר Session.

“ייבוא Cookies” (קובץ JSON).

“ייצוא/גיבוי Session” (מוצפן).

“בדיקת חיבור”.

“ניתוק וניקוי סשן”.

מיקרו־קופי ברור (שגיאות/אזהרות לפי PRD).

4.3 זרימות עבודה (User Flows)
Flow A — התחברות לפייסבוק

Settings → Facebook Connect → “התחבר דרך דפדפן”.

המשתמש משלים Login/2FA בדפדפן הגלוי.

“סיימתי התחברות” → סטטוס מתעדכן ל־🟢; הופכת זמינה פעולה “בדיקת חיבור”.

Flow B — פרסום מיידי

Posts: יצירת פוסט (AI/ידני) + בחירת קבוצות.

“תצוגה מקדימה” → “פרסם עכשיו”.

חלון גלוי נפתח, המערכת מפרסמת לכל קבוצה בתור, דיליי אקראי ביניהן.

תוצאות מוצגות בסוף + נרשמות ב־Logs.

Flow C — תזמון

Posts → “תזמן פרסום”, בחירת חד־פעמי/חוזר.

ב־Schedule: הצגה כ־pending, כולל “Run-Now”.

בזמן היעד ה־Worker מריץ, UI מציג סטטוסים מתקדמים ולבסוף תוצאות בלוג.

4.4 ולידציות ותקלות (UX First)

שדות חובה: גוף פוסט; קבוצה אחת לפחות לפרסום/תזמון.

כפילות: התרעה לפני שליחה אם נמצא fingerprint זהה ב־24 שעות לאותה קבוצה (לא חוסם כברירת מחדל).

מדיה: אזהרה/חסימה אם חריגת גודל/סיומת לא מותרת.

חיבור: אם לא מחובר לפייסבוק → מודל הכוונה קצר (“לחץ להתחבר כעת”).

שגיאות פעולה: דיאלוג תמציתי עם צעד הבא (Retry, Open login, Edit groups).

4.5 טבלאות ומרכיבי UI (המלצות)

טבלאות גדולות: Pagination 25–50 פריטים, חיפוש לקוח, סינון, מיון לפי עמודות שכיחות.

דיאלוגים: לאשר פעולות מסוכנות (Delete, Run-Now).

Toasts: פעולות מהירות (Saved, Imported, Scheduled).

Empty States: מסרים קצרים עם CTA (“הוסף קבוצה ראשונה”, “צור פוסט ראשון”).

Loading/Disabled states: כפתורים מנוטרלים בזמן פעולות, ספינרים עדינים.

4.6 ביצועים ושקיפות

Skeletons בזמן טעינה ראשונית.

Optimistic UI למהלכים לא־מסוכנים (למשל שינוי שם קבוצה), עם rollback בשגיאה.

Poll/WS: לרענן סטטוס תזמונים/לוגים ללא רענון ידני (poll קצר–בינוני; WS בעתיד).

4.7 אבטחה ופרטיות (צד לקוח)

לא לשמור סודות/קוקיז בצד הלקוח.

אזהרה ברורה לפני ייצוא/ייבוא סשן (מודל הסבר).

CORS ממוקד לשרת המקומי בלבד.

הצגת התראות אבטחה רק בעת צורך (ללא פרטים רגישים).

4.8 אנליטיקה בסיסית (אופציונלי)

טלמטריה מקומית בלבד (ספירת פעולות: יצירת פוסט, פרסום, כשלונות) — לצורך שיפור UX.

תיעוד מדדים: זמן ממוצע ליצירת פוסט, יחס הצלחות/כשלונות לכל קבוצה.

4.9 בדיקות קבלה (Acceptance Criteria)

Dashboard מציג סטטוס חיבור מדויק, פריטי תזמון קרובים ולוגים אחרונים.

Posts מאפשר יצירת פוסט AI וידני, תצוגה מקדימה, בחירת קבוצות, ופעולת “פרסם עכשיו/תזמן”.

Groups מנהל רשימה עם חיפוש/סינון, ייבוא/ייצוא CSV, ולידציית URL.

Schedules יוצר חד־פעמי/חוזר, מציג סטטוסים, ותומך ב־Run-Now.

Logs מציג תוצאות עם פילטרים וייצוא CSV.

UX שגיאות: מסרים ברורים, ללא קריסות/מסכים “רדודים”.

RTL מלא ונגישות בסיסית (ניווט מקלדת, ניגודיות תקינה).

4.10 “מלכודות” שכדאי להימנע מהן

יותר מדי אופציות במסך אחד (שמרו על Progressive Disclosure).

בלגן בהזנת קבוצות — הקפידו על ולידציה מיידית ל־URL + Preview.

חוסר תאום עם השרת לגבי פורמטים (תאריכים, מזהים) — הגדירו חוזה JSON ברור מראש.

מסכי שגיאה כלליים — תעדפו שגיאות ממוקדות עם פעולה מתקנת.
מעולה — ממשיכים ל**שלב 5: ה־Worker והתזמון** (ללא קוד, הנחיות והמלצות בלבד).

# שלב 5 — Worker & Scheduling

## 🎯 מטרות

* להוציא לפועל פרסומים “ממתינים” בזמן הנכון, בקצב אנושי, עם שקיפות מלאה ותיעוד.
* לעמוד בכללי בטיחות: דיליי אקראי בין קבוצות, Backoff חכם, חלון Idempotency ל־24 שעות, ואזור זמן Asia/Jerusalem.  

---

## 5.1 ארכיטקטורה ועקרונות

* **Poller קצר־טווח**: תהליך שרץ ברצף ובודק כל X שניות משימות זמינות (ברירת מחדל: 30s). שמרו ערך בקובץ env.  
* **הפרדת תורים**: תור פרסומים ותור בדיקות/בריאות כדי שלא “תשרפו” זמן ריצה על Health. 
* **TZ וקונסיסטנטיות**: שמרו UTC ב־DB, חשבו next runs והצגה ב־Asia/Jerusalem בצד ה־UI/Worker. 
* **קצב אנושי**: Spacing אקראי בין קבוצות (למשל 10–40 שניות), תקרה של קבוצות לדקה. ערכים בקונפיג. 

---

## 5.2 בחירת משימות והרצה (Flow)

1. **שליפה**: בחרו משימות ש־`status=pending` וה־`run_at <= now` (או recurring לפי cron/next).
2. **נעילה**: מיד עם הבחירה עדכנו `status=running` ו־`locked_at`+`locked_by` כדי למנוע ריצות כפולות. 
3. **בדיקות טרום־ריצה**:

   * סטטוס חיבור לפייסבוק; אם “לא מחובר” → סיימו `failed` עם סיבת AUTH_REQUIRED.
   * בדיקת כפילות (Fingerprint) ב־24h לכל (Post, Group). אם קיים → רשמו לוג `duplicate_skipped` והמשיכו לקבוצה הבאה.  
4. **הרצה לקבוצות**:

   * לכל Group בתור: נפתח דפדפן גלוי עם הסשן, ננווט לקבוצה, נאתר Composer, נדביק טקסט/נעלה מדיה, “פרסם”.
   * בין קבוצות: דיליי אקראי לפי טווח הקונפיג (Jitter). 
5. **Backoff חכם**: במקרה שגיאה זמנית/Rate limit — נסו שוב לפי מדרגות (2m/5m/10m עד N ניסיונות), תעדו בלוג. 
6. **סיום**:

   * סיכום per-group (✔/❌ + סיבה).
   * סטטוס משימה: `done`, `done_with_errors`, או `failed` (אם הכל נכשל).
   * recurring: חשבו `next_run_at` ועדכנו `runs_count`; החזירו ל־`pending`. 

---

## 5.3 מצבי כשל ושיקום

* **Session/Checkpoint/2FA**: עצירה נקייה עם לוג `auth_issue`, דרשו Login מחדש בחלון גלוי; ה־Worker לא “ילחץ” עד אשר הסטטוס יחזור תקין. 
* **שינוי UI של פייסבוק**: אם לא נמצא Composer אחרי 2 אסטרטגיות סלקטורים → `failed` עם `ui_changed` ולוג מפורט (כולל אילו סלקטורים נוסו). 
* **מדיה גדולה מדי**: סמנו כשל לאותה קבוצה, המשיכו לאחרות. כללים לפי MAX_MEDIA_MB. 
* **ריבוי כשלים רצופים**: אם 3 משימות נכשלו מ־AUTH_REQUIRED — עברו ל־Health Mode (עצירת פרסומים) + באנר בדשבורד. 

---

## 5.4 קונפיגורציה (ENV) ותזמונים

הגדירו בקובץ `.env` (placeholders ימולאו ידנית):

* **Polling & Concurrency**: מרווח פולינג, מקסימום עבודות במקביל.
* **Pace**: טווח דיליי בין קבוצות, מקס’ קבוצות לדקה.
* **Retry/Backoff**: מספר ניסיונות ומדרגות השהייה.
* **Idempotency Window**: שעות למניעת כפילויות.
  הערכים האלו מוגדרים במפורש ב־PRD ומשרתים את ה־Worker. 

---

## 5.5 Cron ו־Recurring

* תמכו גם ב־CRON חופשי וגם בתבניות מוכנות (יומי/שבועי).
* הוסיפו יכולת **Validate-CRON** שמחזירה 5 מועדים עתידיים, כדי למנוע שגיאות משתמש.  

---

## 5.6 Endpoints שרלוונטיים ל־Worker

* `POST /schedules` — יצירה/עדכון משימות חד־פעמיות/חוזרות.
* `POST /schedules/:id/run-now` — הרצה ידנית (מוגנת).
* `POST /schedules/validate-cron` — ולידציה והצגת Next Runs.
* `GET /schedules` — תצוגת סטטוסים בזמן אמת (pending/running/...). 

---

## 5.7 לוגים ושקיפות

* לכל ניסיון פרסום: רשומת `publish_attempt`; הצלחה `success`; כישלון `fail` עם `message` קצר ו־`meta_json` עשיר (stack/fb-error/selector strategy).
* פילטרים לפי טווח תאריכים/קבוצה/אירוע; ייצוא CSV מהדשבורד. 

---

## 5.8 תחזוקה ובריאות

* **Health Check פעם בשעה**: בדיקת Login (ping לקבוצת בדיקה), בדיקת דיסק בתיקיות data/storage, ניקוי לוגים ישנים (TTL 90 יום).
* **Timeout Guard**: משימות running מעל 30 דק’ → `failed: Timeout`.
* **Quiet Hours** (אופציונלי): חלון שעות שלא מפרסמים בו; פרסומים נדחים אוטומטית לבא. 

---

## 5.9 קונטרקטים נתמכים (ללא קוד, מה לוודא)

* **Schedule**:

  * one_time: `run_at` חובה;
  * recurring: `cron`, `timezone`, `start_at` חובה; `max_runs?`, `end_at?` אופציונליים.
  * שדות נעילה/סטטוס: `locked_at/locked_by`, `status`, `last_run_at`, `runs_count`, `meta_json`. 
* **ScheduleGroup** (מומלץ): קשר Many-to-Many עם `order_index` לשמירה על סדר קבוע של קבוצות. (המלצה משלימה ל־PRD.)

---

## 5.10 UX בזמן ריצה

* בדשבורד/תזמונים הציגו: `pending → running → done/done_with_errors/failed`.
* אפשרו **Pause/Resume** להרצה הנוכחית ו־**Hotkey חירום** לעצירה מידית — בהתאם לסעיף שקיפות “Always Visible Browser”. 

---

## 5.11 קריטריוני קבלה (שלב Worker)

* ה־Worker מזהה משימות בזמן, נועל ומריץ אותן; Spacing/Backoff פועלים ומדווחים בלוג. 
* אין פרסום כפול לאותה קבוצה בחלון 24 שעות (Idempotency). 
* כשלי AUTH/Checkpoint גוררים עצירה בטוחה והנחיה להתחברות; שינויי UI מדווחים כ־`ui_changed`.  
* Quiet Hours/Timeout/Health Check פועלים כנדרש. 

---

## 5.12 “מלכודות” שכדאי להימנע מהן

* **עודף מקביליות**: פרסום לכמה קבוצות במקביל מגדיל סיכוי ל־Rate limit. העדיפו סדרתי עם תקרה לדקה. 
* **שיוך קבוצות כ־CSV** בשדה יחיד: קשה לתחזק/למסך; עדיף טבלת קשר. (המלצה ליישום טוב)
* **חוסר שקיפות**: ריצה Headless/לוגים דלים יקשה על דיבוג; שמרו דפדפן גלוי ולוג עשיר. 
* **CRON שגוי**: חובה מסך Validate-CRON לפני שמירה. 

---


---

# שלב 6 — אבטחה והרשאות

## 🎯 מטרות

* להגן על סודות (Sessions, Cookies, מפתחות) ועל נתוני משתמשים/קבוצות.
* להבטיח שקיפות ובקרה (דפדפן **תמיד גלוי**), ולמנוע שימוש לרעה/טעות אנוש.
* לכסות מודל הרשאות בסיסי להיום (משתמש יחיד) וסקיצה להתרחבות (רולס).

---

## 6.0 Threat Model קצר

* **איומי זהות**: גניבת סשן פייסבוק, שימוש במכשיר לא מורשה.
* **איומי קלט**: קלט זדוני בשדות פוסט/URL (XSS בלקוח, Path Traversal בקבצים).
* **איומי שירות**: עומס/Rate-limit מצד פייסבוק, פרסום חוזר בטעות, CRON שגוי.
* **דליפת מידע**: לוגים “מדברים מדי”, גיבויים לא מוצפנים.

> עיקרון מנחה: **Least Privilege + Fail-Safe Defaults + Visibility**.

---

## 6.1 ניהול סודות וסשנים

**משימת-על 6.1 — שמירת סשן מאובטחת**

* **6.1.1** בחירת מיקום סשן: קובץ מוצפן `session.enc` בתיקיית `data/sessions` (לא ב-DB, לא ב-git).
* **6.1.2** מקור מפתח הצפנה:

  * עבור MVP: מחרוזת סודית ב-ENV (שם חד-משמעי, לדוגמה `FB_SESSION_KEY_SOURCE`), או שימוש בכספת OS (Keytar/OS Keychain).
  * מדיניות רוטציה: החלפת מפתח פעם ברבעון (תהליך ידני מתועד).
* **6.1.3** גיבוי/שחזור: “ייצוא סשן” יוצר קובץ מוצפן + checksum; “ייבוא סשן” דורש אימות ידני במסך Settings.
* **6.1.4** ניתוק בטוח: כפתור “Disconnect” מוחק את `session.enc` ומנקה מטא ב-DB.
* **6.1.5** הרשאות קובץ: הרשאות קריאה/כתיבה למשתמש המקומי בלבד (OS-level).
* **6.1.6** מדיניות אחסון מקומי: אין שמירת Cookies/LS ב-DB; רק סטטוס חיבור ומטא.

**קריטריוני קבלה**:

* פעולות Export/Import/Disconnect מוגנות בדיאלוגי אישור, עם אזהרת אבטחה ברורה.
* אין סודות ב-git; `.env` ב-.gitignore; בדיקות שמבטיחות שאין “טקסט ברור”.

---

## 6.2 גישת דפדפן ואינטגרציית Playwright

**משימת-על 6.2 — דפדפן גלוי ובקרת פרופיל**

* **6.2.1** Always Headful: כל פעולה שפותחת פייסבוק—חלון נראה לעין, פרופיל קבוע (`userDataDir`).
* **6.2.2** בידוד פרופילים: פרופיל נפרד לכל סביבת הרצה (dev/stage/prod) למניעת ערבוב.
* **6.2.3** Lock/Unlock: בזמן ריצה—חיווי ב-UI “ריצה פעילה”; כפתור Pause/Stop חירום.
* **6.2.4** הקלטה ושחזור: שמירת “אסטרטגיות סלקטורים” במסמך תפעולי—כדי להגיב מהר לשינויי UI.
* **6.2.5** מגבלות פעולות: אין “Auto-Login” מאחורי הקלעים; התחברות מחדש תמיד ע"י המשתמש בחלון גלוי.

**קריטריוני קבלה**:

* אין מצב Headless; כל ניסיונות פרסום/בדיקה פותחים חלון נראה.
* לוג ברור מתי/מי פתח חלון ומה הייתה תוצאת הפעולה.

---

## 6.3 בקרת גישה והרשאות (AuthZ)

**משימת-על 6.3 — מודל משתמש יחיד + הכנה לרולס**

* **6.3.1** MVP: הפעלה “מכונת מפעיל” יחידה—גישה מקומית בלבד, ללא ריבוי משתמשים.
* **6.3.2** Future-Proof: תכנון סכמטי לרולס (Admin / Operator / Viewer).

  * *Admin*: ניהול חיבור, מדיניות, מחיקת נתונים.
  * *Operator*: יצירת פוסטים/תזמונים, פרסום.
  * *Viewer*: צפייה בלוגים/סטטוסים בלבד.
* **6.3.3** Session UI Lock: אפשרות “נעילת מסך” מקומית (PIN קצר) לפני פעולות רגישות (Disconnect/Import/Run-Now).

**קריטריוני קבלה**:

* ניתן לשדרג בקלות לריבוי משתמשים מבלי לשבור את ה-API/DB.
* פעולות רגישות מבקשות אישור נוסף (modal עם תקציר סיכון).

---

## 6.4 אבטחת API (Server)

**משימת-על 6.4 — שכבת הגנה ב-Express**

* **6.4.1** CORS מצומצם: הרשאה לדומיין המקומי/המוכר בלבד.
* **6.4.2** Rate-Limit: הגבלת קריאות לנתיבים רגישים (`/auth/*`, `/posts/:id/publish-now`, `/schedules/run-now`).
* **6.4.3** Body & Upload Limits: מגבלת גודל (MB), סינון סיומות (whitelist), MIME sniffing, דחייה של Path Traversal.
* **6.4.4** ולידציות שיטתיות: Zod/Yup לכל בקשה (כולל `facebook.com/...` עבור Groups).
* **6.4.5** CSRF (אם דפדפן משותף): שימוש ב-SameSite Cookies או CSRF Token בהתאם לארכיטקטורה.
* **6.4.6** Error-Handler אחיד: החזרת שגיאות אחידות (code/message/details) מבלי לחשוף מידע רגיש.

**קריטריוני קבלה**:

* בדיקות Smoke של CORS/Rate-Limit/Upload מיד מחזירות תגובה צפויה.
* ולידציות קלט חוסמות URL לא תקף, קבצים אסורים וגופים ריקים.

---

## 6.5 נתונים וקבצים (DB/Storage)

**משימת-על 6.5 — היגיינת נתונים**

* **6.5.1** שמירת DB: UTC ב-DB, הצגה ב-Asia/Jerusalem; מפתחי זמן עם אינדקסים.
* **6.5.2** אחסון מדיה: ספריית storage מאובטחת; שמות קבצים “מנוקים”; אין דריסת קבצים בשמות זהים (הוספת מזהה).
* **6.5.3** מחיקות: Soft-Delete לישויות ניהוליות (אופציונלי), Log Audit במידת הצורך.
* **6.5.4** מניעת כפילויות: Fingerprint (hash) ל-Post/Media; Idempotency Window 24h בקשר Post×Group.

**קריטריוני קבלה**:

* ניסיון לשמירת Group עם URL כפול—נכשל.
* העלאת קובץ פסול—נחסמת עם הודעת שגיאה בהירה.

---

## 6.6 לוגים וטלמטריה

**משימת-על 6.6 — מדיניות לוגים בטוחה ושקופה**

* **6.6.1** רמות: `info` כברירת מחדל; `debug` זמני בלבד עם TTL/רוטציה.
* **6.6.2** רידקציה: הסתרת סודות (Tokens/Cookies) ואובפסקציה של מזהים רגישים.
* **6.6.3** TTL & Rotation: ניקוי לוגים בני 90 ימים (או ערך ENV), רוטציה לפי גודל/זמן.
* **6.6.4** תוכן: `event` קצר + `message` תמציתי + `meta_json` לעומק (stack/fb-error/selector).
* **6.6.5** יצוא CSV: רק שדות “נקיים”—ללא מידע רגיש.

**קריטריוני קבלה**:

* אין סודות בלוגים; בדיקות אוטומטיות שוללות טקסט ברור של Cookies/Headers.

---

## 6.7 תזמון, Backoff, ו-Quiet Hours

**משימת-על 6.7 — בטיחות זמן הרצה**

* **6.7.1** Backoff מדורג: 2m → 5m → 10m, מספר ניסיונות מקסימלי בקונפיג.
* **6.7.2** Spacing/Jitter: השהיה אקראית בין פרסומים לקבוצות (טווח ב-ENV).
* **6.7.3** Quiet Hours (אופציונלי): חלון שעות בהן לא מפרסמים; משימות נדחות אוטומטית.
* **6.7.4** Timeout Guard: משימות running > 30 דק׳ → נכשלות כ-Timeout.

**קריטריוני קבלה**:

* ניסיון חוזר לאחר Rate-Limit מתועד כנדרש; אין “לולאות אין-סופיות”.
* “שעת שקט” מונעת פרסום ומעדכנת סטטוס Pending עם סיבת דחייה.

---

## 6.8 הגנות UX מפני טעויות אנוש

**משימת-על 6.8 — “מנע טעויות לפני שהן קורות”**

* **6.8.1** Confirmations: פרסום המוני/Run-Now/מחיקות—תמיד עם חלון אישור.
* **6.8.2** Preview מחייב: לפני “פרסם עכשיו”—תצוגה מקדימה.
* **6.8.3** CRON Validator: הצגת 5 מועדים עתידיים לפני שמירה.
* **6.8.4** Duplicate Warning: אזהרת כפילות (24h) בזמן בחירת קבוצות.
* **6.8.5** Health Mode: 3 כשלים רצופים מסוג AUTH → עצירת פרסומים והצגת באנר.

**קריטריוני קבלה**:

* לא ניתן “בטעות” לפרסם שוב ושוב; האזהרות ברורות ומעשיות.

---

## 6.9 התאמה למדיניות פלטפורמה (שקיפות משפטית)

**משימת-על 6.9 — שימוש אחראי בפייסבוק**

* **6.9.1** שימוש בחשבון של המשתמש עצמו; לא משתפים סשנים לצדדים שלישיים.
* **6.9.2** הימנעות מעקיפת מנגנוני אבטחה/זיהוי בוטים.
* **6.9.3** כיבוד תנאי פלטפורמה: קצבי פרסום סבירים, תוכן שאינו מפר מדיניות.
* **6.9.4** Traceability: כל פעולה היא אנושית-בפיקוח (Always-Visible Browser).

**קריטריוני קבלה**:

* אין פעולות Headless או הסתרה; כל פרסום נראה לעין וניתן לביטול.

---

## 6.10 התאוששות מאסון וגיבויים

**משימת-על 6.10 — DR & Backup**

* **6.10.1** גיבוי DB יומי (מוצפן), שמור לנתיב מאובטח מקומי/רשת.
* **6.10.2** בדיקות שחזור חודשיות: שחזור DB/Session בסביבת בדיקה.
* **6.10.3** Manual Runbook: מסמך “צעדי שחזור” מודפס/מקומי.

**קריטריוני קבלה**:

* ניתן לשחזר סביבת עבודה מלאה בזמן קצר (SLO פנימי).

---

## 6.11 משתני סביבה (Placeholders; למלא ידנית)

* **אפליקציה**: `PORT`, `NODE_ENV`, `LOG_LEVEL`
* **DB**: `DATABASE_URL`
* **Scheduling**: `SCHED_TIMEZONE=Asia/Jerusalem`, `SCHED_POLL_INTERVAL_MS`, `SCHED_MAX_PARALLEL`, `SCHED_MAX_GROUPS_PER_MINUTE`, `SCHED_SPACING_MIN_MS`, `SCHED_SPACING_MAX_MS`, `SCHED_BACKOFF_STEPS="120000,300000,600000"`, `SCHED_IDEMPOTENCY_HOURS=24`, `SCHED_TIMEOUT_MS=1800000`, `QUIET_HOURS="23:00-07:00"` (אופציונלי)
* **Sessions**: `SESSION_DIR`, `SESSION_FILE="session.enc"`, `FB_SESSION_KEY_SOURCE`
* **Uploads**: `MAX_MEDIA_MB`, `ALLOWED_MEDIA="jpg,png,mp4"`

> תזכורת: `.env` לא נכנס ל-git. לשתף רק `.env.example` עם placeholders.

---

## 6.12 קריטריוני קבלה כוללים (שלב 6)

* סשן פייסבוק מוצפן בקובץ, ניהול Export/Import/Disconnect בטוח.
* דפדפן תמיד גלוי, אין מצב Headless.
* CORS/Rate-Limit/Validations/Uploads—מוגדרים ועוברים בדיקות Smoke.
* לוגים ללא סודות, עם TTL/רוטציה פעילים.
* Backoff/Spacing/Idempotency/Timeout/Quiet Hours—מוגדרים בפרמטרים ומיושמים תפעולית.
* מסכי אישור/אזהרות UX במהלכים מסוכנים (Run-Now, Delete, Bulk Publish).
* Runbook שחזור קיים ובדוק.

---

## 6.13 “מלכודות” שכדאי להימנע מהן

* שמירת סשן ב-DB או ב-git.
* הפעלת דפדפן Headless מטעמי “נוחות”—פוגע בשקיפות ומסכן את החשבון.
* לוגים מפורטים מדי עם מזהים/Headers.
* הגדרות CRON לא-נבדקות.
* קצב פרסום אגרסיבי שאינו “אנושי”.

---
שלב 7 — לוגים ודוחות (Observability & Reporting)
🎯 מטרות

לתעד כל ניסיון/פעולה (publish attempt, success, fail, auth issue, ui changed וכו’) באופן עקבי, קריא ומסונן מפרטים רגישים.

לספק מסך לוגים אפקטיבי עם פילטרים, חיפוש חכם, קיבוץ לפי פוסט/קבוצה/זמן, וייצוא CSV.

להפיק דוחות ביצועים (KPI) לרמת פוסט/קבוצה/חלון זמן — כדי לשפר החלטות ותזמונים.

7.0 טקסונומיית אירועים ורמות חומרה

משימת־על 7.0 — סטנדרט לוגים אחיד

7.0.1 סוגי אירועים (event):
publish_attempt, success, fail, auth_issue, ui_changed, rate_limited, duplicate_skipped, worker_start, worker_stop, schedule_locked, timeout, validation_error, import_groups, export_groups.

7.0.2 רמות חומרה (level): info, warn, error.

success → info;

fail/auth_issue/ui_changed/timeout → error;

rate_limited/duplicate_skipped → warn.

7.0.3 סטטוס תוצאה (outcome): ok, partial, failed.

קריטריוני קבלה: כל רשומה מכילה event, level, outcome עקביים לפי כללים לעיל.

7.1 סכמת לוג (שדות חובה)

משימת־על 7.1 — חוזה נתונים ללוג

7.1.1 שדות חובה בכל לוג:
id, created_at (UTC), event, level, outcome,
message (קצר ומובן),
post_id?, group_id?, schedule_id?,
attempt_no? (מס’ ניסיון),
duration_ms?,
meta_json? (פרטים טכניים: selector strategy, http status, stack, link לפוסט אם קיים).

7.1.2 רידקציה/שמירה על פרטיות:
אין שמירת Cookies/Headers/Access Tokens; אין נתוני התחברות; אין טקסט חופשי שעלול להכיל סודות.

7.1.3 אינדקסים מומלצים:
(created_at), (event, created_at), ו־ (group_id, created_at).

קריטריוני קבלה: שאילתות נפוצות (לפי טווח זמן/קבוצה/אירוע) רצות מהר; אין שדות רגישים.

7.2 מדיניות אגירה (Retention) ורוטציה

משימת־על 7.2 — TTL וניקוי

7.2.1 TTL ברירת מחדל: 90 יום.

7.2.2 רוטציה לפי גודל/ותק (מה שמגיע קודם).

7.2.3 ארכוב מרצון: ייצוא ל־CSV/JSON לפני ניקוי, לפי בחירת המשתמש.

7.2.4 רמת debug זמנית בלבד (כיבוי אוטומטי לאחר X שעות).

קריטריוני קבלה: בסיס הנתונים לא גדל ללא שליטה; ניקוי תקופתי מאומת.

7.3 מסך “לוגים”

משימת־על 7.3 — UI אפקטיבי ללוגים

7.3.1 טבלה: תאריך/שעה (מומר ל־Asia/Jerusalem), אירוע, קבוצה, פוסט (קישור לשורת תקציר), תוצאה (✔/❌/⚠), הודעה קצרה, “לפרטים”.

7.3.2 פילטרים: טווח תאריכים, סוג אירוע, תוצאה, קבוצה, פוסט.

7.3.3 חיפוש חופשי (message + חיפוש ב־meta_json על מפתחות נפוצים כמו selector, httpStatus).

7.3.4 Paginate 25–50 רשומות; שמירת מצב פילטרים ב־URL.

7.3.5 “לפרטים”: פאנל צד המציג meta_json בצורה קריאה (מפתחות שכיחים בראש, “הצג עוד” לשאר).

7.3.6 ייצוא CSV: מכבד את הפילטרים והחיפוש.

קריטריוני קבלה: מציאת “מחט בערמת שחת” תוך ≤ 10 שניות בעזרת סינון/חיפוש.

7.4 דוחות KPI (Performance Reports)

משימת־על 7.4 — מדדים שימושיים להחלטות

7.4.1 KPI לכל קבוצה:

שיעור הצלחות (Success Rate) בתקופה נבחרת.

זמן ממוצע לפוסט (avg duration_ms).

Top Errors (התפלגות fail לפי סיבה).

7.4.2 KPI לכל פוסט (ב־N קבוצות):

כמה קבוצות הצליחו/נכשלו/Skipped (כפילות/מדיה לא תקינה).

יחס הצלחות/כשלונות.

7.4.3 KPI לפי זמן (Time Series):

הצלחות/כשלונות יומיות, מגמות שבועיות.

7.4.4 מטריקות איכות תזמון:

תזמונים עם done_with_errors>0.

ריכוז “שעות חמות/קרות” (Heatmap) לביצועים טובים.

קריטריוני קבלה: ניתן לזהות “קבוצות בעייתיות” ו”חלונות זמן מיטביים” בלחיצה-שתיים.

7.5 דוח חריגות/בעיות (Operational Alerts)

משימת־על 7.5 — איתותים שממוקדים בבעיה

7.5.1 “מדגיש בעיות”:

3× auth_issue רצופים → המלצה להתחברות מחדש.

עלייה חדה ב־ui_changed → בדיקת selectors.

rate_limited סדרתי → המלצה להרחיב Spacing/Jitter.

7.5.2 סקירת “כפילויות שנמנעו”: ספירה/אחוז מסך הניסיונות.

קריטריוני קבלה: הדשבורד מסמן בבירור מה דורש טיפול מיידי.

7.6 יצוא/שיתוף

משימת־על 7.6 — שקיפות החוצה

7.6.1 CSV לוגים: עמודות סטנדרטיות (תאריך, אירוע, קבוצה, פוסט, תוצאה, הודעה, מזהים).

7.6.2 CSV KPI: טבלאות מסוכמות לפי קבוצה/פוסט/זמן.

7.6.3 חתימת זמן וקונפיג: כל קובץ מלווה כותרת עם טווח התאריכים ומדיניות פילטר.

7.6.4 מסך “ייצוא”: בחירת טווח/פילטרים → קובץ מוכן.

קריטריוני קבלה: קובץ הייצוא “נקי” מפרטים רגישים, וניתן לפתיחה באקסל.

7.7 UX: קריאות ונוחות

משימת־על 7.7 — עיצוב לחקירות מהירות

7.7.1 סימוני צבע עקביים: success ירוק, fail אדום, warn צהוב.

7.7.2 תצוגת “סיבה נפוצה” (chips) לפי קוד/סוג.

7.7.3 קיבוץ מהיר: Toggle “קבץ לפי פוסט” / “קבץ לפי קבוצה”.

7.7.4 “קפיצה לשורה דומה”: הצג לוגים דומים (אותו event+group בשבוע האחרון).

קריטריוני קבלה: חווית ניתוח נעימה; מענה לשאלות “מה השתבש, איפה, ולמה” במהירות.

7.8 בדיקות איכות (QA) ללוגים

משימת־על 7.8 — בדיקות ידניות ואוטומטיות

7.8.1 בדיקת רועשות: אין שיטפון לוגים על פעולות “ירוקות”; יחס סביר בין info/warn/error.

7.8.2 בדיקת סודיות: חיפוש מילות מפתח (cookie/token/authorization) מחזיר 0 תוצאות.

7.8.3 בדיקות עומס: 1,000 רשומות בדקה — המסך נשאר חלק, הפילטרים מגיבים.

7.8.4 בדיקת ייצוא: פותחים ב־Excel, העברית/RTL נשמרת, תאריכים בפורמט נכון.

קריטריוני קבלה: כל בדיקה עוברת ללא חריגות; תיעוד תוצאות נשמר.

7.9 “מלכודות” נפוצות להימנע מהן

לוגים עם טקסט חופשי שמכילים סודות.

meta_json “ענקי” שמכביד על UI/DB (הכניסו רק מה שצריך).

היעדר פילטרים/חיפוש — גורם למסך בלתי שימושי.

חוסר אחידות בשמות אירועים/שדות — מקשה על דוחות.

CSV בלי הקשר (טווח/פילטרים) — קשה להבין בדיעבד.

7.10 קריטריוני קבלה כוללים (שלב 7)

טקסונומיה אחידה לאירועים ורמות חומרה.

סכמת לוג מלאה עם שדות חובה, אינדקסים, ורידקציה.

מסך לוגים עם פילטרים, חיפוש, פירוט, וייצוא CSV.

דוחות KPI לפי קבוצה/פוסט/זמן, כולל מדדי איכות תזמון.

מדיניות TTL/רוטציה פעילה; אין סודות בלוגים.

יכולת לאתר חריגות (auth/ui/rate limit/duplicate) ולטפל בהן.
שלב 8 — UX מתקדם, מנגנוני בטיחות וחוויית שימוש
8.0 מטרות

לחזק את חוויית המשתמש מסוף־סוף: זרימות בטוחות, אזהרות חכמות, סטטוסים בזמן אמת, ונראות גבוהה של מה המערכת עושה.

לצמצם טעויות אנוש (פרסום כפול/CRON שגוי/מדיה לא תקינה) ולתעדף פידבק מיידי וברור.

8.1 Validate-CRON אינטראקטיבי

משימת־על 8.1 — תצוגה וולידציה לפני שמירה

8.1.1 שדה CRON + כפתור “בדוק CRON”.

8.1.2 הצגת 5 מועדי ריצה הבאים לפי ה־timezone הנבחר (ברירת מחדל Asia/Jerusalem).

8.1.3 התראות בזמן אמת: CRON לא תקין → הודעה מפורטת + דוגמאות תקינות.

8.1.4 “החלף לתבנית מוכנה”: כפתורי קיצור (יומי/שבועי/מותאם) שממלאים CRON ולצידם ה־next runs.

קריטריוני קבלה: לא ניתן לשמור תזמון חוזר עם CRON לא תקין; המשתמש רואה בבירור מתי זה ירוץ.

8.2 מנגנון Duplicate-Guard (כפילויות) בצד לקוח

משימת־על 8.2 — אזהרה לפני שליחה

8.2.1 חיווי בזמן בחירת קבוצות: “התוכן הזה פורסם בקבוצה X ב־24 השעות האחרונות”.

8.2.2 Toggle “דלג על קבוצות כפולות” (ברירת מחדל דלוק) + הערת הסבר.

8.2.3 לפני “פרסם עכשיו”: סיכום קבוצות שיידלגו מול קבוצות שיתפרסמו.

8.2.4 תיוג ברשימת תוצאות: duplicate_skipped.

קריטריוני קבלה: לא תתבצע שליחה לקבוצות שסומנו ככפולות כאשר הטוגל פעיל; האזהרה בולטת ומובנת.

8.3 “Run-Now” בטוח

משימת־על 8.3 — אישור כפול עם הקשר

8.3.1 כפתור Run-Now זמין רק כאשר יש חיבור FB תקין והמשימה לא Running.

8.3.2 מודל אישור: מציג את שם הפוסט, מספר הקבוצות, שעת הריצה, מדיניות Idempotency.

8.3.3 טוגל “כבדוק כפילויות לפני פרסום (מומלץ)”.

8.3.4 סיכום תוצאות בסוף הריצה + קישור מהיר למסך לוגים מסונן למשימה זו.

קריטריוני קבלה: אי אפשר להריץ בטעות; המשתמש מבין מה יקרה ומתי.

8.4 Pause / Resume ל-Worker מרמת UI

משימת־על 8.4 — בקרה מבוזרת

8.4.1 מתג גלובלי בדשבורד: Pause/Resume.

8.4.2 חיווי מצב: “Worker בפעולה” / “עצור (Paused)”.

8.4.3 בעת Pause: כל משימות pending ממשיכות להיות מוצגות, אך לא יתחילו עד Resume.

8.4.4 מוגן בהרשאה (בעתיד Roles): Pause/Resume דורש אישור.

קריטריוני קבלה: ברור למשתמש מתי worker פעיל; אין ריצות חדשות בזמן Pause.

8.5 Health-Mode Banner (כשלים עקביים)

משימת־על 8.5 — התרעה מבוססת חוקים

8.5.1 תנאי הפעלה: ≥3 כשלים רצופים מסוג auth_issue או עלייה חדה ב־ui_changed.

8.5.2 באנר קבוע בראש הדשבורד: מסביר את הבעיה + CTA: “פתח התחברות מחדש” / “בדוק selectors”.

8.5.3 השתקה זמנית (Dismiss 24h) עם רישום בלוג.

קריטריוני קבלה: המשתמש לא מפספס בעיות מערכתיות; יש פעולה מיידית מוצעת.

8.6 UX למדיה: Pre-flight לפני העלאה

משימת־על 8.6 — בדיקות לפני שליחה

8.6.1 הצגת מגבלות: סיומות מותרות, גודל מקס’, כמות קבצים.

8.6.2 בדיקת גודל/סיומת מקומית לפני שליחה; שגיאות נקיות (מה לא עבר ולמה).

8.6.3 תצוגת ממוזערים (אם רלוונטי) + אפשרות הסרה מהירה.

קריטריוני קבלה: משתמש לא “נתקע” באמצע פרסום על מדיה פסולה; מקבל פידבק מוקדם.

8.7 Groups Import/Export UX

משימת־על 8.7 — העלאה בטוחה ומונחית

8.7.1 תבנית CSV לדוגמה להורדה.

8.7.2 מסך Import: תצוגת Preview של 10 רשומות ראשונות + ספירה של כפולות/שגויים.

8.7.3 כללי ניקוי URL (הסרת פרמטרים זמניים) והבלטת כפילויות שיימנעו.

8.7.4 Export: כולל שדות קיימים + timestamp וטווח פילטר.

קריטריוני קבלה: טעינות קבוצות קלות וללא “זבל”; כפילויות לא נכנסות.

8.8 Empty States, Skeletons ו-Toasts

משימת־על 8.8 — חוויה נקייה גם כשאין נתונים

8.8.1 Empty States: מסרים קצרים עם CTA ברור (הוסף קבוצה/צור פוסט ראשון).

8.8.2 Skeletons בטעינה (טבלאות/כרטיסים) כדי למנוע “קפיצות מסך”.

8.8.3 Toasts לפעולות מהירות (נשמר/ייבוא הצליח/תוזמן בהצלחה) עם אפשרות Undo כשאפשר.

קריטריוני קבלה: אין מסכים “מתים”; המשתמש תמיד מבין מה הצעד הבא.

8.9 Tooltips ועזרה בהקשר

משימת־על 8.9 — מיקרו-קופי מסביר

8.9.1 Tooltips לשדות רגישים (CRON, Idempotency, Backoff, Spacing).

8.9.2 קישור “למד עוד” למסמך עזרה פנימי (דף Settings → Help).

8.9.3 מונחים בעברית/אנגלית (למשל CRON) עם הגדרה קצרה.

קריטריוני קבלה: המשתמש מרגיש “מוחזק ביד” בנקודות המבלבלות.

8.10 התאמות נגישות ו-RTL

משימת־על 8.10 — AA מינימום

8.10.1 ניגודיות כפתורים/טקסט; פוקוס נראה למקלדת.

8.10.2 סדר טאב לוגי; ARIA לתגובות מצב (success/fail).

8.10.3 RTL מלא: תאריכים, כפתורי ניווט, טבלאות מיושרות נכון.

קריטריוני קבלה: שימוש מלא במקלדת אפשרי; טקסטים קריאים; RTL “יושב” נקי.

8.11 ביצועים ועמידות

משימת־על 8.11 — Performance Budget

8.11.1 פגינציה ברירת מחדל 25–50; חיפוש/פילטר בצד שרת.

8.11.2 Debounce בחיפושים; שמירת מצב פילטרים ב־URL.

8.11.3 טיפול חכם ב־meta_json גדול: תקציר + “הצג עוד”.

קריטריוני קבלה: המסכים נשארים חלקים גם עם אלפי לוגים/קבוצות.

8.12 התראות “שעת שקט” ו-Timezone

משימת־על 8.12 — UX ברור לזמני ריצה

8.12.1 טיימזון גלובלי בתצוגה (ברירת מחדל Asia/Jerusalem) עם אופציה לשינוי.

8.12.2 אם מוגדרות Quiet Hours — אזהרה בעת תזמון בתוך החלון + הצעת דחייה אוטומטית.

8.12.3 חיווי “הכול יוצג לפי הזמן המקומי שלך”.

קריטריוני קבלה: אין הפתעות בזמנים; המערכת שקופה לגבי עיכובים מכוונים.

8.13 ניהול מצב (State) מתחשב משתמש

משימת־על 8.13 — קטיעת עבודה בטוחה

8.13.1 שמירת טיוטות מקומית (draft autosave) לעריכת פוסט.

8.13.2 שחזור טיוטה לאחר ריענון/ניתוק רשת.

8.13.3 סנכרון עדין בין טאבים פתוחים (התראה אם שני חלונות עורכים אותו פוסט).

קריטריוני קבלה: לא “מאבדים” עבודה באמצע; אין התנגשויות שקטות.

8.14 דיווח שגיאות ידידותי

משימת־על 8.14 — שפה אנושית

8.14.1 מודלי שגיאה עם “מה קרה” + “מה אפשר לעשות עכשיו” + “הצג פרטים טכניים”.

8.14.2 קישור מהיר ללוגים הרלוונטיים.

8.14.3 קודים עקביים (למשל AUTH_REQUIRED, UI_CHANGED, RATE_LIMITED).

קריטריוני קבלה: המשתמש לא נשאר חסר אונים; תמיד יש צעד מתקדם.

8.15 קריטריוני קבלה כוללים (שלב 8)

Validate-CRON ברור עם תצוגת Next Runs; מניעת שמירת CRON שגוי.

Duplicate-Guard פעיל כבר בשלב בחירת הקבוצות ובסיכום השליחה.

Run-Now מלווה באישור כפול ותצוגת הקשר.

Pause/Resume גלובלי עובד עם חיווי מצב.

Health-Mode מופיע בזמן כשלים עקביים עם CTA לפתרון.

UX למדיה מונע כשלים מאוחרים; ייבוא/ייצוא קבוצות בטוח.

Empty States/Skeletons/Toasts הופכים את ההתנהגות לברורה.

נגישות ו-RTL מדויקים; ביצועים נשמרים בעומס.