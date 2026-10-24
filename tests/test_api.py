import asyncio

from safetruck.api import app, service_info


def test_root_returns_service_information():
    assert "/" in app.openapi()["paths"]
    assert asyncio.run(service_info()) == {
        "service": app.title,
        "docs": app.docs_url,
        "inference_endpoint": "/api/v1/inference",
    }
