import sys
from app.search import dense_search
question = " ".join(sys.argv[1:]) or "How can I restore PostgreSQL?"
for result in dense_search(question, limit=5):
    print(result.filename, "page", result.page_number,
          "score", round(result.score, 3), "chunk", result.chunk_id)
    print(result.content[:240], "\n")