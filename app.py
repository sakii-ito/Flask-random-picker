# Flask web application 만들기

from flask import Flask, render_template, request

# Appication 생성
app = Flask(__name__)

# =====================================================
# 데이터 저장소 (서버 메모리에 저장)
# 실제 서비스라면 DB를 써야 한다.
# =====================================================
items = ["짜장면", "짬뽕", "볶음밥", "탕수육", "마파두부"]


@app.route("/")
def index():
    """
    메인 페이지 - 현재 아이템 목록을 HTML로 전달
    """
    # items를 HTML의 {{ items }}에 전달
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add_item():
    """
    아니템 추가 API
    Request: {"item": "새 아이템"}
    Response: {"status": "ok", "items": [...]}
    """
    data = request.get_json(silent=True) or {}
    item = data.get("item", "").strip()
    
    # 입력값 검증
    if not item:
        return {"error": "아이템 이름을 입력해주세요!"}, 400
    if item in items:
        return {"error": f"'{item}'은 이미 있어요!"}, 400
    if len(items) >= 20:
        return {"error": "최대 20개까지만 추가할 수 있어요!"}, 400
    
    # 목록에 추가
    items.append(item)
    return {"status": "ok", "items": items}

@app.route("/delete", methods=["POST"])
def delete_item():
    """
    아이템 삭제 API
    Request: {"item": "삭제할 아이템"}
    Response: {"status":"ok", "items": [...]}
    """
    data = request.get_json(silent=True) or {}
    item = data.get("item", "").strip()
    
    if item not in items:
        return {"error": f"'{item}'을 찾을 수 없엉요!"}, 400
    if len(items) <= 2:
        return {"error": "최소 2개는 있어야 해요!"}, 400
    
    # 목록에서 제거
    items.remove(item)
    return {"status": "ok", "items": items}
# Application 실행
if __name__ == "__main__":
    app.run(debug=True, port=5000)