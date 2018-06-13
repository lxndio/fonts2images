# fonts2images version 0.1 from 2018-06-13
# Written by lxndio
#
# Licensed under the GNU General Public License v3.0

from PIL import Image, ImageDraw, ImageFont
import string
import os
import argparse

# Handle command line arguments
parser = argparse.ArgumentParser(description="Generate images for all font files in this directory and all subdirectories.")

parser.add_argument('-v', '--verbose', action='store_true', help='print out what the program is doing')
parser.add_argument('-r', '--renew', action='store_true', help='renew all files, no matter if they already exist')
parser.add_argument('-m', '--markdown', action='store_true', help='generate README.md files after generating images')

args = parser.parse_args()

errors = 0

# Iterate through all files in this directory and all subdirectories
for subdir, dirs, files in os.walk(os.getcwd()):
	for file in files:
		# Generate image if current file is a font file
		if file.endswith('.otf') or file.endswith('.ttf'):
			# Skip this file if there is already an image for it (or do it anyway if renew mode is activated)
			if (args.renew) or (not os.path.isfile(os.path.join(subdir, file + '.png'))):
				# Print out file name if verbose mode is activated
				if args.verbose:
					print("Generating image for file \"{}\".".format(file))

				# Generate new image
				im = Image.new("RGB", (2000, 500), "white")
				draw = ImageDraw.Draw(im)

				# Load font
				fontFile = file

				try:
					font = ImageFont.truetype(os.path.join(subdir, fontFile), size=100)
				except IOError:
					print("ERROR: Failed to load font \"{}\".".format(fontFile))
					errors += 1
					continue

				# Draw text on the image
				draw.text((50, 50), string.ascii_uppercase, font=font, fill="#000000")
				draw.text((50, 300), string.ascii_lowercase, font=font, fill="#000000")

				# Save image
				# im.save(os.path.splitext(fontFile)[0] + ".png", "PNG")
				im.save(os.path.join(subdir, fontFile + ".png"), "PNG")

	# Generate README.md file if markdown mode is activated
	if args.markdown:
		# Only generate README.md file if there are image files in the current folder
		imageFiles = False
		for file in files:
			if file.endswith('.png'):
				imageFiles = True
				break

		if imageFiles:
			# Print out current folder if verbose mode is activated
			print("Generating README.md file for folder \"{}\".".format(subdir))

			with open(os.path.join(subdir, 'README.md'), 'w') as mdFile:
				mdFile.write("# Images of fonts in the folder: {}\n\n".format(os.path.basename(os.path.normpath(subdir))))
				for file in files:
					if file.endswith('.png'):
						mdFile.write("## {}\n\n".format(os.path.splitext(file)[0]))
						mdFile.write("![Image of font: {}]({})\n\n".format(os.path.splitext(file)[0], file))

				mdFile.write("*Generated for the [Scosh/fonts](https://github.com/Scosh/fonts) repository on GitHub using the font image generator by [lxndio](https://github.com/lxndio/).*")

print("\nExecution completed. {} errors ocurred.".format(errors))