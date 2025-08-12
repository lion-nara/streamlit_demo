# app.py
# -----------------------------
# 나라 전용: 연금 시뮬레이터 + 가치주 대시보드
# 복붙 후:  streamlit run app.py
# -----------------------------
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # Mac
    matplotlib.rc('font', family='AppleGothic')
else:  # 리눅스 (Streamlit Cloud)
    matplotlib.rc('font', family='NanumGothic')

# 마이너스 깨짐 방지
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="연금 & 가치주 대시보드", page_icon="💰", layout="wide")

st.title("💰 연금 & 가치주 대시보드")
st.caption("슬라이더/입력만 바꿔도 바로 계산되는 미니 금융앱. (by 폴)")

tab1, tab2 = st.tabs(["🧮 연금 시뮬레이터", "📈 가치주 대시보드"])

# -----------------------------
# 🧮 연금 시뮬레이터
# -----------------------------
with tab1:
    st.subheader("적립 → 굴리기 → (선택) 인출 시뮬")
    st.markdown("낮에 배운 **Streamlit** 감각 그대로! 숫자만 바꾸면 표/그래프가 즉시 갱신돼요.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 1) 적립(저축) 구간")
        monthly_pay_krw = st.number_input("월 납입액 (만원)", min_value=0, value=15, step=1)
        years_save = st.slider("납입 기간 (년)", 1, 40, 10)
        annual_return_save = st.slider("연 수익률(%) - 적립기", 0.0, 15.0, 5.0, 0.1)
        compounds_per_year = st.selectbox("복리 주기", ["월복리(12)", "연복리(1)"], index=0)

    with c2:
        st.markdown("### 2) (선택) 인출 구간")
        use_withdrawal = st.checkbox("은퇴 후 인출 시뮬레이션 보기", value=True)
        if use_withdrawal:
            withdrawal_years = st.slider("인출 기간 (년)", 1, 40, 20)
            monthly_withdraw_krw = st.number_input("월 인출액 (만원)", min_value=0, value=200, step=10)
            annual_return_draw = st.slider("연 수익률(%) - 인출기", 0.0, 15.0, 4.0, 0.1)

    # 계산
    m = 12 if "12" in compounds_per_year else 1
    r_save = annual_return_save / 100 / m
    n_save = years_save * m
    pmt = monthly_pay_krw * 10_000  # 만원 → 원 (계산용, 표시는 만원으로)
    # 월 적립의 미래가치: FV = PMT * [((1+r)^n - 1) / r]
    fv_save = pmt * (((1 + r_save) ** n_save - 1) / r_save) if r_save > 0 else pmt * n_save

    # 연도별 잔고(적립기)
    years = np.arange(1, years_save + 1)
    balances = []
    for y in years:
        ny = y * m
        bal = pmt * (((1 + r_save) ** ny - 1) / r_save) if r_save > 0 else pmt * ny
        balances.append(bal)

    df_save = pd.DataFrame({
        "Year": years,
        "Balance(만원)": np.array(balances) / 10_000
    })

    c3, c4 = st.columns(2)
    with c3:
        st.metric("총 납입액(만원)", f"{(monthly_pay_krw*12*years_save):,.0f}")
        st.metric("적립기 끝 잔고(만원)", f"{(fv_save/10_000):,.0f}")
    with c4:
        st.write("연도별 잔고(만원) 미리보기")
        st.dataframe(df_save.head(12), use_container_width=True)

    # 선형 차트(적립기)
    st.markdown("#### 적립기 잔고 변화")
    st.line_chart(df_save.set_index("Year"))

    # 인출 시뮬 (선택)
    if use_withdrawal:
        st.markdown("---")
        st.markdown("### 인출 구간 시뮬레이션 결과")
        # 월 인출 계산
        r_draw = annual_return_draw / 100 / 12
        monthly_withdraw = monthly_withdraw_krw * 10_000

        months = withdrawal_years * 12
        bal = fv_save
        trace = []
        for t in range(1, months + 1):
            bal = bal * (1 + r_draw) - monthly_withdraw
            trace.append(bal)

        df_draw = pd.DataFrame({
            "Month": np.arange(1, months + 1),
            "Balance(만원)": np.array(trace) / 10_000
        })

        # 요약 지표
        depleted_month = next((i+1 for i, v in enumerate(trace) if v <= 0), None)
        c5, c6 = st.columns(2)
        with c5:
            if depleted_month:
                yr = depleted_month // 12
                mo = depleted_month % 12
                when = f"{yr}년 {mo}개월 후" if mo else f"{yr}년 후"
                st.metric("잔고 소진 시점(예상)", when)
            else:
                st.metric("잔고 소진 시점(예상)", "시뮬 기간 내 소진 안 됨")

        with c6:
            st.metric("인출 종료 시 잔고(만원)", f"{max(df_draw['Balance(만원)'].iloc[-1],0):,.0f}")

        # 그래프 (Matplotlib로 히스토리 느낌)
        fig, ax = plt.subplots()
        ax.plot(df_draw["Month"], df_draw["Balance(만원)"])
        ax.set_xlabel("Month")
        ax.set_ylabel("Balance(만원)")
        ax.set_title("인출기 잔고 변화")
        st.pyplot(fig)

        st.info("팁: 인출액을 줄이거나 수익률이 높아지면 소진 시점이 뒤로 밀려요.")

# -----------------------------
# 📈 가치주 대시보드
# -----------------------------
with tab2:
    st.subheader("CSV 업로드 또는 예시 데이터로 바로 시작")
    st.markdown("""
**CSV 컬럼 권장**: `종목, PER, PBR, 배당수익률, ROE`  
최소한 `종목`과 몇 가지 지표만 있어도 됩니다. (숫자 컬럼은 % 없이 숫자만)
""")

    uploaded = st.file_uploader("CSV 업로드 (UTF-8 권장)", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
        except Exception:
            df = pd.read_csv(uploaded, encoding="cp949")
    else:
        # 예시 데이터
        df = pd.DataFrame({
            "종목": ["삼성물산", "현대차2우B", "LG", "GS", "한화", "롯데지주"],
            "PER": [8.5, 5.2, 7.0, 6.3, 6.8, 9.1],
            "PBR": [0.5, 0.3, 0.6, 0.4, 0.5, 0.45],
            "배당수익률": [3.5, 5.2, 4.0, 4.5, 3.0, 2.8],
            "ROE": [8.0, 9.5, 7.2, 6.0, 6.5, 5.0]
        })

    # 숫자형으로 강제 변환(문자 들어와도 안전하게)
    for col in ["PER", "PBR", "배당수익률", "ROE"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    st.markdown("#### 필터")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        max_per = st.number_input("최대 PER", value=float(np.nan))
    with c2:
        max_pbr = st.number_input("최대 PBR", value=float(np.nan))
    with c3:
        min_div = st.number_input("최소 배당수익률(%)", value=float(0.0))
    with c4:
        min_roe = st.number_input("최소 ROE(%)", value=float(0.0))

    filt = pd.Series([True]*len(df))
    if "PER" in df and not np.isnan(max_per):
        filt &= df["PER"] <= max_per
    if "PBR" in df and not np.isnan(max_pbr):
        filt &= df["PBR"] <= max_pbr
    if "배당수익률" in df:
        filt &= df["배당수익률"] >= min_div
    if "ROE" in df:
        filt &= df["ROE"] >= min_roe

    df_f = df[filt].copy()

    # 간단 가치 스코어 (작을수록 좋은 PER/PBR은 역순, 클수록 좋은 배당/ROE는 정순)
    def z(series, reverse=False):
        s = (series - series.mean())/ (series.std() if series.std() else 1)
        return -s if reverse else s

    score_parts = []
    if "PER" in df_f: score_parts.append(z(df_f["PER"], reverse=True))
    if "PBR" in df_f: score_parts.append(z(df_f["PBR"], reverse=True))
    if "배당수익률" in df_f: score_parts.append(z(df_f["배당수익률"], reverse=False))
    if "ROE" in df_f: score_parts.append(z(df_f["ROE"], reverse=False))

    if score_parts:
        df_f["가치스코어"] = np.mean(score_parts, axis=0)
        df_f.sort_values("가치스코어", ascending=False, inplace=True)

    st.markdown("#### 필터 결과")
    st.dataframe(df_f.reset_index(drop=True), use_container_width=True)

    if "배당수익률" in df_f and "종목" in df_f:
        st.markdown("#### 배당수익률 비교")
        st.bar_chart(df_f.set_index("종목")["배당수익률"])

    if "가치스코어" in df_f and "종목" in df_f:
        st.markdown("#### 가치스코어(높을수록 종합 점수 우수)")
        st.bar_chart(df_f.set_index("종목")["가치스코어"])

    st.info("팁: CSV를 ISA 보유 종목으로 바꾸면 **나만의 가치주 대시보드** 완성!")

# 푸터
st.markdown("---")
st.caption("⚙️ 사용법: 파일 저장 → `streamlit run app.py` 실행. 값만 바꿔도 즉시 반영됩니다.")
