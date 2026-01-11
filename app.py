from flask import Flask, render_template, request
from calculator_logic import add, subtract, multiply, divide

app = Flask(__name__)

# הלוגיקה שלך עטופה בתוך פונקציית השרת
@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>מחשבון - חלק D הצלחה!</h2>
            <form action="/calculate" method="post">
                <input type="number" name="num1" required>
                <select name="op">
                    <option value="+">+</option>
                    <option value="-">-</option>
                    <option value="*">*</option>
                    <option value="/">/</option>
                </select>
                <input type="number" name="num2" required>
                <button type="submit">חשב</button>
            </form>
            <div id="result"></div>
        </body>
    </html>
    '''

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        n1 = float(request.form['num1'])
        n2 = float(request.form['num2'])
        op = request.form['op']
        
        if op == '+': res = add(n1, n2)
        elif op == '-': res = subtract(n1, n2)
        elif op == '*': res = multiply(n1, n2)
        elif op == '/': res = divide(n1, n2)
        
        return f"<h2>התוצאה היא: {res}</h2><br><a href='/'>חזור</a>"
    except Exception as e:
        return f"Error: {str(e)}"

# החלק ששומר על הקונטיינר דלוק
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
