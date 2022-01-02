set(classes
  vtkMyStreamTracerFilter)
# Find external packages here using `find_package`.
vtk_module_add_module(StreamTracerFilters
  CLASSES ${classes})
# Link to external packages here using `vtk_module_link(StreamTracerFilters)`.
paraview_add_server_manager_xmls(
  XMLS  MyStreamTracerFilter.xml)