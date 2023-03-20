import sys
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def login():
    uid = ""
    upassword = ""
    
    id = driver.find_element('name','segaId')
    password = driver.find_element('name','password')
    submit = driver.find_element_by_class_name('btn_login')
    
    id.clear()
    id.send_keys(uid)
    password.send_keys(upassword)
    submit.submit()

    sleep(1)
    
    # 1つ目のAimeを選択させるためとりあえずXPath指定
    aime = driver.find_element_by_xpath('//*[@id="inner"]/div[1]/div/div[2]/div[2]/form/button')
    aime.submit()
    
def getscore():
    f = open('out.csv', 'a', errors='ignore')
    
    basic_score = '0'
    basic_cnt = '0'
    adv_score = '0'
    adv_cnt= '0'
    expert_score = '0'
    expert_cnt = '0'
    master_score = '0'
    master_cnt = '0'
    ultima_score = '0'
    ultima_cnt = '0'
    
    sleep(1)
    title = driver.find_element_by_css_selector('.play_musicdata_title').text.replace(",","")
    print("曲名:", title)
    
    #basic
    try:
        data = driver.find_elements_by_css_selector('.bg_basic .text_b')
        basic_score = data[0].text.replace(",","")
        basic_cnt = data[1].text.replace("回","")
        print("[BASIC]")
        print("  点数:", basic_score)
        print("  回数:", basic_cnt)
    except:
        pass
    
    #advanced
    try:
        data = driver.find_elements_by_css_selector('.bg_advanced .text_b')
        adv_score = data[0].text.replace(",","")
        adv_cnt = data[1].text.replace("回","")
        print("[ADVANCED]")
        print("  点数:", adv_score)
        print("  回数:", adv_cnt)
    except:
        pass

    #expert
    try:
        data = driver.find_elements_by_css_selector('.bg_expert .text_b')
        expert_score = data[0].text.replace(",","")
        expert_cnt = data[1].text.replace("回","")
        print("[EXPERT]")
        print("  点数:", expert_score)
        print("  回数:", expert_cnt)
    except:
        pass
    
    #master
    try:
        data = driver.find_elements_by_css_selector('.bg_master .text_b')
        master_score = data[0].text.replace(",","")
        master_cnt = data[1].text.replace("回","")
        print("[MASTER]")
        print("  点数:", master_score)
        print("  回数:", master_cnt)
    except:
        pass
    
    #ultima
    try:
        data = driver.find_elements_by_css_selector('.bg_ultima .text_b')
        ultima_score = data[0].text.replace(",","")
        ultima_cnt = data[1].text.replace("回","")
        print("[ULTIMA]")
        print("  点数:", ultima_score)
        print("  回数:", ultima_cnt)
    except:
        pass
    
    out_data = [title,',',
                 basic_score, ',', basic_cnt, ',',
                 adv_score, ',', adv_cnt, ',',
                 expert_score, ',', expert_cnt, ',',
                 master_score, ',', master_cnt, ',',
                 ultima_score, ',', ultima_cnt,'\n']
    
    f.writelines(out_data)
    
    f.close()
    
def record():
    musicid = []
    driver.find_element_by_class_name('btn_record').click()
    sleep(1)
    driver.find_element_by_class_name('submenu_record').click()
    sleep(1)
    driver.find_element_by_class_name('btn_master').click()
    sleep(1)
    print('曲IDを収集中...')
    musics = driver.find_elements_by_name('idx')
    count = len(musics)
    #print(musics[0].get_attribute('value'))
    for num in range(count):
        musicid.append(musics[num].get_attribute('value'))
        

    print(musicid)
    
    f = open('out.csv', 'w', errors='ignore')
    out_data = ['曲名',',',
                 'BASICスコア', ',', 'BASIC回数', ',',
                 'ADVANCEDスコア', ',', 'ADVANCED回数', ',',
                 'EXPERTスコア', ',', 'EXPERT回数', ',',
                 'MASTERスコア', ',', 'MASTER回数', ',',
                 'ULTIMAスコア', ',', 'ULTIMA回数','\n']
    f.writelines(out_data)
    f.close()
    
    for num in range(count):
        target_element = driver.find_element_by_xpath('//*[@id="inner"]/div[3]/div[2]/div[7]/div[2]/form[1]/div/input[1]')
        driver.execute_script("arguments[0].setAttribute('value','" + musicid[num] + "')", target_element)
        
        sleep(1)
        driver.find_element_by_xpath('//*[@id="inner"]/div[3]/div[2]/div[7]/div[2]/form[1]/div/div[1]').click()
        
        print("=================================================")
        print(num + 1 , " / " , count)
        getscore()
        
        sleep(1)
        driver.find_element_by_class_name('btn_back').click()
                
    
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('C:\chromedriver/chromedriver.exe')
    driver.get('https://new.chunithm-net.com/chuni-mobile/html/mobile/')
    driver.set_window_size(720,1280)
    
    for i in range(0, 3):
        try:
            login()
        except:
            if i == 2:
                print("失敗回数の上限に達しました。プログラムを終了します。")
                driver.quit()
                sys.exit()
            else:
                print("ログインに失敗しました。再度入力して下さい。")
        else:
            break
    
    sleep(1)
    #レコード取得
    record()
    end_time = datetime.datetime.now()
    print("=================================================")
    print('終了しました。')
    print('開始時間:',start_time)
    print('終了時間:',end_time)