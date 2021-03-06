# PTUI

---

## Small, Python, Flutter Inspired TUI Framework

___
___

## Widgets

---

#### Just like in flutter widgets are a way to declare and construct UI.

___

### List of Widgets

---

##### widgets.TextWidget

---
```
text
```
###### Text Widget example

---
Widget that's just text.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| text : `str` | text inside Widget | Required |
| wrap: `int` | the length of the lines to which the text will be wrapped | 35 |

___

#####  widgets.PlaceHolderWidget

---
```
         
         
         
```
###### PlaceHolder Widget example

---
Just an empty space.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| size: `list<int>`| size of the empty space in format `[WIDTH : int, HEIGHT : int]` | Required |

---
#####  widgets.ThickBorderWidget

---
```
-------
|child|
-------


|child|
-------


------
|child
------
```
###### Thin Border Widget examples 

---
Widget that wraps another widget with a thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is wrapped with border | Required |
| border: `List<bool>` | specifies on which side would be border. `[TOP: bool, RIGTH: bool, BOTTOM: bool, LEFT: bool]` | Required |
___

#####  widgets.ThickBorderWidget

---
```
=========
||child||
=========


||child||
=========


=======
||child
=======
```
###### Thick Border Widget examples

---
Widget that wraps another widget with a thick border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is wrapped with border | Required |

___

#####  widgets.ThickTitleWidget

---
```
=title=====
Lorem Ipsum
```
###### Thick Title Widget example (I placed `Lorem impsum` instead of `child` because it looked nicer) 

---
Widget that adds title decorated with thick line to another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added title  | Required |
| title : `TextWidget` | title that is added to widget | Required |

___

#####  widgets.ThinTitleWidget

---
```
-title-----
Lorem Ipsum
```
###### Thick Title Widget example (I placed `Lorem impsum` instead of `child` because it looked nicer)

---
Widget that adds title decorated with thin line to another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added title  | Required |
| title : `TextWidget` | title that is added to widget | Required |

___

#####  widgets.PaddingWidget

---
```

  child

```
###### Padding Widget example 

---
Widget that adds padding around the another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added padding  | Required |
| padding : `list<int>` | size of the padding in format `[TOP : int, RIGHT : int, BOTTOM : int, LEFT : int]` | Required |

___

#####  widgets.ThinBorderCardWidget

---
```
-title-
|child|
-------
```
###### Thin Border Card Widget example 

---
Widget that wraps another widget with Thin Border with title.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is wrapped  | Required |
| title : `TextWidget` | title that is added to BOrder | Required |

___

#####  widgets.ThickBorderCardWidget

---
```
=title===
||child||
=========
```
###### Thick Border Card Widget example 

---
Widget that wraps another widget with Thick Border with title.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is wrapped  | Required |
| title : `TextWidget` | title that is added to Border | Required |

___

#####  widgets.RowWidget

---
```
#0 child,#1 child,#2 child,#3 child,#4 child,
```
###### Row Widget example (commas after each child aren't feature of the widget)

---
Widget that place another widgets in a row.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

#####  widgets.ThinBorderRowWidget

---
```
#0 child|#1 child|#2 child|#3 child|#4 child
```
###### Thin Border Row Widget example

---
Widget that place another widgets in a row and separates them with thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

#####  widgets.ThickBorderRowWidget

---
```
#0 child||#1 child||#2 child||#3 child||#4 child
```
###### Thick Border Row Widget example

---
Widget that place another widgets in a row and separates them with thick border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

#####  widgets.ColumnWidget

---
```
#0 child
#1 child
#2 child
#3 child
#4 child
```
###### Column Widget example

---
Widget that place another widgets in a column.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

#####  widgets.ThinBorderColumnWidget

---
```
#0 child
--------
#1 child
--------
#2 child
--------
#3 child
--------
#4 child
```
###### Thin Border Column Widget example

---
Widget that place another widgets in a column and separates them with thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

#####  widgets.ThickBorderColumnWidget

---
```
#0 child
========
#1 child
========
#2 child
========
#3 child
========
#4 child
```
###### Thick Border Column Widget example

---
Widget that place another widgets in a column and separates them with thick border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___
___

### Passing data to Widgets

There are to ways to pass data to widget:

- Static:
  Data passed with that method never changes.


- Dynamic:
  If you change data passed with that method and refresh the widget, displayed data will also change.

All types all data are passed as an arguments to the Widget constructor, but the dynamic ones are passed as dictionary
returned from an anonymous function created with lambda keyword passed as `dynamic_data`.

###### Example

```python
from PTUI.widgets import ThickBorderCardWidget, TextWidget

title = 'foo'
body = 'bar'
foo = ThickBorderCardWidget(
    dynamic_data=lambda: {
        'title': title
    },
    child=TextWidget(text=body)

)
```

If you change the title variable and refresh the widget will change it's title, but if you do the same to body variable,
nothing will happen.

---
---
## Styling Text

---
#### Because whole UI is text, by styling text you style whole UI.

___

You can style widget by passing to it StyleData object as style parameter.

---
##### styles.StyleData

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| font_color : `styles.Colors.FontColors.*` | font color | default console font color |
| background_color : `styles.Colors.BackgroundColors.*` | font background color | default console font background color |
| font_brightness : `styles.Colors.FontBrightness.*` | font brightness | default console font brightness |

---
---

## Screens

---

#### Screens are the way to display your UI in Terminal.

---

### List of screens:

---
##### screens.ManualRefreshScreen

Screen that you have to refresh manually.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is built and  displayed| Required |
| centered : `bool` | specifies if widget should be in the center of terminal | True |

| Function|      Description      |  parameters |
|----------|:-------------:|------:|
| refresh | refreshes screen | None |
| \_\_str__  | returns rendered string instead of printing it | None |

___

## Screens Manger

---

#### Screens Manager is a way to manage multiple screens.

---

| Function|      Description      |  parameters |
|----------|:-------------:|------:|
| display | display screen, which it was passed as argument | screen_id : `str` |
| refresh  | refreshes actual screen | None |

### Passing data to Screens Manager

You pass Screens to Screen Manager constructor as kwargs, where key is screen id, and the value a Screen.

###### Example

```python
from PTUI.screens import ScreensManager, ManualRefreshScreen
from PTUI.widgets import TextWidget

sm = ScreensManager(
    foo=ManualRefreshScreen(child=TextWidget(text='foo')),
    bar=ManualRefreshScreen(child=TextWidget(text='bar')),
)
```
