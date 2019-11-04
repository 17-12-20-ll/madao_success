import pymysql

# django默认会用mysqldb连接数据库,这里使用下面带代码,将pymysql换成mysqldb
pymysql.install_as_MySQLdb()
