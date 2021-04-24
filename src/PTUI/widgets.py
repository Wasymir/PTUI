import textwrap


# Base

class _Widget:
    def __init__(self, data_generator, **kwargs):
        self.content = []
        self.width = 0
        self.height = 0
        self.dynamic_data = data_generator
        self.static_data = kwargs.copy()
        self.build()

    def _fill_up_widget(self):
        self.content = [line.ljust(self.width) for line in self.content]
        self.content.extend([' ' * self.width] * (self.height - len(self.content)))

    def _render(self, **data):
        pass

    def build(self):
        return self._render(**dict(self.dynamic_data(), **self.static_data))


# Mixins


# Invisible

class PlaceHolderWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(PlaceHolderWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.content = [' ' * data['size']][0] * data['size'][1]
        self.width = data['width']
        self.height = data['height']
        self._fill_up_widget()
        return self.content


class PaddingWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(PaddingWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = data['child'].height + data['padding'][0] + data['padding'][2]
        self.width = data['child'].width + data['padding'][1] + data['padding'][3]
        self.content = [(' ' * data['padding'][3]) + line + (' ' * data['padding'][1]) for line in
                        data['child'].build()]
        if data['padding'][0]:
            for _ in range(data['padding'][0]):
                self.content.insert(0, ' ' * self.width)
        if data['padding'][2]:
            for _ in range(data['padding'][2]):
                self.content.append(' ' * self.width)
        self._fill_up_widget()
        return self.content


# Basic

class TextWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(TextWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.content = [line for un_wrapped_line in data['text'].split('\n') for line in
                        textwrap.wrap(un_wrapped_line, (data['wrap'] if 'wrap' in data.keys() else 35))]
        self.width = max(len(line) for line in self.content)
        self.height = len(self.content)
        self._fill_up_widget()
        return self.content


# Nesting

class ThinTitleWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThinTitleWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.width = max(max(len(line) for line in data['child'].build()), len(data['title']) + 1)
        self.height = data['child'].height + 1
        self.content = [f'={data["title"]}'.ljust(self.width, '-')]
        self.content.extend(map(lambda line: line.ljust(self.width), data['child'].build()))
        self._fill_up_widget()
        return self.content


class ThickTitleWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThickTitleWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.width = max(max(len(line) for line in data['child'].build()), len(data['title']) + 1)
        self.height = data['child'].height + 1
        self.content = [f'={data["title"]}'.ljust(self.width, '=')]
        self.content.extend(map(lambda line: line.ljust(self.width), data['child'].build()))
        self._fill_up_widget()
        return self.content


class ThinBorderWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThinBorderWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        self.width = data['child'].width + (1 if data['border'][1] else 0) + (1 if data['border'][3] else 0)
        self.content = [('|' if data['border'][3] else '') + line + ('|' if data['border'][1] else '') for line in
                        data['child'].build()]
        if data['border'][2]:
            self.content.append('-' * self.width)
        if data['border'][0]:
            self.content.insert(0, '-' * self.width)
        self._fill_up_widget()
        return self.content


class ThickBorderWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThickBorderWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = data['child'].height + (1 if data['border'][0] else 0) + (1 if data['border'][2] else 0)
        self.width = data['child'].width + (2 if data['border'][1] else 0) + (2 if data['border'][3] else 0)
        self.content = [('||' if data['border'][3] else '') + line + ('||' if data['border'][1] else '') for line in
                        data['child'].build()]
        if data['border'][2]:
            self.content.append('=' * self.width)
        if data['border'][0]:
            self.content.insert(0, '=' * self.width)
        self._fill_up_widget()
        return self.content


class ThinBorderCardWidget(ThinBorderWidget):
    def __init__(self, data_generator, **kwargs):
        super(ThinBorderCardWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        data = dict(data, **{'border': [True, True, True, True]})
        super(ThinBorderCardWidget, self)._render(**data)
        self.content[0] = f'-{data["title"]}'.ljust(self.width, '-')
        self.width = len(self.content[0]) if len(self.content[0]) > self.width else self.height
        self._fill_up_widget()
        return self.content


class ThickBorderCardWidget(ThickBorderWidget):
    def __init__(self, data_generator, **kwargs):
        super(ThickBorderCardWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        data = dict(data, **{'border': [True, True, True, True]})
        super(ThickBorderCardWidget, self)._render(**data)
        self.content[0] = f'={data["title"]}'.ljust(self.width, '=')
        self.width = len(self.content[0]) if len(self.content[0]) > self.width else self.height
        self._fill_up_widget()
        return self.content


# Layout

class RowWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(RowWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.width = sum([len(child.width) for child in data['children']])
        self.height = max(child.height for child in data['children'])
        self.content = [''.join(line) for line in zip(*[
            (child.build() + [' ' * child.width] * self.height)[:self.height] for child in data['children']])]
        return self.content


class ThinBorderRowWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThinBorderRowWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.width = sum([len(child.width) for child in data['children']]) + len(data['children']) - 1
        self.height = max(child.height for child in data['children'])
        self.content = ['|'.join(line) for line in
                        zip(*[(child.build() + [' ' * child.width] * self.height)[:self.height] for child in
                              data['children']])]
        self._fill_up_widget()
        return self.content


class ThickBorderRowWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ThickBorderRowWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.width = sum([child.width for child in data['children']]) + (len(data['children']) - 1) * 2
        self.height = max(child.height for child in data['children'])
        self.content = ['||'.join(line) for line in
                        zip(*[(child.build() + [' ' * child.width] * self.height)[:self.height] for child in
                              data['children']])]
        self._fill_up_widget()
        return self.content


class ColumnWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ColumnWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = sum(child.height for child in data['children'])
        self.width = max(child.width for child in data['children'])
        self.content = [line.ljust(self.width) for child in data['children'] for line in child.build()]


class ColumnThinBorderWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ColumnThinBorderWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self.width = max(child.width for child in data['children'])
        for child in data['children']:
            if not child == data['children'][-1]:
                self.content.append('-' * self.width)
            for line in child.build():
                self.content.append(line)


class ColumnThickBorderWidget(_Widget):
    def __init__(self, data_generator, **kwargs):
        super(ColumnThickBorderWidget, self).__init__(data_generator, **kwargs)

    def _render(self, **data):
        self.height = sum(child.height for child in data['children']) + len(data['children']) - 1
        self.width = max(child.width for child in data['children'])
        for child in data['children']:
            if not child == data['children'][-1]:
                self.content.append('=' * self.width)
            for line in child.build():
                self.content.append(line)
