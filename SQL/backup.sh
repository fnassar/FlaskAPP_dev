#  Variables
DB_NAME="sample_db"
CONF_FILE="~/my.cnf"
BACKUP_DIR="backup_directory"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_DIR/backup.log"

mkdir -p $BACKUP_DIR

# Backup file name
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$DATE.sql"

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Starting backup of database '$DB_NAME'" >> $LOG_FILE

export MYSQL_PWD=$(<~/mysql_credentials.txt)

mysqldump -u fanassar -h localhost $DB_NAME > $BACKUP_FILE

unset MYSQL_PWD

if [ $? -eq 0 ]; then
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup successful: $BACKUP_FILE" >> $LOG_FILE
else
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup failed" >> $LOG_FILE
fi

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup process completed" >> $LOG_FILE
