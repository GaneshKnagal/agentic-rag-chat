import pymysql

# === CONFIG ===
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Ganesh55@",  # 🔐 Replace with your actual password
    "database": "rag_demo"
}

def query_documents(keyword=None, agency=None, limit=10, after_date=None):
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "SELECT title, agency_names, publication_date, html_url FROM federal_documents WHERE 1=1"
    params = []

    if keyword:
        # Break keyword into words and match any of them
        words = keyword.lower().split()
        keyword_clauses = " OR ".join(["LOWER(title) LIKE %s OR LOWER(summary) LIKE %s" for _ in words])
        query += f" AND ({keyword_clauses})"
        for w in words:
            like_term = f"%{w}%"
            params.extend([like_term, like_term])

    if agency:
        query += " AND LOWER(agency_names) LIKE %s"
        params.append(f"%{agency.lower()}%")

    if after_date:
        query += " AND publication_date >= %s"
        params.append(after_date)

    query += " ORDER BY publication_date DESC LIMIT %s"
    params.append(limit)

    print(f"\n🔍 Querying: keyword={keyword}, agency={agency}, date>={after_date}, limit={limit}")
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        print("⚠️ No results found.")
    else:
        for i, doc in enumerate(results, 1):
            print(f"\n📄 [{i}] {doc['title']}")
            print(f"   🏢 Agency: {doc['agency_names']}")
            print(f"   📅 Date:   {doc['publication_date']}")
            print(f"   🔗 Link:   {doc['html_url']}")

    conn.close()

# === Try with:
if __name__ == "__main__":
    query_documents(
        keyword="clean energy",
        agency="Energy",
        limit=10,
        after_date="2025-01-01"
    )
