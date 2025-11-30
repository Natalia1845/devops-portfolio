#!/bin/bash
# ==========================
# 🔹 System Monitoring Script with Discord Alerts
# ==========================

# ==== Discord Webhook URL ====
WEBHOOK_URL="https://discord.com/api/webhooks/1416869719696474132/rUDxHHIlhiJAqS5mrNw7Mc9kX8sC8apYgCVbB5etu0ScpR4soIIDo5zZovLYzR3Nvwyr"

# ==== Пороги ====
CPU_THRESHOLD=80
RAM_THRESHOLD=80
DISK_THRESHOLD=90

# ==== Отримання даних ====
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
RAM_USAGE=$(free | grep Mem | awk '{printf("%.0f", ($3/$2)*100)}')
DISK_USAGE=$(df --output=pcent / | tail -n1 | tr -d '% ')

# ==== Вивід для перевірки ====
echo "CPU: ${CPU_USAGE}%"
echo "RAM: ${RAM_USAGE}%"
echo "Disk: ${DISK_USAGE}%"

# ==== Функція надсилання повідомлення ====
send_alert() {
    local message=$1
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\": \"$message\"}" \
         "$WEBHOOK_URL" > /dev/null 2>&1
}

# ==== Перевірка порогів ====
if (( ${CPU_USAGE%.*} > CPU_THRESHOLD )); then
    send_alert "⚠️ High CPU usage: ${CPU_USAGE}% (Threshold: ${CPU_THRESHOLD}%)"
fi

if (( ${RAM_USAGE%.*} > RAM_THRESHOLD )); then
    send_alert "⚠️ High RAM usage: ${RAM_USAGE}% (Threshold: ${RAM_THRESHOLD}%)"
fi

if (( ${DISK_USAGE%.*} > DISK_THRESHOLD )); then
    send_alert "⚠️ High Disk usage: ${DISK_USAGE}% (Threshold: ${DISK_THRESHOLD}%)"
fi

echo "✅ System check completed at $(date '+%Y-%m-%d %H:%M:%S')"
