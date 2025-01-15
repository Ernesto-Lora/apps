import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class example_class:
    def __init__(self, example):
        self.example = example

    def multiply(self):
        self.example *= 2
    def result(self):
        return self.example

    def plot(self):
        self.multiply()
        x = np.linspace(0,10)
        y = self.example*x
        plt.plot(x,y)
        plt.show()
        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convert to base64 for embedding in HTML
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()
        return image_base64
