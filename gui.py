from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line, Translate
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Fbo, ClearColor, ClearBuffers, Scale
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

obstacles = []
positions = []
goal_positions = []
minX = -500
maxX = 500
minY = -500
maxY = 500
scaleX = Window.width*1.0/(maxX-minX)
scaleY = Window.height*1.0/(maxY-minY)
i = 0
noPathFlag=False

class MyWidget(Widget):
    def export_to_png(self, filename, *args):
        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save(filename, flipped=False)
        fbo.remove(self.canvas)

        if self.parent is not None:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        return True

    def points_tuple_to_scaled_array(self, points, scaleX, scaleY):
        points_array = []
        for point in points:
            points_array.append(point[0]*scaleX)
            points_array.append(point[1]*scaleY)
        return points_array

    def my_callback(self, dt):
        global i
        if i < len(positions)+10:
            self.export_to_png('filename'+str(i)+'.png')
        with self.canvas:
            global i
            if noPathFlag == True and i==len(positions):
                Color(0,0,1)
                Label(text='No Further Path!!')
            if i < len(positions):
                print 'Showing next configuration..'
                self.line.points = self.points_tuple_to_scaled_array(positions[i], scaleX, scaleY)
            if i == len(positions)+5:
                self.line.points = []
                for position in positions:
                    Line(points=self.points_tuple_to_scaled_array(position, scaleX, scaleY), width=1.1)
            i = i+1

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        with self.canvas:
            self.translate = Translate(Window.width / 2, Window.height / 2.)
            for obstacle in obstacles:
                Line(points=self.points_tuple_to_scaled_array(obstacle, scaleX, scaleY),width=1.1)
            Color(1, 0, 0)
            for goal_position in goal_positions:
                Line(points=self.points_tuple_to_scaled_array(goal_position, scaleX, scaleY), width=1.1)
            Color(1, 0, 0)
            Ellipse(pos=(0,0), size=(3,3))
            Color(0, 1, 0)
            self.line = Line(points=self.points_tuple_to_scaled_array(goal_positions[0], scaleX, scaleY), width=1.1)
            Clock.schedule_interval(partial(self.my_callback), .5)

        with self.canvas.before:
            pass

        with self.canvas.after:
            pass

class MotionPlanningApp(App):
    def build(self):
        root = GridLayout(cols=1, padding=5, spacing=1)
        root.add_widget(MyWidget())
        return root

if __name__ == '__main__':
    MotionPlanningApp().run()
