FROM python:3.9-slim

# התקן dependencies למערכת
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    libxss1 \
    libgconf-2-4 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libcups2 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# הגדר את התיקייה
WORKDIR /app

# העתק requirements תחילה (למען cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# התקן Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# העתק את הקוד
COPY . .

# צור תיקיות נדרשות
RUN mkdir -p data sessions

# הגדר משתני סביבה
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# חשוף פורט
EXPOSE 5000

# הפעל את האפליקציה
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "300", "dashboard:app"]
