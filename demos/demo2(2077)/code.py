from PTUI.styles import Colors,StyleData
from PTUI.widgets import *
from PTUI.screens import ManualRefreshScreen
leftart =\
'''Byb
yyb
Byb
yyb
Byb
yyb
Byb'''
style1 = StyleData(font_color=Colors.FontColors.Black,background_color=Colors.BackgroundColors.Yellow)
style2 = StyleData(font_color=Colors.FontColors.Black,background_color=Colors.BackgroundColors.Blue)
ui = ManualRefreshScreen(
    child= ThickBorderCardWidget(
        title=TextWidget(text='CyberPunk 2077',style=style2),
        child=RowWidget(
            children=[
                ArtWidget(style=style1,art=leftart),
                TextWidget(style=style1,text='Wake the fu*k up, samurai! We have a city to burn!')
            ]
        ),
        style=style2
    )
).refresh()

