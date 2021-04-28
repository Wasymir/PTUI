from datetime import datetime
from time import sleep
from PTUI.screens import ManualRefreshScreen
from PTUI.styles import StyleData, Colors
from PTUI.widgets import ThickBorderCardWidget, TextWidget, PaddingWidget

style_night = StyleData(background_color=Colors.BackgroundColors.Blue)
style_day = StyleData(background_color=Colors.BackgroundColors.Cyan)
actual_style = lambda: style_night if True else style_day

ui = ManualRefreshScreen(
    child=ThickBorderCardWidget(
        dynamic_data=lambda: {'style': actual_style()},
        title=TextWidget(dynamic_data=lambda: {'style': actual_style()}, text="It's"),
        child=PaddingWidget(
            dynamic_data=lambda: {'style': actual_style()},
            padding=[2, 4, 2, 4],
            child=TextWidget(
                dynamic_data=lambda: {
                    'style': actual_style(),
                    'text': '21:37:00'
                }
            )
        )
    )
)
while True:
    ui.refresh()
    sleep(0.5)

