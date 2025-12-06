from language_learn.heatmap_app.image_canvas import ImageCanvas

def test_image_canvas():
    canvas = ImageCanvas('image',"language_learn/imgs/classroom.jpg")
  

    print("Canvas W:", canvas.W, "H:", canvas.H)

    assert canvas.W > 0 and canvas.H > 0

if __name__ == "__main__":
    test_image_canvas()
