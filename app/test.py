# test_import.py
try:
    # from llama_index.vector_stores.postgres import PGVectorStore
    from llama_index.vector_stores.postgres import PGVectorStore
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
