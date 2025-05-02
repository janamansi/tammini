# app.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("tameni_responses").sheet1

# Signup page
def signup():
    st.subheader("🔐 تسجيل حساب جديد")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل"):
        try:
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            st.success("تم التسجيل! يمكنك الآن تسجيل الدخول.")
        except:
            st.error("اسم المستخدم مستخدم بالفعل.")

# Login page
def login():
    st.subheader("🔑 تسجيل الدخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        if result:
            st.session_state['user'] = username
            st.success("مرحباً بك، تم تسجيل الدخول.")
        else:
            st.error("بيانات الدخول غير صحيحة.")

# Questionnaire page
def questionnaire():
    st.subheader("📝 التقييم النفسي")
    gender = st.radio("ما هو جنسك؟", ["ذكر", "أنثى"])
    age = st.radio("ما هي فئتك العمرية؟", ["18-29", "30-39", "40-49", "50+"])

    q1 = st.text_area("س1: ھل ﺗﺟد ﻧﻔﺳك ﺗﻌﺎﻧﻲ ﻣن اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟزاﺋد ﺗﺟﺎه ﻣﺧﺗﻠف اﻷﻣور اﻟﺣﯾﺎﺗﯾﺔ اﻟﻣﺣﯾطﺔ ﺑك، ﺳواء ﻛﺎﻧت ﻣﺗﻌﻠﻘﺔ ﺑﺎﻟﻌﻣل، اﻟدراﺳﺔ، اﻟﻣﻧزل، أو ﻏﯾرھﺎ ﻣن اﻟﺟواﻧب اﻟﯾوﻣﯾﺔ؟ اﻋط اﻣﺛﻠﺔ ﻋﻠﻰ ﺑﻌض ﻣن ھذه اﻷﻣور وﻛﯾف ﯾؤﺛر اﻟﺗﻔﻛﯾر و اﻟﻘﻠق ﺑﮭﺎ ﻋﻠﻰ أﻓﻛﺎرك وﺳﻠوﻛك ﺧﻼل اﻟﯾوم")
    q2 = st.text_area("س2: ھل ﺗواﺟﮫ ﺻﻌوﺑﺔ ﻓﻲ اﻟﺳﯾطرة ﻋﻠﻰ أﻓﻛﺎرك اﻟﻘﻠﻘﺔ أو اﻟﺗﺣﻛم ﻓﻲ ﻣﺳﺗوى اﻟﻘﻠق اﻟذي ﺗﺷﻌر ﺑﮫ، ﺑﺣﯾث ﺗﺷﻌر أن اﻷﻣر ﺧﺎرج ﻋن إرادﺗك أو أﻧﮫ ﻣﺳﺗﻣر ﻋﻠﻰ ﻧﺣو ﯾرھﻘك؟ اﺟﻌل اﺟﺎﺑﺗك ﺗﻔﺻﯾﻠﯾﺔ ﺑﺣﯾث ﺗوﺿﺢ ﻛﯾف ﯾﻛون ﺧﺎرج ﻋﻧ ارادﺗك او اﻟﻰ اي ﻣدى ﯾرھﻘك")
    q3 = st.text_area("س3: ھل ﯾﺗراﻓق ﻣﻊ اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟﻣﺳﺗﻣر ﺛﻼﺛﺔ أﻋراض أو أﻛﺛر ﻣن اﻷﻋراض اﻟﺗﺎﻟﯾﺔ: اﻟﺷﻌور ﺑﻌدم اﻻرﺗﯾﺎح أو ﺑﺿﻐط ﻧﻔﺳﻲ ﻛﺑﯾر، اﻹﺣﺳﺎس ﺑﺎﻟﺗﻌب واﻹرھﺎق ﺑﺳﮭوﻟﺔ ﺣﺗﻰ ﻋﻧد اﻟﻘﯾﺎم ﺑﺄﻋﻣﺎل ﯾوﻣﯾﺔ ﺑﺳﯾطﺔ، ﺻﻌوﺑﺔ واﺿﺣﺔ ﻓﻲ اﻟﺗرﻛﯾز، اﻟﻌﺻﺑﯾﺔ أو اﻻﻧﻔﻌﺎﻟﯾﺔ، ﺷد ﻋﺿﻠﻲ، اﻧزﻋﺎج ﺟﺳدي، أو اﺿطراﺑﺎت ﻓﻲ اﻟﻧوم؟ اذﻛر الأعراض التي تعاني منها وهل تؤثر على مهامك اليومية مثل العمل أو الدراسة أو حياتك الاجتماعية؟ وﻛﯾف ﯾؤﺛرﻋﻠﯾك ﺑﺷﻛل ﯾوﻣﻲ؟")
    q4 = st.text_area("س4: ھل ﻣررت ﺑﻔﺗرة اﺳﺗﻣرت أﺳﺑوﻋﯾن أو أﻛﺛر ﻛﻧت ﺗﻌﺎﻧﻲ ﺧﻼﻟﮭﺎ ﻣن ﺧﻣﺳﺔ أﻋراض أو أﻛﺛر ﻣﻣﺎ ﯾﻠﻲ، ﻣﻊ ﺿرورة وﺟود ﻋرض اﻟﻣزاج اﻟﻣﻛﺗﺋب أو ﻓﻘدان اﻟﺷﻐف واﻻھﺗﻣﺎم ﺑﺎﻷﻧﺷطﺔ اﻟﺗﻲ ﻛﻧت ﺗﺳﺗﻣﺗﻊ ﺑﮭﺎ ﺳﺎﺑﻘًﺎ؟ اﻷﻋراض ﺗﺷﻣل: اﻟﺷﻌور ﺑﻣزاج ﻣﻛﺗﺋب ﻣﻌظم ﺳﺎﻋﺎت اﻟﯾوم، ﻓﻘدان اﻷﻣل، اﻟﺗﻌب، ﻓﻘدان اﻟﻣﺗﻌﺔ، ﺗﻐﯾّرات ﻓﻲ اﻟﺷﮭﯾﺔ أو الوزن، ﺻﻌوﺑﺔ ﻓﻲ اﻟﻧوم، ﺧﻣول أو ﻧﺷﺎط ﻏﯾر ﻣﻧﺗظم، ﺗﺄﻧﯾب ﺿﻣﯾر، ﺻﻌوﺑﺔ ﻓﻲ اﻟﺗرﻛﯾز، أو أﻓﻛﺎر اﻧﺗﺣﺎرﯾﺔ. اذﻛر الأعراض التي عانيت منها بالتفصيل و كيف أثرت عليك؟")
    q5 = st.text_area("س5: ھل أدت اﻷﻋراض اﻟﺗﻲ ﻣررت ﺑﮭﺎ إﻟﻰ ﺷﻌورك ﺑﺿﯾق ﻧﻔﺳﻲ ﺷدﯾد أو إﻟﻰ ﺗﻌطﯾل واﺿﺢ ﻟﻘدرﺗك ﻋﻠﻰ أداء ﻣﮭﺎﻣك اﻟﯾوﻣﯾﺔ، ﺳواء ﻓﻲ ﺣﯾﺎﺗك اﻻﺟﺗﻣﺎﻋﯾﺔ، اﻟوظﯾﻔﯾﺔ، أو اﻟﺷﺧﺻﯾﺔ؟ ﻛﯾف ﻻﺣظت ﺗﺄﺛﯾر ذﻟك ﻋﻠﯾك وﻋﻠﻰ ﺗﻔﺎﻋﻼﺗك ﻣﻊ ﻣن ﺣوﻟك؟")
    q6 = st.text_area("س6: ھل ھذه اﻷﻋراض اﻟﺗﻲ ﻋﺎﻧﯾت ﻣﻧﮭﺎ ﻟم ﺗﻛن ﻧﺎﺗﺟﺔ ﻋن ﺗﺄﺛﯾر أي ﻣواد ﻣﺧدرة، أدوﯾﺔ ﻣﻌﯾﻧﺔ، أو ﺑﺳﺑب ﺣﺎﻟﺔ ﻣرﺿﯾﺔ ﻋﺿوﯾﺔ أﺧرى ﻗد ﺗﻛون أﺛرت ﻋﻠﻰ ﺳﻠوﻛك أو ﻣﺷﺎﻋرك ﺧﻼل ﺗﻠك اﻟﻔﺗرة؟")
    
    

    if st.button("إرسال التقييم"):
        sheet.append_row([st.session_state['user'], gender, age, q1, q2, q3, q4, q5, q6])
        st.success("✅ تم حفظ الإجابات. سيتم تحليلها الآن.")
        st.image("ffd21d58-2e22-4afd-b179-3b1a07971f34.png", caption="نتيجة التقييم")

# Main app
st.set_page_config(page_title="منصة طمني", layout="centered", page_icon="🧠")
st.markdown("""
    <div style='background-color:#001f4d;padding:30px;border-radius:10px;'>
        <h1 style='text-align:center;color:white;'>طَمّني</h1>
    </div>
    <div style='text-align:center;margin-top:40px;'>
        <h3 style='color:#666;'>Tameni platform for mental health diagnosis using AI</h3>
        <h2 style='color:#003366;'>منصة طَمّني لتقييم الصحة النفسية باستخدام الذكاء الصناعي</h2>
        <img src='https://cdn-icons-png.flaticon.com/512/4320/4320337.png' width='100' alt='brain'/>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    if st.button("Log in / Sign up"):
        st.session_state.page = "auth"
    st.stop()

if 'user' not in st.session_state:
    page = st.radio("اختر الصفحة", ["تسجيل الدخول", "تسجيل جديد"], horizontal=True)
    if page == "تسجيل الدخول":
        login()
    else:
        signup()
    st.stop()
else:
    questionnaire()

if 'page' not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    st.session_state.page = "auth"

if 'user' not in st.session_state:
    page = st.sidebar.selectbox("اختر الصفحة", ["تسجيل الدخول", "تسجيل جديد"])
    if page == "تسجيل الدخول":
        login()
    else:
        signup()
else:
    questionnaire()
