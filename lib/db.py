# -*- encoding: utf-8 -*-
import lib.util
import MySQLdb as mysql
import os
import logging
from lib.log import log
from config.views import get_dir
#
# level = get_dir("log_level")
# log_path = get_dir("log_path")
# log("db.log", level, log_path)


class Cursor(object):
    def __init__(self, config):
        self.config = config
        if 'port' in config:
            self.config['port'] = int(self.config['port'])
        if self.config:
            self._connect_db()

    def _connect_db(self):
        self.db = mysql.connect(**self.config)
        self.db.autocommit(True)
        self.cur = self.db.cursor()

    def _close_db(self):
        self.cur.close()
        self.db.close()

    def _execute(self, sql):
        logging.info(sql);
        try:
            return self.cur.execute(sql)
        except:
            self._close_db()
            self._connect_db()
            return self.cur.execute(sql)

    def _fetchone(self):
        return self.cur.fetchone()

    def _fetchall(self):
        return self.cur.fetchall()

    def _insert_sql(self, table_name, data):
        fields, values = [], []
        for k, v in data.items():
            fields.append(k)
            values.append("'%s'" % v)
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ','.join(fields), ','.join(values))
        # util.write_log('api').info("Insert sql: %s" % sql)
        return sql

    def execute_insert_sql(self, table_name, data):
        # try:
        sql = self._insert_sql(table_name, data)
        if not sql:
            return None
        return self._execute(sql)

    def execute_insert_sql1(self, table_name, ip_value):
        # try:
        sql = "INSERT INTO %s (ip) VALUES ('%s')" % (table_name, ip_value)
        print(sql)
        if not sql:
            return None
        return self._execute(sql)


    # except:
    # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))

    def execute_clean_sql(self, table_name):
        # try:
        sql = "truncate %s" % (table_name)
        return self._execute(sql)

    # except:
    # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))

    def _select_sql(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        if isinstance(where, dict) and where:
            conditions = []
            for k, v in where.items():
                if isinstance(v, list):
                    conditions.append("%s IN (%s)" % (k, ','.join(v)))
                elif isinstance(v, str) or isinstance(v, unicode):
                    conditions.append("%s='%s'" % (k, v))
                elif isinstance(v, int):
                    conditions.append("%s=%s" % (k, v))

            sql = "SELECT %s FROM %s WHERE %s" % (','.join(fields), table_name, ' AND '.join(conditions))
        elif not where:
            sql = "SELECT %s FROM %s" % (','.join(fields), table_name)
        else:
            sql = ""
        if order and (isinstance(order, str) or isinstance(order, unicode)):
            sql = "%s ORDER BY %s %s" % (sql, order, 'ASC' if asc_order else 'DESC')
        if limit and isinstance(limit, tuple) and len(limit) == 2:
            sql = "%s LIMIT %s,%s" % (sql, limit[0], limit[1])
        # util.write_log('api').info("Select sql: %s" % sql)
        return sql

    def get_one_result(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        try:
            sql = self._select_sql(table_name, fields, where, order, asc_order, limit)
            if not sql:
                return None
            self._execute(sql)
            result_set = self._fetchone()
	    logging.info(result_set)
            return dict([(k, '' if result_set[i] is None else result_set[i]) for i, k in enumerate(fields)])
        except:
            # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))
            return {}

    def get_results(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        try:
            sql = self._select_sql(table_name, fields, where, order, asc_order, limit)
            self._execute(sql)
            result_sets = self._fetchall()
            return [dict([(k, '' if row[i] is None else row[i]) for i, k in enumerate(fields)]) for row in result_sets]
        except:
            # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))
            return []

    def get_where_results(self, table_name, fields, where):
        try:
            for k, v in where.items():
                sql = "SELECT %s FROM %s WHERE %s=%s" % (','.join(fields), table_name, k, v)
                self._execute(sql)
                result_sets = self._fetchall()
                return [dict([(k, '' if row[i] is None else row[i]) for i, k in enumerate(fields)]) for row in
                        result_sets]
        except:
            # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))
            return []

    def _update_sql(self, table_name, data, where, fields=None):
        if not (where and isinstance(where, dict)):
            return ""
        where_cond = ["%s='%s'" % (k, v) for k, v in where.items()]
        if fields:
            conditions = ["%s='%s'" % (k, data[k]) for k in fields]
        else:
            conditions = ["%s='%s'" % (k, data[k]) for k in data]
        sql = "UPDATE %s SET %s WHERE %s" % (table_name, ','.join(conditions), ' AND '.join(where_cond))
        # util.write_log('api').info("Update sql: %s" % sql)
        return sql

    def execute_update_sql(self, table_name, data, where, fields=None):
        # try:
        sql = self._update_sql(table_name, data, where, fields)
        if sql:
            return self._execute(sql)

    # except:
    # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))

    def _delete_sql(self, table_name, where):
        if not (where and isinstance(where, dict)):
            return ""
        where_cond = ["%s='%s'" % (k, v) for k, v in where.items()]
        sql = "DELETE FROM %s WHERE %s" % (table_name, ' AND '.join(where_cond))
        # util.write_log('api').info("Delete sql: %s" % sql)
        return sql

    def execute_delete_sql(self, table_name, where):
        # try:
        sql = self._delete_sql(table_name, where)
        if sql:
            return self._execute(sql)

    # except:
    # util.write_log('api').error("Execute '%s' error: %s" % (sql, traceback.format_exc()))

    def if_id_exist(self, table_name, field_id):
        if isinstance(field_id, list):
            id_num = len(field_id)
            result = self.get_results(table_name, ['id'], {'id': field_id})
            if id_num != len(result):
                result = False
        else:
            result = self.get_one_result(table_name, ['id'], {'id': field_id})
        if result:
            return True
        else:
            # util.write_log('api').error("%s '%s' is not exist" % (table_name,field_id))
            return False

    def getinfo(self, table_name, fields):
        '''

        查询单个数据表内容，fields首字段为key
        fields为两个字段，返回{v1: v2, ...}，格式为 ['field1','field2'], 例如['id','name'],['name','r_id']
        返回结果一，两列都是字符串如：用户id2name {'1':'tom','2','jerry'}; 组信息id2name {'1':'sa','2':'ask'}
        返回结果二，第二列是个列表如：用户权限信息：{u'songpeng': [u'1', u'2'], u'admin': [u'1', u'2', u'4', u'3']}

        '''
        result = Cursor(
            lib.util.get_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'service.conf'),
                                        'api')).get_results(table_name, fields)
        if fields[1] in ['r_id', 'p_id', 'user_all_perm']:  # 第二列的结果为列表的字段拼接为字符串
            result = dict((str(x[fields[0]]), x[fields[1]].split(',')) for x in result)
        else:
            result = dict((str(x[fields[0]]), x[fields[1]]) for x in result)
        return result

    @property
    def users(self):
        return self.getinfo('user', ['id', 'username'])

    @property
    def groups(self):
        return self.getinfo('user_group', ['id', 'name'])

    @property
    def user_groups(self):
        return self.getinfo('user', ['id', 'r_id'])

    @property
    def projects(self):
        return self.getinfo('project', ['id', 'name'])

    @property
    def project_perms(self):
        return self.getinfo('project', ['id', 'user_all_perm'])


if __name__ == '__main__':
    # host = get_dir("log_level")
    # port = get_dir("log_level")
    # level = get_dir("log_level")
    # level = get_dir("log_level")
    # level = get_dir("log_level")
    # level = get_dir("log_level")
    # level = get_dir("log_level")
    # config = {""}
    # db = Cursor()
    lib.util.get_config("../conf")