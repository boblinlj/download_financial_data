
def write_text_file(text_input, output_file):
    f = open(output_file, "w", encoding='utf-8')
    f.write(text_input)
    f.close()
    return None