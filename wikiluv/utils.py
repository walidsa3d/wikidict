import textwrap
import hyphen
import shutil

def justify(text, width=None):
    if width is None:
        width = shutil.get_terminal_size().columns

    # Initialize the hyphenator
    h = hyphen.Hyphenator('en_US')
    
    # Split the text into words
    words = text.split()
    
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                # Justify the current line
                spaces_needed = width - current_length
                gaps = len(current_line) - 1
                if gaps > 0:
                    space_per_gap = spaces_needed // gaps
                    extra_spaces = spaces_needed % gaps
                    justified_line = ''
                    for i, w in enumerate(current_line):
                        justified_line += w
                        if i < gaps:
                            justified_line += ' ' * (space_per_gap + (1 if i < extra_spaces else 0))
                    lines.append(justified_line)
                else:
                    lines.append(current_line[0].ljust(width))
            
            # Start a new line
            current_line = [word]
            current_length = len(word)
        
        # Check if hyphenation is needed
        while current_length > width:
            hyphenated = h.wrap(current_line[-1], width - current_length + len(current_line[-1]))
            if len(hyphenated) > 1:
                current_line[-1] = hyphenated[0] + '-'
                lines.append(' '.join(current_line).ljust(width))
                current_line = [hyphenated[1]]
                current_length = len(hyphenated[1])
            else:
                break
    
    # Add the last line without justification
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

