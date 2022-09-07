# -*- coding: utf-8 -*-
"""0821_SLEClassification&SLEDAI_for_users(NEWEST)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LssIBj18P4g6d2QRYYdcAb4fEC2sA50m

1. Proteinuria > 0.5g/24hr 讓他填數字! ； Renal Biopsy可以是配合題(Class II or lll or IV or V只會有一個)
2. 當lupus nephritis選擇題輸入非規定的正整數時，雖然不會錯誤提醒，但也視同無效不會被計分；例外處理時，盡量讓電腦幫忙列出錯誤(eg.型態轉換不符)，其餘輸入型態正確但不合乎SLE臨床知識與邏輯等錯誤則盡量手動羅列。
3. Ans_confirmation: 在處理資訊前提供目前答案給作答者參考，且呈現出容易判讀的dataframe格式，並能輸入題號做修正；修正完畢後再次提供目前作答情形給作答者參考，做資料處理與判讀前的最後確認(具有防呆裝置，限定輸入正確格式與題號)
4. 如果輸入時誤打空白建則自動刪除 (利用str.strip())
"""

## A. SLE Classification:
# create domain array 
import numpy as np
SLE_domain = np.array([['Constitutional'], ['Hematologic'], ['Neuropsychiatric'], ['Mucocutaneous'], ['Serosal'], ['Musculoskeletal'], ['Renal'], ['Antiphospholipid antibodies'], ['Complement_proteins'], ['SLE-specific antibodies']])
# condition nparray(10*4 = 7*4 + 3*4)
SLE_ccond = np.array([['Fever', None, None, None], ['Leukopenia', 'Thrombocytopenia', 'Autoimmune hemolysis', None], ['Delirium', 'Psychosis', 'Seizure', None], ['Non-scarring alopecia', 'Oral ulcers', 'Subacute cutaneous OR discoid lupus', 'Acute cutaneous lupus'], ['Pleural or pericardial effusion', 'Acute pericarditis', None, None], ['Joint involvement',None, None, None], ['Proteinuria = ___ g/24hours by 24-hour urine?\n*Please input a positive integer or float.', 'Which class best subscribes your status of lupus nephritis according to renal biopsy?\n*Please input a integer from 0 to 6("0":Normal ; "1"-"6":Class 1-6 lupus nephritis)', None, None]])
SLE_icond = np.array([['Anti-cardiolipin antibodies OR Anti-β2GP1 antibodes OR Lupus anticoagulant', None, None, None], ['Low C3 OR low C4', 'Low C3 AND low C4', None, None],['Anti-dsDNA antibody OR Anti-Smith antibody', None, None, None]])
SLE_cond = np.vstack((SLE_ccond, SLE_icond))
# weight array
SLE_weight = np.array([[2, 0, 0, 0], [3, 4, 4, 0], [2, 3, 5, 0], [2, 2, 4, 6], [5, 6, 0, 0], [6, 0, 0, 0], [4, 8, 10, 0], [2, 0, 0, 0], [3, 4, 0, 0], [6, 0, 0, 0]])
# Ans array
SLE_ans = np.array(None, (object, [10, 4]))
# 製作問答loop_control_array(元素為各domain之condition個數) >>用於SLE各condition問答  
SLE_loop_control = np.count_nonzero(SLE_cond, axis=1)

#------------------------------------------------------------------------------------------#

### 各流程建立function

## 在初始介面先使用二分法確認使用者狀態(類似分類樹概念):
def Qstatus():
  print('Have you been diagnosed as SLE by a qualified physician?')
  sta = 'str'
  while sta != 'Y' and sta != 'N':
    sta = input('Please input "Y" for YES and "N" for NO.(case-insensitive大小寫不拘) ').strip()
    sta = sta.capitalize() 
  return sta

def QbeforeDAI():
  print('Would you like to further understand your SLE disease severity?')
  sta = 'str'
  while sta != 'Y' and sta != 'N':
    sta = input('Please input "Y" for YES and "N" for NO.(case-insensitive大小寫不拘) ').strip()
    sta = sta.capitalize() 
  return sta
  
##entry_criterion_防呆裝置
titer = None
def entry_criterion_防呆裝置():
  global titer
  while type(titer) != type(6.6) or titer <= 0:
    try:
      titer = float(input('ANA at a titer of 1:"?" on HEp-2 cells.(Please input a number of type"float".)').strip())
      if titer <= 0:
        print('You should input a positive number!')
        continue
    except Exception as ex:   # Exception為各種exceptions的superclass；將此exception存在ex變數中!!!   
      print(type(ex))          #當不確定例外種類，且想知道例外的原因時，可利用左邊範例的方法。
      print('Error!', ex)    
  return 'finished'    

## additive_criteria問答 (利用巢狀while loop 處理與使用者的問答以及答題紀錄，適用於clinical & immunological)     
# 以SLE_domain、SLE_cond、SLE_ccond、SLE_ans、SLE_loop_control作為argument，考慮與SLEDAI_condition_QA合併(?)
def ConditionCriteria_QA(domain_array, CondArray, CCondArray, ans_array, LoopControlArray): 
  print('\n*Please input "Y", "N" or "NI" to answer this question OR "B" or "F" to jump to another question for check.')
  i = 0
  while i < len(domain_array):
      if i == 0:
        print(f'\n*Clinacal Conditions Questionaire:')
      if i == len(CCondArray): 
        print(f'\n*Immunological Conditions Questionaire:')
      print(f'\n{(i%len(CCondArray))+1}. Questions about {domain_array[i, 0]} domain:') #字串格式化
      j = 0
      while j < LoopControlArray[i]:     # while j < len(CondArray[i]) and CondArray[i, j] is not None: 也可以
          if i == 6:   
            print('In this special domain, you should read the instruction carefully and fill in the correct "Number"!')  
            print(f'({(i%len(CCondArray))+1}-{j+1}) {CondArray[i, j]} (Current Ans: "{ans_array[i, j]}")')      
            check = input(f'Please input the right key word(specific Number, "NI", "B", or "F" ; case-insensitive大小寫不拘)!  ' ).strip().upper()
            if check == "NI":
                ans_array[i, j] = check   ##
                j = j + 1  
            elif check == "B": 
                print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")                   
                if j == 0:                   #當輸入B或F時，讓使用者知道自己正跳至別題檢查，並可更正答案(v)(*希望呈現出目前答案給使用者參考?)
                    if i != 0:
                        i -= 1 
                        j = LoopControlArray[i] - 1 
                    else:
                        print("*This is the first question!(No questions above)")            
                else:
                    j -= 1
            elif check == "F":
                print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")
                if j == LoopControlArray[i] - 1:
                    if i != len(domain_array) - 1:
                        i += 1
                        j = 0
                    else:
                        print("*This is the last question!(No questions below)")    
                else:
                    j += 1
            else:
                # if not isinstance(check, float) or titer <= 0:
                try:
                  check = float(check)
                  if check < 0:
                    print('You shouldn\'t input a negative number!')
                    j = j
                  else:
                    ans_array[i, j] = check
                    j += 1  
                except ValueError:
                  print("You just filled in a wrong key word, please be more careful and try again!")
                  j = j 
          else:
            print(f'({(i%len(CCondArray))+1}-{j+1}) {CondArray[i, j]} ? (Current Ans: "{ans_array[i, j]}")')      #是否附註該condition的定義給使用者作確認(?)/back&forward(V)/預設no information(v)
            check = input(f'Please input the right key word("Y", "N", "NI","B", or "F" ; case-insensitive大小寫不拘)!  ' ).strip().upper()
            if check == "Y":
                ans_array[i, j] = check   #先用Y、N組成ans_array，之後再process為ans_Number_array(0, 1)，再與SLEDAI_weight相乘，得到ans_Weight_array
                j = j + 1
            elif check == "N":
                ans_array[i, j] = check
                j = j + 1
            elif check == "NI":
                ans_array[i, j] = check   ##
                j = j + 1  
            elif check == "B": 
                print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")                   
                if j == 0:                   #當輸入B或F時，讓使用者知道自己正跳至別題檢查，並可更正答案(v)(*希望呈現出目前答案給使用者參考?)
                    if i != 0:
                        i -= 1 
                        j = LoopControlArray[i] - 1 
                    else:
                        print("*This is the first question!(No questions above)")            
                else:
                    j -= 1
            elif check == "F":
                print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")
                if j == LoopControlArray[i] - 1:
                    if i != len(domain_array) - 1:
                        i += 1
                        j = 0
                    else:
                        print("*This is the last question!(No questions below)")    
                else:
                    j += 1
            else:
                print("You just filled in a wrong key word(not \"Y\" or \"N\"), please be more careful and try again!")
                j = j  
       #惟最後一題無法更改>考慮新增一項for最後檢查?        
      i += 1
  return ans_array

##ans confirmation(分為clinical & immunological)
def Ans_Confirmation(CondArray, ans_array, LoopControlArray):
  # 1. 呈現出目前答題狀況(題號, condition, ans)
  print('\n* The following dataframe shows your current answers to each question, and we\'ll help you confirm them before the next step.')
  print('Q_Num  ', "Condition".ljust(85), 'Current_Ans\n', '-' * 125)
  for i in range(len(CondArray)):
    j = 0
    while j < LoopControlArray[i]:
      a = CondArray[i, j].find('?')
      if a != -1:
        print(f'{i+1}-{j+1:<6}{CondArray[i, j][0:a]:<85} {ans_array[i, j]}')
      else:
        print(f'{i+1}-{j+1:<6}{CondArray[i, j]:<85} {ans_array[i, j]}')
      j += 1
  # 2. 修正
  confirm2 = None
  while confirm2 != 'Y':
    confirm1 = None
    while confirm1 != 'Y' and confirm1 != 'N':
      confirm1 = input('Is there anything wrong that you\'d like to modify? (Please input "Y" or "N")').strip().upper()
    while confirm1 == 'Y':
      while True:
        QNum = input('Please input the question number in correct format! (eg. 1-1, 3-3, or 7-2 ; one at a time!)').strip()
        try:
          i, j = QNum.split('-')
          i = int(i) - 1
          j = int(j) - 1
          if 0 <= i < len(CondArray) and 0 <= j < LoopControlArray[i]:
            break
          else:
            print('Wrong question number!')
            continue  
        except Exception as ex:   # Exception為各種exceptions的superclass；將此exception存在ex變數中!!!  
          print('You just filled in a wrong word, please be more careful and try again!') 
          print('Error_type:', type(ex))          
          print('Error!', ex)
      if i == 6:   
        print('In this special domain, you should read the instruction carefully and fill in the correct "Number"!')
        while True:
          print(f'({i+1}-{j+1}) {CondArray[i, j]} (Current Ans: "{ans_array[i, j]}")')      
          check = input(f'Please input the right key word(specific Number or "NI" ; case-insensitive大小寫不拘)!  ' ).strip().upper()
          if check == "NI":
              ans_array[i, j] = check   ##
              break
          else:
            try:
              check = float(check)
              if check < 0:
                print('You shouldn\'t input a negative number!')
              else:
                ans_array[i, j] = check
                break
            except Exception as ex:   # Exception為各種exceptions的superclass；將此exception存在ex變數中!!!   
              print("You just filled in a wrong key word, please be more careful and try again!")
              print('Error_type:',type(ex))          
              print('Error!', ex)
      else:
        print(f'({i+1}-{j+1}) {CondArray[i, j]} ? (Current Ans: "{ans_array[i, j]}")')      #是否附註該condition的定義給使用者作確認(?)/back&forward(V)/預設no information(v)
        while True:
          check = input(f'Please input the right key word("Y", "N", or "NI" ; case-insensitive大小寫不拘)!  ' ).strip().upper()
          if check == "Y":
              ans_array[i, j] = check   #先用Y、N組成ans_array，之後再process為ans_Number_array(0, 1)，再與SLEDAI_weight相乘，得到ans_Weight_array
              break
          elif check == "N":
              ans_array[i, j] = check
              break
          elif check == "NI":
              ans_array[i, j] = check   ##
              break
          else:
              print("You just filled in a wrong key word, please be more careful and try again!")
      confirm1 = input('Is there anything else wrong that you\'d like to modify? (Please input "Y" or "N")').strip().upper()
    #再次確認目前ans 
    print('Again! The following dataframe shows your current answers to each question. Please double check them!') 
    print('Q_Num  ', "Condition".ljust(85), 'Current_Ans\n', '-' * 125)
    for i in range(len(CondArray)):
      j = 0
      while j < LoopControlArray[i]:
        a = CondArray[i, j].find('?')
        if a != -1:
          print(f'{i+1}-{j+1:<6}{CondArray[i, j][0:a]:<85} {ans_array[i, j]}')
        else:
          print(f'{i+1}-{j+1:<6}{CondArray[i, j]:<85} {ans_array[i, j]}')
        j += 1
    #最後確認
    confirm2 = None
    while confirm2 != 'Y' and confirm2 != 'N':
      confirm2 = input('Have you already confirmed that all answers correspond with your current health status? (Please input "Y" or "N")').strip().upper()
  print('Answer confirmation has finished! Please wait a moment for the results!')  
#---------------------------------------------------------------------------------------------------------------#
## 處理各domains的weights(適用於clinical & immunological)
## key idea: 先用Y、N組成ans_array(v)，之後再process為ans_Number_array(-1無此問題, 0無症狀或無資料, 1有症狀)，再與SLEDAI_weight相乘，得到ans_Weight_array
SLE_ansNum = SLE_weight.copy()
#各domain之condition答案欄如出現No Information，則將此特例的位置index儲存至ans_No_Information(nested list)中>>>方便產出最終建議
SLE_ansNI = []
for i in range(len(SLE_cond)):
  SLE_ansNI.append([])    # 此list(SLE_ansNI) 將用來放置各domain無資料的index
#process為ans_Number_array(-1, 0, 1)
def Change_YN_to_Number(Ans_Array, AnsNum, AnsNI):
  for i in range(len(Ans_Array)):
    for j in range(len(Ans_Array[i])):
      if i == 6:  # renal domain就你最特別
        if j == 0:  #proteinuria
          if isinstance(Ans_Array[i, j], float):  #可能為float的只可能是proteinuria(0)、lupus nephritis(1)
            AnsNum[i, j] = 1 if Ans_Array[i, j] > 0.5 else 0
          else:  #只可能是NI
            AnsNum[i, j] = 0
            AnsNI[i].append(j)
        elif j == 1:  #lupus nephritis (2,5>>8 pts；3,4>>10 pts)，好複雜QQ
          if isinstance(Ans_Array[i, j], float): 
            if Ans_Array[i, j] == 2 or Ans_Array[i, j] == 5:
              AnsNum[i, j] = 1
              AnsNum[i, j+1] = 0
            elif Ans_Array[i, j] == 3 or Ans_Array[i, j] == 4:
              AnsNum[i, j] = 0
              AnsNum[i, j+1] = 1
            else:
              AnsNum[i, j] = 0
              AnsNum[i, j+1] = 0  
          else:   #只可能是NI
            AnsNum[i, j] = 0
            AnsNum[i, j+1] = 0
            AnsNI[i].extend([j, j+1])    
        else:  #沒題目None  
          AnsNum[i, 3] = -1    #否則會出問題，[6, 2]會蓋過[6, 1]時產生的數字
      else:  
        if Ans_Array[i, j] == "Y":
          AnsNum[i, j] = 1
        elif Ans_Array[i, j] == "N":
          AnsNum[i, j] = 0
        elif Ans_Array[i, j] == "NI":
          AnsNum[i, j] = 0
          AnsNI[i].append(j)  
        else:
          AnsNum[i, j] = -1       
  return AnsNum
#找出各domain最高分
def Find_Domain_Max(AnsWeight):
  Trueweight2 = []
  for i in AnsWeight:
    Trueweight2.append(max(i))
  return Trueweight2  
# 找到weight最高的domain  >>判定main determinant instead of main cause!!! 
# 或highest_score = max(Domain_weight)  
highest_score = 0 
def Find_Main_Detreminamt(DomainWeight, Domain, SLECCond):
  global highest_score
  highest_score = max(DomainWeight)
  main_cdeterminant = []
  main_ideterminant = []
  for i in range(len(DomainWeight)):
    if DomainWeight[i] == highest_score:
      if i < len(SLECCond):
        main_cdeterminant.append(f'{Domain[i, 0]} domain')
      else:
        main_ideterminant.append(f'{Domain[i, 0]} domain')          
  return main_cdeterminant, main_ideterminant  

# SLE final diagnosis: SLE classification requires at least one clinical criterion and ≥10 points.
def SLE_Classification_Advice(total_score, DomainWeight, SLECCond):
  Nccri = 0  #確認是否完全沒有達到任何clinical_criteria
  for i in DomainWeight[0:len(SLECCond)]:
    if i == 0:
      Nccri += 1
  print(f'\n*Diagnostic result:')    
  if total_score >= 10:
    if Nccri == len(SLECCond):
      return f'No. This patient is probably not classified as SLE because he/she doesn\'t meet any single clinical criterion.' 
    else:
      #不知道使用全域變數是否需要傳入該引數
      return f'''Yes. This patient is probably classified as SLE.
Main determinants: (1)clinical: {main_cdeterminant} ； (2)immunology: {main_ideterminant}  
Each gets {highest_score} pts of total {total_score} pts and accounts for {highest_score/total_score * 100:.2f} % of total weights.'''
  else:
    return f'''No. This patient is probably not classified as SLE.
The total weights add up to only {total_score} pts, which doesn't reach the standard 10 pts for SLE diagnosis.'''

# No_Information_Suggestion
def NI_Suggestion1(Ans_NI, DomainArray, CondArray):  # ConditionArray(SLE_cond) ; DomainArray(SLE_domain)
  print(f'\nThe conditions with no information, if any, are as follows:') 
  list1 = []
  for i in range(len(Ans_NI)):
    if Ans_NI[i] == []:
      continue
    else:
      for j in Ans_NI[i]:
        print(f'{CondArray[i, j]} (in {DomainArray[i]} domain)')
        list1.append(f'{CondArray[i, j]} (in {DomainArray[i]} domain)')
  print(f'\n*IF you have some questions with NO INFORMATION, those conditions are considered negative automatically by the App and thus it is likely that the patient\'s disease severity is underestimated. In this case, We suggest that you take further examinations to make up the dificiency and then you can get more accurate predictions from the App! Thanks!''')
  return list1 
#============================================================borderline=========================================================
## B. SLEDAI:  #盡量不要重複問(Fever, Thrombocytopenia, Psychosis, Seizure, Proteinuria)
#如果使用者有意願 >>> 用SLEDAI進一步嚴重度分級 / 先不做科別方類
import numpy as np
SLEDAI_cond = np.array(["Seizure(recent onset)", "Psychosis", "Organic brain syndrome", "Visual disturbance", "Cranial nerve disorder", "Lupus headache", "CVA(new onset)", "Vasculitis", "Arthritis", "Myositis", "Urinary casts", "Hematuria", "Proteinuria", "Pyuria", "Rash", "Alopecia", "Mucosal ulcers", "Pleurisy", "Pericarditis", "Low complement", "Increased DNA binding", "Fever", "Thrombocytopenia", "Leukopenia"])
SLEDAI_def = np.array(["Recent onset, exclude metabolic, infections, or drug causes.", "Altered ability to function in normal activity due to severe disturbance in the perception of reality. Exclude uremia and drug causes.", " Altered mental function with impaired orientation, memory, or other intellectual function, with rapid onset and fluctuating clinical features, inability to sustain attention to environment, plus at least 2 of the following: perceptual disturbance, incoherent speech, insomnia or daytime drowsiness, or increased or decreased psychomotor activity. Exclude metabolic, infectious, or drug causes.", "Retinal changes of SLE. Exclude hypertension, infection, or drug causes", "New onset of sensory or motor neuropathy involving cranial nerves.", "Severe, persistent headache; may be migrainous, but must be nonresponsive to narcotic analgesia.", "New onset of cerebrovascular accident(s). Exclude arteriosclerosis.", "Ulceration, gangrene, tender finger nodules, periungual infarction, splinter hemorrhages, or biopsy or angiogram proof of vasculitis.", "≥2 joints with pain and signs of inflammation (i.e., tenderness, swelling, or effusion).", "Proximal muscle aching/weakness, associated with elevated creatine phosphokinase/aldolase or electromyogram changes or a biopsy showing myositis.", "Heme-granular or red blood cell casts", ">5 red blood cells/high power field. Exclude stone, infection, or other cause.", ">0.5 gram/24 hours", ">5 white blood cells/high power field. Exclude infection.", "Inflammatory type rash", "Abnormal, patchy or diffuse loss of hair", "Oral or nasal ulcerations", "Pleuritic chest pain with pleural rub or effusion or pleural thickening", "Pericardial pain with at least 1 of the following: rub, effusion, or electrocardiogram or echocardiogram confirmation", "Decrease in CH50, C3, or C4 below the lower limit of normal for testing laboratory", "Increased DNA binding by Farr assay above normal range for testing laboratory", ">38° C. Exclude infectious cause", "<100,000 platelets/× 10^9/L, exclude drug causes", "<3000 white blood cells/× 10^9/L, exclude drug causes."])
SLEDAI_weight = np.array([8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1])
SLEDAI_ans = np.array(None, (object, [24]))
SLEDAI_ans_num = SLEDAI_ans.copy()

# SLEDAI_QA問答與答案紀錄完成
def SLEDAI_QA(CondArray, DefArray, AnsArray, AnsNumArray): 
  print('\n*Please input "Y", "N" or "NI" to answer this question OR "B" or "F" to jump to another question for check.')
  i = 0
  while i < len(CondArray):
      print(f'\n{i+1}. {CondArray[i]} ? (Current Ans: "{AnsArray[i]}")')     #是否附註該condition的定義給使用者作確認(v)/back&forward(V)/預設no information(v)
      print(f'(Definition: {DefArray[i]})')    #呈現出目前答題狀況(v)(*惟最後一題無法更改>考慮新增一項for最後檢查?)
      check = input(f'Please input the right key word("Y", "N", "NI","B", or "F" ; case-insensitive大小寫不拘)!  ' ).strip().upper()  #str.upper()是小寫轉大寫；str.capitalize()是字首大寫其餘小寫
      if check == "Y":
          AnsArray[i] = check   #先用Y、N組成ans_array，之後再process為ans_Number_array(0, 1)，再與SLEDAI_weight相乘，得到ans_Weight_array
          AnsNumArray[i] = 1
          i = i + 1
      elif check == "N":
          AnsArray[i] = check
          AnsNumArray[i] = 0
          i = i + 1
      elif check == "NI":  
          AnsArray[i] = check  ##這邊有改
          AnsNumArray[i] = 0
          i = i + 1 
      elif check == "B": 
          print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")                   
          if i == 0:        #當輸入B或F時，讓使用者知道自己正跳至別題檢查，並可更正答案(v)(*希望呈現出目前答案給使用者參考?)
            print("*This is the first question!(No questions above)") 
          else:
            i -= 1       
      elif check == "F":
          print(f"For check: Please input the corrected answer if necessary OR input \"B\" or \"F\" to jump to another question.")
          if i == len(CondArray) - 1:
            print("*This is the last question!(No questions below)")  
          else:
            i += 1        
      else:
          print("\nYou just filled in a wrong key word, please be more careful and try again!")
          i = i         
  return AnsArray

##SLEDAI_ans confirmation
def SLEDAI_Ans_Confirmation(CondArray, ans_array):
  # 1. 呈現出目前答題狀況(題號, condition, ans)
  print('\n* The following dataframe shows your current answers to each question, and we\'ll help you confirm them before the next step.')
  print('Q_Num  ', "Condition".ljust(70), 'Current_Ans\n', '-' * 125)
  for i in range(len(CondArray)):
    print(f'{i+1:<8}{CondArray[i]:<70} {ans_array[i]}')
  # 2. 修正
  confirm2 = None
  while confirm2 != 'Y':
    confirm1 = None
    while confirm1 != 'Y' and confirm1 != 'N':
      confirm1 = input('Is there anything wrong that you\'d like to modify? (Please input "Y" or "N")').strip().upper()
    while confirm1 == 'Y':
      while True:
        QNum = input('Please input the question number in correct format! (eg. 1, 3, or 17 ; one at a time!)').strip()
        try:
          i = int(QNum) - 1
          if 0 <= i < len(CondArray):
            break
          else:
            print('Wrong question number!')
            continue  
        except Exception as ex:   # Exception為各種exceptions的superclass；將此exception存在ex變數中!!!  
          print('You just filled in a wrong word, please be more careful and try again!') 
          print('Error_type:', type(ex))          
          print('Error!', ex)     
      print(f'({i+1}) {CondArray[i]} ? (Current Ans: "{ans_array[i]}")')      
      while True:
        check = input(f'Please input the right key word("Y", "N", or "NI" ; case-insensitive大小寫不拘)!  ' ).strip().upper()
        if check == "Y":
            ans_array[i] = check   #先用Y、N組成ans_array，之後再process為ans_Number_array(0, 1)，再與SLEDAI_weight相乘，得到ans_Weight_array
            break
        elif check == "N":
            ans_array[i] = check
            break
        elif check == "NI":
            ans_array[i] = check   ##
            break
        else:
            print("You just filled in a wrong key word, please be more careful and try again!")
      confirm1 = input('Is there anything else wrong that you\'d like to modify? (Please input "Y" or "N")').strip().upper()
    #再次確認目前ans 
    print('Again! The following dataframe shows your current answers to each question. Please double check them!') 
    print('Q_Num  ', "Condition".ljust(70), 'Current_Ans\n', '-' * 125)
    for i in range(len(CondArray)):
      print(f'{i+1:<8}{CondArray[i]:<70} {ans_array[i]}')
    #最後確認
    confirm2 = None
    while confirm2 != 'Y' and confirm2 != 'N':
      confirm2 = input('Have you already confirmed that all answers correspond with your current health status? (Please input "Y" or "N")').strip().upper()
  print('Answer confirmation has finished! Please wait a moment for the results!')  

###處理各domains的weights(適用於clinical & immunological) 
## 先用Y、N組成ans_array(v)，問答時已產生SLEDAI_ans_num(0無症狀或無資料, 1有症狀)，將與SLEDAI_weight相乘，得到ans_Weight_array

#SLEDAI_Class(嚴重度分級)
def SLEDAI_Class(SLEDAI_Total):
  if SLEDAI_Total == 0:
    return 'no activity'
  elif SLEDAI_Total < 6:
    return 'mild activity'
  elif SLEDAI_Total < 11:
    return 'moderate activity(Suggestion: greater than 50% probability of initiating therapy)'
  elif SLEDAI_Total < 20: 
    return 'high activity(Suggestion: greater than 50% probability of initiating therapy)' 
  else:
    return 'very high activity(Suggestion: greater than 50% probability of initiating therapy)' 

# No_Information_Suggestion2 
def NI_Suggestion2(Ans, Cond):  # 參數AnsArray（SLEDAI_ans）；ConditionArray(SLE_condition) 
  print(f'\n*The conditions with no information, if any, are as follows:') 
  NI_index = []
  NI_list = []
  for i in range(len(Ans)):
    if Ans[i] == "NI":
      NI_index.append(i)
  for i in NI_index:
    print(Cond[i])
    NI_list.append(Cond[i])    
  print(f'\nIf you have some questions with NO INFORMATION, those conditions are considered negative automatically by the App and thus it is likely that the patient\'s disease severity is underestimated. In this case, We suggest that you take further examinations to make up the dificiency and then you can get more accurate predictions from the App! Thanks!')
  return NI_list   
##-------------------------------------------------------------我是分隔線-----------------------------------------------------------------##
##-------------------------------------------------------------我是分隔線-----------------------------------------------------------------##
### 二、各流程與函數呼叫
# 在初始介面先使用二分法確認使用者狀態(類似分類樹概念)
status1 = Qstatus()
status3 = 'N'   #當classify as not SLE時，不會再問QbeforeDAI，因此預設為'N'

if status1 == 'N':   #進入classification
  #entry criterion
  print('''\nWelcome to SLE diagnosis assistant! We will predict whether or not you are classified as SLE before long.
 *Instructions for users: This App serves only as a diagnosis assistant, which is not designed for diagnosis or treatment decisions. Diagnosis of SLE remains the purview of an appropriately trained physician evaluating an individual patient.''')
  print('\nHere comes entry criteron.')
  entry_criterion_防呆裝置 = entry_criterion_防呆裝置()
  if titer <= 80:   
    print('\nAdditive criteria are needed before final diagnosis.')
    print(f'''There will be a survey about conditions in clinical or immunological domains.\n
*Here are something you should be informed of before the questionaire:
1. Please input correct key words for the App to run smoothly!
 "Y" stands for "Yes"(i.e. a patient meets the condition); "N" for "No"(i.e. one doesn't meet the criteria); "NI" for "no information" 
 "B" or "F" respectively for "jump *Back or *Forward to another question"   
2. All criteria are only to be counted if SLE is thought to be the most likely cause of the manifestation； occurrence of a criterion on at least one occasion is sufficient.
~ Thank you for your cooperation! ~''')   

    # SLE additive criteria各condition問答 (利用巢狀while loop 處理與使用者的問答以及答題紀錄，適用於clinical & immunological) 
    SLE_ans = ConditionCriteria_QA(SLE_domain, SLE_cond, SLE_ccond, SLE_ans, SLE_loop_control)
    #ans confirmation(分為clinical & immunological)##
    Ans_Confirmation(SLE_cond, SLE_ans, SLE_loop_control)

    #Data-processing: SLE_ans 轉換為 ans_Number_array(-1, 0, 1)    
    SLE_ansNum = Change_YN_to_Number(SLE_ans, SLE_ansNum, SLE_ansNI) 
    # ans_Number_array與SLE_weight相乘，得到SLE_ans_Weight_array
    SLE_ans_Weight = np.multiply(SLE_ansNum, SLE_weight)
    #找出各domain最高分
    Domain_weight = Find_Domain_Max(SLE_ans_Weight)
    # 找到weight最高的domain  >>判定main determinant instead of major cause!!! 
    main_cdeterminant, main_ideterminant = Find_Main_Detreminamt(Domain_weight, SLE_domain, SLE_ccond)
    main_cdeterminant = tuple(main_cdeterminant) 
    main_ideterminant = tuple(main_ideterminant)
    
    # 最終結果與呈現診斷建議
    total_score = sum(Domain_weight)
    SLE_classification_advice = SLE_Classification_Advice(total_score, Domain_weight, SLE_ccond)
    print(SLE_classification_advice)
    # No_Information_Suggestion
    SLE_NI_Cond = NI_Suggestion1(SLE_ansNI, SLE_domain, SLE_cond) 
  else:
    print('\nDiagnostic result:')
    print('This patient is probably not classified as SLE because he/she doesn\'t the entry criterion!')
  print("\nReference: The result is based on the 2019 EULAR/ACR classification criteria of SLE.")
  # 如果probably classified as SLE >>> 詢問使用者是否想進入SLEDAI了解嚴重度分級
  if SLE_classification_advice.startswith('Yes') and titer <= 80:
    status3 = QbeforeDAI()
  else:
    pass  
else:
  status3 = QbeforeDAI()  
##-------------------------------------------------------------我是分隔線-----------------------------------------------------------------##
#如果使用者有意願 >>> 用SLEDAI進一步嚴重度分級  #盡量不要重複問(Fever, Thrombocytopenia, Psychosis, Seizure, Proteinuria)
if status3 == 'N':
  print('Thank you for using this App! Bye!')
else:
  print(f'''--------------------------------------------------------------------------------------------------------------------
\nGiven that the patient probably suffers from SLE, we would like to further measure the disease activity baesd on "SLEDAI-2K(30 Days).2010".
Hopefully, we can help you understand the patient's current condition and even predict the outcome and prognosis.\n''')
  #問答前詳細說明判定標準
  print('''*Here are something you should be informed of before the questionaire. 
  1. Enter "Y" if descriptor in SLEDAI-2K sheet is present at the time of the visit or in the preceding 30 days.      
  2. Please input correct key words for the App to run smoothly! (case-insensitive大小寫不拘)
  "Y" stands for "Yes"(i.e. a patient meets the condition); "N" for "No"(i.e. one doesn't meet the criteria); "NI" for "no information" 
  "B" or "F" respectively for "jump *Back or *Forward to another question"   
  3. Detailed definition is showed below each question. Please refer to it if necessary.''')
  # SLEDAI各condition問答 (先不做科別的分類)/ 問答時已產生SLEDAI_ans_num(0無症狀或無資料, 1有症狀)
  SLEDAI_ans = SLEDAI_QA(SLEDAI_cond, SLEDAI_def, SLEDAI_ans, SLEDAI_ans_num)
  # SLEDAI_Ans_Confirmation
  SLEDAI_Ans_Confirmation(SLEDAI_cond, SLEDAI_ans)

  # ans_Number_array與SLEDAI_weight相乘，得到SLEDAI_ans_Weight_array
  SLEDAI_TrueWeight = np.multiply(SLEDAI_ans_num, SLEDAI_weight)
  #計算總分
  SLEDAI_total = np.sum(SLEDAI_TrueWeight)
  print(f'SLEDAI_total_score = {SLEDAI_total}pts')
  # SLEDAI分級與final suggestion
  SLEDAI_Class = SLEDAI_Class(SLEDAI_total)
  print(f'*Judgement Result: This patient\'s SLE Disease Activity is classified as {SLEDAI_Class}.')
  # No_Information_Suggestion
  SLEDAI_NI_Condition = NI_Suggestion2(SLEDAI_ans, SLEDAI_cond)
  print(f'''\nRegerence: The result is based on SLEDAI-2K(30 Days).2010.
  Thank you for your patronage!''')