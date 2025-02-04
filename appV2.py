import streamlit as st
import pandas as pd

# 自訂 CSS 移除頂部空白
st.markdown(
    """
    <style>
    .main {
        padding-top: 0px !important;
    }
    header {
        visibility: hidden;
    }
    .block-container {
        padding-top: 0px !important;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        margin-top: 20px;
        font-family: Arial, sans-serif;
    }
    td, th {
        border: 1px solid black;
        padding: 10px;
    }
    .header {
        background-color: #f2f2f2;
        font-weight: bold;
        font-size: 16px;
    }
    .spacer {
        background-color: #e8e8e8;
    }
    .elevator {
        background-color: #d9ead3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 標題與介紹
st.title("🏡 錦州街都更補償計算器")
st.markdown("""
這個應用程式可以幫助您快速計算錦州街都更分房與找補金額。
請輸入相關資訊，我們將根據原始計算邏輯為您提供結果。
""")

# 使用者輸入權狀坪數
saved_area = st.number_input("請輸入分到的土地權狀坪數（坪）", min_value=0.0, value=100.0)
selected_floors = st.multiselect("請選擇樓層（可多選）", options=list(range(3, 29)), default=[26])
car_space = st.selectbox("請選擇想要保留的車位數", [0, 1, 2])
car_floor = st.selectbox("請選擇車位樓層 (地下幾樓)", [1, 2, 3, 4, 5])

# 動態生成房屋數據
def generate_floor_data(floor):
    base_floor = floor
    HouseID = [f"P{base_floor}", f"O{base_floor}", f"N{base_floor}", f"M{base_floor}", f"L{base_floor}", f"K{base_floor}", f"Q{base_floor}", f"R{base_floor}"]
    LandSize = [40.1, 19.1, 19.1, 19.1, 41.9, 23.1, 14.2, 15.1]
    Compensate = [10.5] * len(HouseID)  # 每坪找補金額（假設）
    return HouseID, LandSize, Compensate

# 動態顯示房屋參考圖
st.subheader(f"🏢 選擇的樓層房子及其權狀坪數")
for floor in selected_floors:
    HouseID, LandSize, _ = generate_floor_data(floor)
    house_layout = f"""
    <table>
        <tr class="header">
            <td>{HouseID[6]}</td>
            <td>{HouseID[7]}</td>
            <td class="elevator" rowspan="2">電梯<br>| X |</td>
            <td class="elevator" rowspan="2">電梯<br>| X |</td>
            <td>{HouseID[5]}</td>
        </tr>
        <tr>
            <td>{LandSize[6]} 坪</td>
            <td>{LandSize[7]} 坪</td>
            <td>{LandSize[5]} 坪</td>
        </tr>
        <tr class="spacer">
            <td colspan="5">走廊</td>
        </tr>
        <tr>
            <td>{HouseID[0]}</td>
            <td>{HouseID[1]}</td>
            <td>{HouseID[2]}</td>
            <td>{HouseID[3]}</td>
            <td>{HouseID[4]}</td>
        </tr>
        <tr>
            <td>{LandSize[0]} 坪</td>
            <td>{LandSize[1]} 坪</td>
            <td>{LandSize[2]} 坪</td>
            <td>{LandSize[3]} 坪</td>
            <td>{LandSize[4]} 坪</td>
        </tr>
    </table>
    """
    st.markdown(house_layout, unsafe_allow_html=True)

# 房屋選擇功能
selected_houses = []
for floor in selected_floors:
    HouseID, _, _ = generate_floor_data(floor)
    selected_houses += st.multiselect(f"請選擇 {floor} 樓的房號（可多選）", HouseID)

# 計算已選擇的房屋數據
total_selected_area = 0
total_compensate = 0
selected_house_details = []

for house in selected_houses:
    for floor in selected_floors:
        HouseID, LandSize, Compensate = generate_floor_data(floor)
        if house in HouseID:
            index = HouseID.index(house)
            selected_house_details.append({
                "樓層": floor,
                "房號": house,
                "權狀坪": LandSize[index],
                "每坪找補 (萬)": Compensate[index],
                "總找補金額 (萬)": LandSize[index] * Compensate[index]
            })
            total_selected_area += LandSize[index]
            total_compensate += LandSize[index] * Compensate[index]

# 顯示已選擇的房屋詳細資訊
st.subheader("🏢 已選擇的房屋資訊")
if selected_house_details:
    df_selected = pd.DataFrame(selected_house_details)
    st.table(df_selected)
else:
    st.write("尚未選擇任何房屋。")

# 計算剩餘坪數
remaining_area = saved_area - total_selected_area
if remaining_area >= 0:
    st.success(f"剩餘可用土地權狀坪數：{remaining_area:.2f} 坪")
else:
    over_area = abs(remaining_area)
    over_compensate = over_area * 120 * 0.9
    st.error(f"⚠️ 超出權狀坪數：{over_area:.2f} 坪，需補償金額：約 {over_compensate:.2f} 萬")

# 顯示總結果
st.subheader("💰 計算結果")
st.write(f"🔹 **土地權狀坪數**: {saved_area:.2f} 坪")
st.write(f"🔹 **已選擇的總坪數**: {total_selected_area:.2f} 坪")
st.write(f"🔹 **剩餘坪數**: {remaining_area:.2f} 坪")
if remaining_area < 0:
    st.write(f"🔹 **需補償金額**: 約 {over_compensate:.2f} 萬")
else:
    st.write(f"🔹 **總找補金額**: {total_compensate:.2f} 萬")
