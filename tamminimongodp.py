import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://tammeni25:MytamminiPass25@tammini.pcsh9ci.mongodb.net/?retryWrites=true&w=majority&appName=tammini")
db = client["tammini_db"]
users_col = db["users"]
responses_col = db["responses"]

st.set_page_config(page_title="منصة طَمّني", layout="centered", page_icon="🧠")

# ----------------- Auth -----------------
def signup():
    st.subheader("🔐 تسجيل حساب جديد")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل"):
        if users_col.find_one({"username": username}):
            st.error("اسم المستخدم مستخدم بالفعل.")
        else:
            users_col.insert_one({"username": username, "password": password})
            st.success("تم التسجيل! يمكنك الآن تسجيل الدخول.")

def login():
    st.subheader("🔑 تسجيل الدخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        user = users_col.find_one({"username": username, "password": password})
        if user:
            st.session_state['user'] = username
            st.success("مرحباً بك، تم تسجيل الدخول.")
        else:
            st.error("بيانات الدخول غير صحيحة.")

# ----------------- Questionnaire -----------------\
def questionnaire():
    st.subheader("📝 التقييم النفسي")
    
    user = st.session_state.get('user')
    if not user:
        st.error("⚠️ يرجى تسجيل الدخول أولاً.")
        return

    gender = st.radio("ما هو جنسك؟", ["ذكر", "أنثى"])
    age = st.radio("ما هي فئتك العمرية؟", ["18-29", "30-39", "40-49", "50+"])

    q1_label = "س1: ھل ﺗﺟد ﻧﻔﺳك ﺗﻌﺎﻧﻲ ﻣن اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟزاﺋد ﺗﺟﺎﻩ ﻣﺧﺗﻠﻑ اﻷﻣور اﻟﺣﯾﺎﺗﯾﺔ اﻟﻣﺣﯾطﺔ ﺑك، ﺳواء ﻛﺎﻧت ﻣﺗﻌﻠﻘﺔ ﺑﺎﻟﻌﻣل، اﻟدراﺳﺔ، اﻟﻣﻧزل، أو ﻏﯾرھﺎ ﻣن اﻟﺟواﻧب اﻟﯾوﻣﯾﺔ؟ اﻋط اﻣﺛﻠﺔ ﻋﻠﻰ ﺑﻌض ﻣن ھذه اﻷﻣور وﻛﯾف ﯾؤﺛراﻟﺗﻔﻛﯾر و اﻟﻘﻠق ﺑﮭﺎ ﻋﻠﻰ أﻓﻛﺎرك وﺳﻠوﻛك ﺧﻼل اﻟﯾوم"
    q2_label = "س2: ھل ﺗواﺟﮫ ﺻﻌوﺑﺔ ﻓﻲ اﻟﺳﯾطرة ﻋﻠﻰ أﻓﻛﺎرك اﻟﻘﻠﻘﺔ أو اﻟﺗﺣﻛم ﻓﻲ ﻣﺳﺗوى اﻟﻘﻠق اﻟذي ﺗﺷﻌر ﺑﮫ، ﺑﺣﯾث ﺗﺷﻌر أن اﻷﻣر ﺧﺎرج ﻋن إرادﺗك أو أﻧﮫ ﻣﺳﺗﻣر ﻋﻠﻰ ﻧﺣو ﯾرھﻘك؟ اﺟﻌل اﺟﺎﺑﺗك ﺗﻔﺻﯾﻠﯾﺔ ﺑﺣﯾث ﺗوﺿﺢ ﻛﯾف ﯾﻛون ﺧﺎرج ﻋﻥ ارادﺗك او اﻟﻰ اي ﻣدى ﯾرھﻘك"
    q3_label = "س3: ھل ﯾﺗراﻓق ﻣﻊ اﻟﺗﻔﻛﯾر اﻟﻣﻔرط أو اﻟﻘﻠق اﻟﻣﺳﺗﻣر ﺛﻼﺛﺔ أﻋراض أو أﻛﺛر ﻣن اﻷﻋراض اﻟﺗﺎﻟﯾﺔ: اﻟﺷﻌور ﺑﻌدم اﻻرﺗﯾﺎح أو ﺑﺿﻐط ﻧﻔﺳﻲ ﻛﺑﯾر، اﻹﺣﺳﺎس ﺑﺎﻟﺗﻌب واﻹرھﺎق ﺑﺳﮭوﻟﺔ، ﺻﻌوﺑﺔ واﺿﺣﺔ ﻓﻲ اﻟﺗرﻛﯾز، اﻟﺷﻌور ﺑﺎﻟﻌﺻﺑﯾﺔ اﻟزاﺋدة، ﺷد ﻋﺿﻠﻲ ﻣزﻣن، اﺿطراﺑﺎت ﻓﻲ اﻟﻧوم، وﻏﯾرھﺎ؟ اذكر كل عرض تعاني منه وهل يؤثر على مهامك اليومية مثل العمل أو الدراسة أو حياتك الاجتماعية؟ وﻛﯾف ﯾؤﺛرﻋﻠﻳك ﺑﺷﻛل ﯾوﻣﻲ؟"
    q4_label = "س4: ھل ﻣررت ﺑﻔﺗرة اﺳﺗﻣرت أﺳﺑوﻋﯾن أو أﻛﺛر ﻛﻧت ﺗﻌﺎﻧﻲ ﺧﻼﻟﮭﺎ ﻣن ﺧﻣﺳﺔ أﻋراض أو أﻛﺛر ﻣﻣﺎ ﯾﻠﻲ، ﻣﻊ ﺿرورة وﺟود ﻋرض اﻟﻣزاج اﻟﻣﻛﺗﺋب أو ﻓﻘدان اﻟﺷﻐف واﻻھﺗﻣﺎم؟ اذكر الأعراض التي عانيت منها بالتفصيل و كيف أثرت عليك؟"
    q5_label = "س5: ھل أدت اﻷﻋراض اﻟﺗﻲ ﻣررت ﺑﮭﺎ إﻟﻰ ﺷﻌورك ﺑﺿﯾق ﻧﻔﺳﻲ ﺷدﯾد أو إﻟﻰ ﺗﻌطﯾل واﺿﺢ ﻟﻘدرﺗك ﻋﻠﻰ أداء ﻣﮭﺎﻣك اﻟﯾوﻣﯾﺔ، ﺳواء ﻓﻲ ﺣﯾﺎﺗك اﻻﺟﺗﻣﺎﻋﯾﺔ، اﻟوظﯾﻔﯾﺔ، أو اﻟﺷﺧﺻﯾﺔ؟ ﻛﯾف ﻻﺣظت ﺗﺄﺛﯾر ذﻟك ﻋﻠﻳك وﻋﻠﻰ ﺗﻔﺎﻋﻼﺗك ﻣﻊ ﻣن ﺣوﻟك؟"
    q6_label = "س6: ھل ھذه اﻷﻋراض اﻟﺗﻲ ﻋﺎﻧﯾت ﻣﻧﮭﺎ ﻟم ﺗﻛن ﻧﺎﺗﺟﺔ ﻋﻥ ﺗﺄﺛﯾر أي ﻣواد ﻣﺧدرة، أدوﯾﺔ ﻣﻌﯾﻧﺔ، أو ﺑﺳﺑب ﺣﺎﻟﺔ ﻣرﺿﯾﺔ ﻋﺿوﯾﺔ أﺧرى ﻗد ﺗﻛون أﺛرت ﻋﻠﻰ ﺳﻠوﻛك أو ﻣﺷﺎﻋرك ﺧﻼل ﺗﻠك اﻟﻔﺗرة؟"
    
    q1 = st.text_area(q1_label)
    q2 = st.text_area(q2_label)
    q3 = st.text_area(q3_label)
    q4 = st.text_area(q4_label)
    q5 = st.text_area(q5_label)
    q6 = st.text_area(q6_label)

    if st.button("إرسال التقييم"):
        import re

        answers = [q1, q2, q3, q4, q5, q6]

        # Check for empty answers
        if any(ans.strip() == "" for ans in answers):
            st.warning("⚠️ الرجاء تعبئة جميع الإجابات قبل الإرسال.")
            return

        # Check for English characters
        if any(re.search(r"[a-zA-Z]", ans) for ans in answers):
            st.warning("⚠️ الرجاء عدم استخدام اللغة الإنجليزية في الإجابات.")
            return

       #insert into MongoDB
        responses_col.insert_one({
            "username": user,
            "gender": gender,
            "age": age,
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4,
            "q5": q5,
            "q6": q6,
            "diagnosis": "Pending",  # Will be updated by model later
            "timestamp": datetime.now()
        })

        st.success("✅ تم حفظ الإجابات.")



# ----------------- UI Header -----------------
st.markdown("""
<style>
body {
    background-image: url('https://raw.githubusercontent.com/streamlit/example-data/main/topographic-pattern-light.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.header-bar {
    background-color: #001f4d;
    padding: 10px 30px;
    color: white;
    font-size: 28px;
    text-align: left;
    font-family: 'Arial';
}
.center-box {
    text-align: center;
    margin-top: 100px;
}
.center-box h2 {
    color: #003366;
    font-size: 32px;
    line-height: 1.8;
}
.login-button {
    display: inline-block;
    margin-top: 30px;
    padding: 10px 30px;
    color: #003366;
    border: 2px solid #003366;
    text-decoration: none;
    border-radius: 6px;
    transition: 0.3s;
}
.login-button:hover {
    background-color: #003366;
    color: white;
}
</style>

<div class="header-bar">طمني</div>

<div class="center-box">
    <h2>منصة طمني لتقييم<br>الصحة النفسية باستخدام الذكاء الصناعي</h2>
    <a class="login-button" href="#">تسجيل الدخول / إنشاء حساب</a>
</div>
""", unsafe_allow_html=True)


# ----------------- Navigation -----------------
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
