from PTUI.widgets import ArtWidget, PaddingWidget
from PTUI.screens import ManualRefreshScreen
from PTUI.styles import StyleData, Colors
art = \
    '''   rrrrr    
  rrrrrrrrr 
  BBByyBy   
 ByByyyByyy 
 ByBByyyByyy
 BByyyyBBBB 
   yyyyyyy  
  rrbrrr    
 rrrbrrbrrr 
rrrrbbbbrrrr
yyrbybbybryy
yyybbbbbbyyy
yybbbbbbbbyy
  bbb  bbb  
 BBB    BBB 
BBBB    BBBB'''
bg = StyleData(background_color=Colors.BackgroundColors.White)
ui = ManualRefreshScreen(
    child=PaddingWidget(
        style=bg,
        padding=[2,4,2,4],
        child=ArtWidget(
            art=art,
            style=bg)
    )
).refresh()
