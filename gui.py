from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line, Translate
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window

obstacles = []
positions = []
minX = -400
maxX = 400
minY = -400
maxY = 400
scaleX = Window.width*1.0/(maxX-minX)
scaleY = Window.height*1.0/(maxY-minY)
i = 0

class MyWidget(Widget):
    def points_tuple_to_scaled_array(self, points, scaleX, scaleY):
        points_array = []
        for point in points:
            points_array.append(point[0]*scaleX)
            points_array.append(point[1]*scaleY)
        return points_array

    def my_callback(self, dt):
        with self.canvas:
            Color(0, 1, 0)
            global i
            if i < len(positions):
                print 'Showing next configuration..'
                Line(points=self.points_tuple_to_scaled_array(positions[i], scaleX, scaleY), width=1)
                i = i+1
            # for position in positions:
            #     # print position

            # self.line.points = [100, 100, 200, 100, 100, 200]
            # self.line.width = 5
            # Line(points=[100, 100, 200, 100, 100, 200], width=10)
        pass

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        with self.canvas:
            self.translate = Translate(Window.width / 2, Window.height / 2.)
            # self.line = Line(points=[100, 100, 200, 100, 100, 200], width=1)
            for obstacle in obstacles:
                # print 'Placing on GUI..'
                Line(points=self.points_tuple_to_scaled_array(obstacle, scaleX, scaleY),width=1)
            Color(1, 0, 0)
            Ellipse(pos=(0,0), size=(3,3))
            Clock.schedule_interval(partial(self.my_callback), .1)
            pass
            # add your instruction for main canvas here

        with self.canvas.before:
            pass
            # you can use this to add instructions rendered before

        with self.canvas.after:
            pass
            # you can use this to add instructions rendered after

class MotionPlanningApp(App):
    def build(self):
        root = GridLayout(cols=1, padding=5, spacing=1)
        root.add_widget(MyWidget())
        return root

if __name__ == '__main__':
    MotionPlanningApp().run()
