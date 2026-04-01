from moore_num import convert_to_text, text_to_num
from random import randint


for _ in range(10):
    num =102 #randint(1, 100000)
    text = convert_to_text(num, is_money=True)#"tus kobsi la pis-naase la a yoobe la kobs-wɛ la piig la a tã" #convert_to_text(num)
    print(f"{num} -> {text}")
    print(f"{text_to_num(text)} -- {text}")