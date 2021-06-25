from flask import Flask, session, render_template, request, redirect, url_for
import process_db as pro


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/home')
def index():
    if 'user_id' in session:
        data = dict()
        user_id = session['user_id']
        data['incomplete'] = pro.get_todo_incomplete(user_id)
        data['complete'] = pro.get_todo_complete(user_id)
        if 'delete_item_successful' in session:
            data['successful_message'] = session['delete_item_successful']
            del session['delete_item_successful']
        if 'delete_item_failed' in session:
            data['error_message'] = session['delete_item_failed']
            del session['delete_item_failed']
        if 'update_item_successful' in session:
            data['successful_message'] = session['update_item_successful']
            del session['update_item_successful']
        if 'update_item_failed' in session:
            data['error_message'] = session['update_item_failed']
            del session['update_item_failed']
        return render_template('list.html', data=data)
    return redirect(url_for('login'))


@app.route('/add_todo', methods =['POST'])
def add_todo():
    data = dict()
    user_id = session['user_id']
    if request.method == 'POST':
        data['body'] = request.form['text']
        data['author_id'] = user_id
        data['type'] = 0  # incomplete 0 / complete 1
        response = pro.insert_todo(**data)

        if response[0]:
            session['add successfully'] = response[1]
            return redirect(url_for('index'))
        else:
            session['add error'] = response[1]
            return redirect(url_for('index'))


@app.route('/login')
def login():
    data = dict()
    if 'user_id' in session:
        return redirect(url_for('index'))
    if 'error' in session:
        data['error_message'] = session['error']
        del session['error']
    if 'Successfully_add_user' in session:
        data['successful_message'] = session['Successfully_add_user']
        del session['Successfully_add_user']
    return render_template('login.html', data=data)


@app.route('/login_pro', methods = ['POST'])
def pro_login():
    data=dict()
    if request.method == 'POST':
        data['email'] = request.form['email']
        data['password'] = request.form['pass']
        response = pro.login_user(**data)
        if response[0]:
            session['user_id'] = response[1]
            return redirect(url_for('index'))
        elif response[0] == False :
            session['error'] = response[1]
            print(session['error'])
            return redirect(url_for('login'))


@app.route('/register')
def register():
    data = dict()
    if 'user_id' in session:
        return redirect(url_for('index'))
    if 'error_add_user' in session:
        data['error_message'] = session['error_add_user']
        del session['error_add_user']
    return render_template('register.html', data=data)


@app.route('/register_pro', methods=['POST'])
def register_pro():
    data = dict()
    if request.method == 'POST':
        data['username'] = request.form['name']
        data['email'] = request.form['email']
        data['password'] = request.form['pass']
        response = pro.insert_user(**data)
        print(response)
        if response[0]:
            session['Successfully_add_user'] = response[1]
            return redirect(url_for('login'))
        elif not response[0]:
            session['error_add_user'] = response[1]
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))


@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
        return redirect(url_for('login'))


@app.route('/delete/<id>')
def delete(id):
    if 'user_id' in session:
        response = pro.delete(int(id))
        if response[0]:
            session['delete_item_successful'] = response[1]
            return redirect(url_for('index'))
        elif not response[0]:
            session['delete_item_failed'] = response[1]
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/update/<id>')
def update(id):
    if 'user_id' in session:
        response = pro.update(int(id))
        if response[0]:
            session['update_item_successful'] = response[1]
            return redirect(url_for('index'))
        elif not response[0]:
            session['update_item_failed'] = response[1]
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def error_hand(error):
    return render_template('error.html', data=error)


if __name__ == '__main__':
    app.run(debug=True)