from django.db import connection


def run_query(sql, params=None):
    with connection.cursor() as cur:
        cur.execute(sql, params or [])
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def overdue_books():
    return run_query("""
        SELECT m.name AS member, b.title AS book, i.due_date
        FROM library_issue i
        JOIN library_member m ON m.id = i.member_id
        JOIN library_book b ON b.id = i.book_id
        WHERE i.return_date IS NULL AND i.due_date < CURDATE()
    """)


def popular_books():
    return run_query("""
        SELECT b.title, COUNT(*) AS times_issued
        FROM library_issue i
        JOIN library_book b ON b.id = i.book_id
        GROUP BY b.id, b.title
        ORDER BY times_issued DESC
        LIMIT 5
    """)


def top_members():
    return run_query("""
        SELECT m.name, COUNT(*) AS total_issues
        FROM library_issue i
        JOIN library_member m ON m.id = i.member_id
        GROUP BY m.id, m.name
        HAVING COUNT(*) >= 2
        ORDER BY total_issues DESC
    """)