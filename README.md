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

##### TextWidget

Widget that's just text.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| text : `str` | text inside Widget | Required |
| wrap: `int` | the length of the lines to which the text will be wrapped | 35 |

___

##### PlaceHolderWidget

Just an empty space.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| size: `list<int>`| size of the empty space in format `[WIDTH : int, HEIGHT : int]` | Required |

##### ThinBorderWidget

Widget that wraps another widget with a thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is wrapped with border | Required |

___

##### ThickBorderWidget

Widget that wraps another widget with a thick border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is wrapped with border | Required |

___

##### ThinBorderWidget

Widget that wraps another widget with a thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is wrapped with border | Required |

___

##### ThickTitleWidget

Widget that adds title decorated with thick line to another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added title  | Required |
| title : `str` | title that is added to widget | Required |

___

##### ThinTitleWidget

Widget that adds title decorated with thin line to another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added title  | Required |
| title : `str` | title that is added to widget | Required |

___

##### PaddingWidget

Widget that adds padding around the another widget.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is added padding  | Required |
| padding : `list<int>` | size of the padding in format `[TOP : int, RIGHT : int, BOTTOM : int, LEFT : int]` | Required |

___

##### ThinBorderCardWidget

Widget that wraps another widget with Thin Border with title.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is wrapped  | Required |
| title : `str` | title that is added to BOrder | Required |

___

##### ThickBorderCardWidget

Widget that wraps another widget with Thick Border with title.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget which is wrapped  | Required |
| title : `str` | title that is added to Border | Required |

___

##### RowWidget

Widget that place another widgets in a row.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

##### ThinBorderRowWidget

Widget that place another widgets in a row and separates them with thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

##### ThickBorderRowWidget

Widget that place another widgets in a row and separates them with thick border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

##### ColumnWidget

Widget that place another widgets in a column.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

##### ColumnThinBorderWidget

Widget that place another widgets in a column and separates them with thin border.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| children : `list<wiget>` | list of widgets that will be placed in a row | Required |

___

##### ColumnThickBorderWidget

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
returned from an anonymous function created with lambda keyword, and the static ones are passed just as kwargs.

###### Example

```python
from PTUI.widgets import ThickBorderCardWidget

title = 'bar'
child =  # place here another Widget
foo = ThickBorderCardWidget(
    lambda: {
        'title': title
    },
    **{
        'child': child
    }
)
```

If you change the title variable and refresh the widget will change it's title, but if you do the same to child
variable, nothing will happen.

### Remember that dynamic_data is a required argument, so even if you don't want to pass any dynamic data, you have to pass empty dictionary as lambda function return!

---
---

## Screens

---

#### Screens are the way to display your UI in Terminal.

---

### List of screens:

---

##### AutoRefreshingScreen

Screen that refreshes itself one per specified period of time.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is built and  displayed| Required |
| centered : `bool` | specifies if widget should be in the center of terminal | True |
| refresh_time : `float` | specified period of time in which screen should be refreshed | 0.1 |

| Function|      Description      |  parameters |
|----------|:-------------:|------:|
| start | stops refreshing screen | None |
| stop  | starts refreshing screen | None |
| \_\_str__  | returns rendered string instead of printing it | None |


___

##### ManualRefreshScreen

Screen that you have to refresh manually.

| Parameters : type  |      Description      |  Required/Default |
|----------|:-------------:|------:|
| child : `Widget` | widget that is built and  displayed| Required |
| centered : `bool` | specifies if widget should be in the center of terminal | True |

| Function|      Description      |  parameters |
|----------|:-------------:|------:|
| refresh | refreshes screen | None |




___


