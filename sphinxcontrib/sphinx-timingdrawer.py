from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList
from sphinx.util import logging
from sphinx.util.i18n import search_image_for_language
import subprocess
import sys
from os import path
from random import randint

sys.path.append('/cad/projects/ReUseDB/work/chrbe/timingdrawer/timingdrawer-code-r54-trunk')
import TimingDrawer

logger = logging.getLogger(__name__)

################################################################################
# SETUP
################################################################################

def setup(app):
    app.add_node(TimingDrawerNode,
                 html=(html_visit_timingdrawer, None),
                 latex=(latex_visit_timingdrawer, None),
                 text=(text_visit_timingdrawer, None))

    app.add_directive('timingdrawer', TimingDrawerDirective)
    app.connect('build-finished', on_build_finished)

    return {'version': '0.1'}   # identifies the version of our extension

################################################################################
# TimingDrawerNode
################################################################################

class TimingDrawerNode(nodes.General, nodes.Inline, nodes.Element):
    pass

def html_visit_timingdrawer(self, node):
    pass

def latex_visit_timingdrawer(self, node):
    render_timingdrawer_latex(self, node, node['code'])

def text_visit_timingdrawer(self, node):
    pass

def figure_wrapper(directive, node, caption):
    # type: (Directive, nodes.Node, unicode) -> nodes.figure
    figure_node = nodes.figure('', node)
    if 'align' in node:
        figure_node['align'] = node.attributes.pop('align')

    parsed = nodes.Element()
    directive.state.nested_parse(ViewList([caption], source=''),
                                 directive.content_offset, parsed)
    caption_node = nodes.caption(parsed[0].rawsource, '',
                                 *parsed[0].children)
    caption_node.source = parsed[0].source
    caption_node.line = parsed[0].line
    figure_node += caption_node
    return figure_node

################################################################################
# Directive
################################################################################

class TimingDrawerDirective(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
    #     'alt': directives.unchanged,
    #     'align': align_spec,
         'caption': directives.unchanged,
    #     'graphviz_dot': directives.unchanged,
    #     'name': directives.unchanged,
    }

    # def run(self):
    #     env = self.state.document.settings.env
    #     serial = env.new_serialno('TimingDrawerNode')
    #     todo_node = TimingDrawerNode('\n'.join(self.content), ids=[serial])

    #     return [todo_node]

    def run(self):
        # type: () -> List[nodes.Node]
        if self.arguments:
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    __('timingdrawer directive cannot have both content and '
                       'a filename argument'), line=self.lineno)]
            argument = search_image_for_language(self.arguments[0], self.env)
            rel_filename, filename = self.env.relfn2path(argument)
            self.env.note_dependency(rel_filename)
            try:
                with codecs.open(filename, 'r', 'utf-8') as fp:  # type: ignore
                    timingcode = fp.read()
            except (IOError, OSError):
                return [document.reporter.warning(
                    __('External TimingDrawer file %r not found or reading '
                       'it failed') % filename, line=self.lineno)]
        else:
            timingcode = '\n'.join(self.content)
            if not timingcode.strip():
                return [self.state_machine.reporter.warning(
                    __('Ignoring "graphviz" directive without content.'),
                    line=self.lineno)]
        node = TimingDrawerNode()
        node['code'] = timingcode
        node['options'] = {
            'docname': path.splitext(self.state.document.current_source)[0],
        }

        # if 'graphviz_dot' in self.options:
        #     node['options']['graphviz_dot'] = self.options['graphviz_dot']
        # if 'alt' in self.options:
        #     node['alt'] = self.options['alt']
        # if 'align' in self.options:
        #     node['align'] = self.options['align']

        caption = self.options.get('caption')
        if caption:
            node = figure_wrapper(self, node, caption)

        self.add_name(node)
        return [node]

################################################################################
# Event handlers
################################################################################

def on_build_finished(app, exc):
    # type: (Sphinx, Exception) -> None
    # if exc is None:
    #     src = path.join(sphinx.package_dir, 'templates', 'graphviz', 'graphviz.css')
    #     dst = path.join(app.outdir, '_static')
    #     copy_asset_file(src, dst)
    pass

################################################################################
# Rendering
################################################################################

def render_timingdrawer_latex(self, node, code):
    try:
        ext = 'eps'
        rand = randint(0,2**16)
        fname = 'timingdrawer-%i.%s' % (rand, ext)
        fullpath = path.join(self.builder.outdir, fname)
        TimingDrawer.create_timing_diagram(code, ext, fullpath)
    except TimingDrawer.ParseError as e:
        logger.warning(__('dot code %r: %s'), code, text_type(exc))
        raise nodes.SkipNode

    is_inline = self.is_inline(node)

    if not is_inline:
        pre = ''
        post = ''
        if 'align' in node:
            if node['align'] == 'left':
                pre = '{'
                post = r'\hspace*{\fill}}'
            elif node['align'] == 'right':
                pre = r'{\hspace*{\fill}'
                post = '}'
            elif node['align'] == 'center':
                pre = r'{\hfill'
                post = r'\hspace*{\fill}}'
        self.body.append('\n%s' % pre)

    self.body.append(r'\sphinxincludegraphics[]{%s}' % fname)

    if not is_inline:
        self.body.append('%s\n' % post)

    raise nodes.SkipNode