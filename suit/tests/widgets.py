from django.test import TestCase
from suit.widgets import LinkedSelect, HTML5Input, EnclosedInput, \
    NumberInput, SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget, \
    AutosizedTextarea
from django.utils.translation import ugettext as _
from django.templatetags.static import static
from suit import utils

django_version = utils.django_major_version()


class WidgetsTestCase(TestCase):
    def test_NumberInput(self):
        inp = NumberInput()
        self.assertEqual('number', inp.input_type)

    def test_HTML5Input(self):
        input_type = 'calendar'
        inp = HTML5Input(input_type=input_type)
        self.assertEqual(input_type, inp.input_type)

    def test_LinkedSelect(self):
        ls = LinkedSelect()
        self.assertTrue('linked-select' in ls.attrs['class'])

    def test_LinkedSelect_with_existing_attr(self):
        ls = LinkedSelect(attrs={'class': 'custom-class', 'custom': 123})
        self.assertEqual('linked-select custom-class', ls.attrs['class'])
        self.assertEqual(ls.attrs['custom'], 123)

    def render_enclosed_widget(self, enclosed_widget):
        return enclosed_widget.render('enc', 123)

    def get_enclosed_widget_html(self, values):
        return '<div class="input-prepend input-append">%s<input name="enc" ' \
               'type="text" value="123" />%s</div>' % values

    def test_EnclosedInput_as_text(self):
        inp = EnclosedInput(prepend='p', append='a')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="add-on">p</span>',
                  '<span class="add-on">a</span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_icon(self):
        inp = EnclosedInput(prepend='icon-fire', append='icon-leaf')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="add-on"><i class="icon-fire"></i></span>',
                  '<span class="add-on"><i class="icon-leaf"></i></span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_html(self):
        inp = EnclosedInput(prepend='<em>p</em>', append='<em>a</em>')
        output = self.render_enclosed_widget(inp)
        result = ('<em>p</em>', '<em>a</em>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_SuitDateWidget(self):
        sdw = SuitDateWidget()
        self.assertTrue('vDateField' in sdw.attrs['class'])

    def test_SuitDateWidget_with_existing_class_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Date:')[:-1], sdw.attrs['placeholder'])

    def test_SuitDateWidget_with_existing_placeholder_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def get_SuitDateWidget_output(self):
        if django_version < (1, 11):
            return '<div class="input-append suit-date"><input class="vDateField ' \
                   'input-small " name="sdw" placeholder="Date" ' \
                   'size="10" type="text" /><span class="add-on"><i ' \
                   'class="icon-calendar"></i></span></div>'
        else:
            return '<div class="input-append suit-date"><input type="text" name="sdw" ' \
                   'value="" class="vDateField input-small " size="10" placeholder="Date" />' \
                   '<span class="add-on"><i class="icon-calendar"></i></span></div>'

    def test_SuitDateWidget_output(self):
        sdw = SuitDateWidget(attrs={'placeholder': 'Date'})
        output = sdw.render('sdw', '')
        self.assertHTMLEqual(
            self.get_SuitDateWidget_output(), output)

    def test_SuitTimeWidget(self):
        sdw = SuitTimeWidget()
        self.assertTrue('vTimeField' in sdw.attrs['class'])

    def test_SuitTimeWidget_with_existing_class_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Time:')[:-1], sdw.attrs['placeholder'])

    def test_SuitTimeWidget_with_existing_placeholder_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def get_SuitTimeWidget_output(self):
        if django_version < (1, 11):
            return '<div class="input-append suit-date suit-time"><input ' \
                   'class="vTimeField input-small " name="sdw" ' \
                   'placeholder="Time" size="8" type="text" /><span ' \
                   'class="add-on"><i class="icon-time"></i></span></div>'
        else:
            return '<div class="input-append suit-date suit-time"><input ' \
                   'type="text" name="sdw" value="" class="vTimeField input-small " ' \
                   'size="8" placeholder="Time" /><span class="add-on">' \
                   '<i class="icon-time"></i></span></div>'

    def test_SuitTimeWidget_output(self):
        sdw = SuitTimeWidget(attrs={'placeholder': 'Time'})
        output = sdw.render('sdw', '')
        self.assertHTMLEqual(
            self.get_SuitTimeWidget_output(),
            output)

    def get_SuitSplitDateTimeWidget_output(self):
        if django_version < (1, 11):
            dwo = self.get_SuitDateWidget_output().replace('sdw', 'sdw_0')
            two = self.get_SuitTimeWidget_output().replace('sdw', 'sdw_1')
            return '<div class="datetime">%s %s</div>' % (dwo, two)
        else:
            return '<div class="datetime"><input type="text" name="sdw_0" ' \
                   'class="vDateField input-small " size="10" placeholder="Date" ' \
                   '/><input type="text" name="sdw_1" class="vTimeField input-small " ' \
                   'size="8" placeholder="Time" /></div>'

    def test_SuitSplitDateTimeWidget(self):
        ssdtw = SuitSplitDateTimeWidget()
        output = ssdtw.render('sdw', '')
        self.assertHTMLEqual(
            self.get_SuitSplitDateTimeWidget_output(),
            output)

    def test_AutosizedTextarea(self):
        txt = AutosizedTextarea()
        self.assertTrue('autosize' in txt.attrs['class'])
        self.assertEqual(2, txt.attrs['rows'])

    def test_AutosizedTextarea_with_existing_attrs(self):
        txt = AutosizedTextarea(attrs={'class': 'custom-class', 'rows': 3})
        self.assertTrue('autosize ' in txt.attrs['class'])
        self.assertTrue(' custom-class' in txt.attrs['class'])
        self.assertEqual(txt.attrs['rows'], 3)

    def test_AutosizedTextarea_output(self):
        txt = AutosizedTextarea()
        self.assertHTMLEqual(txt.render('txt', ''), (
            '<textarea class="autosize " cols="40" name="txt" '
            'rows="2">\r\n</textarea><script type="text/javascript">Suit.$('
            '\'#id_txt\').autosize();</script>'))

    def test_AutosizedTextarea_media(self):
        txt = AutosizedTextarea()
        js_url = static('suit/js/jquery.autosize-min.js')
        self.assertHTMLEqual(str(txt.media),
                             '<script type="text/javascript" src="%s"></script>'
                             % js_url)
