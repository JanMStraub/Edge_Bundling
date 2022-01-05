set(classes vtkMyTracerFilter)
# Find external packages here using `find_package`.
vtk_module_add_module(TracerFilters
  CLASSES ${classes})
# Link to external packages here using `vtk_module_link(TracerFilters)`.
paraview_add_server_manager_xmls(
  XMLS  MyTracerFilter.xml)