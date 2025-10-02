// Application Constants

export const APP_CONFIG = {
  NAME: 'Facebook Automation',
  VERSION: '1.0.0',
  DESCRIPTION: 'מערכת אוטומטית לפרסום פוסטים לפייסבוק עם תזמון וניהול קבוצות',
} as const;

// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:3001',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
} as const;

// Facebook Configuration
export const FACEBOOK_CONFIG = {
  BASE_URL: 'https://www.facebook.com',
  COMPOSER_SELECTORS: [
    '[data-testid="status-attachment-mentions-input"]',
    '[contenteditable="true"][data-testid="status-attachment-mentions-input"]',
    '[role="textbox"]',
    'div[contenteditable="true"]',
  ],
  POST_BUTTON_SELECTORS: [
    '[data-testid="react-composer-post-button"]',
    '[aria-label="פרסם"]',
    '[aria-label="Post"]',
    'button[type="submit"]',
  ],
} as const;

// Scheduling Configuration
export const SCHEDULING_CONFIG = {
  DEFAULT_TIMEZONE: 'Asia/Jerusalem',
  POLL_INTERVAL_MS: 30000, // 30 seconds
  MAX_PARALLEL_JOBS: 1,
  GROUP_SPACING_MIN_MS: 10000, // 10 seconds
  GROUP_SPACING_MAX_MS: 40000, // 40 seconds
  GROUPS_PER_MINUTE: 5,
  RETRY_MAX_ATTEMPTS: 3,
  RETRY_DELAYS_MS: [120000, 300000, 600000], // 2m, 5m, 10m
  DUP_WINDOW_HOURS: 24,
} as const;

// Media Configuration
export const MEDIA_CONFIG = {
  MAX_SIZE_MB: 15,
  ALLOWED_EXTENSIONS: ['jpg', 'jpeg', 'png', 'mp4', 'mov'],
  ALLOWED_MIME_TYPES: [
    'image/jpeg',
    'image/png',
    'video/mp4',
    'video/quicktime',
  ],
} as const;

// Security Configuration
export const SECURITY_CONFIG = {
  SESSION_KEY_SOURCE: 'keytar', // 'keytar' | 'env'
  SESSION_DIR: 'data/storage',
  SESSION_FILE: 'session.enc',
  ENCRYPTION_ALGORITHM: 'aes-256-gcm',
} as const;

// Browser Configuration
export const BROWSER_CONFIG = {
  ENGINE: 'chromium',
  HEADLESS: false, // Always visible for transparency
  USER_DATA_DIR: '.data/chrome-profile',
  NAVIGATION_TIMEOUT_MS: 60000, // 1 minute
  START_MINIMIZED: false,
} as const;

// Logging Configuration
export const LOGGING_CONFIG = {
  LEVEL: 'info', // 'debug' | 'info' | 'warn' | 'error'
  DEBUG_TRACES_ENABLED: false,
  DEBUG_TRACES_TTL_DAYS: 7,
  ROTATION_DAYS: 90,
} as const;

// AI Configuration (Ollama)
export const AI_CONFIG = {
  BASE_URL: 'http://127.0.0.1:11434',
  DEFAULT_MODEL: 'aya:8b',
  FALLBACK_MODELS: ['qwen2.5:7b-instruct', 'gemma2:9b-instruct'],
  DEFAULT_PROMPT: 'כתוב פוסט קצר בעברית לקבוצת פייסבוק של בעלי עסקים קטנים בנושא {topic}, בסגנון חם ולא מכירתי.',
  MAX_TOKENS: 500,
  TEMPERATURE: 0.7,
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  FACEBOOK_NOT_CONNECTED: 'לא מחובר לפייסבוק',
  INVALID_GROUP_URL: 'כתובת קבוצה לא תקינה',
  POST_BODY_REQUIRED: 'תוכן הפוסט נדרש',
  MEDIA_TOO_LARGE: 'קובץ המדיה גדול מדי',
  INVALID_MEDIA_TYPE: 'סוג קובץ לא נתמך',
  SCHEDULE_NOT_FOUND: 'תזמון לא נמצא',
  POST_NOT_FOUND: 'פוסט לא נמצא',
  GROUP_NOT_FOUND: 'קבוצה לא נמצאה',
  AUTH_REQUIRED: 'נדרש אימות מחדש',
  UI_CHANGED: 'ממשק פייסבוק השתנה',
  RATE_LIMITED: 'הוגבל קצב הפרסום',
  DUPLICATE_CONTENT: 'תוכן זהה פורסם לאחרונה',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  POST_CREATED: 'פוסט נוצר בהצלחה',
  POST_PUBLISHED: 'פוסט פורסם בהצלחה',
  GROUP_ADDED: 'קבוצה נוספה בהצלחה',
  SCHEDULE_CREATED: 'תזמון נוצר בהצלחה',
  AUTH_CONNECTED: 'התחברות לפייסבוק הצליחה',
  SCHEDULE_EXECUTED: 'תזמון בוצע בהצלחה',
} as const;
