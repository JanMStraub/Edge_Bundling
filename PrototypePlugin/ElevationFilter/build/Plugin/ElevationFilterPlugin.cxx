#include "ElevationFilterPlugin.h"

#include "vtkObjectFactory.h"
#include "vtkPVPluginLoader.h"

#define _paraview_add_plugin_EULA 0
#define _paraview_add_plugin_SERVER_MANAGER_XML 0
#define _paraview_add_plugin_MODULES 1
#define _paraview_add_plugin_UI_INTERFACES 0
#define _paraview_add_plugin_with_resources 0

#if !_paraview_add_plugin_built_shared && _paraview_add_plugin_with_resources
// For Q_INIT_RESOURCE
#include <QtCore/QtGlobal>
#endif

#if _paraview_add_plugin_EULA
#include ""
#endif

#include "ElevationFilter_qch.h"

namespace
{
  // This ensures that when the shared library for this plugin is
  // unloaded during finalization sequence, it notifies the vtkPVPluginLoader
  // so it does not double-dlclose() an already unloaded plugin.
  // This does not affect static builds and hence we don't need to worry about
  // making sure this instance gets created in static builds.
  class ElevationFilterPluginCleaner
  {
  public:
    ElevationFilterPluginCleaner() = default;
    ~ElevationFilterPluginCleaner()
    {
      // The plugin library is being unloaded.
      // Let the plugin loader know so it doesn't try to unload it again.
      vtkPVPluginLoader::PluginLibraryUnloaded("ElevationFilter");
    }
  } ElevationFilterPluginCleaner_Instance;
}

//-----------------------------------------------------------------------------
#if _paraview_add_plugin_SERVER_MANAGER_XML
#include "ElevationFilter_server_manager.h"
#endif

#if _paraview_add_plugin_MODULES
#include "ElevationFilter_server_manager_modules.h"
#include "ElevationFilter_client_server.h"
#endif

//-----------------------------------------------------------------------------
void ElevationFilterPlugin::GetBinaryResources(
  std::vector<std::string>& resources)
{
  {
    const char *text = ElevationFilter_qch();
    resources.emplace_back(text);
    delete [] text;
  }

  (void)resources;
}

//-----------------------------------------------------------------------------
#if _paraview_add_plugin_with_ui


#endif

//-----------------------------------------------------------------------------
#if _paraview_add_plugin_with_xml
vtkClientServerInterpreterInitializer::InterpreterInitializationCallback
ElevationFilterPlugin::GetInitializeInterpreterCallback()
{
#if _paraview_add_plugin_MODULES
  return ElevationFilter_client_server_initialize;
#else
  return nullptr;
#endif
}

//-----------------------------------------------------------------------------
void ElevationFilterPlugin::GetXMLs(std::vector<std::string> &xmls)
{
  (void)xmls;
#if _paraview_add_plugin_SERVER_MANAGER_XML
  ElevationFilter_server_manager_initialize(xmls);
#endif
#if _paraview_add_plugin_MODULES
  ElevationFilter_server_manager_modules_initialize(xmls);
#endif
}
#endif

//-----------------------------------------------------------------------------
#if _paraview_add_plugin_with_ui
QObjectList ElevationFilterPlugin::interfaces()
{
  QObjectList ifaces;
#if _paraview_add_plugin_UI_INTERFACES
  PARAVIEW_ADD_INTERFACES(ifaces);
#endif
  return ifaces;
}
#endif

//-----------------------------------------------------------------------------
#if _paraview_add_plugin_with_python

void ElevationFilterPlugin::GetPythonSourceList(std::vector<std::string>& modules,
  std::vector<std::string>& sources,
  std::vector<int> &package_flags)
{
  const char *moduleNames[] = {

  };
  char *moduleSources[] = {

  };
  const int packageFlags[] = {

  };

  for (int cc=0; moduleNames[cc]; cc++)
  {
    modules.push_back(moduleNames[cc]);
    sources.push_back(moduleSources[cc]);
    package_flags.push_back(packageFlags[cc]);

    // free allocated memory.
    delete moduleSources[cc];
    moduleSources[cc] = nullptr;
  }
}
#endif

//-----------------------------------------------------------------------------
static void initialize_ElevationFilter_plugin_qt_resources()
{
#if !_paraview_add_plugin_built_shared && _paraview_add_plugin_with_resources
  // For static builds, initialize the Qt resources.

#endif
#if !_paraview_add_plugin_built_shared && _paraview_add_plugin_with_ui
  // For static builds, initialize the Qt plugin.
  Q_IMPORT_PLUGIN(ElevationFilterPlugin)
#endif
}

//-----------------------------------------------------------------------------
ElevationFilterPlugin::ElevationFilterPlugin()
{
  initialize_ElevationFilter_plugin_qt_resources();
}

//-----------------------------------------------------------------------------
const char* ElevationFilterPlugin::GetEULA()
{
#if _paraview_add_plugin_EULA
  return ElevationFilter_EULA;
#else
  return nullptr;
#endif
}

//-----------------------------------------------------------------------------
// Mark this as a ParaView-ServerManager plugin.
PV_PLUGIN_EXPORT(ElevationFilter, ElevationFilterPlugin)
