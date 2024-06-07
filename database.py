from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text, Text, QueuePool
from sqlalchemy.orm import sessionmaker
import config

from sqlalchemy.orm import declarative_base

import utils

Base = declarative_base()


class V2ServerTrojan(Base):
    __tablename__ = 'v2_server_trojan'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='节点ID')
    group_id = Column(String(255), nullable=False, comment='节点组')
    route_id = Column(String(255), nullable=True)
    parent_id = Column(Integer, nullable=True, comment='父节点')
    tags = Column(String(255), nullable=True, comment='节点标签')
    name = Column(String(255), nullable=False, comment='节点名称')
    rate = Column(String(11), nullable=False, comment='倍率')
    host = Column(String(255), nullable=False, comment='主机名')
    port = Column(String(11), nullable=False, comment='连接端口')
    server_port = Column(Integer, nullable=False, comment='服务端口')
    network = Column(String(11), nullable=True, comment='传输方式')
    network_settings = Column(Text, nullable=True, comment='传输配置')
    allow_insecure = Column(Boolean, nullable=False, default=False, comment='是否允许不安全')
    server_name = Column(String(255), nullable=True)
    show = Column(Boolean, nullable=False, default=False, comment='是否显示')
    sort = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<V2ServerTrojan(id={self.id}, name={self.name})>"


class V2ServerVless(Base):
    __tablename__ = 'v2_server_vless'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Text, nullable=False)
    route_id = Column(Text, nullable=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    server_port = Column(Integer, nullable=False)
    tls = Column(Boolean, nullable=False)
    tls_settings = Column(Text, nullable=True)
    flow = Column(String(64), nullable=True)
    network = Column(String(11), nullable=False)
    network_settings = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    rate = Column(String(11), nullable=False)
    show = Column(Boolean, nullable=False, default=False)
    sort = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<V2ServerVless(id={self.id}, name={self.name})>"


class V2ServerVMess(Base):
    __tablename__ = 'v2_server_vmess'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(String(255), nullable=False)
    route_id = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=True)
    host = Column(String(255), nullable=False)
    port = Column(String(11), nullable=False)
    server_port = Column(Integer, nullable=False)
    tls = Column(Boolean, nullable=False, default=False)
    tags = Column(String(255), nullable=True)
    rate = Column(String(11), nullable=False)
    network = Column(String(11), nullable=False)
    rules = Column(Text, nullable=True)
    networkSettings = Column(Text, nullable=True)
    tlsSettings = Column(Text, nullable=True)
    ruleSettings = Column(Text, nullable=True)
    dnsSettings = Column(Text, nullable=True)
    show = Column(Boolean, nullable=False, default=False)
    sort = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<V2ServerVMess(id={self.id}, name={self.name})>"


engine = None
# Example usage
# engine = create_engine('sqlite:///dmm-av-daily.db', echo=True)
if ".db" in config.GlobalConfig.db_connect_url:
    db_url = config.GlobalConfig.db_connect_url
    engine = create_engine(f'sqlite:///{db_url}', echo=True)
    Base.metadata.create_all(engine)
else:
    db_url = config.GlobalConfig.db_connect_url
    db_url = utils.process_atin_dburl(db_url)
    engine = create_engine(f'mysql+mysqlconnector://{db_url}', echo=True,
                           poolclass=QueuePool,
                           pool_size=5,
                           max_overflow=20,
                           pool_timeout=360,
                           pool_pre_ping=True,
                           pool_recycle=3600)

Session = sessionmaker(bind=engine)
session = Session()
