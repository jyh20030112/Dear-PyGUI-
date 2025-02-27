import dearpygui.dearpygui as dpg

def set_chinese_font(font,cond_rang):
    with dpg.font_registry():  # 注册字体，自选字体
        with dpg.font("geetypeqingkongwantixiti.ttf", 20) as font1:  # 增加中文编码范围，防止问号
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    return font1