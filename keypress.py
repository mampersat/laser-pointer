#From https://stackoverflow.com/a/6599441/149506
import termios, fcntl, sys, os

def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns a tuple of characters of the key that was pressed - on Linux, 
    pressing keys like up arrow results in a sequence of characters. Returns 
    ('\x03',) on KeyboardInterrupt which can happen when a signal gets
    handled.

    """
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        ret.append('\x03')
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return tuple(ret)

# Recursive function to accumulate known control sequences and
# treat them as one character.
def accumulate_sequence(keys, sequence):
    if len(keys) == 0:
        return keys, sequence

    c = keys[0]
    if c == '\x1b' and sequence == '':
        sequence = c
        return accumulate_sequence(keys[1:], sequence)
    if c == '[' and sequence == '\x1b':
        sequence += c
        return accumulate_sequence(keys[1:], sequence)
    if sequence == '\x1b[':
        sequence += c
        return accumulate_sequence(keys[1:], sequence)
    if c == '~' and sequence in ['\x1b[5', '\x1b[6']:
        # page up / page down
        sequence += c    
        return accumulate_sequence(keys[1:], sequence)

    # non control character - get out.
    if sequence == '':
        return keys[1:], keys[0]
    # We've built up a control sequence, and this character isn't part of it
    # Let it get processed next time.
    return keys, sequence


# read_single_keypress will "stack" keys that are held down.
# however, some keys (e.g. arrow keys) show up as multiple characters.
# This filter function will obliterate characters that are the same, and
# combine different characters into one string. The resulting return tuple
# is appropriate for looking for multi-character strings that represent
# e.g. arrow keys and for not repeating commands that were buffered
# from a key being held down.
# In applications where a lot of processing is going on while the user
# could be pressing keys, this will return a tuple with multiple entries.
# Repeates can be filtered by filter_repeats. Note if you want to "ignore
# all key presses while I was busy", you should just look at the last
# element in the resulting tuple.
def filter_keys(keys, filter_repeats=False):
    last_char = ''
    keys, last_char = accumulate_sequence(keys, last_char)

    result = [last_char]

    while len(keys) > 0:
        this_char = ''
        keys, this_char = accumulate_sequence(keys, this_char)
        
        if filter_repeats:
            if this_char == last_char: 
                continue
        last_char = this_char
        result.append(last_char)

    return tuple(result)


# If we're busy doing something, read_single_keypress won't be able to "absorb"
# characters; instead, they'll show up in the terminal. This is because it restores
# terminal flags to whatever they were set to before the call. So we kill echo here,
# and restore it ourselves by surrounding main() in a try block and calling this again
# before any possible exit point.
# See https://docs.python.org/3/library/termios.html
def echo_off():
    fd = sys.stdin.fileno()
    attr = termios.tcgetattr(fd)
    attr[3] = attr[3] & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, attr)

def echo_on():
    fd = sys.stdin.fileno()
    attr = termios.tcgetattr(fd)
    attr[3] = attr[3] | termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, attr)


# Example of usage
if __name__ == '__main__':
    import time
    try:
        # Wrap your entire program in a try block so you can always turn echo
        # back on.
        echo_off()
        print('Press q to quit. Otherwise, try pressing and holding down keys.')
        quit = False
        while True:
            keys = filter_keys(read_single_keypress(), filter_repeats=True)
            keys_pressed = []
            for key in keys:
                if key.upper() == 'Q':
                    quit = True
                    break
                # need repr so things like arrow keys don't actually behave like arrow keys.
                keys_pressed.append(repr(key)) 
            if quit: break
            print(f'Keys pressed: {", ".join(keys_pressed)}')
            time.sleep(1)
    finally:
        echo_on()