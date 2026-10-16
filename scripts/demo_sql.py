"""Execute the supplied SQL examples against the real database, read-only."""
from pathlib import Path
import csv
import io
import json
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import validate_core_outputs

def main():
    validate_core_outputs(ROOT)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    database = ROOT / 'outputs/real_estate.sqlite'
    benchmark = json.loads((ROOT / 'outputs/sql_benchmark.json').read_text(encoding='utf-8'))
    sql_text = (ROOT / 'sql/02_queries.sql').read_text(encoding='utf-8')
    sql_text = '\n'.join(line for line in sql_text.splitlines() if not line.lstrip().startswith('--'))
    statements = [q.strip() for q in sql_text.split(';') if q.strip()]
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as connection:
        for i, query in enumerate(statements, start=1):
            params = benchmark['parameters'] if '?' in query else ()
            cursor = connection.execute(query, params)
            rows = cursor.fetchall()
            print(f'\nTruy vấn {i} · {len(rows)} dòng · hiển thị tối đa 20 dòng')
            output = io.StringIO()
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([x[0] for x in cursor.description])
            writer.writerows(rows[:20])
            print(output.getvalue())
        print('Kiểm tra database:', connection.execute('PRAGMA integrity_check').fetchone()[0])

if __name__ == '__main__':
    main()
