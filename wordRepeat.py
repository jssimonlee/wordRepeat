import streamlit as st
import time
import random
import os

def showWords(data, questCol, answCol, dilimCol, timeSel, searchFilter):
    try:
        with open(selected_file,'r', encoding='utf-8') as f:
            voc = f.readlines()
            if searchFilter:
                try:
                    if "-" in searchFilter:
                        start = int(searchFilter.split("-")[0])-1
                        end = int(searchFilter.split("-")[1])
                        if start <= len(voc) and end <= len(voc) + 1:
                            voc = voc[start:end]
                        else:
                            st.warning(f'구간이 전체 범위를 초과하였습니다. 다시 설정해 주세요. 최대범위: {len(voc)}')
                    else:
                        vocFilter = []
                        for v in voc:
                            if searchFilter in v:
                                vocFilter.append(v)
                        voc = vocFilter
                except Exception as e:
                    st.write(e)
                    st.warning('구간을 지정하려면 숫자 2개를 중간에 "-"를 넣고 연결하세요(예:1-20)')
    except:
        st.warning("파일을 utf-8로 다시 저장해서 업로드 해주세요.")
    if dilimCol == "자동":
        if  "\t" in voc[0].strip():
            dilimCol = "\t"
        elif "  " in voc[0].strip():
            dilimCol = "  "
        elif "," in voc[0].strip():
            dilimCol = ","
        elif " " in voc[0].strip():
            dilimCol = " "
        else:
            dilimCol = "    "
    elif dilimCol == "탭": dilimCol = "\t"
    elif dilimCol == "빈칸1개": dilimCol = " "
    elif dilimCol == "빈칸2개": dilimCol = "  "
    elif dilimCol == "콤마": dilimCol = ","
    placeholder = st.empty()
    try:
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
    except:
        try:
            if "  " in voc[0].strip():
                st.warning("열구분자를 빈칸2개로 설정하세요(또는 열선택을 확인하세요)")
            elif "\t" in voc[0].strip():
                st.warning("열구분자를 탭으로 설정하세요(또는 열선택을 확인하세요)")
            else:
                st.warning("설정 값을 확인하고 다시 실행하세요.")
        except:
            st.warning("파일이 정상적이지 않습니다.")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['🕹️ 반복학습', "파일 업로드/내용확인", "파일편집", "단어 직접입력/단어찾기", "파일삭제", "파일 다운로드"])
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
        col1,col2,col3,col4,col5,col6 = st.columns([10,4,4,6,4,5])
        with col1:
            selected_file = st.selectbox('파일선택',file_list_wanted)
        with col2:
            questCol = st.selectbox("질문열",[1,2,3,4]) - 1
        with col3:
            answCol = st.selectbox("해답열",[1,2,3,4],1) - 1
        with col4:
            dilimCol = st.selectbox("열 구분자",["자동","탭","빈칸1개","빈칸2개","콤마"],0)
        with col5:
            timeSel = st.selectbox("시간 간격",[1,2,3,4,5,6,8,10,20,30,60],2)
        with col6:
            searchFilter = st.text_input("필터/구간(-)")
        submitted = st.form_submit_button("시작")
        if submitted:
            showWords(selected_file, questCol, answCol, dilimCol, timeSel, searchFilter)

    on = st.toggle('필터/구간 설명')
    if on:
        st.write('* "필터/구간"설정중 필터는 원하는 단어를 입력하면 입력한 단어가 포함된 것만 추출함 \n* 구간은 데이터의 일부 번호대(예:1-20) 만 나오게 할 수 있다 \n* 둘다 는 "|"로 연결한다')

with tab2:
    # 파일 업로드/내용확인
    with st.form("upload_Form"):
        st.subheader("파일 업로드")
        st.info("* 파일은 txt파일(utf-8로 저장)로 되어 있어야 하고 구분자(Tab등)로 열이 구분되어 있어야 한다.")
        uploaded_file = st.file_uploader("업로드 파일을 선택하세요", type=extList)
        if uploaded_file is not None:
            with open(uploaded_file.name,"wb") as f:
                f.write(uploaded_file.getbuffer())
        submitted = st.form_submit_button("파일저장")
        if submitted:
            st.info(f'{uploaded_file.name}이 업로드 되었습니다.')
    with st.form("check_file"):
        st.subheader("파일 간단 내용확인")
        file_list = os.listdir()
        file_list_wanted = []
        for file in file_list:
            root, extension = os.path.splitext(file)
            if extension.replace('.','') in extList:
                if file != 'requirements.txt':
                    file_list_wanted.append(file)
        selected_file = st.selectbox('확인하고 싶은 파일을 선택하세요.',file_list_wanted)
        submitted = st.form_submit_button("내용확인")
        if selected_file and submitted:
            try:
                with open(selected_file,'r', encoding='utf-8') as f:
                    firstline = f.readline().replace("  ","{2칸}").replace("\t","{tab}")
                    secondline = f.readline().strip().replace("  ","{2칸}").replace("\t","{tab}")
                    kbyteSize = int(os.path.getsize(selected_file)/1024)
                    kbyteSizeStr = str(kbyteSize) + " Kbytes"
                    if kbyteSize < 10:
                        kbyteSize = os.path.getsize(selected_file)
                        kbyteSizeStr = str(kbyteSize) + " bytes"
                    dispTxt = f"""[1번째라인] {firstline}
[2번째라인] {secondline}\n
[총 라인수] {len(f.readlines())}\n
[파일사이즈] {kbyteSizeStr}"""
                    st.success(dispTxt)
                    # st.write(len(f.readlines()))
            except:
                st.warning('파일을 메모장에서 "utf-8"로 다시 저장하세요')
with tab3:
    # 파일편집
    file_list = os.listdir()
    file_list_wanted = []
    for file in file_list:
        root, extension = os.path.splitext(file)
        if extension.replace('.','') in extList:
            if file != 'requirements.txt':
                file_list_wanted.append(file)
    selected_file = st.selectbox('편집하고 싶은 파일을 선택하세요.',file_list_wanted)
    with open(selected_file,'r', encoding='utf-8') as f:
        vocTxt = f.read()
    inputText = st.text_area("파일내용",vocTxt,250)
    submitted = st.button("저장")
    if submitted and inputText:
        with open(selected_file,"w",encoding="utf-8") as f:
            f.write(inputText)
            st.info('파일이 저장되었습니다.')
with tab4:
    # 단어 직접입력
    with st.form("inputText_Form"):
        st.subheader("단어 직접입력")
        st.info("* 만들 텍스트 화일의 이름과 내용을(2칸 띄워서 나열하거나 복사한 것을 붙여넣기) 넣고 저장버튼을 누르세요.")
        fName = st.text_input('저장 할 파일 이름을 입력하세요(.txt는 자동입력)')
        inputText = st.text_area('저장 할 내용을 입력하세요')
        submitted3 = st.form_submit_button('저장')
        if fName and inputText and submitted3:
            with open(fName + ".txt","w",encoding="utf-8") as f:
                f.write(inputText)
                st.info('파일이 저장되었습니다.')
    # 단어 찾기
    with st.form("find_word"):
        st.subheader("전체에서 단어 찾기")
        searchWord = st.text_input('찾을 단어를 입력하세요')
        submittedSearch = st.form_submit_button('찾기')
        if searchWord and submittedSearch:
            file_list = os.listdir()
            file_list_wanted = []
            for file in file_list:
                root, extension = os.path.splitext(file)
                if extension.replace('.','') in extList:
                    if file != 'requirements.txt':
                        with open(file,"r",encoding="utf-8") as f:
                            count = 0
                            for line in f.readlines():
                                count += 1
                                if searchWord in line:
                                    st.success(f"[{file}] [{count}번라인] : {line}")
   
with tab5:
    # with st.form("delete_Form"):
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
    submitted1 = st.button("삭제")
    if submitted1 and selected_file:
        os.remove(os.path.join(os.getcwd(),selected_file))
        st.warning(f'"{selected_file}" 파일이 삭제되었습니다.')
        st.info("사이트를 다시 로드하세요(재실행)")
        # if "button1" not in st.session_state:
        #     st.session_state["button1"] = False
        # if "button2" not in st.session_state:
        #     st.session_state["button2"] = False
        # if submitted1:
        #     st.session_state["button1"] = not st.session_state["button1"]
        # if st.session_state["button1"]:
        #     submitted2 = st.button(f'"{selected_file}" 이 파일을 정말로 삭제하시겠습니까?')
        #     if submitted2:
        #         st.session_state["button2"] = not st.session_state["button2"]
        # if st.session_state["button2"]:
        #     os.remove(selected_file)
        #     st.warning(f'"{selected_file}" 파일이 삭제되었습니다.')
        #     st.info("사이트를 다시 로드하세요(재실행)")

with tab6:
    #form에서는  download_button을 쓸 수 없어서 form 사용 안함
    # 다운로드
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
