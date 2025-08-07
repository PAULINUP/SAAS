# openapi_docs.py
"""
Gera documentação interativa da API REST do Q-Core AI usando OpenAPI/Swagger.
Roda localmente ou exporta como JSON para portais externos.
"""

from fastapi.openapi.utils import get_openapi
from api_gateway import app
import json

def generate_openapi_schema(output_file="openapi_qcore.json"):
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    with open(output_file, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"✅ Documentação OpenAPI salva em: {output_file}")

if __name__ == "__main__":
    generate_openapi_schema()
