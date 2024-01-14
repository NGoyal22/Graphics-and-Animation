import vtk
from stl import mesh
import numpy as np

# Find number of vertices
a = mesh.Mesh.from_file('Low_Poly_Skull.stl')
points = np.around(np.unique(a.vectors.reshape([int(a.vectors.size/3), 3]), axis=0),2)
print(len(points))

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("Low_Poly_Skull.stl")
reader.Update()

# Compute normals
teanormals = vtk.vtkPolyDataNormals()
teanormals.SetInputConnection(reader.GetOutputPort())

# Set actor and mapper
mapper = [vtk.vtkPolyDataMapper() for i in range(4)]
actor = [vtk.vtkActor() for i in range(4)]
for i in range(4):
    mapper[i].SetInputConnection(teanormals.GetOutputPort())
    actor[i].SetMapper(mapper[i])

    # Set actor properties
    prop = actor[i].GetProperty()
    prop.SetAmbient(0.2)
    prop.SetDiffuse(0.3)
    prop.SetSpecular(0.8)
    prop.SetSpecularPower(40.0)
    if i == 0:
        prop.SetRepresentationToWireframe()
    if i == 1:
        prop.SetInterpolationToFlat()
    if i == 2:
        prop.SetInterpolationToGouraud()
    if i == 3:
        prop.SetInterpolationToPhong()
    prop.ShadingOn()

# Set render window
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1600, 1600)

# Set renderer
ren = [vtk.vtkRenderer() for i in range(4)]

# Set viewport dimensions
xmins = [0, 0.5, 0, 0.5]
xmaxs = [0.5, 1, 0.5, 1]
ymins = [0.5, 0.5, 0, 0]
ymaxs = [1, 1, 0.5, 0.5]

for i in range(4):
    ren[i].AddActor(actor[i])

    # Add light
    lightkit = vtk.vtkLightKit()
    lightkit.AddLightsToRenderer(ren[i])

    ren[i].SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])
    renWin.AddRenderer(ren[i])

# Set interactor, render loop
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.Render()
iren.Start()

# Save render window to jpeg file
writer = vtk.vtkJPEGWriter()
filter = vtk.vtkWindowToImageFilter()
filter.SetInput(renWin)
filter.ReadFrontBufferOff()
filter.Update()


writer.SetFileName("output.jpeg")
writer.SetInputConnection(filter.GetOutputPort())
writer.Write()
