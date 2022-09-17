from faulthandler import disable
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

movies = pickle.load(open('./data/movies.pickle', 'rb'))
cosine_sim = pickle.load(open('./data/cosine_sim.pickle', 'rb'))

ott_idx = {
    0 : "Seezn",
    1 : "Serieson",
    2 : "Watcha",
    3 : "Wavve",
    4 : "Netflix",
    5 : "Tving"
}

def get_recommendation(title):
  # return data type
  return_dict = {}
  ott_dict = {}

  # ott 가격정보 상수화하기
  seezn_price = 9000
  watcha_price = 7900
  wavve_price = 7900
  netflix_price = 9500
  tiving_price = 7900  

  # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
  idx = movies[movies['name'] == title].index[0]

  # 코사인 유사도 매트릭스 에서 idx에 해당하는 데이터를 (idx, 유사도 형태로 얻기)
  sim_scores = list(enumerate(cosine_sim[idx]))

  # 정렬하기
  # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
  sim_scores = sorted(sim_scores, key=lambda x : x[1], reverse=True)

  # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
  sim_scores = sim_scores[1:10] # 자기 자신을 제외함

  # 추천 영화 목록 10개의 인덱스 정보 추출
  movie_indices = [i[0] for i in sim_scores]

  synopsis = []
  for item in movie_indices:
    return_dict[movies['name'].iloc[item]] = list(movies.iloc[item, 3:])
    synopsis.append(movies['synopsis'].iloc[item])

  
  images = []
  for title in list(return_dict.keys()):
    path = "./ott_image/" + title + ".jpg"
    images.append(path)

  # 가성비 확인 ott dict 만들기
  ott_list = []
  for _, ott in return_dict.items():
    ott_list.append(ott)
  ott_nparray = np.array(ott_list)
  ott_sum = np.sum(ott_nparray, axis=0)
  # print(ott_sum)

  try :
    ott_dict['seezn'] = int(seezn_price / ott_sum[0])
  except:
    ott_dict['seezn'] = seezn_price
  # seris_on은 편당 가격제이기 때문에 가성비 체크에서 제외
  try:
    ott_dict['watcha'] = int(watcha_price / ott_sum[2])
  except:
    ott_dict['watcha'] = watcha_price
  try:
    ott_dict['wavve'] = int(wavve_price / ott_sum[3])
  except:
    ott_dict['wavve'] = wavve_price
  try:
    ott_dict['netflix'] = int(netflix_price / ott_sum[4])
  except:
    ott_dict['netflix'] = netflix_price
  try:
    ott_dict['tiving'] = int(tiving_price / ott_sum[5])
  except:
    ott_dict['tiving'] = tiving_price
  # print(ott_dict)

  # 최선의 선택 출력
  vest_choice = np.argmin(np.array(list(ott_dict.values())))
  # print(vest_choice)
  ott_dict['vest_choice'] = 0 if vest_choice == 0 else vest_choice + 1

  # 인덱스 값을 통해서 영화 제목을 얻어오기(return)
  return images, return_dict, ott_dict, synopsis, ott_sum


# print(get_recommendation("이상한 변호사 우영우"))


st.set_page_config(
    page_title="stolio flix",
    page_icon="🔥")

st.image('./logo/stolio_logo.png', width=150)
st.header('stolio flix')

movie_list = movies['name'].values
title = st.selectbox('Choose a drama you like', movie_list)  # 선택한 변수가 title로 들어간다
# st.balloons()
if st.button('Recommend'):
    images, return_dict, ott_dict, synopsis, ott_sum = get_recommendation(title)
    titles = list(return_dict.keys())

    st.write("")
    st.write("")
    st.write("")

    # st.info("추천 결과!")
    st.header(title + "과 가장 유사한 드라마는..?")
    idx = 0
    for i in range(0, 3):
        cols = st.columns(3)
        for col in cols:
          try:
            col.image(images[idx])
          except:
            col.image("./ott_image/img_falut.jpg")
          col.subheader(titles[idx])
          col.caption(synopsis[idx])

          for idx_, ott in enumerate(return_dict[titles[idx]]):
            if ott:
              col.image("./logo/" + ott_idx[idx_] + ".png", width=50)
          idx += 1

    st.write("")
    st.write("")
    st.write("")

    st.title("OTT 가성비 비교")
    st.info("추천한 드라마를 모두 보는데 가장 가성비가 좋은 OTT를 알려드립니다. 아래 차트는 추천된 드라마가 있는 OTT를 보여줍니다.")
    # ott_data = [['seezn', ott_sum[0]], ['watcha', ott_sum[2]], ['wavve', ott_sum[3]], ['netflix', ott_sum[4]], ['tiving', ott_sum[5]]]
    # df = pd.DataFrame(ott_data, columns=['ott', 'frequency'])
    # fig = px.bar(df, x='ott', y='frequency')
    # st.plotly_chart(fig)

    # plot
    COLOR = 'white'
    plt.rc('font', family='AppleGothic') # For MacOS
    plt.rcParams['axes.labelcolor'] = COLOR
    # plt.rcParams['text.color'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

    colors = ["#F94144", "#F3722C", "#F8961E", "#F9844A", "#F9C74F", "#90BE6D", "#43AA8B", "#4D908E", "#577590"]
    x = ['seezn', 'watcha', 'wavve', 'netflix', 'tving']
    fig = plt.figure(figsize=(11,7), facecolor='black')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor("black")
    before = np.array([0,0,0,0,0])
    for i, name in enumerate(return_dict.keys()):
        ott_ls = return_dict[name]
        input_ls = np.array(ott_ls[:1]+ott_ls[2:])
        ax.bar(x, input_ls, bottom=before, label=name, color=colors[i])
        before += input_ls

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1,1))
    st.pyplot(fig)

    st.write("")
    st.write("")
    st.write("")

    st.info("OTT 별 한개의 드라마를 시청하는데 들어가는 비용")
    st.caption("Seezn - " + str(ott_dict['seezn']) + "원 / 1 drama")
    st.caption("Watcha - " + str(ott_dict['watcha']) + "원 / 1 drama")
    st.caption("Wavve - " + str(ott_dict['wavve']) + "원 / 1 drama")
    st.caption("Netflix - " + str(ott_dict['netflix']) + "원 / 1 drama")
    st.caption("Tving - " + str(ott_dict['tiving']) + "원 / 1 drama")
    st.subheader("추천된 영화를 모두 보기에 가성비가 가장 좋은 OTT 는 \"" + ott_idx[ott_dict['vest_choice']] + "\" 입니다.")
    st.write("")
    st.write("")
    st.write("")
    st.warning('Seezn : 월 9000원, Watcha : 월 7900원, Wavve : 월 7900원, Netflix : 월 9500원, Tving : 월 7900원을 기준으로 계산되었습니다.', icon="⚠️")
