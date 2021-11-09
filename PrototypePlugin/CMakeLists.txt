# search for paraview.plugin files in subdir:
#   paraview_plugin_find_plugins(plugin_files "subdir")
# explicitly provide paths to paraview.plugin files:
cmake_minimum_required(VERSION 3.8)
project(PrototypePlugin)

set(plugin_files
  "MyPlugin/paraview.plugin")
paraview_plugin_scan(
  PLUGIN_FILES      ${plugin_files}
  PROVIDES_PLUGINS  plugins
  REQUIRES_MODULES  plugin_required_modules
  ENABLE_BY_DEFAULT ON)
paraview_plugin_build(
  PLUGINS ${plugins}
  TARGET  ParaViewPlugins
  LIBRARY_DESTINATION "${CMAKE_INSTALL_BINDIR}"
  LIBRARY_SUBDIRECTORY "plugins")