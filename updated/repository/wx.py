from wxconv import WXC
def convert_to_hindi(word):
    # print(word,'llllllll')
    # wx = WXC(order='wx2utf', lang='hin')
    wx = WXC(order='utf2wx', lang='hin')
    hindi_text_list = wx.convert(word)
    # print(hindi_text_list,'klklklkl')
    return hindi_text_list

word ='सरकार'
print(convert_to_hindi(word))