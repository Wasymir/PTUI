import textwrap


# Base

class _Widget:
    def __init__(self, **kwargs):
        self.content = []
        self._width = 0
        self._height = 0
        self.dynamic_data = (kwargs['dynamic_data'] if 'dynamic_data' in kwargs.keys() else lambda: {})
        self.static_data = kwargs.copy()
        self.build()

    @property
    def height(self):
        self.build()
        return self._height

    @property
    def width(self):
        self.build()
        return self._width

    def _render(self, **data):
        self.content = []
        return self.content

    def build(self):
        self.content.clear()
        return [line.ljust(self._width) for line in self._render(**dict(self.dynamic_data(), **self.static_data))]


# Mixins


# Invisible

class PlaceHolderWidget(_Widget):
    def __init__(self, **kwargs):
        super(PlaceHolderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self.content = [' ' * data['size'][0]] * data['size'][1]
        self._width = data['size'][0]
        self._height = data['size'][1]
        return self.content


class PaddingWidget(_Widget):
    def __init__(self, **kwargs):
        super(PaddingWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = data['child'].height + data['padding'][0] + data['padding'][2]
        self._width = data['child'].width + data['padding'][1] + data['padding'][3]
        self.content = [(' ' * data['padding'][3]) + line + (' ' * data['padding'][1]) for line in
                        data['child'].build()]
        if data['padding'][0]:
            for _ in range(data['padding'][0]):
                self.content.insert(0, ' ' * self._width)
        if data['padding'][2]:
            for _ in range(data['padding'][2]):
                self.content.append(' ' * self._width)
        return self.content


# Basic

class TextWidget(_Widget):
    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self.content = [line for un_wrapped_line in data['text'].split('\n') for line in
                        textwrap.wrap(un_wrapped_line, (data['wrap'] if 'wrap' in data.keys() else 35))]
        self._width = max(len(line) for line in self.content)
        self._height = len(self.content)
        self.content = [line.ljust(self._width) for line in self.content]
        return self.content


# Nesting

class ThinTitleWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinTitleWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(max(len(line) for line in data['child'].build()), len(data['title']) + 1)
        self._height = data['child'].height + 1
        self.content = [f'-{data["title"]}'.ljust(self._width, '-')]
        self.content.extend(map(lambda line: line.ljust(self._width), data['child'].build()))
        return self.content


class ThickTitleWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickTitleWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(max(len(line) for line in data['child'].build()), len(data['title']) + 1)
        self._height = data['child'].height + 1
        self.content = [f'={data["title"]}'.ljust(self._width, '=')]
        self.content.extend(map(lambda line: line.ljust(self._width), data['child'].build()))
        return self.content


class ThinBorderWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        self._width = data['child'].width + (1 if data['border'][1] else 0) + (1 if data['border'][3] else 0)
        self.content = [('|' if data['border'][3] else '') + line + ('|' if data['border'][1] else '') for line in
                        data['child'].build()]
        if data['border'][2]:
            self.content.append('-' * self._width)
        if data['border'][0]:
            self.content.insert(0, '-' * self._width)
        return self.content


class ThickBorderWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        self._width = data['child'].width + (2 if data['border'][1] else 0) + (2 if data['border'][3] else 0)
        self.content = [('||' if data['border'][3] else '') + line + ('||' if data['border'][1] else '') for line in
                        data['child'].build()]
        if data['border'][2]:
            self.content.append('=' * self._width)
        if data['border'][0]:
            self.content.insert(0, '=' * self._width)
        return self.content


class ThinBorderCardWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderCardWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width + 2, len(data["title"]) + 1)
        self._height = data['child'].height + 2
        self.content.append(f'-{data["title"]}'.ljust(self._width, '-'))
        self.content.extend(['|' + (line.center(self._width - 2)) + '|' for line in data['child'].build()])
        self.content.append('-' * self._width)
        return self.content


class ThickBorderCardWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderCardWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = max(data['child'].width + 4, len(data["title"]) + 1)
        self._height = data['child'].height + 2
        self.content.append(f'={data["title"]}'.ljust(self._width, '='))
        self.content.extend(['||' + (line.center(self._width - 4)) + '||' for line in data['child'].build()])
        self.content.append('=' * self._width)
        return self.content


# Layout

class RowWidget(_Widget):
    def __init__(self, **kwargs):
        super(RowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']])
        self._height = max(child.height for child in data['children'])
        self.content = [''.join(line) for line in zip(*[
            (child.build() + [' ' * child.width] * self._height)[:self._height] for child in data['children']])]
        return self.content


class ThinBorderRowWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderRowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']]) + len(data['children']) - 1
        self._height = max(child.height for child in data['children'])
        self.content = ['|'.join(line) for line in
                        zip(*[(child.build() + [' ' * child.width] * self._height)[:self._height] for child in
                              data['children']])]
        return self.content


class ThickBorderRowWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderRowWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._width = sum([child.width for child in data['children']]) + (len(data['children']) - 1) * 2
        self._height = max(child.height for child in data['children'])
        self.content = ['||'.join(line) for line in
                        zip(*[(child.build() + [' ' * child.width] * self._height)[:self._height] for child in
                              data['children']])]
        return self.content


class ColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children'])
        self._width = max(child.width for child in data['children'])
        self.content = [line.ljust(self._width) for child in data['children'] for line in child.build()]
        return self.content


class ThinBorderColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThinBorderColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self._width = max(child.width for child in data['children'])
        for child in data['children']:

            for line in child.build():
                self.content.append(line)
            if not child == data['children'][-1]:
                self.content.append('-' * self._width)
        return self.content


class ThickBorderColumnWidget(_Widget):
    def __init__(self, **kwargs):
        super(ThickBorderColumnWidget, self).__init__(**kwargs)

    def _render(self, **data):
        self._height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self._width = max(child.width for child in data['children'])
        for child in data['children']:
            for line in child.build():
                self.content.append(line)
            if not child == data['children'][-1]:
                self.content.append('=' * self._width)
        return self.content
