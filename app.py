# Flask web application 만들기

from flask import Flask, render_template

# Appication 생성
app = Flask(__name__)

# 메인 페이지 라우트
@app.route("/")
def index():
    """
    /로 접석하면 index.html을 보여준다.
    """
    return render_template("index.html")

# Application 실행
if __name__ == "__main__":
    app.run(debug=True, port=5000)