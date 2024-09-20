FETCH_USER = 'select * from users WHERE id = %s'
FETCH_RECORD = 'select * from records WHERE id = %s'
FETCH_SUMMARY = 'select * from summaries WHERE id = %s'
# FETCH_RECORDS = 'select * from records where id in (%s)'
FETCH_ONE_RECORDS = 'select * from records where id = %s'
FETCH_RECORDS = lambda length: f'select * from records where id in (' + ', '.join(['%s' for _ in range(length)]) + ')'
INSERT_WORKBOOKS = 'insert into workbooks (u_id, title, problem_set) values (%s, %s, %s)'
INSERT_KEYWORDS = lambda rs_id, keywords: f'insert into keywords (rs_id, name) values ' + ', '.join([f'({rs_id}, %s)' for _ in range(len(keywords))])
INSERT_SUMMARIES = 'insert into record_summaries (r_id, summary) values (%s, %s)'

