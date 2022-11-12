from PIL import Image
import pytesseract

SCORE_POS=[(290,730,500,795),(580,730,780,795),(870,730,1065,795),(1160,730,1355,795)]
    
def get_scores(img_url):
    img=Image.open(img_url)
    result=[]
    for i in SCORE_POS:
        result.append(int(pytesseract.image_to_string(img.crop(i))))
    return result

if __name__=='__main__':
    print(get_scores('images/mahjong.jpg'))