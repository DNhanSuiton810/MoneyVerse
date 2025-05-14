import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel('quiz_questions_fully_extended.xlsx')

# Tabs
tab1, tab2 = st.tabs(["📘 Flashcard (Quizlet Style)", "📝 Làm Quiz"])

# ---------------- TAB 1: Flashcard ----------------
with tab1:
    st.markdown("<h2 style='text-align: center; color: #333;'>📘 Flashcard - Quizlet Style</h2>", unsafe_allow_html=True)

    categories = ['Tất cả câu hỏi'] + list(df['Category'].unique())
    selected_category = st.selectbox("Chọn chủ đề:", categories, key="flash_category")

    if selected_category == 'Tất cả câu hỏi':
        filtered_df = df.reset_index(drop=True)
    else:
        filtered_df = df[df['Category'] == selected_category].reset_index(drop=True)

    total_cards = len(filtered_df)

    if 'flash_index' not in st.session_state:
        st.session_state.flash_index = 0
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False

    if total_cards == 0:
        st.warning("⚠ Không có câu hỏi nào trong chủ đề này.")
    else:
        question = filtered_df.iloc[st.session_state.flash_index]

        st.markdown(f"""
            <div style="
                background-color: #ffffff;
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            ">
                <h4 style='color: #888;'>📂 {question['Category']}</h4>
                <h3 style='color: #222;'>{question['Question']}</h3>
            </div>
        """, unsafe_allow_html=True)

        if st.button("👁 Hiển thị / Ẩn đáp án", key=f"show_answer_button_{st.session_state.flash_index}"):
            st.session_state.show_answer = not st.session_state.show_answer

        if st.session_state.show_answer:
            correct_letter = question['Correct Answer']
            correct_text = question[correct_letter]
            explanation = question['Explanation']

            if 'tất cả các phương án trên' in correct_text.lower():
                all_answers = f"""
                <ul>
                    <li>A: {question['A']}</li>
                    <li>B: {question['B']}</li>
                    <li>C: {question['C']}</li>
                    <li>D: {question['D']}</li>
                </ul>
                """
                correct_text += all_answers

            st.markdown(f"""
                <div style="
                    background-color: #e7f5ff;
                    border-left: 5px solid #339af0;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    text-align: left;
                ">
                    <b>✅ Đáp án đúng:</b> {correct_text}
                </div>
                <div style="
                    background-color: #fff3bf;
                    border-left: 5px solid #f59f00;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: left;
                ">
                    <b>💡 Giải thích:</b> {explanation}
                </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Trước", key="prev_button"):
                if st.session_state.flash_index > 0:
                    st.session_state.flash_index -= 1
                    st.session_state.show_answer = False
        with col3:
            if st.button("➡️ Tiếp", key="next_button"):
                if st.session_state.flash_index < total_cards - 1:
                    st.session_state.flash_index += 1
                    st.session_state.show_answer = False

        st.markdown(f"<p style='text-align: center;'>📄 Thẻ {st.session_state.flash_index + 1} / {total_cards}</p>", unsafe_allow_html=True)

# ---------------- TAB 2: Quiz ----------------
with tab2:
    st.markdown("<h2 style='text-align: center;'>📝 Làm bài kiểm tra</h2>", unsafe_allow_html=True)
    selected_category_quiz = st.selectbox("Chọn chủ đề Quiz:", df['Category'].unique(), key="quiz_category")
    filtered_df_quiz = df[df['Category'] == selected_category_quiz].reset_index(drop=True)

    if len(filtered_df_quiz) == 0:
        st.warning("⚠ Không có câu hỏi nào trong chủ đề này.")
    else:
        num_questions = st.slider("Số câu hỏi:", min_value=1, max_value=min(20, len(filtered_df_quiz)), value=5)
        questions = filtered_df_quiz.sample(n=num_questions).reset_index(drop=True)
        score = 0
        user_answers = []

        with st.form("quiz_form"):
            for i, row in questions.iterrows():
                st.markdown(f"""
                    <div style="
                        background-color: #ffffff;
                        border-radius: 15px;
                        padding: 20px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                        margin-bottom: 20px;
                    ">
                        <h4 style='color:#222;'>Câu {i+1}: {row['Question']}</h4>
                """, unsafe_allow_html=True)

                options = {
                    'A': f"A: {row['A']}",
                    'B': f"B: {row['B']}",
                    'C': f"C: {row['C']}",
                    'D': f"D: {row['D']}"
                }

                selected = st.radio(
                    label="Chọn đáp án:",
                    options=list(options.keys()),
                    format_func=lambda x: options[x],
                    key=f"q{i}",
                    horizontal=False
                )

                user_answers.append((selected, row['Correct Answer'], row[selected], row['Explanation']))
                st.markdown("</div>", unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Nộp bài")

            if submitted:
                st.markdown("<hr>", unsafe_allow_html=True)
                for idx, (user_ans, correct_ans, user_text, explanation) in enumerate(user_answers):
                    if user_ans == correct_ans:
                        st.markdown(f"""
                            <div style="
                                background-color: #d3f9d8;
                                border-left: 5px solid #37b24d;
                                padding: 15px;
                                border-radius: 8px;
                                margin-bottom: 10px;
                            ">
                                <b>Câu {idx+1}:</b> ✅ Đúng ({user_ans}) - {user_text}
                            </div>
                        """, unsafe_allow_html=True)
                        score += 1
                    else:
                        st.markdown(f"""
                            <div style="
                                background-color: #ffe3e3;
                                border-left: 5px solid #f03e3e;
                                padding: 15px;
                                border-radius: 8px;
                                margin-bottom: 10px;
                            ">
                                <b>Câu {idx+1}:</b> ❌ Sai (Bạn chọn {user_ans} - {user_text})<br>
                                👉 Đáp án đúng: {correct_ans} - {questions.loc[idx, correct_ans]}<br>
                                💡 Giải thích: {explanation}
                            </div>
                        """, unsafe_allow_html=True)

                st.success(f"🎯 Tổng điểm: {score}/{len(user_answers)} đúng")
