import vtk
#Step 1
reader = vtk.vtkSTLReader()
reader.SetFileName("Agnes_000000.asc")
reader.Update()
polydata = reader.GetOutputPort()
number_of_vertices = reader.GetOutput().GetNumberOfPoints()

#Step 2
center = reader.GetOutput().GetCenter()
plane = vtk.vtkPlane()
plane.SetOrigin(center)
plane.SetNormal(1, 0, 1) 

#Step 3
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(reader.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()
clipper.GenerateClippedOutputOn()
clipper.SetValue(0)
clipper.Update()
clipper1 = vtk.vtkClipPolyData()
clipper1.SetInputConnection(reader.GetOutputPort())
clipper1.SetClipFunction(plane)
clipper1.SetValue(0)
clipper1.Update()


#Step 4
cutter = vtk.vtkCutter()
cutter.SetInputConnection(reader.GetOutputPort())
cutter.SetCutFunction(plane)
stripper = vtk.vtkStripper()
stripper.SetInputConnection(cutter.GetOutputPort())
stripper.Update()
triangleFilter = vtk.vtkTriangleFilter()
triangleFilter.SetInputConnection(stripper.GetOutputPort())
triangleFilter.Update()


#Step 5
sample = vtk.vtkSampleFunction()
sample.SetImplicitFunction(plane)
sample.SetModelBounds(reader.GetOutput().GetBounds())
sample.SetSampleDimensions(100, 100, 100)
sample.ComputeNormalsOff()

contour = vtk.vtkContourFilter()
contour.SetInputConnection(sample.GetOutputPort())
contour.GenerateValues(1, 0, 0)

planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(contour.GetOutputPort())
planeMapper.ScalarVisibilityOff()

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.GetProperty().SetColor(1,1,0)


# Visualize the results
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())

vertices1 = mapper.GetInput().GetNumberOfPoints()
print("Number of vertices in clipped part: ", vertices1)

actor1 = vtk.vtkActor()
actor1.SetMapper(mapper)
actor1.GetProperty().SetColor(0,0.9,0.3) # green
actor1.GetProperty().SetInterpolationToGouraud()
actor1.GetProperty().ShadingOn()
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(triangleFilter.GetOutputPort())
vertices1 = mapper2.GetInput().GetNumberOfPoints()
print("Number of vertices in intersection part: ", vertices1)

actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)
actor2.GetProperty().SetColor(1, 0, 0) # red
actor2.GetProperty().SetLineWidth(5)
mapper3 = vtk.vtkPolyDataMapper()
mapper3.SetInputConnection(clipper1.GetOutputPort())
vertices1 = mapper3.GetInput().GetNumberOfPoints()
print("Number of vertices in remaining part: ", vertices1)

actor3 = vtk.vtkActor()
actor3.SetMapper(mapper3)
actor3.GetProperty().SetColor(0, 0.4, 0.9) # blue
actor3.GetProperty().SetRepresentationToWireframe()
actor3.GetProperty().SetInterpolationToFlat()


# Create four view ports
viewport2 = [0.0, 0.0, 0.5, 0.5]
viewport1 = [0.5, 0.0, 1.0, 0.5]
viewport3 = [0.0, 0.5, 0.5, 1.0]
viewport4 = [0.5, 0.5, 1.0, 1.0]
renderer1 = vtk.vtkRenderer()
renderer1.AddActor(actor1)
renderer2 = vtk.vtkRenderer()
renderer2.AddActor(actor2)
renderer3 = vtk.vtkRenderer()
renderer3.AddActor(actor3)
renderer4 = vtk.vtkRenderer()
renderer4.AddActor(planeActor)
renderer4.AddActor(actor3)
renderer4.AddActor(actor1)



# Add light
lightkit = vtk.vtkLightKit()
lightkit.AddLightsToRenderer(renderer1)
lightkit.AddLightsToRenderer(renderer2)
lightkit.AddLightsToRenderer(renderer3)
lightkit.AddLightsToRenderer(renderer4)


window = vtk.vtkRenderWindow()
window.SetSize(900, 900)
window.AddRenderer(renderer1)
window.AddRenderer(renderer2)
window.AddRenderer(renderer3)
window.AddRenderer(renderer4)

renderer1.SetViewport(viewport1)
window.Render()
renderer2.SetViewport(viewport2)
window.Render()
renderer3.SetViewport(viewport3)
window.Render()
renderer4.SetViewport(viewport4)
window.Render()
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
window.Render()
interactor.Start()
