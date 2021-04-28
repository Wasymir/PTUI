import itertools
import re
import textwrap

from .exeptions import BadInputData, InputStringMustBeOneCharacterLong
from .styles import StyleData, style, Colors


# Base

class _Widget:
    def __init__(self, **kwargs):
        self._width = 0
        self._height = 0
        self.dynamic_data = (kwargs['dynamic_data'] if 'dynamic_data' in kwargs.keys() else lambda: {})
        self.static_data = kwargs.copy()
        self.style_data = (self.data['style'] if 'style' in self.data.keys() else StyleData())
        self.build()

    def char(self, char=' '):
        if len(char) != 1:
            raise InputStringMustBeOneCharacterLong
        return style(char, self.style_data)

    @property
    def data(self):
        try:
            return dict(self.dynamic_data(), **self.static_data)
        except KeyError:
            raise BadInputData

    def get_from_data(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise BadInputData

    @property
    def height(self):
        self.build()
        return self._height

    @property
    def width(self):
        self.build()
        return self._width

    def _render(self, **data):
        content = []
        return content

    def build(self, width=None, height=None):
        if width is None:
            width = self._width
        if height is None:
            height = self._height
        raw = self._render(**self.data)
        left = (width - max([len(row) for row in raw])) // 2
        right = width - max([len(row) for row in raw]) - left
        content = list(map(lambda row: [self.char()] * left + row + [self.char()] * right, raw))
        content = (content + [[self.char() for _ in range(width)]] * height)[:height]
        return content


# Mixins
class _TitleToolsMixin:
    @staticmethod
    def parse_to_title(child):
        def remove_styling(text):
            reaesc = re.compile(r'\x1b[^m]*m')
            return reaesc.sub('', text)

        content = []
        for line in child.build():
            for key, value in enumerate(line):
                if remove_styling(value) == ' ':
                    line.pop(key)
                else:
                    break

            for key, value in reversed(list(enumerate(line))):
                if remove_styling(value) == ' ':
                    line.pop(key)
                else:
                    break
            content.extend(line + [child.char()])
        return content


# Invisible
class PlaceHolderWidget(_Widget):
    def __init__(self, **kwargs):
        super(PlaceHolderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        content = [[self.char() for _ in range(data['size'][1])] for _ in range(data['size'][1])]
        self._width = data['size'][0]
        self._height = data['size'][1]
        return content


class PaddingWidget(_Widget):
    def __init__(self, **kwargs):
        super(PaddingWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = data['child'].height + data['padding'][0] + data['padding'][2]
        self._width = data['child'].width + data['padding'][1] + data['padding'][3]
        content = [
            [self.char() for _ in range(data['padding'][3])] + line + [self.char() for _ in range(data['padding'][1])]
            for line in data['child'].build()
        ]
        if data['padding'][0]:
            for _ in range(data['padding'][0]):
                content.insert(0, [self.char() for _ in range(self._width)])
        if data['padding'][2]:
            for _ in range(data['padding'][2]):
                content.append([self.char() for _ in range(self._width)])
        return content


# Basic

class TextWidget(_Widget):
    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)

    def _render(self, **data):
        wrap = (data['wrap'] if 'wrap' in data.keys() else 35)
        self._width = max(
            len(line) for un_wrapped in data['text'].split('\n') for line in textwrap.wrap(un_wrapped, wrap))
        self._height = len(
            list(line for un_wrapped in data['text'].split('\n') for line in textwrap.wrap(un_wrapped, wrap)))
        content = [
            [self.char(char) for char in line.ljust(self._width)]
            for un_wrapped in data['text'].split('\n') for line in textwrap.wrap(un_wrapped, wrap)
        ]
        return content


class CharWidget(_Widget):
    def __init__(self, **kwargs):
        super(CharWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = 0
        self._height = 0
        return self.char(data['chr'])


# Nesting

class ThinTitleWidget(_Widget, _TitleToolsMixin):
    def __init__(self, **kwargs):
        super(ThinTitleWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width, 1 + len(self.parse_to_title(data['title'])))
        self._height = data['child'].height + 1
        content = [[self.char('-')] + self.parse_to_title(data['title']) + [self.char('-')] * self._width][
                  :self._width] + data['child'].build(width=self._width)
        return content


class ThickTitleWidget(_Widget, _TitleToolsMixin):
    def __init__(self, **kwargs):
        super(ThickTitleWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width, 1 + len(self.parse_to_title(data['title'])))
        self._height = data['child'].height + 1
        content = [[self.char('=')] + self.parse_to_title(data['title']) + [self.char('=')] * self._width][
                  :self._width] + data['child'].build(width=self._width)
        return content


class ThinBorderWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = data['child'].width + (1 if data['border'][1] else 0) + (1 if data['border'][3] else 0)
        self._height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        content = []
        if data['border'][0]:
            content.append([self.char('-')] * self._width)
        for line in data['child'].build():
            content.append([])
            if data['border'][3]:
                content[-1].append(self.char('|'))
            content[-1].extend(line)
            if data['border'][1]:
                content[-1].append(self.char('|'))
        if data['border'][2]:
            content.append([self.char('-')] * self._width)
        return content


class ThickBorderWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = data['child'].width + (2 if data['border'][1] else 0) + (2 if data['border'][3] else 0)
        self._height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        content = []
        if data['border'][0]:
            content.append([self.char('=')] * self._width)
        for line in data['child'].build():
            content.append([])
            if data['border'][3]:
                content[-1].append(self.char('|'))
                content[-1].append(self.char('|'))
            content[-1].extend(line)
            if data['border'][1]:
                content[-1].append(self.char('|'))
                content[-1].append(self.char('|'))
        if data['border'][2]:
            content.append([self.char('=')] * self._width)
        return content


class ThinBorderCardWidget(_Widget, _TitleToolsMixin):
    def __init__(self, **kwargs):
        super(ThinBorderCardWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width + 2, 1 + len(self.parse_to_title(data['title'])))
        self._height = data['child'].height + 2
        content = [
            ([self.char('-')] + self.parse_to_title(data['title']) + [self.char('-')] * self._width)[:self._width]]
        for line in data['child'].build(width=self._width - 2):
            content.append([self.char('|')] + line + [self.char('|')])
        content.append([self.char('-')] * self._width)
        return content


class ThickBorderCardWidget(_Widget, _TitleToolsMixin):
    def __init__(self, **kwargs):
        super(ThickBorderCardWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width + 4, 1 + len(self.parse_to_title(data['title'])))
        self._height = data['child'].height + 2
        content = [
            ([self.char('=')] + self.parse_to_title(data['title']) + [self.char('=')] * self._width)[:self._width]]
        for line in data['child'].build(width=self._width - 4):
            content.append([self.char('|'), self.char('|')] + line + [self.char('|'), self.char('|')])
        content.append([self.char('=')] * self._width)
        return content


# Layout

class RowWidget(_Widget):
    def __init__(self, **kwargs):
        super(RowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']])
        self._height = max(child.height for child in data['children'])
        content = [list(itertools.chain(*row)) for row in
                   zip(*[child.build(height=self._height) for child in data['children']])]
        return content


class ThinBorderRowWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderRowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']]) + len(data['children']) - 1
        self._height = max(child.height for child in data['children'])
        content = []
        for row in zip(*[child.build(height=self._height) for child in data['children']]):
            content.append([])
            for index, widget_row in enumerate(row):
                content[-1].extend(widget_row)
                if not index == len(row) - 1:
                    content[-1].append(self.char('|'))
        return content


class ThickBorderRowWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderRowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']]) + (len(data['children']) - 1) * 2
        self._height = max(child.height for child in data['children'])
        content = []
        for row in zip(*[child.build(height=self._height) for child in data['children']]):
            content.append([])
            for index, widget_row in enumerate(row):
                content[-1].extend(widget_row)
                if not index == len(row) - 1:
                    content[-1].append(self.char('|'))
                    content[-1].append(self.char('|'))
        return content


class ColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children'])
        self._width = max(child.width for child in data['children'])
        content = [line for child in data['children'] for line in child.build(width=self._width)]
        return content


class ThinBorderColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self._width = max(child.width for child in data['children'])
        content = []
        for child in data['children']:
            for row in child.build(width=self._width):
                content.append(row)
            if not child == data['children'][-1]:
                content.append([self.char('-')] * self._width)
        return content


class ThickBorderColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self._width = max(child.width for child in data['children'])
        content = []
        for child in data['children']:
            for row in child.build(width=self._width):
                content.append(row)
            if not child == data['children'][-1]:
                content.append([self.char('=')] * self._width)
        return content


# artistic
class ArtWidget(_Widget):
    def __init__(self, **kwargs):
        super(ArtWidget, self).__init__(**kwargs)

    def _render(self, **data):
        pixels = {
            'B': style(' ', StyleData(background_color=Colors.BackgroundColors.Black)),
            'r': style(' ', StyleData(background_color=Colors.BackgroundColors.Red)),
            'g': style(' ', StyleData(background_color=Colors.BackgroundColors.Green)),
            'y': style(' ', StyleData(background_color=Colors.BackgroundColors.Yellow)),
            'b': style(' ', StyleData(background_color=Colors.BackgroundColors.Blue)),
            'm': style(' ', StyleData(background_color=Colors.BackgroundColors.Magenta)),
            'c': style(' ', StyleData(background_color=Colors.BackgroundColors.Cyan)),
            'w': style(' ', StyleData(background_color=Colors.BackgroundColors.White)),
            ' ': self.char()
        }

        def pixel(color_key):
            try:
                return pixels[color_key]
            except KeyError:
                raise BadInputData

        self._height = len(data['art'].split('\n'))
        self._width = max(len(line) for line in data['art'].split('\n'))
        content = []
        for line in data['art'].split('\n'):
            content.append([])
            for char in ([pixel(char) for char in line] + [self.char()] * self._width)[:self._width]:
                content[-1].append(char)
        return content
