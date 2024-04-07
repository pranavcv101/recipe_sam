from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import Users
from app.forms import LoginForm, RegistrationForm,MyForm
from app.gemini import rmodel
from sqlalchemy.exc import SQLAlchemyError


convo = rmodel.start_chat(history=[])





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username = form.username.data).first()
        print(attempted_user.username)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
        
            login_user(attempted_user)  
           # next_page = request.args.get('next')  # Get the next page from the URL query parameters
            #return redirect(next_page or url_for('welcome'))  # Redirect to the next page if provided, else to the welcome page
            return redirect(url_for('welcome'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    #this  is enough this inbuilt function will automatically logout the user
    #now we can put some flashmesssage to show the user that v have logout but this flash shit is not working in my 
    #flash("logged out succesfully",category='info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users()
        user.username=form.username.data
        user.email=form.email.data
        user.height = form.height.data
        user.weight = form.weight.data
        user.password = form.password.data
        bmi = "{:.2f}".format((form.weight.data)/((form.height.data)**2))
        user.bmi= bmi
        db.session.add(user)
        db.session.commit()
        try:
          attempted_user = Users.query.all()
          print(attempted_user)
        except SQLAlchemyError as e:
           print("An error occurred while retrieving users:", e)
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/welcome')
#@login_required
def welcome():
    return render_template('welcome.html')


@app.route('/diet',methods=['GET', 'POST'])
def diet():





    generated_text = None
    if request.method == 'POST':
        action = request.form['action']
        if action == 'action1':
            convo.send_message("generate a healty breakfast for a 30 year old guy who's weight is 70 kg and height is 180cm")
            generated_text2 = convo.last.text
            generated_text = format_as_paragraph(generated_text2)
        elif action == 'action2':
            convo.send_message("suggest a healty lunch")
            generated_text = convo.last.text
        elif action == 'action3':
            convo.send_message("where r u")
            generated_text = convo.last.text
        elif action == 'action4':
            convo.send_message("where r u")
            generated_text = convo.last.text
    return render_template('dietary_control.html', generated_text=generated_text)

def format_as_paragraph(text):
    # Replace '**' with an empty string to remove bold formatting
    text = text.replace('**', '')
    # Replace '*' with '-' to change bullet points to dashes
    text = text.replace('*', '-')
    # Replace '****' with two newline characters to add line breaks before and after headings
    text = text.replace('****', '\n\n')
    # Replace '***' with newline characters to add line breaks after headings
    text = text.replace('***', '\n')
    # Replace '**' with a colon followed by a space to add formatting for section titles
    text = text.replace('**', ': ')    
    return text



@app.route('/generate_recipe', methods=['GET', 'POST'])
def generate_recipe():
        form = MyForm()
        generated_text = None
        if request.method == 'POST':
            #user_data = request.form['string_input'] -- this or below one both working
            user_data = form.string_input.data
            #convo = rmodel.start_chat(history=[])
            convo.send_message(user_data)
            generated_text = convo.last.text
        return render_template('generate_recipe.html', form=form, generated_text=generated_text)


    

@app.route('/profile')
#@login_required add this
def profile():
    # Logic to fetch and display user profile information
    return render_template('profile.html')

@app.route('/choose_option')
#@login_required
def choose_option():
    # This page allows users to choose between diet and recipe options
    return render_template('choose_option.html')

# You can add more routes as needed for additional functionalities
