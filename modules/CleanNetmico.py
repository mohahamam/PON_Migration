import re

#@staticmethod

def strip_ansi_escape_codes(string_buffer):

    """

    Remove any ANSI (VT100) ESC codes from the output



    http://en.wikipedia.org/wiki/ANSI_escape_code



    Note: this does not capture ALL possible ANSI Escape Codes only the ones

    I have encountered



    Current codes that are filtered:

    ESC = '\x1b' or chr(27)

    ESC = is the escape character [^ in hex ('\x1b')

    ESC[24;27H   Position cursor

    ESC[?25h     Show the cursor

    ESC[E        Next line (HP does ESC-E)

    ESC[K        Erase line from cursor to the end of line

    ESC[2K       Erase entire line

    ESC[1;24r    Enable scrolling from start to row end

    ESC[?6l      Reset mode screen with options 640 x 200 monochrome (graphics)

    ESC[?7l      Disable line wrapping

    ESC[2J       Code erase display



    HP ProCurve's, Cisco SG300, and F5 LTM's require this (possible others)

    """

    debug = False

    if debug:

        print("In strip_ansi_escape_codes")

        print("repr = %s "% repr(string_buffer))



    code_position_cursor = chr(27)+ r'\[\d+;\d+H'

    code_show_cursor =chr(27)+ r'\[\?25h'

    code_next_line =chr(27)+ r'E'

    code_erase_line_end =chr(27)+ r'\[K'

    code_erase_line =chr(27)+ r'\[2K'

    code_erase_start_line =chr(27)+ r'\[K'

    code_enable_scroll =chr(27)+ r'\[\d+;\d+r'

    code_form_feed =chr(27)+ r'\[1L'

    code_carriage_return =chr(27)+ r'\[1M'

    code_disable_line_wrapping =chr(27)+ r'\[\?7l'

    code_reset_mode_screen_options =chr(27)+ r'\[\?\d+l'

    code_erase_display =chr(27)+ r'\[2J'

    code_erase_nokia =r'\-?'+ chr(27)+ r'\[1D'+ r'[\\\|\/\s]?'

    code_erase_nokia2 =' ' + chr(27)+ r'\[1D'

    code_erase_nokia3 =r'[ ]{2,}' + chr(27)+ r'\[74C'+ chr(27)+ r'\[1A' + r'[\s]?'

    code_erase_nokia4 =r'[ ]{2,}' + chr(27)+ r'\[6D'


    code_set = [code_position_cursor, code_show_cursor, code_erase_line, code_enable_scroll,

                code_erase_start_line, code_form_feed, code_carriage_return,

                code_disable_line_wrapping, code_erase_line_end,

                code_reset_mode_screen_options, code_erase_display,code_erase_nokia,
               
                code_erase_nokia2,code_erase_nokia3, code_erase_nokia4 ]



    output = string_buffer

    for ansi_esc_code in code_set:

        output = re.sub(ansi_esc_code,'', output)



    # CODE_NEXT_LINE must substitute with '\n'

    output = re.sub(code_next_line,'\n', output)



    if debug:

        print("new_output = %s"% output)

        print("repr = %s"% repr(output))



    return output