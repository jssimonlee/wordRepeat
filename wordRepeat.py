import streamlit as st
import time
import random
import os

def showWords(data, questCol, answCol, dilimCol, timeSel):
    if dilimCol == "탭": dilimCol = "\t"
    elif dilimCol == "빈칸1개": dilimCol = " "
    elif dilimCol == "빈칸2개": dilimCol = "  "
    elif dilimCol == "콤마": dilimCol = ","
    with open(selected_file,'r', encoding='utf-8') as f:
        voc = f.readlines()
    placeholder = st.empty()
    while True:
        ranNum = random.randint(0,len(voc)-1)
        # 마지막 빈 공간이 선택되면 그냥 무시하도록
        if voc[ranNum].strip() == "":
            continue
        with placeholder.container():
            st.success(voc[ranNum].split(dilimCol)[questCol])
            st.write(str(ranNum+1) + " / " + str(len(voc)))
            time.sleep(timeSel)
            placeholder1 = st.empty()
            with placeholder.container():
                disTxt = voc[ranNum].split(dilimCol)[questCol] + ' :\t' + voc[ranNum].split(dilimCol)[answCol]
                # 질문열과 해답열을 제외하고 나머지는 그냥 답에 뒤에 같이 표시
                if len(voc[ranNum].split(dilimCol)) > 2:
                    colList = list(range(len(voc[ranNum].split(dilimCol))))
                    colList.remove(questCol)
                    colList.remove(answCol)
                    for i in range(len(voc[ranNum].split(dilimCol))-2):
                        disTxt = disTxt + "\t" + voc[ranNum].split(dilimCol)[colList[i]]  
                        
                st.success(disTxt)
                time.sleep(timeSel)
tab1, tab2, tab3, tab4 = st.tabs(['반복학습', "파일 업로드", "파일삭제", "파일 다운로드"])
extList = ['txt']

with tab1:
    with st.form("run_Form"):
        file_list = os.listdir()
        file_list_wanted = []
        for file in file_list:
            root, extension = os.path.splitext(file)
            if extension.replace('.','') in extList:
                if file != 'requirements.txt':
                    file_list_wanted.append(file)
        col1,col2,col3,col4,col5 = st.columns([10,4,4,6,4])
        with col1:
            selected_file = st.selectbox('파일선택',file_list_wanted)
        with col2:
            questCol = st.selectbox("질문열 선택",[1,2,3]) - 1
        with col3:
            answCol = st.selectbox("해답열 선택",[1,2,3],1) - 1
        with col4:
            dilimCol = st.selectbox("열 구분자",["탭","빈칸1개","빈칸2개","콤마"],2)
        with col5:
            timeSel = st.selectbox("시간 간격",[1,2,3,4,5,6,8,10,20,30,60],2)
        submitted = st.form_submit_button("시작")
        try:
            if submitted:
                showWords(selected_file, questCol, answCol, dilimCol, timeSel)
        except:
            st.warning("설정 값을 확인하고 다시 실행하세요.")

with tab2:
    with st.form("upload_Form"):
        st.info("* 파일은 txt파일(utf-8로 저장)로 되어 있어야 하고 구분자로 열이 구분되어 있어야 한다.")
        uploaded_file = st.file_uploader("업로드 파일을 선택하세요", type=extList)
        
        if uploaded_file is not None:
            # st.write(uploaded_file.name,uploaded_file.size)
            # with open(uploaded_file.name,"wb") as f:
            #     f.write(uploaded_file.getbuffer())
        file_list = os.listdir()
        file_list_wanted = []
        for file in file_list:
            root, extension = os.path.splitext(file)
            if extension.replace('.','') in extList:
                if file != 'requirements.txt':
                    file_list_wanted.append(file)
        selected_file = st.selectbox('확인하고 싶은 파일을 선택하세요.',file_list_wanted)
        submitted = st.form_submit_button("파일저장/내용확인")
        if selected_file and submitted:
            try:
                with open(selected_file,'r', encoding='utf-8') as f:
                    firstline = f.readline().replace("  ","{2칸}").replace("\t","{tab}")
                    secondline = f.readline().strip().replace("  ","{2칸}").replace("\t","{tab}")
                    dispTxt = f"""[1번째라인] {firstline}
[2번째라인] {secondline}\n
[총 라인수] {len(f.readlines())}"""
                    st.success(dispTxt)
                    # st.write(len(f.readlines()))
            except:
                st.warning('파일을 메모장에서 "utf-8"로 다시 저장하세요')

with tab3:
    with st.form("delete_Form"):
        extList = ['txt']
        file_list = os.listdir()
        file_list_wanted = []
        for file in file_list:
            root, extension = os.path.splitext(file)
            if extension.replace('.','') in extList:
                if file != 'requirements.txt':
                    file_list_wanted.append(file)
        selected_file = st.selectbox('삭제하고 싶은 파일을 선택하세요.',file_list_wanted)
        # button은 한번 실행하면 rerun이 되어서 다음 버튼이 실행이 안된다.
        submitted1 = st.form_submit_button("삭제")
        if submitted1 and selected_file:
            if "button1" not in st.session_state:
                st.session_state["button1"] = False
            if "button2" not in st.session_state:
                st.session_state["button2"] = False
            if submitted1:
                st.session_state["button1"] = not st.session_state["button1"]
            if st.session_state["button1"]:
                submitted2 = st.form_submit_button(f'"{selected_file}" 이 파일을 정말로 삭제하시겠습니까?')
                if submitted2:
                    st.session_state["button2"] = not st.session_state["button2"]
            if st.session_state["button2"]:
                os.remove(selected_file)
                st.warning(f'"{selected_file}" 파일이 삭제되었습니다.')
                st.info("사이트를 다시 로드하세요(재실행)")

with tab4:
    #form에서는  download_button을 쓸 수 없어서 form 사용 안함
    file_list = os.listdir()
    file_list_wanted = []
    for file in file_list:
        root, extension = os.path.splitext(file)
        if extension.replace('.','') in extList:
            if file != 'requirements.txt':
                file_list_wanted.append(file)
    selected_file = st.selectbox('파일선택',file_list_wanted)
    if selected_file:
        with open(selected_file,'r',encoding='utf-8') as f:
            if st.download_button('다운로드', f, selected_file):
                st.success(f'{selected_file} 파일이 다운로드 되었습니다.')
