cmake_minimum_required(VERSION 3.22)
project(StreamTracerFilter)

find_package(ParaView REQUIRED)

option(BUILD_SHARED_LIBS "Build shared libraries" ON)

set("_paraview_plugin_default_${CMAKE_PROJECT_NAME}" ON)
paraview_plugin_scan(
  PLUGIN_FILES      "${CMAKE_CURRENT_SOURCE_DIR}/plugin/paraview.plugin"
  PROVIDES_PLUGINS  plugins
  REQUIRES_MODULES  required_modules)

paraview_plugin_build(
  RUNTIME_DESTINATION "${CMAKE_INSTALL_BINDIR}"
  LIBRARY_DESTINATION "${CMAKE_INSTALL_LIBDIR}"
  LIBRARY_SUBDIRECTORY "${PARAVIEW_PLUGIN_SUBDIR}"
  PLUGINS ${plugins})
