# utils/response.py
from flask import jsonify
from typing import Any, Dict

def success_response(
    data: Any = None,
    message: str = "Success",
    code: int = 200
) -> Dict[str, Any]:
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    })

def error_response(
    message: str,
    code: int = 400,
    details: Any = None
) -> Dict[str, Any]:
    return jsonify({
        "code": code,
        "message": message,
        "details": details
    }),code