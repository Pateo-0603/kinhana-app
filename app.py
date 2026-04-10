import math
import streamlit as st
import pandas as pd

# キングハナハナ-30のスペック
HANA_SPECS = {
    1: {"big": 292, "reg": 489},
    2: {"big": 282, "reg": 448},
    3: {"big": 273, "reg": 412},
    4: {"big": 264, "reg": 378},
    5: {"big": 253, "reg": 344},
    6: {"big": 232, "reg": 296},
}

def calculate_setting_probability(spins, big_count, reg_count):
    likelihoods = {}
    total_likelihood = 0

    for setting, spec in HANA_SPECS.items():
        p_big = 1 / spec["big"]
        p_reg = 1 / spec["reg"]

        prob_big = math.comb(spins, big_count) * (p_big ** big_count) * ((1 - p_big) ** (spins - big_count))
        prob_reg = math.comb(spins, reg_count) * (p_reg ** reg_count) * ((1 - p_reg) ** (spins - reg_count))

        likelihood = prob_big * prob_reg
        likelihoods[setting] = likelihood
        total_likelihood += likelihood

    if total_likelihood == 0:
        return None

    results = {}
    for setting, likelihood in likelihoods.items():
        percentage = (likelihood / total_likelihood) * 100
        results[f"設定{setting}"] = round(percentage, 2)

    return results

# ==========================================
# ここからがアプリの画面（UI）を作るコード
# ==========================================

st.title("🌺 キングハナハナ 設定推測アプリ")
st.write("現在の回転数とボーナス回数を入力してください。")

# 入力フォーム（横に並べる）
col1, col2, col3 = st.columns(3)

with col1:
    spins = st.number_input("総回転数", min_value=1, value=3000, step=100)
with col2:
    big = st.number_input("BIG回数", min_value=0, value=10, step=1)
with col3:
    reg = st.number_input("REG回数", min_value=0, value=10, step=1)

# ボタンが押されたら計算開始
if st.button("判別する！", type="primary"):
    probabilities = calculate_setting_probability(spins, big, reg)

    if probabilities:
        st.subheader("📊 判別結果")
        
        # 確率が高い順に並び替え
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        
        # 最も可能性が高い設定を強調表示
        top_setting = sorted_probs[0][0]
        top_prob = sorted_probs[0][1]
        st.success(f"現在最も可能性が高いのは **{top_setting} ({top_prob}%)** です！")

        # グラフで表示して「アプリ感」を出す
        df = pd.DataFrame(probabilities.values(), index=probabilities.keys(), columns=["確率(%)"])
        st.bar_chart(df)
        
        # 詳細な数値を表で表示
        st.write("▼ 各設定の詳細な確率")
        st.table(df.T) # 横向きの表にして見やすくする

    else:
        st.error("データが極端すぎるため計算できませんでした。（入力ミスがないか確認してください）")