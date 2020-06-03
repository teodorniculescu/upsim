#!/bin/bash

mariadb -B -u upsim -p -D upsimdb --disable-column-names --execute "SELECT CONCAT('DROP TABLE IF EXISTS \`', TABLE_SCHEMA, '\`.\`', TABLE_NAME, '\`;') FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'upsimdb';" > remove_all.sql

mariadb -u upsim -p -D upsimdb < remove_all.sql

rm remove_all.sql

