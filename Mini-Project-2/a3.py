import vtk

# read a DICOM dataset using vtkDICOMImageReader
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("CT")
reader.Update()

# get image data
image_data = reader.GetOutput()
dims = image_data.GetDimensions()
spacing = image_data.GetSpacing()

# get minimum and maximum pixel intensities
scalar_range = image_data.GetScalarRange()
minimum_intensity = scalar_range[0]
maximum_intensity = scalar_range[1]

# print information
print("Dimensions:", dims)
print("Voxel resolution:", spacing)
print("Minimum pixel intensity:", minimum_intensity)
print("Maximum pixel intensity:", maximum_intensity)

# create a vtkColorTransferFunction and vtkPiecewiseFunction for volume rendering

color_tf = vtk.vtkColorTransferFunction()
color_tf.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(255, 1.0, 1.0, 1.0)

opacity_tf = vtk.vtkPiecewiseFunction()
opacity_tf.AddPoint(0, 0.0)
opacity_tf.AddPoint(255, 1.0)


# create 3 viewports, and render the dataset in viewport 1 with volume rendering
ren = vtk.vtkRenderer()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(1200, 400)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

# create 3 viewports
viewport1 = [0, 0, 0.33, 1.0]
viewport2 = [0.33, 0, 0.66, 1.0]
viewport3 = [0.66, 0, 1.0, 1.0]

# viewport 1 - volume rendering
vol_mapper = vtk.vtkSmartVolumeMapper()
vol_mapper.SetInputConnection(reader.GetOutputPort())
vol_mapper.SetBlendModeToComposite()
vol_mapper.SetRequestedRenderModeToGPU()

vol_property = vtk.vtkVolumeProperty()
vol_property.SetColor(color_tf)
vol_property.SetScalarOpacity(opacity_tf)
vol_property.ShadeOff()

volume = vtk.vtkVolume()
volume.SetMapper(vol_mapper)
volume.SetProperty(vol_property)

ren.SetViewport(viewport1)
ren.AddVolume(volume)

# viewport 2 - iso-surface
iso_value = 200

# create an iso-surface using the marching cubes algorithm
iso_mapper = vtk.vtkMarchingCubes()
iso_mapper.SetInputConnection(reader.GetOutputPort())
iso_mapper.SetValue(0, iso_value)
iso_mapper.ComputeNormalsOn()

iso_mapper.Update()

iso_mapper_output = iso_mapper.GetOutput()

iso_mapper_mapper = vtk.vtkPolyDataMapper()
iso_mapper_mapper.SetInputData(iso_mapper_output)

iso_actor = vtk.vtkActor()
iso_actor.SetMapper(iso_mapper_mapper)
iso_actor.GetProperty().SetColor(1, 0, 0)

ren2 = vtk.vtkRenderer()
ren2.SetViewport(viewport2)
ren2.AddActor(iso_actor)
ren_win.AddRenderer(ren2)

# viewport 3 - volume rendering and iso-surface
ren3 = vtk.vtkRenderer()
ren3.SetViewport(viewport3)
ren3.AddVolume(volume)
ren3.AddActor(iso_actor)
ren_win.AddRenderer(ren3)

camera = ren.GetActiveCamera()
bounds = iso_actor.GetBounds() # get the bounds of the actor
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2] # compute the center of the actor
distance = 2 * max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4]) # compute the distance to the actor
camera.SetFocalPoint(center[0], center[1], center[2])
camera.SetPosition(center[0], center[1], center[2]+distance)
camera.SetViewUp(0, 1, 0)
camera.SetClippingRange(distance/100, distance*100) # adjust the clipping range based on the distance
ren2.SetActiveCamera(camera)
ren3.SetActiveCamera(camera)

# start the rendering loop
iren.Initialize()
ren_win.Render()
iren.Start()
