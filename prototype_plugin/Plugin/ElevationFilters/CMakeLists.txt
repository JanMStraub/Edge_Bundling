set(classes
  vtkMyElevationFilter)
# Find external packages here using `find_package`.
vtk_module_add_module(ElevationFilters
  CLASSES ${classes})
# Link to external packages here using `vtk_module_link(ElevationFilters)`.
paraview_add_server_manager_xmls(
  XMLS  MyElevationFilter.xml)