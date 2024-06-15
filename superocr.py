from subprocess import Popen, run, PIPE

stdout = run(["osascript", "-e", "get the clipboard as «class PNGf»"], stdout=PIPE).stdout
# print(p)
# exit()
# stdout, stderr = p.communicate()
png_bytes = bytes.fromhex(stdout.decode('utf-8').strip()[10:-1])

convert_command = ['convert', 'png:-', '-colorspace', 'HSL', '-channel', 'Lightness', '-separate', '-format', '%[fx:mean*100]', 'info:']

average_lightness = run(convert_command, input=png_bytes, stdout=PIPE, stderr=PIPE).stdout.decode('utf-8').strip()

p = run(["convert", "png:-","ppm:-"], input=png_bytes, stdout=PIPE, stderr=PIPE)
ppm_data = p.stdout

p = run([ 'tesseract', 'stdin', 'stdout', '--psm', '4', '-l', 'eng' ], input=ppm_data, stdout=PIPE, stderr=PIPE)

extracted_text = p.stdout.decode('utf-8').strip()

result = '\n'.join(line for line in extracted_text.split('\n') if any(char.isalnum() for char in line))


# Print results
print(f"Average Lightness: {average_lightness}")
print(f"Extracted Text: {result}")
