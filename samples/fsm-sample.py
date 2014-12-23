# -*- coding: UTF-8 -*-
__author__ = 'yangtianhang'

from pyttern.fsm import stateful, behavior

codes = '''
public class Comment {
    // "this is a comment"

    /*
      "this is a comment"
     */

    /*
      // this is a comment
      'in comment'
      "in comment"
     **/

    /*
      // this is a comment
    **/

    void comment() {
        String s0 = "this is not a comment";
        String s1 = "// this is not a comment";
        String s2 = "/* this is not a comment */";
        String s3 = "/* this is not a comment */";
        String s4 = "'";
        String s5 = "\\"";

        char c0 = '/';
        char c1 = '"';
        char c2 = '\\'';
    }
}
'''

state_normal = 0
state_slash = 1
state_line_comment = 2
state_block_comment = 3
state_block_comment_star = 4
state_double_quotation = 5
state_double_quotation_backslash = 6
state_single_quotation = 7
state_single_quotation_backslash = 8


@stateful(init_state=state_normal)
class RemoveComment(object):
    def __init__(self):
        self.codes = ''

    @behavior(state=state_normal, event='/')
    def first_slash(self):
        self.switch(state_slash)

    @behavior(state=state_slash, event='/')
    def line_comment(self):
        self.switch(state_line_comment)

    @behavior(state=state_line_comment, event='\n')
    def complete_line_comment(self):
        self.codes += '\n'
        self.switch(state_normal)

    @behavior(state=state_line_comment, event=None)
    def in_line_comment(self):
        pass

    @behavior(state=state_slash, event='*')
    def block_comment(self):
        self.switch(state_block_comment)

    @behavior(state=state_block_comment, event='*')
    def block_comment_star(self):
        self.switch(state_block_comment_star)

    @behavior(state=state_block_comment_star, event='*')
    def block_comment_star_after_star(self):
        self.switch(state_block_comment_star)

    @behavior(state=state_block_comment_star, event='/')
    def complete_block_comment(self):
        self.switch(state_normal)

    @behavior(state=state_block_comment_star, event=None)
    def in_block_comment_star(self):
        self.switch(state_block_comment)

    @behavior(state=state_block_comment, event=None)
    def in_block_comment(self):
        pass

    @behavior(state=state_normal, event='"')
    def double_quotation(self):
        self.codes += self.event()
        self.switch(state_double_quotation)

    @behavior(state=state_double_quotation, event='\\')
    def double_quotation_slash(self):
        self.codes += self.event()
        self.switch(state_double_quotation_backslash)

    @behavior(state=state_double_quotation_backslash, event=None)
    def in_double_quotation_slash(self):
        self.codes += self.event()
        self.switch(state_double_quotation)

    @behavior(state=state_double_quotation, event='"')
    def complete_double_quotation(self):
        self.codes += self.event()
        self.switch(state_normal)

    @behavior(state=state_double_quotation, event=None)
    def in_double_quotation(self):
        self.codes += self.event()

    @behavior(state=state_normal, event="'")
    def single_quotation(self):
        self.codes += self.event()
        self.switch(state_single_quotation)

    @behavior(state=state_single_quotation, event='\\')
    def single_quotation_slash(self):
        self.codes += self.event()
        self.switch(state_single_quotation_backslash)

    @behavior(state=state_single_quotation_backslash, event=None)
    def in_single_quotation_slash(self):
        self.codes += self.event()
        self.switch(state_single_quotation)

    @behavior(state=state_single_quotation, event="'")
    def complete_single_quotation(self):
        self.codes += self.event()
        self.switch(state_normal)

    @behavior(state=state_single_quotation, event=None)
    def in_single_quotation(self):
        self.codes += self.event()

    @behavior(state=state_normal, event=None)
    def default(self):
        self.codes += self.event()
        self.switch(state_normal)

    def print_codes(self):
        print self.codes


rm_comment = RemoveComment()

try:
    for c in codes:
        rm_comment.handle(c)
finally:
    rm_comment.print_codes()
