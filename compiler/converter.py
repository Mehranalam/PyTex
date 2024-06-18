from PIL import Image, ImageDraw, ImageFont
from parser import Token

class Renderer:
    def __init__(self, font_path='vazirmatn.ttf', font_size=20):
        self.font = ImageFont.truetype(font_path, font_size)
        self.image = Image.new('RGB', (800, 200), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def render(self, node, x=10, y=10):
        if node.type == 'NUMBER' or node.type == 'IDENT':
            self.draw.text((x, y), node.value, font=self.font, fill='black')
            return x + self.font.getsize(node.value)[0], y
        elif node.type == 'OP':
            left_x, left_y = self.render(node.children[0], x, y)
            op_x = left_x + self.font.getsize(' ')[0]
            self.draw.text((op_x, y), node.value, font=self.font, fill='black')
            right_x, right_y = self.render(node.children[1], op_x + self.font.getsize(node.value)[0] + self.font.getsize(' ')[0], y)
            return right_x, y
        elif node.type == 'FRAC':
            numerator_x, numerator_y = self.render(node.children[0], x, y)
            denominator_x, denominator_y = self.render(node.children[1], x, y + self.font.getsize(' ')[1] * 2)
            max_width = max(numerator_x - x, denominator_x - x)
            self.draw.line((x, y + self.font.getsize(' ')[1], x + max_width, y + self.font.getsize(' ')[1]), fill='black')
            return x + max_width, y + self.font.getsize(' ')[1] * 3
        elif node.type == 'SUP':
            base_x, base_y = self.render(node.children[0], x, y)
            exponent_x, exponent_y = self.render(node.children[1], base_x, y - self.font.getsize(' ')[1] // 2)
            return exponent_x, y
        elif node.type == 'NEG':
            self.draw.text((x, y), '-', font=self.font, fill='black')
            return self.render(node.children[0], x + self.font.getsize('-')[0], y)
        else:
            raise ValueError(f'Unknown node type: {node.type}')

    def show(self):
        self.image.show()

renderer = Renderer()
renderer.render(ast)
renderer.show()