paraview_add_plugin(StreamTracerFilter
  VERSION "1.0"
  MODULES StreamTracerFilters
  MODULE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/StreamTracerFilters/vtk.module")