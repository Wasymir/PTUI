from PTUI.widgets import ArtWidget, RowWidget, TextWidget
from PTUI.screens import ManualRefreshScreen
from PTUI.styles import StyleData, Colors

art =\
'''
          BBBBBBBBBBBBBBBBBBBBBB
        BB                     BBBBB
       BB                           BB
       B                              BB
      B         BBBBBB                 BB
      B        B              BBBBB     B
     B                             B    B
     B         BBBBBBB          BB       B
    B        BBBBBB   B       BBB B      BB
   B         BBBBBBBB  B     BBBBBBB      BB
 BBB  BBBB       B   BB    BBB             B
 B   B    BB   BB     B      B             BB
B   B   B   BBB       B      B              B
B   B   BB          BBB      BB             B
B   B  BB BBB       B   BB    BB      B    B
B   B   B   BBB      B        BB     BB   BB
 B      BB   B BBB           BB      BB   B
  B      BBB B    BB        B      BBBBB  B
   B     BB BBB    BBBBBBBBBBBBBBBB B BB B      
    B     B  BBBBB B     B   B  B B B BB B
    B      B B  BBBB     B   B  B B BBBB B
     B      BB     BBBBBBBBBBBBBBBBBBBBB B        
     B       B     B  BBBBBBBBBBBBBBBBB  B       
      B       BB  B     B BBBBBBBBB B B  B       
       B       BB B     B    B  B B B B  B
        B        BBB    B   B   B B BB    B
         BB        BBBBBBBBBBBBBBBBBB     B    
          BB                             B
            BB                           B
              BBB                        B
                 BB                      B
                   BB                    B
                     BBBB               B
                        BBBB          BB
                            BBBBBBBBBB                          
'''

style = StyleData(background_color=Colors.BackgroundColors.White,font_color=Colors.FontColors.Black)
ui = ManualRefreshScreen(
    child=RowWidget(
        children=[ArtWidget(art=art,style=style),
                  TextWidget(text="You've been hacked!!!\n" * 37,style=style)]
    )
).refresh()

