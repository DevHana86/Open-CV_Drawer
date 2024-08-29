import inkex
import subprocess

class BitmapToSVG(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--input", type=str, help="Input PNG file")
        pars.add_argument("--output-file", type=str, help="Output SVG file")

    def effect(self):
        input_file = self.options.input
        output_file = self.options.output_file

        subprocess.run([
            'inkscape',
            input_file,
            '--export-filename=' + output_file,
            '--export-plain-svg'
        ])

        inkex.utils.debug(f"SVG 파일이 생성되었습니다: {output_file}")

if __name__ == '__main__':
    BitmapToSVG().run()