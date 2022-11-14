from PIL import Image
import cv2
import pytesseract

SCORE_POS=[(220,520,375,615),(430,520,590,615),(645,520,800,615),(855,520,1015,615)]
NAME_POS=[(215,320,420,395),(430,320,635,395),(645,320,850,395),(855,320,1060,395)]
RANK_SCORE=[20,5,-5,-20]

def get_info(img_url):
    img=cv2.imread(img_url,0)
    result=[]
    for i in range(4):
        name_img=img[NAME_POS[i][1]:NAME_POS[i][3],NAME_POS[i][0]:NAME_POS[i][2]]
        score_img=img[SCORE_POS[i][1]:SCORE_POS[i][3],SCORE_POS[i][0]:SCORE_POS[i][2]]
        cv2.resize(name_img,(name_img.shape[0]//3,name_img.shape[1]//3))
        cv2.resize(score_img,(score_img.shape[0]//2,score_img.shape[1]//2))
        _,name_img=cv2.threshold(name_img,127,255,cv2.THRESH_BINARY_INV)
        _,score_img=cv2.threshold(score_img,127,255,cv2.THRESH_BINARY_INV)
        name_str=pytesseract.image_to_string(name_img).split('\n')[0]
        score_str=pytesseract.image_to_string(score_img).split('\n')[0].split(' ')[0]
        while not score_str[1:].isnumeric(): 
            score_str=score_str[:-1]
            if score_str=='': return
        print('result append ',{"name":name_str,"score":int(score_str)})
        result.append({"name":name_str,"score":int(score_str)})
    return result

def get_point(info_list):
    newlist = sorted(info_list, key=lambda d: d['score'],reverse=True)
    ans=[]
    last=0
    for i,d in enumerate(newlist):
        point= RANK_SCORE[i]
        if i<=2:
            point+=(d['score']-30000)//2000
            if d['score']<30000: point+=1
            last-=point
            ans.append({"name":d['name'],'score':point})
            print('ans append ',{"name":d['name'],'score':point})
        else:
            ans.append({"name":d['name'],'score':last})
            print('ans append ',{"name":d['name'],'score':last})
            
    return ans
if __name__=='__main__':
    print(get_scores('images/mahjong.jpg'))