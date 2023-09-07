#!/bin/bash

  # Load environment variables from .env file
  source mysql/.db_env

  # Set variables.
  LATEST_DB_DUMP="latest_db_dump.sql"
  CURRENT_DB_DUMP="current_db_dump.sql"
  DB_NAME=${MYSQL_DB_NAME}

  # Generate filename using machine value and timestamp.
  BACKUP_FILENAME="backup_${MACHINE_VALUE}_$(date +%Y%m%d%H%M).sql.gz"

  # Check if the latest dump file is different from the current one.
  if [ -f $CURRENT_DB_DUMP ] && cmp -s $CURRENT_DB_DUMP $LATEST_DB_DUMP ; then
      echo "Database dump has not changed."
  else
      echo "New database dump found. Restoring..."

      # Try rsync with a dry run first
      rsync --dry-run -avz -e "ssh -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" $SFTP_USER@$SFTP_SERVER:$NEW_DB_REMOTE_PATH/$NEW_DB_NAME $LATEST_DB_DUMP

      exit_status=$?

      if [ $exit_status -ne 0 ]; then
          echo "Failed to connect with rsync, exit status: $exit_status"
          exit $exit_status
      else
          echo "Rsync connection successful. Proceeding..."
      fi

      # Backup current database to SFTP server.
      mysqldump -h db -u"${MYSQL_USER}" -p"${MYSQL_DB_PASSWORD}" "$DB_NAME" | gzip > mysql/back_ups/$BACKUP_FILENAME
      exit_status=$?
      if [ $exit_status -ne 0 ]; then
          echo "mysqldump failed with exit status $exit_status"
          exit $exit_status
      fi

      # Rsync backup to a SFTP server
      rsync -avz --progress -e "ssh -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" mysql/back_ups/$BACKUP_FILENAME $SFTP_USER@$SFTP_SERVER:$BACKUP_REMOTE_PATH/$BACKUP_FILENAME
      exit_status=$?
      if [ $exit_status -ne 0 ]; then
          echo "First rsync failed with exit status $exit_status"
          exit $exit_status
      fi

      # Drop the current database.
      if ! mysql -h db -u"${MYSQL_USER}" -p"${MYSQL_DB_PASSWORD}" -e "DROP DATABASE $DB_NAME"; then
          echo "Error dropping current database."
          exit 1
      fi

      # Create a new database.
      if ! mysql -h db -u"${MYSQL_USER}" -p"${MYSQL_DB_PASSWORD}" -e "CREATE DATABASE $DB_NAME"; then
          echo "Error creating new database."
          exit 1
      fi

      # Rsync the latest dump from SFTP server
      rsync -avz --progress -e "ssh -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" $SFTP_USER@$SFTP_SERVER:$NEW_DB_REMOTE_PATH/$NEW_DB_NAME $LATEST_DB_DUMP
      exit_status=$?
      if [ $exit_status -ne 0 ]; then
          echo "Second rsync failed with exit status $exit_status"
          exit $exit_status
      fi

      # Import the latest database dump into MySQL.
      if ! mysql -h db -u"${MYSQL_USER}" -p"${MYSQL_DB_PASSWORD}" "$DB_NAME" < $LATEST_DB_DUMP; then
          echo "Error importing latest database dump."
          exit 1
      fi

      # Done, so move the latest dump to current.
      mv $LATEST_DB_DUMP $CURRENT_DB_DUMP

      echo "Database restoration complete."
  fi