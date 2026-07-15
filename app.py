# Flask web application 만들기
import random
from datetime import datetime
from flask import Flask, render_template, request

# Appication 생성
app = Flask(__name__)

# =====================================================
# 데이터 저장소 (서버 메모리에 저장)
# 실제 서비스라면 DB를 써야 한다.
# =====================================================
items = ["짜장면", "짬뽕", "볶음밥", "탕수육", "마파두부"]
history = []

@app.route("/")
def index():
    """
    메인 페이지 - 현재 아이템 목록을 HTML로 전달
    """
    # items를 HTML의 {{ items }}에 전달
    return render_template("index.html", items=items, history=history)

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

@app.route("/pick")
def pick():
    """
    랜덤 뽑기 API
    쿼리 파라미터: ?count=N (몇 개 뽑을지, 기본값=1)
    Response: {"picked": ["짜장면"], "timestamp": "20:15:30"}
    """
    # URL에서 count 값 읽기 (?count=3 이런 식으로)
    count = request.args.get("count", 1, type=int)
    
    # 입력값 검증
    if count < 1:
        return {"error": "1개 이상 뽑아야 해요!"}, 400
    if count > len(items):
        return {"error": f"목록에 {len(items)}개밖에 없어요!"}, 400
    
    # 중복 없이 랜덤 뽑기
    # random.sample(items, count)
    picked = random.sample(items, count)
    
    # 현재 시간 기록
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 히스토리 기록! (최신순, 최대 10개)
    history.insert(0, {"picked": picked, "timestamp": timestamp})
    if len(history) > 10:
        history.pop()
        
    return {"picked": picked, "timestamp": timestamp}
# Application 실행
if __name__ == "__main__":
    app.run(debug=True, port=5000)