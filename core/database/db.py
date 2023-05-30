# from core.lib import cfg
#
# MYSQL_USER = cfg.get('MYSQL_USER')
# MYSQL_PASSWORD = cfg.get('MYSQL_PASSWORD')
# MYSQL_SERVER = cfg.get('MYSQL_SERVER')
# MYSQL_DB = cfg.get('MYSQL_DB')
#
# MYSQL_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}'
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
