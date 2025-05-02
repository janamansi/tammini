# app.py
import streamlit as st
st.set_page_config(page_title="منصة طمني", layout="centered", page_icon="🧠")

import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = st.secrets["google"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1FH5hZvV4HM9WvIbNg9hc2lqMalghMES5OLB-f_NwKZY").sheet1

# SQLite DB setup
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS responses (
    username TEXT,
    gender TEXT,
    age TEXT,
    q1 TEXT,
    q2 TEXT,
    q3 TEXT,
    q4 TEXT,
    q5 TEXT,
    q6 TEXT
)''')
conn.commit()

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

def questionnaire():
    st.subheader("📝 التقييم النفسي")
    gender = st.radio("ما هو جنسك؟", ["ذكر", "أنثى"])
    age = st.radio("ما هي فئتك العمرية؟", ["18-29", "30-39", "40-49", "50+"])

    q1_label = "س1: ھل ﺗﺟد ﻧﻔﺳك ﺗﻌﺎﻧﻲ ﻣن اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟزاﺋد ﺗﺟﺎﻩ ﻣﺧﺗﻠف اﻷﻣور اﻟﺣﯾﺎﺗﯾﺔ اﻟﻣﺣﯾطﺔ ﺑك، ﺳواء ﻛﺎﻧت ﻣﺗﻌﻠﻘﺔ ﺑﺎﻟﻌﻣل، اﻟدراﺳﺔ، اﻟﻣﻧزل، أو ﻏﯾرھﺎ ﻣن اﻟﺟواﻧب اﻟﯾوﻣﯾﺔ؟ اﻋط اﻣﺛﻠﺔ ﻋﻠﻰ ﺑﻌض ﻣن ھذه اﻷﻣور وﻛﯾف ﯾؤﺛراﻟﺗﻔﻛﯾر و اﻟﻘﻠق ﺑﮭﺎ ﻋﻠﻰ أﻓﻛﺎرك وﺳﻠوﻛك ﺧﻼل اﻟﯾوم"
    q2_label = "س2: ھل ﺗواﺟﮫ ﺻﻌوﺑﺔ ﻓﻲ اﻟﺳﯾطرة ﻋﻠﻰ أﻓﻛﺎرك اﻟﻘﻠﻘﺔ أو اﻟﺗﺣﻛم ﻓﻲ ﻣﺳﺗوى اﻟﻘﻠق اﻟذي ﺗﺷﻌر ﺑﮫ، ﺑﺣﯾث ﺗﺷﻌر أن اﻷﻣر ﺧﺎرج ﻋن إرادﺗك أو أﻧﮫ ﻣﺳﺗﻣر ﻋﻠﻰ ﻧﺣو ﯾرھﻘك؟ اﺟﻌل اﺟﺎﺑﺗك ﺗﻔﺻﯾﻠﯾﺔ ﺑﺣﯾث ﺗوﺿﺢ ﻛﯾف ﯾﻛون ﺧﺎرج ﻋﻥ ارادﺗك او اﻟﻰ اي ﻣدى ﯾرھﻘك"
    q3_label = "س3: ھل ﯾﺗراﻓق ﻣﻊ اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟﻣﺳﺗﻣر ﺛﻼﺛﺔ أﻋراض أو أﻛﺛر ﻣن اﻷﻋراض اﻟﺗﺎﻟﯾﺔ: اﻟﺷﻌور ﺑﻌدم اﻻرﺗﯾﺎح أو ﺑﺿﻐط ﻧﻔﺳﻲ ﻛﺑﯾر، اﻹﺣﺳﺎس ﺑﺎﻟﺗﻌب واﻹرھﺎق ﺑﺳﮭوﻟﺔ، ﺻﻌوﺑﺔ واﺿﺣﺔ ﻓﻲ اﻟﺗرﻛﯾز، اﻟﺷﻌور ﺑﺎﻟﻌﺻﺑﯾﺔ اﻟزاﺋدة، ﺷد ﻋﺿﻠﻲ ﻣزﻣن، اﺿطراﺑﺎت ﻓﻲ اﻟﻧوم، وﻏﯾرھﺎ؟ اذكر كل عرض تعاني منه وهل يؤثر على مهامك اليومية مثل العمل أو الدراسة أو حياتك الاجتماعية؟ وﻛﯾف ﯾؤﺛرﻋﻠﻳك ﺑﺷﻛل ﯾوﻣﻲ؟"
    q4_label = "س4: ھل ﻣررت ﺑﻔﺗرة اﺳﺗﻣرت أﺳﺑوﻋﯾن أو أﻛﺛر ﻛﻧت ﺗﻌﺎﻧﻲ ﺧﻼﻟﮭﺎ ﻣن ﺧﻣﺳﺔ أﻋراض أو أﻛﺛر ﻣﻣﺎ ﯾﻠﻲ، ﻣﻊ ﺿرورة وﺟود ﻋرض اﻟﻣزاج اﻟﻣﻛﺗﺋب أو ﻓﻘدان اﻟﺷﻐف واﻻھﺗﻣﺎم؟ اذكر الأعراض التي عانيت منها بالتفصيل و كيف أثرت عليك؟"
    q5_label = "س5: ھل أدت اﻷﻋراض اﻟﺗﻲ ﻣررت ﺑﮭﺎ إﻟﻰ ﺷﻌورك ﺑﺿﯾق ﻧﻔﺳﻲ ﺷدﯾد أو إﻟﻰ ﺗﻌطﯾل واﺿﺢ ﻟﻘدرﺗك ﻋﻠﻰ أداء ﻣﮭﺎﻣك اﻟﯾوﻣﯾﺔ، ﺳواء ﻓﻲ ﺣﯾﺎﺗك اﻻﺟﺗﻣﺎﻋﯾﺔ، اﻟوظﯾﻔﯾﺔ، أو اﻟﺷﺧﺻﯾﺔ؟ ﻛﯾف ﻻﺣظت ﺗﺄﺛﯾر ذﻟك ﻋﻠﻳك وﻋﻠﻰ ﺗﻔﺎﻋﻼﺗك ﻣﻊ ﻣن ﺣوﻟك؟"
    q6_label = "س6: ھل ھذه اﻷﻋراض اﻟﺗﻲ ﻋﺎﻧﯾت ﻣﻧﮭﺎ ﻟم ﺗﻛن ﻧﺎﺗﺟﺔ ﻋن ﺗﺄﺛﯾر أي ﻣواد ﻣﺧدرة، أدوﯾﺔ ﻣﻌﯾﻧﺔ، أو ﺑﺳﺑب ﺣﺎﻟﺔ ﻣرﺿﯾﺔ ﻋﺿوﯾﺔ أﺧرى ﻗد ﺗﻛون أﺛرت ﻋﻠﻰ ﺳﻠوﻛك أو ﻣﺷﺎﻋرك ﺧﻼل ﺗﻠك اﻟﻔﺗرة؟"

    q1 = st.text_area(q1_label)
    q2 = st.text_area(q2_label)
    q3 = st.text_area(q3_label)
    q4 = st.text_area(q4_label)
    q5 = st.text_area(q5_label)
    q6 = st.text_area(q6_label)

    if st.button("إرسال التقييم"):
        user = st.session_state.get('user')
        if user:
            c.execute("INSERT INTO responses (username, gender, age, q1, q2, q3, q4, q5, q6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (user, gender, age, q1, q2, q3, q4, q5, q6))
            conn.commit()

            headers = sheet.row_values(1)
            expected_headers = [
                "اسم المستخدم", "الجنس", "العمر",
                q1_label, q2_label, q3_label, q4_label, q5_label, q6_label
            ]
            if headers != expected_headers:
                sheet.delete_rows(1)
                sheet.insert_row(expected_headers, index=1)

            sheet.append_row([user, gender, age, q1, q2, q3, q4, q5, q6])
            st.success("✅ تم حفظ الإجابات.")
        else:
            st.error("⚠️ حدث خطأ: لم يتم تسجيل الدخول. الرجاء تسجيل الدخول أولاً.")

# Page Header UI
st.markdown("""
    <div style='background-color:#001f4d;padding:30px;border-radius:10px;'>
        <h1 style='text-align:center;color:white;'>طَمّني</h1>
    </div>
    <div style='text-align:center;margin-top:40px;'>
        <h3 style='color:#666;'>Tameni platform for mental health diagnosis using AI</h3>
        <h2 style='color:#003366;'>منصة طمأني لتقييم الصحة النفسية باستخدام الذكاء الصناعي</h2>
        <img src='https://cdn-icons-png.flaticon.com/512/4320/4320337.png' width='100' alt='brain'/>
    </div>
""", unsafe_allow_html=True)

# Navigation
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
