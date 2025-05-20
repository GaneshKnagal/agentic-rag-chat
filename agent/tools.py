import aiomysql

# 🔁 Normalizes common aliases the model might generate
def normalize_agency(agency: str) -> str:
    aliases = {
        "EPA": "Environmental Protection Agency",
        "Environmental Protection Agency (EPA)": "Environmental Protection Agency",
        "DOE": "Energy Department",
        "Department of Energy": "Energy Department",
        "NOAA": "Commerce Department",
        "National Oceanic and Atmospheric Administration": "Commerce Department",
        "National Oceanic and Atmospheric Administration (NOAA)": "Commerce Department",
        "FAA": "Transportation Department, Federal Aviation Administration",
        "Federal Aviation Administration (FAA)": "Transportation Department, Federal Aviation Administration",
        "Trade Representative": "U.S. Trade Representative",
    }
    return aliases.get(agency.strip(), agency)

async def search_documents(query: str = "", agency: str = "", limit: int = 5):
    conn = await aiomysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Ganesh55@",  # 🔐 Replace as needed
        db="rag_demo"
    )

    async with conn.cursor(aiomysql.DictCursor) as cur:
        sql = "SELECT title, summary, publication_date, html_url FROM federal_documents WHERE 1=1"
        params = []

        # 🔍 Smart keyword search: split query and match ANY word
        if query:
            words = query.lower().split()
            word_clauses = " OR ".join([
                "(LOWER(title) LIKE %s OR LOWER(summary) LIKE %s)"
                for _ in words
            ])
            sql += f" AND ({word_clauses})"
            for word in words:
                like_term = f"%{word}%"
                params.extend([like_term, like_term])

        # 🔍 Case-insensitive agency match with alias support
        if agency:
            agency = normalize_agency(agency)
            sql += " AND LOWER(agency_names) LIKE %s"
            params.append(f"%{agency.lower()}%")

        sql += " ORDER BY publication_date DESC LIMIT %s"
        params.append(limit)

        await cur.execute(sql, params)
        results = await cur.fetchall()

    await conn.ensure_closed()
    return results
