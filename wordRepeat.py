import streamlit as st
import time
import random
import os
import re
# import extra_streamlit_components as stx

# 일본어 변환기
def engToHira(engTxt):
    jptoRomaji3 = {"pp":"っp","ss":"っs","tt":"っt","kk":"っk","dd":"っd","nn":"ん",
        "kya":"きゃ","kyu":"きゅ","kyo":"きょ","gya":"ぎゃ","gyu":"ぎゅ","gyo":"ぎょ","sha":"しゃ","shu":"しゅ","sho":"しょ","cha":"ちゃ","chu":"ちゅ",
        "cho":"ちょ","nya":"にゃ","nyu":"にゅ","nyo":"にょ","hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ","bya":"びゃ","byu":"びゅ","byo":"びょ","pya":"ぴゃ",
        "pyu":"ぴゅ","pyo":"ぴょ","mya":"みゃ","myu":"みゅ","myo":"みょ","rya":"りゃ","ryu":"りゅ","ryo":"りょ","xya":"ゃ","xyu":"ゅ","xtu":"っ",
        "chi":"ち","tsu":"つ","shi":"し","thi":"てぃ","dhu":"でゅ","dhi":"でぃ","gwi":"ぐぃ"}
    jptoRomaji2 = {"ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ","ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
        "sa":"さ","si":"し","su":"す","se":"せ","so":"そ","za":"ざ","zi":"じ","ji":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
        "ta":"た","ti":"ち","tu":"つ","te":"て","to":"と","da":"だ","di":"ぢ","du":"づ","de":"で","do":"ど",
        "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の","ha":"は","hi":"ひ","hu":"ふ","he":"へ","ho":"ほ",
        "ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ","pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
        "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も","ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
        "ya":"や","yu":"ゆ","yo":"よ","wa":"わ","fu":"ふ","wo":"を","ja":"じゃ","ju":"じゅ","jo":"じょ","fi":"ふぃ","fo":"ふぉ","fa":"ふぁ","fe":"ふぇ"}
    jptoRomaji1 = {"a":"あ","i":"い","u":"う","e":"え","o":"お"}
    hiraTxt = ""
    tempTxt = ""
    for txt in engTxt:
        if len(tempTxt) == 0:
            tempTxt = txt
        else:
            tempTxt = tempTxt + txt
        if tempTxt in jptoRomaji1:
            hiraTxt = hiraTxt + jptoRomaji1[tempTxt]
            tempTxt = ""
        elif tempTxt in jptoRomaji2:
            hiraTxt = hiraTxt + jptoRomaji2[tempTxt]
            tempTxt = ""
        elif tempTxt in jptoRomaji3:
            hiraTxt = hiraTxt + jptoRomaji3[tempTxt]
            if hiraTxt[-1] in ["p","s","t","k","d"]:
                tempTxt = hiraTxt[-1]
                hiraTxt = hiraTxt[:-1]
            else:
                tempTxt = ""
    # placeholder = st.empty()
    # with placeholder.container(): 
    #     st.write(hiraTxt)
    return hiraTxt

# 찾는 단어만 들어간 줄만 리스트로 반환해 주는 함수
def vocFilterFunc(voc, searchFilter):
    vocFilter = []
    filterList = []
    if "+" in searchFilter:
        filterList = searchFilter.split("+")
        for f in filterList:
            for v in voc:
                if f in v:
                    vocFilter.append(v)
    else:
        for v in voc:
            if searchFilter in v:
                vocFilter.append(v)
    return vocFilter

# 구간안의 데이터만 리스트로 반환해 주는 함수
def inbetween(voc, searchFilter):
    start = int(searchFilter.split("-")[0])-1
    if searchFilter.split("-")[1] == "":
        end = len(voc)
    else:
        end = int(searchFilter.split("-")[1])
    if start <= len(voc) and end <= len(voc) + 1:
        return voc[start:end]
    else:
        st.warning(f'구간이 전체 범위를 초과하였습니다. 다시 설정해 주세요. 최대범위: {len(voc)}')

def showWords(data, questCol, answCol, dilimCol, timeSel, playWay, searchFilter):
    # 순차적으로 할건지 결정하는 Flag
    # sequential = False
    # reverse = False
    try:
        with open(selected_file,'r', encoding='utf-8') as f:
            voc = f.readlines()
            if searchFilter:
                try:
                    # if playWay == "순차":
                    #     sequential = True
                    #     # searchFilter = searchFilter[1:]
                    # if playWay == "역순":
                    #     reverse = True
                    #     # searchFilter = searchFilter[1:]
                    if "|" in searchFilter:
                        voc = vocFilterFunc(voc, searchFilter.split("|")[0])
                        voc = inbetween(voc, searchFilter.split("|")[1])
                    else:
                        if "-" in searchFilter:
                            voc = inbetween(voc, searchFilter)
                        else:
                            voc = vocFilterFunc(voc, searchFilter)
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

    # 밑에 주관식 문항을 만들기위해 voc를 session에 저장
    data = []
    for v in voc:
        quest = v.split(dilimCol)[questCol]
        answ = v.split(dilimCol)[answCol]
        linedata = quest + '\t' + answ
        data.append(linedata)
    # 그냥 data를 대입하면 리스트와 같은 곳을 가리키므로 같이 움직이게 된다 그래서 .copy()를 써서 넣는다
    st.session_state['vocSingleOriginal'] = data.copy()
    st.session_state['vocSingle'] = data.copy()
    if 'point' not in st.session_state:
        st.session_state['point'] = 0

    placeholder = st.empty()
    try:
        ranNum = -1
        if playWay == "역순":
            ranNum = len(voc)
        while True:
            if playWay == "순차":
                if ranNum == len(voc) - 1:
                    ranNum = 0
                else:
                    ranNum = ranNum + 1
            elif playWay == "역순":
                if ranNum == 0:
                    ranNum = len(voc) -1
                else:
                    ranNum = ranNum - 1
            else:
                ranNum = random.randint(0,len(voc)-1)
            # 마지막 빈 공간이 선택되면 그냥 무시하도록
            if voc[ranNum].strip() == "":
                continue
            with placeholder.container():
                # 질문이 비어 있으면(가끔 한자가 없고 히라가나만 있을때) 그냥 답항을 질문에 넣는다
                quesWord = voc[ranNum].split(dilimCol)[questCol]
                if quesWord == "":
                    quesWord = voc[ranNum].split(dilimCol)[answCol]
                st.success(quesWord)
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

# 주관식 데이터 session에서 불러오기
def fetchData():
    if len(st.session_state['vocSingle']) == 0:
        st.session_state['vocSingle'] = st.session_state['vocSingleOriginal'].copy()
        st.info("다 맞추었습니다. 새로 시작합니다.")
    vocSingle = st.session_state['vocSingle']
    quest = [i.split("\t")[0].strip() for i in vocSingle]
    answ = [i.split("\t")[1].split(",")[0].replace(" ","").strip() for i in vocSingle]
    answ = [re.sub(r'\([^)]*\)', '', i.split("\t")[1].split(",")[0].replace(" ","").strip()) for i in vocSingle]
    return quest, answ, vocSingle

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
        # 초기선택파일을 ini파일에서 읽어옴
        try:
            with open("initFile.ini","r",encoding="utf-8") as f:
                init_idx = file_list_wanted.index(f.read().strip())
        except Exception as e:
            st.warning(e)
            init_idx = 0

        # 쿠키 읽어오기
        # @st.cache_resource(experimental_allow_widgets=True)
        # def get_manager():
        #     return stx.CookieManager()
        # cookie_manager = get_manager()
        # cookies = cookie_manager.get_all()
        # init_idx = 0
        # value = cookie_manager.get('prevFile')
        # if value:
        #     init_idx = file_list_wanted.index(value)
        col1,col2,col3 = st.columns([14,5,5])
        with col1:
            selected_file = st.selectbox('파일선택',file_list_wanted,init_idx)
        with col2:
            questCol = st.selectbox("질문열",[1,2,3,4]) - 1
        with col3:
            answCol = st.selectbox("해답열",[1,2,3,4],1) - 1
        col4,col5,col6,col7 = st.columns([7,6,8,8])
        # col1,col2,col3,col4,col5,col6,col7 = st.columns([10,4,4,6,5,6,6])
        with col4:
            dilimCol = st.selectbox("열 구분자",["자동","탭","빈칸1개","빈칸2개","콤마"],0)
        with col5:
            timeSel = st.selectbox("시간 간격",[0.5,1,2,3,4,5,6,8,10,20,30,60],3)
        with col6:
            playWay = st.selectbox("동작순서",["순차","역순","랜덤"],1)
        with col7:
            searchFilter = st.text_input("필터/구간")
        submitted = st.form_submit_button("시작")
        if submitted:
            with open("initFile.ini","w",encoding="utf-8") as f:
                f.write(selected_file)
            # cookie_manager.set('prevFile', selected_file)
            showWords(selected_file, questCol, answCol, dilimCol, timeSel, playWay, searchFilter)

    on = st.toggle('필터/구간 설명')
    if on:
        st.write('* 원하는 단어를 입력하면 입력한 단어가 포함된 것만 추출함 \n* 여러개의 추출 검색어를 다 나오게 하려면 "+"를 이용해서 연결\n* 데이터의 일부 번호대를 입력하면(예:1-20) 그 순번 만 나오게 할 수 있다, 뒷 번호 생략시 끝까지 \n* 단어와 순번을 모두 원하면 단어와 순번을 "|"로(예: N3|1-20) 연결한다\n* 맨앞에 @를 넣고 시작하면 문제가 순차적으로 나옴\n* 맨앞에 %를 넣고 시작하면 문제가 역순으로 나옴')
    
    single = st.toggle('주관식')
    if single:
        placeholder = st.empty()
        with st.form("주관식"):
            quest, answ, vocSingle = fetchData()
            vocSingleOriginal = st.session_state["vocSingleOriginal"]
            questOriginal = [i.split("\t")[0] for i in vocSingleOriginal]
            answIn = st.text_input('답을 하나씩 넣거나, ","를 이용해 여러개를 한번에 넣으세요')
            submitted = st.form_submit_button('확인')
            japWord = ""
            if submitted:
                for word in answIn.split(","):
                    if re.match(r'[ぁ-んァ-ン]', answ[0]):
                        word = engToHira(word)
                        japWord = word
                    if word.replace(" ","") in answ:
                        with placeholder.container():
                            quest, answ, vocSingle = fetchData()
                            idx = answ.index(word.replace(" ",""))
                            del vocSingle[idx]
                            st.session_state["vocSingle"] = vocSingle
                            st.session_state['point'] = st.session_state['point'] + 1
                    else:
                        st.warning(japWord + " 틀렸습니다.")
            quest, answ, vocSingle = fetchData()
            if japWord:
                st.write(word)
            st.success(quest)
            st.write(f"점수: {st.session_state['point']}")


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
