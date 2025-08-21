# streamlit_app.py

import streamlit as st
import time
import random
from datetime import datetime, timedelta

# --- 1. 세션 상태(Session State) 초기화 ---
# 앱의 상태를 저장하기 위한 변수들을 설정합니다.

# 페이지 관리
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 유저 데이터
if 'money' not in st.session_state:
    st.session_state.money = 0
if 'total_study_time' not in st.session_state:
    st.session_state.total_study_time = 0

# 타이머 데이터
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 0
if 'timer_end_time' not in st.session_state:
    st.session_state.timer_end_time = None
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False

# --- ✨ 캐릭터 꾸미기 기능 추가 ✨ ---
# 보유 아이템과 장착 아이템을 관리하는 상태 변수
if 'owned_items' not in st.session_state:
    # 카테고리별로 아이템을 관리합니다. '기본' 아이템은 처음부터 주어집니다.
    st.session_state.owned_items = {'모자': ['기본'], '액세서리': ['기본']}
if 'equipped_items' not in st.session_state:
    st.session_state.equipped_items = {'모자': '기본', '액세서리': '기본'}

# --- 상점에서 판매할 아이템 목록 ---
SHOP_ITEMS = {
    '모자': [
        {'name': '🤠 카우보이 모자', 'price': 100},
        {'name': '👑 왕관', 'price': 300},
        {'name': '🎓 학사모', 'price': 500}
    ],
    '액세서리': [
        {'name': '🕶️ 선글라스', 'price': 80},
        {'name': '🧣 목도리', 'price': 120},
        {'name': '🥇 금메달', 'price': 1000}
    ]
}

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
    
    # 버튼들을 컬럼으로 배치하여 깔끔하게 정렬
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏰ 공부하기", type="primary", use_container_width=True):
            go_to_page('timer_setup')
            st.rerun()
    with col2:
        if st.button("🎮 게임하기", use_container_width=True):
            go_to_page('game')
            st.rerun()
    with col3:
        # 캐릭터 꾸미기 페이지로 가는 버튼 추가
        if st.button("👕 캐릭터 꾸미기", use_container_width=True):
            go_to_page('character_shop')
            st.rerun()

# --- 타이머 설정 및 실행 화면 (이전과 동일) ---
# (코드는 이전 버전과 동일하므로 생략)
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

# --- 게임 화면 (이전과 동일, 오류 수정 버전) ---
# (코드는 이전 버전과 동일하므로 생략)
elif st.session_state.page == 'game':
    st.title("🎮 미니 게임")
    st.write(f"현재 보유 머니: **{st.session_state.money} 머니**")
    st.divider()
    MIN_BET = 10
    if st.session_state.money < MIN_BET:
        st.warning(f"머니가 부족하여 게임을 할 수 없습니다. 최소 {MIN_BET}머니가 필요합니다.")
        st.info("공부를 해서 머니를 모아오세요! 💪")
    else:
        game_choice = st.selectbox("플레이할 게임을 선택하세요!", ("🎲 홀/짝 게임", "🔢 숫자 맞추기", "🔮 구슬 레이스"))
        if game_choice == "🎲 홀/짝 게임":
            st.subheader("🎲 홀/짝 게임")
            bet_money_odd_even = st.number_input("머니를 거세요!", min_value=MIN_BET, max_value=st.session_state.money, step=10, key="bet_odd_even")
            user_choice_odd_even = st.radio("선택하세요:", ("홀", "짝"), key="choice_odd_even")
            if st.button("결과 확인!", key="btn_odd_even"):
                random_number = random.randint(1, 100)
                result = "홀" if random_number % 2 != 0 else "짝"
                st.info(f"컴퓨터의 숫자는 **{random_number}** 이므로 **'{result}'** 입니다!")
                if user_choice_odd_even == result:
                    st.session_state.money += bet_money_odd_even
                    st.success(f"축하합니다! **{bet_money_odd_even}머니**를 얻었습니다!"); st.balloons()
                else:
                    st.session_state.money -= bet_money_odd_even
                    st.error(f"아쉽네요. **{bet_money_odd_even}머니**를 잃었습니다.")
                time.sleep(2); st.rerun()
        elif game_choice == "🔢 숫자 맞추기":
            st.subheader("🔢 숫자 맞추기 (1~10)")
            bet_money_number = st.number_input("머니를 거세요!", min_value=MIN_BET, max_value=st.session_state.money, step=10, key="bet_number")
            user_guess_number = st.number_input("1부터 10 사이의 숫자를 선택하세요.", min_value=1, max_value=10, step=1, key="guess_number")
            if st.button("결과 확인!", key="btn_number"):
                correct_number = random.randint(1, 10)
                st.info(f"정답은 **{correct_number}** 입니다!")
                if user_guess_number == correct_number:
                    st.session_state.money += bet_money_number
                    st.success(f"대단해요! **{bet_money_number}머니**를 얻었습니다!"); st.balloons()
                else:
                    st.session_state.money -= bet_money_number
                    st.error(f"아쉽네요. **{bet_money_number}머니**를 잃었습니다.")
                time.sleep(2); st.rerun()
        elif game_choice == "🔮 구슬 레이스":
            st.subheader("🔮 구슬 레이스")
            bet_money_marble = st.number_input("머니를 거세요!", min_value=MIN_BET, max_value=st.session_state.money, step=10, key="bet_marble")
            user_choice_marble = st.radio("어떤 구슬이 1등을 할까요?", ("🔴 빨강 구슬", "🔵 파랑 구슬", "🟢 초록 구슬"), key="choice_marble")
            if st.button("레이스 시작!", key="btn_marble"):
                marbles = ["🔴 빨강 구슬", "🔵 파랑 구슬", "🟢 초록 구슬"]
                winner = random.choice(marbles)
                with st.spinner("구슬들이 열심히 달리는 중..."): time.sleep(2)
                st.info(f"**{winner}**이(가) 1등으로 들어왔습니다!")
                if user_choice_marble == winner:
                    st.session_state.money += bet_money_marble
                    st.success(f"정확해요! **{bet_money_marble}머니**를 얻었습니다!"); st.balloons()
                else:
                    st.session_state.money -= bet_money_marble
                    st.error(f"아쉽네요. **{bet_money_marble}머니**를 잃었습니다.")
                time.sleep(2); st.rerun()
    if st.button("🏠 홈으로 돌아가기", key="btn_game_home"):
        go_to_page('home'); st.rerun()


# --- ✨ 캐릭터 꾸미기 & 상점 페이지 (신규 추가!) ✨ ---
elif st.session_state.page == 'character_shop':
    st.title("👕 내 캐릭터 & 상점 🛒")
    st.write(f"현재 보유 머니: **{st.session_state.money} 머니**")
    st.divider()

    # st.tabs를 사용해 '꾸미기'와 '상점'을 분리
    tab1, tab2 = st.tabs(["내 캐릭터 꾸미기", "상점"])

    with tab1: # --- 내 캐릭터 꾸미기 탭 ---
        st.header("✨ 내 캐릭터")
        
        col1, col2 = st.columns([1, 2]) # 캐릭터와 아이템 선택 영역 분리

        with col1: # 캐릭터 표시 영역
            # 장착한 아이템에 따라 이모지를 표시
            # 아이템 이름에서 첫번째 글자(이모지)를 가져옵니다.
            hat_emoji = st.session_state.equipped_items['모자'].split(' ')[0] if st.session_state.equipped_items['모자'] != '기본' else '🙂'
            accessory_emoji = st.session_state.equipped_items['액세서리'].split(' ')[0] if st.session_state.equipped_items['액세서리'] != '기본' else ''
            
            # HTML과 CSS를 사용해 이모지를 크고 가운데 정렬하여 보여줍니다.
            st.markdown(f"<p style='font-size: 120px; text-align: center;'>{hat_emoji}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 60px; text-align: center;'>{accessory_emoji}</p>", unsafe_allow_html=True)
        
        with col2: # 아이템 장착 영역
            st.subheader("아이템 장착")
            # 보유한 아이템 목록으로 selectbox를 만듭니다.
            # 현재 장착 중인 아이템이 기본으로 선택되도록 index를 설정합니다.
            
            # 모자 장착
            current_hat_index = st.session_state.owned_items['모자'].index(st.session_state.equipped_items['모자'])
            equipped_hat = st.selectbox(
                "모자 변경",
                options=st.session_state.owned_items['모자'],
                index=current_hat_index
            )
            st.session_state.equipped_items['모자'] = equipped_hat

            # 액세서리 장착
            current_accessory_index = st.session_state.owned_items['액세서리'].index(st.session_state.equipped_items['액세서리'])
            equipped_accessory = st.selectbox(
                "액세서리 변경",
                options=st.session_state.owned_items['액세서리'],
                index=current_accessory_index
            )
            st.session_state.equipped_items['액세서리'] = equipped_accessory

    with tab2: # --- 상점 탭 ---
        st.header("🛒 아이템 상점")

        # 각 카테고리(모자, 액세서리)별로 아이템을 보여줍니다.
        for category, items in SHOP_ITEMS.items():
            st.subheader(f"{category} 상점")
            for item in items:
                col1, col2 = st.columns([3, 1])
                with col1:
                    # 이미 보유한 아이템은 '보유 중'으로 표시
                    if item['name'] in st.session_state.owned_items[category]:
                        st.markdown(f"✅ ~~{item['name']} (가격: {item['price']} 머니)~~ (보유 중)")
                    else:
                        st.markdown(f"{item['name']} (가격: {item['price']} 머니)")

                with col2:
                    # 보유하지 않은 아이템만 '구매' 버튼을 보여줍니다.
                    if item['name'] not in st.session_state.owned_items[category]:
                        # 각 버튼을 구분하기 위해 item 이름을 key로 사용
                        if st.button("구매", key=f"buy_{item['name']}", use_container_width=True):
                            if st.session_state.money >= item['price']:
                                st.session_state.money -= item['price']
                                st.session_state.owned_items[category].append(item['name'])
                                st.success(f"'{item['name']}'을(를) 구매했습니다!")
                                time.sleep(1) # 메시지를 잠시 보여준 후
                                st.rerun()    # 페이지를 새로고침하여 상태 업데이트
                            else:
                                st.error("머니가 부족합니다.")
            st.divider()

    if st.button("🏠 홈으로 돌아가기", key="btn_char_home"):
        go_to_page('home')
        st.rerun()