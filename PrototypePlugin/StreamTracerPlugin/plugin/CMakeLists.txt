paraview_add_plugin(StreamTracerFilter
  VERSION "1.0"
  MODULES VTK::StreamTracerFilters
  SERVER_MANAGER_XML "${CMAKE_CURRENT_SOURCE_DIR}/plugin/StreamTracerFilters/MyStreamTracerFilter.xml")
