# coding:utf-8
from sqlalchemy import create_engine, Integer,String,DateTime,BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT


# 创建数据库的连接
engine = create_engine("mysql://root:abc123456@127.0.0.1:3306/db_taobao?charset=utf8mb4")
# 操作数据库，需要我们创建一个session
Session = sessionmaker(bind=engine)

# 声明一个基类
Base = declarative_base()


# 类别表，tb首页轮播左侧所有类别
class tb_index_category(Base):
    # 表名称
    __tablename__ = 'tb_index_category'
    # 主类别
    main_category = Column(String(length=40))
    # 第二类别
    second_category_name = Column(String(length=10))
    # 类别名称
    category_name = Column(String(length=10))
    # 类别链接
    category_href = Column(String(length=200),primary_key=True)
    # 抓取日期
    crawl_time = Column(DateTime)


# 商品信息表
class tb_goods_info(Base):
    # 表名称
    __tablename__ = 'tb_goods_info'
    # 商品ID
    goods_id = Column(BIGINT, primary_key=True)
    # 商品标题
    title = Column(String(length=100))
    # 商品价格
    price = Column(String(length=15))
    # 卖家所在地
    local = Column(String(length=10))
    # 筛选信息
    v_text = Column(String(length=100))
    # 收货人数
    view_sales = Column(String(length=10))
    # 评论人数
    comment_count = Column(Integer,default=0)
    # 卖家用户ID
    user_id = Column(BIGINT)
    # 卖家昵称
    nick = Column(String(length=30))
    # 商品详情页url
    good_url = Column(LONGTEXT)
    # 主类别
    main_category = Column(String(length=40))
    # 第二类别
    second_category_name = Column(String(length=10))
    # 类别名称
    category_name = Column(String(length=10))
    # 类别链接
    category_href = Column(String(length=200))
    # 抓取日期
    crawl_time = Column(DateTime)


class tb_data(object):
    # 重写父类
    def __init__(self):
        # 实例化session信息
        self.mysql_session = Session()

    # 类别表数据的存储方法
    def index_category_data(self,item):
        # 存储的数据结构
        data = tb_index_category(
            # 主类别
            main_category = item['main_category'],
            # 第二类别
            second_category_name = item['second_category_name'],
            # 类别名称
            category_name = item['category_name'],
            # 类别链接
            category_href = item['category_href'],
            # 抓取日期
            crawl_time = item['crawl_time'],
        )
        # 数据去重
        query_result = self.mysql_session.query(tb_index_category).filter(tb_index_category.category_href==item['category_href']).first()
        if query_result:
            try:
                # 更新数据
                self.mysql_session.query(tb_index_category).filter(tb_index_category.category_href == item['category_href']).update(dict)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('tb_index_category数据表update：%s：%s：%s' % (item['main_category'], item['second_category_name'], item['category_name']))
            except:
                print("该数据入库存在问题：%s" % item)
        else:
            try:
                # 插入数据
                self.mysql_session.add(data)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('tb_index_category数据表add：%s：%s：%s' % (item['main_category'], item['second_category_name'], item['category_name']))
            except:
                print("该数据入库存在问题：%s" % item)

    # 商品信息数据的存储方法
    def goods_data(self, item):
        # 存储的数据结构
        data = tb_goods_info(
            # 商品ID
            goods_id=item['goods_id'],
            # 商品标题
            title = item['title'],
            # 商品价格
            price = item['price'],
            # 卖家所在地
            local = item['local'],
            # 筛选信息
            v_text = item['v_text'],
            # 收货人数
            view_sales = item['view_sales'],
            # 评论人数
            comment_count = item['comment_count'],
            # 卖家用户ID
            user_id = item['user_id'],
            # 卖家昵称
            nick = item['nick'],
            # 商品详情页url
            good_url = item['good_url'],
            # 主类别
            main_category = item['main_category'],
            # 第二类别
            second_category_name = item['second_category_name'],
            # 类别名称
            category_name = item['category_name'],
            # 类别链接
            category_href = item['category_href'],
            # 抓取日期
            crawl_time = item['crawl_time']
        )
        # 数据去重
        query_result = self.mysql_session.query(tb_goods_info).filter(tb_goods_info.goods_id == item['goods_id']).first()
        if query_result:
            try:
                # 更新数据
                self.mysql_session.query(tb_goods_info).filter(tb_goods_info.goods_id == item['goods_id']).update(item)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('tb_goods_info数据表update：%s：%s' % (item['goods_id'], item['title']))
            except Exception as e:
                with open("../tb_log.txt", "a+", encoding="utf-8") as f:
                    f.write("tb_goods_info update ERROR：%s:\n%s" % (item,e))
                f.close()
        else:
            try:
                # 插入数据
                self.mysql_session.add(data)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('tb_goods_info数据表add：%s：%s' % (item['goods_id'], item['title']))
            except Exception as e:
                with open("../tb_log.txt", "a+", encoding="utf-8") as f:
                    f.write("tb_goods_info add ERROR：%s:\n%s" % (item,e))
                f.close()

    # 获取类别信息
    def get_index_category(self):
        query_result = self.mysql_session.query(tb_index_category.category_href,tb_index_category.main_category,tb_index_category.second_category_name,tb_index_category.category_name).all()
        return query_result


tb_mysql = tb_data()


if __name__ == '__main__':
    # 创建数据表
    # tb_index_category.metadata.create_all(engine)
    result =  tb_mysql.get_index_category()
    print(result)