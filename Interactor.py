#!/usr/bin/env python
from vtk import vtkInteractorStyleUser


class MouseAndKeysInteractor(vtkInteractorStyleUser):
    """vtkInteractorStyleUser subclass to control user interaction with the graph view."""

    def __init__(self, ActiveView):
        """Constructor

        @type active_view: GraphLayoutView
        @param active_view: GraphLayoutView of the graph with which the user is interacting.
        """
        self.AddObserver('KeyPressEvent', self.on_key_down)
        self.SetAutoAdjustCameraClippingRange(1)
        self._active_view = ActiveView
        self._camera = ActiveView.GetRenderer().GetActiveCamera()
        self._transform = self._camera.GetViewTransformObject()
        self._transform.PostMultiply()
        self._angle = 0.6
        self._minus_angle = -0.6
        self._translate_z_list = [0, 0, 5]
        self._minus_translate_z_list = [0, 0, -5]
        self._translate_x_list = [5, 0, 0]
        self._minus_translate_x_list = [-5, 0, 0]
        self._zoom_in_factor = 1.05
        self._zoom_out_factor = 0.95

    def on_key_down(self, arg1, arg2):
        """Callback when a key is pressed

        @type arg1: self
        @param arg1: The callback passes self and keypress as params. They are ignored.
        @type arg2: str
        @param arg2: The callback passes self and keypress as params. They are ignored.
        """

        key = self.GetKeySym()

        if self.GetCtrlKey():
            if key == 'Up':
                self._rotate_x(self._minus_angle)
            if key == 'Down':
                self._rotate_x(self._angle)
            if key == 'Left':
                self._rotate_y(self._minus_angle)
            if key == 'Right':
                self._rotate_y(self._angle)

        elif self.GetShiftKey():
            if key == 'Up':
                self._zoom(self._zoom_in_factor)
            if key == 'Down':
                self._zoom(self._zoom_out_factor)

        else:
            if key == 'Up':
                self._translate(self._translate_z_list)
            if key == 'Down':
                self._translate(self._minus_translate_z_list)
            if key == 'Left':
                self._translate(self._translate_x_list)
            if key == 'Right':
                self._translate(self._minus_translate_x_list)

    def _zoom(self, float_zoom_factor):
        """zooms the camera in.

        @type float_zoom_factor: float
        @param float_zoom_factor: ratio by which to zoom.
        """
        self._camera.Zoom(float_zoom_factor)
        self._active_view.Render()

    def _dolly(self, float_dolly_factor):
        """dolly the camera forward and backward

        unused. Probably won't be.

        @type float_dolly_factor: float
        @param float_dolly_factor: proportion to dolly per step
        """
        self._camera.Dolly(float_dolly_factor)
        self._active_view.Render()

    def _translate(self, xyz_list):
        """Translate the camera

        @type xyz_list: list
        @param xyz_list: list of x, y, and z values for translation.
        """
        self._transform.Translate(xyz_list)
        self._active_view.Render()

    def _rotate_x(self, angle):
        """rotates up and down as nodding one's head.

        @type angle: float
        @param angle: angle in degrees to rotate
        """
        self._transform.RotateX(angle)
        self._active_view.Render()

    def _rotate_y(self, angle):
        """rotates about y-axis, as shaking one's head.

        @type angle: float
        @param angle: angle in degrees to rotate
        """
        self._transform.RotateY(angle)
        self._active_view.Render()
