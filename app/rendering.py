import matplotlib.pyplot as plt
from PIL import Image
import io

def render_math_formula(formula: str, filename: str, dpi: int = 300):
    """
    Renders a mathematical formula into an image file.

    :param formula: The mathematical formula to render.
    :param filename: The output image file name.
    :param dpi: The resolution of the output image.
    """
    fig, ax = plt.subplots()

    ax.axis('off')

    ax.text(0.5, 0.5, f'${formula}$', horizontalalignment='center', verticalalignment='center', fontsize=20)
    ax.text(0.5, 0.1, f'PyTex - V0.0.1', horizontalalignment='center', verticalalignment='bottom', fontsize=20)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)

    img = Image.open(buf)
    img.save(filename)

    buf.close()

    plt.close(fig)

if __name__ == "__main__":
    formula = r'\int_{0}^{\infty} e^{-x^2} dx'
    output_file = "formula.png"
    render_math_formula(formula, output_file)
    print(f"PyTex : Saved rendered formula to {output_file}")