import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    .main {
        padding-top: 0px !important; /* 完全移除主頁面的頂部內距 */
    }
    header {
        visibility: hidden; /* 隱藏 Streamlit 預設的頁面標題與資訊 */
    }
    .block-container {
        padding-top: 0px !important; /* 再次減少內容區的頂部內距 */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 設定標題
st.title("🏡 錦州街都更補償計算器")
st.markdown("""
這個應用程式可以幫助您快速計算錦州街都更分房與找補金額。
請輸入相關資訊，我們將根據原始計算邏輯為您提供結果。
""")

# **用戶輸入**
saved_area = st.number_input("請輸入分到的房子坪數（坪）", min_value=0.0, value=89.09)
floor = st.slider("請選擇樓層", min_value=3, max_value=28, value=15)  # 樓層選擇
car_space = st.selectbox("請選擇想要保留的車位數", [0, 1, 2])
car_floor = st.selectbox("請選擇車位樓層", [1, 2, 3, 4, 5])

# **根據樓層決定可選房號**
house_ids = ["K", "L", "M", "N", "O", "P", "Q", "R"]
floor_index = (28 - floor) * 8  # 計算對應的樓層索引
available_houses = [f"{house}{floor}" for house in house_ids]

# **建立房屋數據**
data = {
    "房號": available_houses,
    "權狀坪": [23.1, 41.9, 19.1, 19.1, 19.1, 40.1, 14.2, 15.1],
    "專有坪": [15.2, 27.5, 12.6, 12.6, 12.6, 26.4, 9.3, 9.9],
    "公設坪": [7.9, 14.4, 6.6, 6.6, 6.6, 13.8, 4.9, 5.2],
    "找補金額/坪": [10.5, 13.5, 13.5, 13.5, 13.5, 13.5, 10.5, 10.5]
}

df = pd.DataFrame(data)

# **顯示樓層結構**
st.subheader("🏢 乙棟可選的房子及其權狀坪數")
house_layout = f"""
<style>
    table {{
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        margin-top: 20px;
        font-family: Arial, sans-serif;
    }}
    td, th {{
        border: 1px solid black;
        padding: 10px;
    }}
    .header {{
        background-color: #f2f2f2;
        font-weight: bold;
        font-size: 16px;
    }}
    .spacer {{
        background-color: #e8e8e8;
    }}
</style>

<table>
    <tr class="header">
        <td colspan="5">乙棟可選的房子及其權狀坪數</td>
    </tr>
    <tr class="header">
        <td colspan="5">選房時，可參考都更前 3 號三樓的情況</td>
    </tr>
    <tr class="header">
        <td colspan="5">權狀 47.2 坪，室內 33.82 坪</td>
    </tr>
    <tr>
        <td>{available_houses[6]}</td>
        <td>{available_houses[7]}</td>
        <td rowspan="2">電梯<br>| X |<br>{available_houses[0]}</td>
        <td>{available_houses[1]}</td>
        <td>{available_houses[2]}</td>
    </tr>
    <tr>
        <td>14.2 坪</td>
        <td>15.1 坪</td>
        <td>41.9 坪</td>
        <td>19.1 坪</td>
    </tr>
    <tr class="spacer">
        <td colspan="5">走廊</td>
    </tr>
    <tr>
        <td>{available_houses[5]}</td>
        <td>{available_houses[4]}</td>
        <td>{available_houses[3]}</td>
        <td>{available_houses[2]}</td>
        <td>{available_houses[1]}</td>
    </tr>
    <tr>
        <td>40.1 坪</td>
        <td>19.1 坪</td>
        <td>19.1 坪</td>
        <td>19.1 坪</td>
        <td>41.9 坪</td>
    </tr>
</table>
"""
st.markdown(house_layout, unsafe_allow_html=True)

# **選擇房號**
selected_house = st.selectbox("請選擇房號", df["房號"])

# **計算選擇房子的找補**
house_info = df[df["房號"] == selected_house]
land_size = house_info["權狀坪"].values[0]
compensate_per_pings = house_info["找補金額/坪"].values[0]
total_compensate = land_size * compensate_per_pings

# **計算車位補償**
car_compensate = [80, 60, 40, 20, 0]
car_adjustment = car_compensate[car_floor - 1] * car_space - 240 * 0.9 * (saved_area / 55 - car_space)

# **顯示計算結果**
st.subheader("🏠 計算結果")
st.write(f"🏢 **選擇的樓層**: {floor} 樓")
st.write(f"🔹 **土地權狀坪數**: {saved_area:.2f} 坪")
st.write(f"🔹 **可分得車位**: {saved_area / 55:.2f} 個")
st.write(f"🚗 **選擇的車位樓層**: 地下 {car_floor} 樓，共 {car_space} 個")
st.write(f"🔹 **選擇的房號**: {selected_house}")
st.write(f"🏡 **權狀坪數**: {land_size:.2f} 坪")
st.write(f"💰 **每坪找補金額**: {compensate_per_pings:.2f} 萬")
st.write(f"💰 **此房總找補金額**: {total_compensate:.2f} 萬")
st.write(f"🚗 **車位補償金額調整**: {car_adjustment:.2f} 萬")

final_compensate = total_compensate + car_adjustment
st.success(f"💰 **最終找補金額**: {final_compensate:.2f} 萬")
