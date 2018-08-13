from docutils.parsers.rst import Directive
from docutils import nodes
import subprocess
import sys

sys.path.append('/cad/projects/ReUseDB/work/chrbe/timingdrawer/timingdrawer-code-r54-trunk')
import TimingDrawer

################################################################################
# SETUP
################################################################################

def setup(app):
    app.add_node(TimingDrawerNode,
                 html=(visit_timingdrawer_node, depart_timingdrawer_node),
                 latex=(visit_timingdrawer_node, depart_timingdrawer_node),
                 text=(visit_timingdrawer_node, depart_timingdrawer_node))

    app.add_directive('timingdrawer', TimingDrawerDirective)
    app.connect('doctree-resolved', process_timingdrawer_nodes)
    app.connect('env-purge-doc', purge_timingdrawer)

    return {'version': '0.1'}   # identifies the version of our extension

################################################################################
# TimingDrawerNode
################################################################################

class TimingDrawerNode(nodes.Admonition, nodes.Element):
    pass

def visit_timingdrawer_node(self, node):
    self.visit_admonition(node)

def depart_timingdrawer_node(self, node):
    self.depart_admonition(node)

################################################################################
# Directive
################################################################################

class TimingDrawerDirective(Directive):

    # this enables content in the directive
    has_content = True

    def run(self):
        env = self.state.document.settings.env
        serial = env.new_serialno('TimingDrawerNode')
        todo_node = TimingDrawerNode('\n'.join(self.content), ids=[serial])

        return [todo_node]

################################################################################
# Event handlers
################################################################################

def purge_timingdrawer(app, env, docname):
    return

def process_timingdrawer_nodes(app, doctree, fromdocname):
    # Replace all todolist nodes with a list of the collected todos.
    # Augment each todo with a backlink to the original location.
    env = app.builder.env

    import pdb; pdb.set_trace()

    for node in doctree.traverse(TimingDrawerNode):
        # Replace node with empty list unless timing drawer succeeds
        content = []
        # Run TimingDrawer
        ext = 'eps'
        filename = 'timingdrawer-%i.%s' % (node.attributes['ids'][0], ext)
        path = 'build/%s' % filename
        try:
            TimingDrawer.create_timing_diagram(node.rawsource, ext, path)
            content.append(create_figure(node, filename))
        except TimingDrawer.ParseError as e:
            # TODO add cerror message to log
            pass
        node.replace_self(content)

################################################################################
# MISC
################################################################################

def create_figure(node, filename):
    """Create a set of nodes that describe a figure
    """
    # figure = nodes.figure()
    newimage = nodes.image()
    newimage.parent = node.parent
    newimage.source = node.source
    newimage.line = node.line
    newimage.tagname = 'image'
    newimage_attribs = {}
    newimage_attribs['uri'] = filename
    newimage_attribs['ids'] = []
    newimage_attribs['backrefs'] = []
    newimage_attribs['dupnames'] = []
    newimage_attribs['classes'] = []
    newimage_attribs['candidates'] = {'*': filename}
    newimage_attribs['names'] = []
    newimage.attributes = newimage_attribs
    # figure += newimage

    return newimage