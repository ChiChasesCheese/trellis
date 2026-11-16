"""真实工作区的 `app.py`：Flask 只负责路由和传输，合同在 `shortener.Api` 里（把 `solution.py` 放成 `shortener.py` 使用）。"""

from flask import Flask, jsonify, redirect, request
from werkzeug.exceptions import HTTPException

from shortener import Api, Reply, URLShortener

app = Flask(__name__)
app.url_map.strict_slashes = False
svc = URLShortener()
api = Api(svc)


def send(reply: Reply):
    if reply.location is not None:
        return redirect(reply.location, code=reply.status)
    return jsonify(reply.body), reply.status


def body_json():
    return request.get_json(force=True, silent=True)  # 不看 Content-Type；坏 JSON 得到 None，由 Api 回 400


@app.post("/links")
def create_link():
    return send(api.create_link(body_json(), request.host_url))


@app.get("/stats")
def stats():
    return send(api.stats())


@app.get("/links/<short_code>")
def get_link(short_code: str):
    return send(api.get_link(short_code))


@app.delete("/links/<short_code>")
def delete_link(short_code: str):
    return send(api.delete_link(short_code, body_json()))


@app.get("/<short_code>")
def redirect_link(short_code: str):
    return send(api.redirect(short_code))


@app.errorhandler(HTTPException)
def http_error(exc: HTTPException):
    return jsonify({"error": exc.description}), exc.code  # 404、405 以及 Flask 自己抛的其他 4xx


@app.errorhandler(Exception)
def crash(exc: Exception):
    return jsonify({"error": "internal error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False, threaded=True)
