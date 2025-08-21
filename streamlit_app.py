# streamlit_app.py

import streamlit as st
import time
import random
from datetime import datetime, timedelta

# --- 1. 세션 상태(Session State) 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'money' not in st.session_state:
    st.session_state.money = 0
if 'total_study_time' not in st.session_state:
    st.session_state.total_study_time = 0
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 0
if 'timer_end_time' not in st.session_state:
    st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False

# --- 페이지 이동 함수 ---
def go_to_page(page_name):
    st.session_state.page = page_name

# --- 2. 페이지 렌더링 ---

# --- 홈 화면 ---
if st.session_state.page == 'home':
    st.title("🏠 게부 홈")
    st.write("열심히 공부해서 부자가 되어보세요!")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="💰 보유 머니", value=f"{st.session_state.money} 머니")
    with col2:
        total_minutes = st.session_state.total_study_time
        hours = total_minutes // 60
        minutes = total_minutes % 60
        st.metric(label="누적 공부 시간", value=f"{hours}시간 {minutes}분")
    st.divider()
    if st.button("⏰ 공부 타이머 맞추러 가기", type="primary"):
        go_to_page('timer_setup')
        st.rerun()
    if st.button("🎮 게임하러 가기"):
        go_to_page('game')
        st.rerun()

# --- 타이머 설정 화면 ---
elif st.session_state.page == 'timer_setup':
    st.title("⏱️ 공부 시간 설정")
    duration_minutes = st.number_input(
        "몇 분 동안 공부할 건가요? (1분 = 10머니)",
        min_value=1, max_value=180, value=25, step=1
    )
    if st.button("공부 시작!"):
        st.session_state.timer_duration = duration_minutes
        st.session_state.timer_end_time = datetime.now() + timedelta(minutes=duration_minutes)
        st.session_state.timer_active = True
        go_to_page('timer_running')
        st.rerun()
    if st.button("🏠 홈으로 돌아가기"):
        go_to_page('home')
        st.rerun()

# --- 타이머 실행 화면 ---
elif st.session_state.page == 'timer_running':
    st.title("🔥 열공 중...")
    timer_placeholder = st.empty()
    button_placeholder = st.empty()
    while st.session_state.timer_active and datetime.now() < st.session_state.timer_end_time:
        remaining_time = st.session_state.timer_end_time - datetime.now()
        remaining_seconds = max(0, remaining_time.total_seconds())
        minutes = int(remaining_seconds // 60)
        seconds = int(remaining_seconds % 60)
        timer_placeholder.markdown(f"## 남은 시간: {minutes:02d}:{seconds:02d}")
        time.sleep(1)
    st.session_state.timer_active = False
    timer_placeholder.success("목표 시간 완료! '제출' 버튼을 눌러 보상을 받으세요.")
    if button_placeholder.button("공부 끝! (제출)"):
        earned_money = st.session_state.timer_duration * 10
        st.session_state.money += earned_money
        st.session_state.total_study_time += st.session_state.timer_duration
        st.balloons()
        st.success(f"💰 **{earned_money}머니**를 획득했습니다! 잠시 후 홈으로 이동합니다.")
        time.sleep(3)
        go_to_page('home')
        st.rerun()

# --- 게임 화면 (수정된 부분!) ---
elif st.session_state.page == 'game':
    st.title("🎮 미니 게임")
    st.write(f"현재 보유 머니: **{st.session_state.money} 머니**")
    st.divider()

    # --- ✨ 핵심 수정 ✨ ---
    # 게임을 시작하기 전에 최소 배팅 금액(10머니)이 있는지 확인합니다.
    MIN_BET = 10
    if st.session_state.money < MIN_BET:
        st.warning(f"머니가 부족하여 게임을 할 수 없습니다. 최소 {MIN_BET}머니가 필요합니다.")
        st.info("공부를 해서 머니를 모아오세요! 💪")
    else:
        # 돈이 충분할 때만 게임 선택 화면을 보여줍니다.
        game_choice = st.selectbox(
            "플레이할 게임을 선택하세요!",
            ("🎲 홀/짝 게임", "🔢 숫자 맞추기", "🔮 구슬 레이스")
        )

        # --- 게임 1: 홀/짝 게임 ---
        if game_choice == "🎲 홀/짝 게임":
            st.subheader("🎲 홀/짝 게임")
            bet_money_odd_even = st.number_input(
                "머니를 거세요!", 
                min_value=MIN_BET, 
                max_value=st.session_state.money,
                step=10,
                key="bet_odd_even"
            )
            user_choice_odd_even = st.radio("선택하세요:", ("홀", "짝"), key="choice_odd_even")
            if st.button("결과 확인!", key="btn_odd_even"):
                random_number = random.randint(1, 100)
                result = "홀" if random_number % 2 != 0 else "짝"
                st.info(f"컴퓨터의 숫자는 **{random_number}** 이므로 **'{result}'** 입니다!")
                if user_choice_odd_even == result:
                    st.session_state.money += bet_money_odd_even
                    st.success(f"축하합니다! **{bet_money_odd_even}머니**를 얻었습니다!")
                    st.balloons()
                else:
                    st.session_state.money -= bet_money_odd_even
                    st.error(f"아쉽네요. **{bet_money_odd_even}머니**를 잃었습니다.")
                time.sleep(2)
                st.rerun()

        # --- 게임 2: 숫자 맞추기 ---
        elif game_choice == "🔢 숫자 맞추기":
            st.subheader("🔢 숫자 맞추기 (1~10)")
            bet_money_number = st.number_input(
                "머니를 거세요!", min_value=MIN_BET, max_value=st.session_state.money, step=10, key="bet_number"
            )
            user_guess_number = st.number_input(
                "1부터 10 사이의 숫자를 선택하세요.", min_value=1, max_value=10, step=1, key="guess_number"
            )
            if st.button("결과 확인!", key="btn_number"):
                correct_number = random.randint(1, 10)
                st.info(f"정답은 **{correct_number}** 입니다!")
                if user_guess_number == correct_number:
                    st.session_state.money += bet_money_number
                    st.success(f"대단해요! **{bet_money_number}머니**를 얻었습니다!")
                    st.balloons()
                else:
                    st.session_state.money -= bet_money_number
                    st.error(f"아쉽네요. **{bet_money_number}머니**를 잃었습니다.")
                time.sleep(2)
                st.rerun()

        # --- 게임 3: 구슬 레이스 ---
        elif game_choice == "🔮 구슬 레이스":
            st.subheader("🔮 구슬 레이스")
            bet_money_marble = st.number_input(
                "머니를 거세요!", min_value=MIN_BET, max_value=st.session_state.money, step=10, key="bet_marble"
            )
            user_choice_marble = st.radio(
                "어떤 구슬이 1등을 할까요?",
                ("🔴 빨강 구슬", "🔵 파랑 구슬", "🟢 초록 구슬"),
                key="choice_marble"
            )
            if st.button("레이스 시작!", key="btn_marble"):
                marbles = ["🔴 빨강 구슬", "🔵 파랑 구슬", "🟢 초록 구슬"]
                winner = random.choice(marbles)
                with st.spinner("구슬들이 열심히 달리는 중..."):
                    time.sleep(2)
                st.info(f"**{winner}**이(가) 1등으로 들어왔습니다!")
                if user_choice_marble == winner:
                    st.session_state.money += bet_money_marble
                    st.success(f"정확해요! **{bet_money_marble}머니**를 얻었습니다!")
                    st.balloons()
                else:
                    st.session_state.money -= bet_money_marble
                    st.error(f"아쉽네요. **{bet_money_marble}머니**를 잃었습니다.")
                time.sleep(2)
                st.rerun()
            
    if st.button("🏠 홈으로 돌아가기", key="btn_game_home"):
        go_to_page('home')
        st.rerun()