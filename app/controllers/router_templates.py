from flask import render_template,session,abort
from flask_cors import cross_origin
from app import app,tokenSafe
from app.models import User


@app.route('/register',methods=['GET'])
def register_render():
    return render_template('register.html')
    

@app.route('/forgot/password/<token>',methods=['GET'])
def forgot_password_token_render(token):
    try:
        id_user = tokenSafe.loads(token,salt='passwordForgot',max_age=1200)
        user  = User.query.get(id_user)
        if user is None: return abort(404)

        return render_template("password_reset.html"),200

    except:return abort(404)

@app.route('/forgot/password',methods=['GET'])
def forgot_password_render():
    return render_template('forgot_password.html')

@app.route('/painel',methods=['GET'])
def painel():
    return render_template('painel.html')

@app.route('/',methods=['GET'])
def index():
    session['user'] = [False,False]
    return render_template('index.html')

@app.route('/balance',methods=['GET'])
@cross_origin()
def balance():
    return render_template('balance.html')

@app.route('/activations',methods=['GET'])
def activations():
    return render_template('activations.html')
    
@app.route('/historic',methods=['GET'])
def historic():
    return render_template('historic.html')

@app.route('/profile',methods=['GET'])
def profile():
    return render_template('profile.html')

@app.route('/transactions',methods=['GET'])
def transactions():
    return render_template('transactions.html')

@app.route('/pix/verification',methods=['GET'])
def pixVerification():
    return render_template('payment_verification.html')

@app.route('/pix/payment/',methods=['GET'])
def pixPayment():
    return render_template('pix_payment.html')
    
@app.route('/bot',methods=['GET'])
def bot():
    return render_template('bot.html')

@app.route('/app',methods=['GET'])
def app_mobile():
    return render_template('app.html')
    
@app.route('/faq',methods=['GET'])
def faq():
    return render_template('faq.html')
    
@app.route('/termos_de_uso',methods=['GET'])
def termos_de_uso():
    return render_template('termos.html')

@app.route('/politica_de_privacidade',methods=['GET'])
def politica_de_privacidade():
    return render_template('private.html')

