import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import hashlib
from PIL import Image


# Set page configuration with wide layout and custom title
st.set_page_config(
    page_title="Multi-Disease Prediction System",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# ========== BACKGROUND IMAGE ==========
def set_bg_hack():
    """
    Set background image using local file
    """
    bg_image = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: url("https://kartinki.pics/pics/uploads/posts/2022-08/1660828291_3-kartinkin-net-p-fon-dlya-prezentatsii-virusi-krasivo-3.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(5px);
    }
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

set_bg_hack()


# ========== MySQL CONNECTION ==========
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Satyam@19102003",
        database="disease_app"
    )

# ========== PASSWORD HASHING ==========
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_hash(password, hashed):
    return make_hash(password) == hashed

# ========== AUTH FUNCTIONS ==========
def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = make_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and verify_hash(password, result[0]):
        return True
    return False

# ========== SESSION STATE ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# ========== ENHANCED LOGIN/SIGNUP UI ==========
def login_signup():
    # Main container styling
    st.markdown("""
    <style>
        .auth-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .auth-title {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 1.5rem;
            font-size: 2rem;
            font-weight: 700;
        }
        
        .auth-subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 2rem;
        }
        
        .stTextInput>div>div>input {
            border-radius: 8px !important;
            padding: 10px 15px !important;
            border: 1px solid #dfe6e9 !important;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
            border: none !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .forgot-link {
            text-align: right;
            margin-top: -15px;
            margin-bottom: 15px;
        }
        
        .forgot-link a {
            color: #6e8efb;
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .tab-container {
            margin-top: 1.5rem;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 1.5rem 0;
        }
        
        .divider::before, .divider::after {
            content: "";
            flex: 1;
            border-bottom: 1px solid #dfe6e9;
        }
        
        .divider-text {
            padding: 0 10px;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main container
    with st.container():
        st.markdown("""
        <div class="auth-container">
            <h1 class="auth-title">👨‍⚕️ Multiple Disease Prediction System 👨‍⚕️</h1>
            <p class="auth-subtitle">Please login or create an account to continue</p>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        # LOGIN TAB
        with tab1:
            st.markdown("""
            <div class="tab-container">
            """, unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            # Forgot password section
            col1, col2 = st.columns([3, 1])
            with col2:
                forgot = st.checkbox("Forgot Password?")
            
            if forgot:
                st.info("🔒 Password Reset")
                new_pass = st.text_input("New Password", type="password", key="new_pass")
                if st.button("Reset Password", key="reset_pass"):
                    if username and new_pass:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                        result = cursor.fetchone()
                        if result:
                            hashed = make_hash(new_pass)
                            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed, username))
                            conn.commit()
                            st.success("✅ Password reset successfully! Please login with your new password.")
                        else:
                            st.error("❌ Username not found.")
                        conn.close()
                    else:
                        st.warning("⚠️ Please enter both username and new password")
            
            if st.button("Login", key="login_btn"):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)

        # SIGNUP TAB
        with tab2:
            st.markdown("""
            <div class="tab-container">
            """, unsafe_allow_html=True)
            
            new_username = st.text_input("Choose Username", placeholder="Enter a username", key="signup_username")
            new_password = st.text_input("Create Password", type="password", placeholder="Enter a password", key="signup_password")
            
            if st.button("Create Account", key="signup_btn"):
                if new_username and new_password:
                    if add_user(new_username, new_password):
                        st.success("✅ Account created successfully! Please login.")
                    else:
                        st.error("❌ Username already exists")
                else:
                    st.warning("⚠️ Please fill in all fields")
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)

# ========== PREDICTION PAGE STYLING ==========
def prediction_page_style():
    st.markdown("""
    <style>
        .prediction-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            margin-bottom: 2rem;
        }
        
        .prediction-title {
            color: #2c3e50;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
        }
        
        .input-label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            border-radius: 8px !important;
            padding: 10px 15px !important;
            border: 1px solid #dfe6e9 !important;
            background-color: rgba(255,255,255,0.8) !important;
        }
        
        .prediction-btn {
            background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .prediction-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }
        
        .result-box {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            border-left: 5px solid #6e8efb;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .result-title {
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .positive {
            color: #e74c3c;
            font-weight: 700;
        }
        
        .negative {
            color: #2ecc71;
            font-weight: 700;
        }
    </style>
    """, unsafe_allow_html=True)

def set_bg_hack(disease=None):
    """
    Set background image based on the disease prediction page
    """
    backgrounds = {
        'default': "https://kartinki.pics/pics/uploads/posts/2022-08/1660828291_3-kartinkin-net-p-fon-dlya-prezentatsii-virusi-krasivo-3.jpg",
        'diabetes': "https://chfht.ca/wp-content/uploads/2018/08/GettyImages-651356550.jpg",
        'heart': "https://www.shutterstock.com/image-photo/cardiologist-showing-anatomy-model-human-600nw-2373470475.jpg",
        'parkinsons': "https://parkinsonsnewstoday.com/wp-content/uploads/2021/02/shutterstock_323930780_zpsedywvhv4.jpg",
        'kidney': "https://plus.unsplash.com/premium_photo-1702598804759-8fb687f774fb?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8a2lkbmV5JTIwZGlzZWFzZXxlbnwwfHwwfHx8MA%3D%3D",
        'liver': "https://mumcdnstorage.blob.core.windows.net/dwnews/2023/08/Diseased-liver-on-abstract-medical-background.jpg"
    }
    
    bg_image = backgrounds.get(disease, backgrounds['default'])
    
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(5px);
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# ========== SHOW LOGIN IF NOT LOGGED IN ==========
if not st.session_state.logged_in:
    set_bg_hack('default')
    login_signup()
    st.stop()

# ========== AFTER LOGIN ==========
prediction_page_style()
   
# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# loading the saved models

diabetes_model = pickle.load(open('D:\\project_final-year\\multiple-disease-prediction-system\\saved_models\\diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('D:\\project_final-year\\multiple-disease-prediction-system\\saved_models\\heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open('D:\\project_final-year\\multiple-disease-prediction-system\\saved_models\\parkinsons_model.sav', 'rb'))

kidney_disease_model = pickle.load(open('D:\\project_final-year\\multiple-disease-prediction-system\\saved_models\\kindey_model.sav','rb'))

liver_disease_model = pickle.load(open('D:\\project_final-year\\multiple-disease-prediction-system\\saved_models\\liver.pkl', 'rb'))

# sidebar for navigation
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center;'>
            <h3 style='color: #4CAF50;'>Welcome, {st.session_state.username}!</h3>
            <p style='font-size: 16px;'>Select a prediction model below:</p>
        </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title='Multiple Disease Prediction System',
        options=[
            'Diabetes Prediction',
            'Heart Disease Prediction',
            'Parkinsons Prediction',
            'Kidney Disease Prediction',
            'Liver Disease Prediction'
        ],
        icons=['activity', 'heart', 'person', 'droplet', 'person'],
        menu_icon='hospital-fill',
        default_index=0
    )

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    set_bg_hack('diabetes')
    st.title('Diabetes Prediction using ML')

    # Custom CSS for label formatting
    st.markdown("""
        <style>
            .label-custom {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: -8px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='label-custom'>Number of Pregnancies</div>", unsafe_allow_html=True)
        Pregnancies = st.text_input('', key='preg')

    with col2:
        st.markdown("<div class='label-custom'>Glucose Level</div>", unsafe_allow_html=True)
        Glucose = st.text_input('', key='glucose')

    with col3:
        st.markdown("<div class='label-custom'>Blood Pressure value</div>", unsafe_allow_html=True)
        BloodPressure = st.text_input('', key='bp')

    with col1:
        st.markdown("<div class='label-custom'>Skin Thickness value</div>", unsafe_allow_html=True)
        SkinThickness = st.text_input('', key='skin')

    with col2:
        st.markdown("<div class='label-custom'>Insulin Level</div>", unsafe_allow_html=True)
        Insulin = st.text_input('', key='insulin')

    with col3:
        st.markdown("<div class='label-custom'>BMI value</div>", unsafe_allow_html=True)
        BMI = st.text_input('', key='bmi')

    with col1:
        st.markdown("<div class='label-custom'>Diabetes Pedigree Function</div>", unsafe_allow_html=True)
        DiabetesPedigreeFunction = st.text_input('', key='dpf')

    with col2:
        st.markdown("<div class='label-custom'>Age of the Person</div>", unsafe_allow_html=True)
        Age = st.text_input('', key='age')

    diab_diagnosis = ''

    if st.button('🔍 Diabetes Test Result'):
        try:
            user_input = [
                Pregnancies, Glucose, BloodPressure, SkinThickness,
                Insulin, BMI, DiabetesPedigreeFunction, Age
            ]

            user_input = [float(x) for x in user_input]

            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 0:
                diab_diagnosis = '✅ <span style="font-size:20px; font-weight:bold; color:green;">This person is not diabetic.</span>'
            else:
                diab_diagnosis = '⚠️ <span style="font-size:20px; font-weight:bold; color:red;">This person has diabetes.</span>'

            st.markdown(diab_diagnosis, unsafe_allow_html=True)

        except ValueError:
            st.error("❌ Please enter valid numeric values in all fields.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    set_bg_hack('heart')
    st.title('Heart Disease Prediction using ML')

    # Custom CSS for input labels
    st.markdown("""
        <style>
            .label-custom {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: -8px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='label-custom'>Age</div>", unsafe_allow_html=True)
        age = st.text_input('', key='age')

    with col2:
        st.markdown("<div class='label-custom'>Sex</div>", unsafe_allow_html=True)
        sex = st.text_input('', key='sex' )

    with col3:
        st.markdown("<div class='label-custom'>Chest Pain types</div>", unsafe_allow_html=True)
        cp = st.text_input('', key='cp')

    with col1:
        st.markdown("<div class='label-custom'>Resting Blood Pressure</div>", unsafe_allow_html=True)
        trestbps = st.text_input('', key='trestbps')

    with col2:
        st.markdown("<div class='label-custom'>Serum Cholestoral in mg/dl</div>", unsafe_allow_html=True)
        chol = st.text_input('', key='chol')

    with col3:
        st.markdown("<div class='label-custom'>Fasting Blood Sugar > 120 mg/dl</div>", unsafe_allow_html=True)
        fbs = st.text_input('', key='fbs')

    with col1:
        st.markdown("<div class='label-custom'>Resting Electrocardiographic results</div>", unsafe_allow_html=True)
        restecg = st.text_input('', key='restecg')

    with col2:
        st.markdown("<div class='label-custom'>Maximum Heart Rate achieved</div>", unsafe_allow_html=True)
        thalach = st.text_input('', key='thalach')

    with col3:
        st.markdown("<div class='label-custom'>Exercise Induced Angina</div>", unsafe_allow_html=True)
        exang = st.text_input('', key='exang')

    with col1:
        st.markdown("<div class='label-custom'>ST depression induced by exercise</div>", unsafe_allow_html=True)
        oldpeak = st.text_input('', key='oldpeak')

    with col2:
        st.markdown("<div class='label-custom'>Slope of the peak exercise ST segment</div>", unsafe_allow_html=True)
        slope = st.text_input('', key='slope')

    with col3:
        st.markdown("<div class='label-custom'>Major vessels colored by flourosopy</div>", unsafe_allow_html=True)
        ca = st.text_input('', key='ca')

    with col1:
        st.markdown("<div class='label-custom'>Thal: 0 = normal; 1 = fixed defect; 2 = reversable defect</div>", unsafe_allow_html=True)
        thal = st.text_input('', key='thal')

    # Prediction logic
    heart_diagnosis = ''

    if st.button('❤️ Heart Disease Test Result'):
        try:
            # Collecting inputs
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg,
                        thalach, exang, oldpeak, slope, ca, thal]

            # Convert input to float
            user_input = [float(x) for x in user_input]

            # Make prediction
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = '⚠️ <span style="font-size:20px; font-weight:bold; color:red;">The person **is having heart disease**.</span>'
            else:
                heart_diagnosis = '✅ <span style="font-size:20px; font-weight:bold; color:green;">The person **does not have any heart disease**.</span>'

            # Display the result with styling
            st.markdown(heart_diagnosis, unsafe_allow_html=True)

        except ValueError:
            st.error("❌ Please enter valid numeric values in all fields.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    set_bg_hack('parkinsons')
    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')
    
    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    if st.button("🔍 Parkinson's Test Result"):
        try:
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                          RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                          APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

            user_input = [float(x) for x in user_input]

            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 0:
                parkinsons_diagnosis = '✅ <span style="font-size:20px; font-weight:bold; color:green;">The person **does not have Parkinson\'s disease**.</span>'
            else:
                parkinsons_diagnosis = '⚠️ <span style="font-size:20px; font-weight:bold; color:red;">The person **has Parkinson\'s disease**.</span>'

            # Display the result with styling
            st.markdown(parkinsons_diagnosis, unsafe_allow_html=True)

        except ValueError:
            st.error("❌ Please enter valid numeric values in all fields.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")

# Kidney's Prediction Page
if selected == 'Kidney Disease Prediction':
    set_bg_hack('kidney')
    st.title("Kidney Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        age = st.text_input('Age')

    with col2:
        blood_pressure = st.text_input('Blood Pressure')

    with col3:
        specific_gravity = st.text_input('Specific Gravity')

    with col4:
        albumin = st.text_input('Albumin')

    with col5:
        sugar = st.text_input('Sugar')

    with col1:
        red_blood_cells = st.selectbox('Red Blood Cell', ['normal', 'abnormal'])

    with col2:
        pus_cell = st.selectbox('Pus Cell', ['normal', 'abnormal'])

    with col3:
        pus_cell_clumps = st.selectbox('Pus Cell Clumps', ['present', 'notpresent'])

    with col4:
        bacteria = st.selectbox('Bacteria', ['present', 'notpresent'])

    with col5:
        blood_glucose_random = st.text_input('Blood Glucose Random')

    with col1:
        blood_urea = st.text_input('Blood Urea')

    with col2:
        serum_creatinine = st.text_input('Serum Creatinine')

    with col3:
        sodium = st.text_input('Sodium')

    with col4:
        potassium = st.text_input('Potassium')

    with col5:
        haemoglobin = st.text_input('Haemoglobin')

    with col1:
        packed_cell_volume = st.text_input('Packet Cell Volume')

    with col2:
        white_blood_cell_count = st.text_input('White Blood Cell Count')

    with col3:
        red_blood_cell_count = st.text_input('Red Blood Cell Count')

    with col4:
        hypertension = st.selectbox('Hypertension', ['yes', 'no'])

    with col5:
        diabetes_mellitus = st.selectbox('Diabetes Mellitus', ['yes', 'no'])

    with col1:
        coronary_artery_disease = st.selectbox('Coronary Artery Disease', ['yes', 'no'])

    with col2:
        appetite = st.selectbox('Appetite', ['good', 'poor'])

    with col3:
        peda_edema = st.selectbox('Peda Edema', ['yes', 'no'])

    with col4:
        anemia = st.selectbox('Anemia', ['yes', 'no'])

    # code for Prediction
    kindey_diagnosis = ''

    # creating a button for Prediction    
    if st.button("🔍 Kidney's Test Result"):
        try:
            # Prepare the user input for prediction
            user_input = [
                float(age), 
                float(blood_pressure), 
                float(specific_gravity), 
                float(albumin), 
                float(sugar),
                red_blood_cells, 
                pus_cell, 
                pus_cell_clumps, 
                bacteria,
                float(blood_glucose_random), 
                float(blood_urea), 
                float(serum_creatinine), 
                float(sodium),
                float(potassium), 
                float(haemoglobin), 
                float(packed_cell_volume),
                float(white_blood_cell_count), 
                float(red_blood_cell_count), 
                hypertension,
                diabetes_mellitus, 
                coronary_artery_disease, 
                appetite,
                peda_edema, 
                anemia
            ]

            prediction = kidney_disease_model.predict([user_input])

            if prediction[0] == 0:
                kindey_diagnosis = "✅ The person does not have Kidney's disease"
            else:
                kindey_diagnosis = "⚠️ The person has Kidney's disease"
            
            st.success(kindey_diagnosis)
        
        except ValueError:
            st.error("❌ Please enter valid numeric values in all fields.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")    

# Liver Disease Prediction Page
if selected == 'Liver Disease Prediction':
    set_bg_hack('liver')
    st.title('Liver Disease Prediction using ML')

    # Custom CSS for label formatting
    st.markdown("""
        <style>
            .label-custom {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: -8px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='label-custom'>Age</div>", unsafe_allow_html=True)
        age = st.text_input('', key='age')

    with col2:
        st.markdown("<div class='label-custom'>Gender</div>", unsafe_allow_html=True)
        gender = st.selectbox('', ['Male', 'Female'], key='gender')

    with col3:
        st.markdown("<div class='label-custom'>Total Bilirubin</div>", unsafe_allow_html=True)
        total_bilirubin = st.text_input('', key='total_bilirubin')

    with col1:
        st.markdown("<div class='label-custom'>Direct Bilirubin</div>", unsafe_allow_html=True)
        direct_bilirubin = st.text_input('', key='direct_bilirubin')

    with col2:
        st.markdown("<div class='label-custom'>Alkaline Phosphotase</div>", unsafe_allow_html=True)
        alkaline_phosphotase = st.text_input('', key='alkaline_phosphotase')

    with col3:
        st.markdown("<div class='label-custom'>Alamine Aminotransferase</div>", unsafe_allow_html=True)
        alamine_aminotransferase = st.text_input('', key='alamine_aminotransferase')

    with col1:
        st.markdown("<div class='label-custom'>Aspartate Aminotransferase</div>", unsafe_allow_html=True)
        aspartate_aminotransferase = st.text_input('', key='aspartate_aminotransferase')

    with col2:
        st.markdown("<div class='label-custom'>Total Proteins</div>", unsafe_allow_html=True)
        total_proteins = st.text_input('', key='total_proteins')

    with col3:
        st.markdown("<div class='label-custom'>Albumin</div>", unsafe_allow_html=True)
        albumin = st.text_input('', key='albumin')

    with col1:
        st.markdown("<div class='label-custom'>Albumin and Globulin Ratio</div>", unsafe_allow_html=True)
        albumin_and_globulin_ratio = st.text_input('', key='albumin_and_globulin_ratio')

    liver_diagnosis = ''

    if st.button('🔍 Liver Disease Test Result'):
        try:
            # Encode gender
            gender_encoded = 1.0 if gender == 'Male' else 0.0

            # User input for liver disease
            liver_input = [
                age, gender_encoded, total_bilirubin, direct_bilirubin, alkaline_phosphotase,
                alamine_aminotransferase, aspartate_aminotransferase, total_proteins,
                albumin, albumin_and_globulin_ratio
            ]

            # Convert all inputs to float
            liver_input = [float(value) for value in liver_input]

            # Predict using the liver disease model
            liver_prediction = liver_disease_model.predict([liver_input])

            # Diagnose based on the prediction
            if liver_prediction[0] == 1:
                liver_diagnosis = '✅ <span style="font-size:20px; font-weight:bold; color:green;">The person has liver disease.</span>'
            else:
                liver_diagnosis = '⚠️ <span style="font-size:20px; font-weight:bold; color:red;">The person does not have liver disease.</span>'
            
            st.markdown(liver_diagnosis, unsafe_allow_html=True)

        except ValueError:
            st.error("❌ Please enter valid numeric values in all fields.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")
