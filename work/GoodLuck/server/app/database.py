
from . import config
from .api.mysql_pymysql import DatabaseConfig, ClassManagementSystem
from .api import opengauss

# 创建系统实例
Mysql = ClassManagementSystem(config.MySql_db_config)
OpenGauss=opengauss.ClassManagementSystem(config.OG_db_config)
# print(system.user_manager.get_all_users())

# 初始化数据库
# print("正在初始化数据库...")

# print("✅ 数据库初始化成功！")



def get_db(db='mysql'):
    if db == 'mysql':
        if not Mysql.initialize():
            print("❌ 数据库初始化失败！请检查MySQL连接配置。")
            exit(1)

        return Mysql
    elif  db == 'opengauss':
        if not OpenGauss.initialize():
            print("❌ 数据库初始化失败！请检查opengauss连接配置。")
            exit(1)
        return OpenGauss
    return None



