cmake_minimum_required(VERSION 3.8)
project(TracerFilter)

include(GNUInstallDirs)

set(BUILD_SHARED_LIBS ON)

find_package(ParaView REQUIRED)

paraview_plugin_scan (
  PLUGIN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/plugin/paraview.plugin"
  PROVIDES_PLUGINS plugins
  ENABLE_BY_DEFAULT ON)

paraview_plugin_build (
  PLUGINS ${plugins})