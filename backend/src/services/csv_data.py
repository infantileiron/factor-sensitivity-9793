import csv,io
def records(text,columns,limit=100):
 reader=csv.DictReader(io.StringIO(text.strip()))
 if reader.fieldnames!=columns:raise ValueError('CSV列须为'+','.join(columns))
 rows=list(reader)
 if len(rows)>limit:raise ValueError('CSV超过行数上限')
 if any(None in row or any(value is None for value in row.values()) for row in rows):raise ValueError('CSV行列不完整')
 return rows
